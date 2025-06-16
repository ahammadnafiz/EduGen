from manim import *
import tempfile
import os
import sys
import subprocess
import py_compile
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# LLM client using LangChain with Google Generative AI
class LLMClient:
    def __init__(self):
        try:
            # Get API key from environment variables
            google_api_key = os.getenv('GOOGLE_API_KEY_FIX')
            if not google_api_key:
                raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
            # Initialize the Google Generative AI model
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=google_api_key,
                model="gemini-2.0-flash",
                temperature=0.7,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )
            
        except Exception as e:
            print(f"Warning: Failed to initialize LLM client: {e}")
            print("Falling back to basic error handling")
            self.llm = None
    
    def fix_manim_code(self, manim_code, error_message=None):
        """
        Direct fix of Manim code using LLM
        
        Args:
            manim_code (str): The Manim code to fix
            error_message (str, optional): Specific error message if available
            
        Returns:
            str: Fixed Manim code
        """
        if self.llm is None:
            print("LLM not available, returning original code")
            return manim_code
        
        try:
            # Create prompt for fixing the code
            if error_message:
                prompt = f"""Fix this Manim Python code that has the following error:

ERROR: {error_message}

MANIM CODE TO FIX:
{manim_code}

Return only the corrected Python code with proper Manim syntax."""
            else:
                prompt = f"""Review and fix this Manim Python code to ensure it compiles and runs correctly:

MANIM CODE:
{manim_code}

Return only the corrected Python code with proper Manim syntax."""
            
            # Direct LLM call
            messages = [
                SystemMessage(content="You are an expert Manim code fixer. Return only corrected Python code, no explanations or markdown."),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            fixed_code = response.content.strip()
            
            # Clean up any markdown formatting
            if fixed_code.startswith("```python"):
                fixed_code = fixed_code[9:]
            if fixed_code.startswith("```"):
                fixed_code = fixed_code[3:]
            if fixed_code.endswith("```"):
                fixed_code = fixed_code[:-3]
            
            return fixed_code.strip()
            
        except Exception as e:
            print(f"Error fixing code with LLM: {e}")
            return manim_code

llm_client = LLMClient()

def validate_and_fix_manim_code(manim_code, max_attempts=5):
    """
    Validates Manim code through compilation and fixes errors using LLM feedback
    
    Args:
        manim_code: Generated Manim code string
        max_attempts: Maximum number of fix attempts
    
    Returns:
        tuple: (validated_code, success_status, error_log)
    """
    
    attempt = 0
    current_code = manim_code
    error_history = []
    
    while attempt < max_attempts:
        # Create temporary Python file for validation
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(current_code)
            temp_file_path = temp_file.name
        
        try:
            # Attempt compilation
            py_compile.compile(temp_file_path, doraise=True)
            
            # If successful, clean up and return
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
            return current_code, True, error_history
            
        except py_compile.PyCompileError as e:
            # Capture compilation error
            error_info = {
                'attempt': attempt + 1,
                'error': str(e),
                'code_snapshot': current_code[:500] + "..." if len(current_code) > 500 else current_code
            }
            error_history.append(error_info)
            
            print(f"Attempt {attempt + 1} failed compilation: {e}")
            
            # Send to LLM for fixing
            print("Attempting to fix code with LLM...")
            current_code = llm_client.fix_manim_code(current_code, str(e))
            attempt += 1
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    # If all attempts failed
    print(f"Failed to validate and fix code after {max_attempts} attempts.")
    return current_code, False, error_history

def trial_render_manim(temp_file_path, scene_class_name, output_dir="trial_media"):
    """
    Perform a trial render of Manim code to check for rendering errors
    
    Args:
        temp_file_path (str): Path to temporary Python file with Manim code
        scene_class_name (str): Name of the scene class to render
        output_dir (str): Directory for trial render output
        
    Returns:
        tuple: (success_status, error_message)
    """
    try:
        # Ensure trial output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Trial render command with low quality for speed
        cmd = [
            'manim', 
            temp_file_path,
            scene_class_name,
            '-ql',  # low quality for trial
            '--disable_caching',
            f'--media_dir={output_dir}'
        ]
        
        print(f"Running trial render: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            print("Trial render successful!")
            # Clean up trial animations after successful render
            cleanup_trial_animations(output_dir)
            return True, None
        else:
            error_message = f"Trial render failed:\nReturn Code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
            print(f"Trial render failed: {error_message}")
            return False, error_message
            
    except Exception as e:
        error_message = f"Trial render exception: {str(e)}"
        print(error_message)
        return False, error_message

def cleanup_trial_animations(trial_output_dir):
    """
    Clean up trial animation files and directories after successful trial render
    
    Args:
        trial_output_dir (str): Directory containing trial render output
    """
    try:
        if os.path.exists(trial_output_dir):
            import shutil
            shutil.rmtree(trial_output_dir)
            print(f"✓ Cleaned up trial animations from: {trial_output_dir}")
    except Exception as e:
        print(f"Warning: Failed to clean up trial animations from {trial_output_dir}: {e}")

def create_animation_from_code(manim_code, output_dir="media/videos", max_render_attempts=3):
    """
    Enhanced animation creator with pre-validation and trial rendering.
    Create animation from generated Manim code.
    
    Args:
        manim_code (str): Complete Manim Python code
        output_dir (str): Directory to save the rendered video
        max_render_attempts (int): Maximum attempts for render fixes
        
    Returns:
        str: Path to the generated video file, or None if failed
    """
    if not manim_code:
        print("No Manim code provided")
        return None

    # Pre-validate the code
    validated_code, is_valid, error_log = validate_and_fix_manim_code(manim_code)
    
    if not is_valid:
        print("Failed to generate valid Manim code after maximum attempts.")
        print("Error history:")
        for err_info in error_log:
            print(f"  Attempt {err_info['attempt']}: {err_info['error']}")
        return None
    
    # Extract scene class name from validated code
    scene_class_name = extract_scene_class_name(validated_code)
    if not scene_class_name:
        print("Could not find scene class in the validated code.")
        return None
    
    # Trial rendering loop
    render_attempt = 0
    current_code = validated_code
    
    while render_attempt < max_render_attempts:
        # Create temporary file with current code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(current_code)
            temp_file_path = temp_file.name
        
        try:
            # Perform trial render
            trial_success, trial_error = trial_render_manim(temp_file_path, scene_class_name)
            
            if trial_success:
                print("Trial render successful! Proceeding with final render...")
                break
            else:
                print(f"Trial render attempt {render_attempt + 1} failed.")
                
                if render_attempt < max_render_attempts - 1:
                    print("Attempting to fix rendering errors with LLM...")
                    # Send to LLM for fixing rendering issues
                    current_code = llm_client.fix_manim_code(current_code, trial_error)
                    render_attempt += 1
                else:
                    print(f"Failed to fix rendering errors after {max_render_attempts} attempts.")
                    return None
                    
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    # If we reach here, trial render was successful
    # Proceed with final rendering using validated and render-tested code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(current_code)
        temp_file_path = temp_file.name
    
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Run final Manim rendering
        cmd = [
            'manim', 
            temp_file_path,
            scene_class_name,
            '-qm',  # medium quality for final render
            '--disable_caching',
            f'--media_dir={output_dir}' 
        ]
        
        print(f"Running final render: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            # Find the generated video
            video_path = find_generated_video(output_dir, scene_class_name, os.path.basename(temp_file_path).replace('.py',''))
            if video_path:
                print(f"Animation created successfully: {video_path}")
                return video_path
            else:
                print(f"Final rendering succeeded but the video file was not found in {output_dir} for scene {scene_class_name}.")
                print(f"Manim stdout: {result.stdout}")
                print(f"Manim stderr: {result.stderr}")
                return None        
        else:
            print(f"Final rendering failed unexpectedly after successful trial render.")
            print(f"Return Code: {result.returncode}")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            
            # Log the code that failed final rendering
            print("\n" + "="*60)
            print("🚨 FINAL MANIM RENDERING FAILED AFTER SUCCESSFUL TRIAL")
            print("="*60)
            print("Code that failed final rendering:")
            print("─" * 40)
            lines = current_code.split('\n')
            for i, line in enumerate(lines, 1):
                print(f"{i:3}: {line}")
            print("─" * 40)
            print("="*60)
            return None
            
    except Exception as e:
        print(f"An unexpected error occurred during final animation creation: {e}")
        print("Code at time of exception:")
        print(current_code)
        return None
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except OSError as e:
                print(f"Error deleting temporary file {temp_file_path}: {e}")

def extract_scene_class_name(manim_code):
    """
    Extract the Scene class name from Manim code.
    
    Args:
        manim_code (str): Manim Python code
        
    Returns:
        str: Scene class name or None if not found
    """
    import re
    # Improved regex to handle various Scene inheritances like class MyScene(Scene): or class MyScene(MovingCameraScene):
    match = re.search(r'class\s+(\w+)\s*\(\s*(?:\w*?Scene\w*?)\s*\)', manim_code)
    return match.group(1) if match else None

def find_generated_video(base_dir, scene_class_name, temp_file_name_stem=None):
    """
    Find the generated video file in Manim's output structure
    """
    possible_paths_to_check = []
    if temp_file_name_stem:
        # Path structure: <media_dir>/<temp_file_name_stem>/<quality_subdir>/<scene_name>.mp4
        search_root = os.path.join(base_dir, temp_file_name_stem)
        if os.path.isdir(search_root):
            possible_paths_to_check.append(search_root)
    
    # Fallback to searching the entire base_dir
    possible_paths_to_check.append(base_dir)

    for search_path in possible_paths_to_check:
        if not os.path.isdir(search_path):
            continue
        for root, dirs, files in os.walk(search_path):
            for file in files:
                # Check if the scene class name is part of the filename and it's an mp4
                if scene_class_name in file and file.endswith('.mp4'):
                    if file == f"{scene_class_name}.mp4" or scene_class_name in os.path.splitext(file)[0]:
                         return os.path.join(root, file)
    
    print(f"Video file for scene '{scene_class_name}' not found in expected Manim output structure under '{base_dir}'. Searched paths: {possible_paths_to_check}")
    return None

def create_animation(script):
    """
    Legacy function for backward compatibility - creates basic text animation
    
    Args:
        script (str): Text script to display
    """
    class MyScene(Scene):
        def construct(self):
            text = Text(script[:100] + "..." if len(script) > 100 else script)
            self.play(Write(text))
            self.wait(2)

    # This would need to be rendered separately
    print("Legacy create_animation called. Use create_animation_from_code for full functionality.")