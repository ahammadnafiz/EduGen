from manim import *
import tempfile
import os
import sys
import subprocess

def create_animation_from_code(manim_code, output_dir="media/videos"):
    """
    Create animation from generated Manim code.
    
    Args:
        manim_code (str): Complete Manim Python code
        output_dir (str): Directory to save the rendered video
        
    Returns:
        str: Path to the generated video file, or None if failed
    """
    if not manim_code:
        print("No Manim code provided")
        return None
    
    try:
        # Create a temporary Python file with the Manim code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(manim_code)
            temp_file_path = temp_file.name
        
        # Extract scene class name from the code
        scene_class_name = extract_scene_class_name(manim_code)
        if not scene_class_name:
            print("Could not find scene class in the generated code")
            return None
        
        # Run Manim to render the animation
        cmd = [
            'manim', 
            temp_file_path, 
            scene_class_name, 
            '-qm',  # medium quality
            '--disable_caching',
            f'--media_dir={output_dir}'        ]
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Find the generated video file
            video_path = find_generated_video(output_dir, scene_class_name)
            if video_path:
                print(f"Animation created successfully: {video_path}")
                return video_path
            else:
                print("Animation rendered but video file not found")
                return None        
        else:
            print(f"Manim rendering failed: {result.stderr}")
            print(f"Command output: {result.stdout}")
            
            # Enhanced error reporting for syntax errors
            if "IndentationError" in result.stderr or "SyntaxError" in result.stderr:
                print("\n" + "="*60)
                print("🚨 SYNTAX ERROR DETECTED IN GENERATED CODE")
                print("="*60)
                print("Generated code that caused the error:")
                print("─" * 40)
                lines = manim_code.split('\n')
                for i, line in enumerate(lines, 1):
                    print(f"{i:3}: {line}")
                print("─" * 40)
                print("This indicates the Manim code generator needs improvement.")
                print("The code should be sent back to the LLM for fixing.")
                print("="*60)
            elif "NameError" in result.stderr:
                print("\n" + "="*60)
                print("🚨 NAME ERROR DETECTED IN GENERATED CODE")
                print("="*60)
                print("This suggests missing imports or undefined variables.")
                print("Generated code preview:")
                print("─" * 40)
                for i, line in enumerate(manim_code.split('\n')[:20], 1):
                    print(f"{i:3}: {line}")
                print("─" * 40)
                print("="*60)
            
            return None
            
    except Exception as e:
        print(f"Error creating animation: {e}")
        return None
    finally:
        # Clean up temporary file
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass

def extract_scene_class_name(manim_code):
    """
    Extract the Scene class name from Manim code.
    
    Args:
        manim_code (str): Manim Python code
        
    Returns:
        str: Scene class name or None if not found
    """
    import re
    match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', manim_code)
    return match.group(1) if match else None

def find_generated_video(base_dir, scene_class_name):
    """
    Find the generated video file in the media directory.
    
    Args:
        base_dir (str): Base media directory
        scene_class_name (str): Name of the scene class
        
    Returns:
        str: Path to video file or None if not found
    """
    # Manim typically saves videos in media/videos/[temp_file_name]/[resolution]/[scene_name].mp4
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.mp4') and scene_class_name in file:
                return os.path.join(root, file)
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
