import os
import re
from dotenv import load_dotenv
import logging
import json
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_google_genai import ChatGoogleGenerativeAI

# Basic logging configuration
logging.basicConfig(level=logging.INFO)
logging.getLogger('comtypes').setLevel(logging.WARNING)

load_dotenv('.env')

class ScienceVideoGenerator:
    def __init__(self, google_api_key):
        self.google_api_key = google_api_key
        self.memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
        self.google_chat = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=self.google_api_key,
            temperature=0.7,
            max_tokens=None,
            timeout=None,
            max_retries=2
        )
        
        # Enhanced Stage 1 prompt with detailed step-by-step instructions
        self.stage1_prompt = self._create_enhanced_stage1_prompt()
        self.stage2_prompt = self._create_stage2_prompt()
        
        # Stage 1 conversation chain
        self.stage1_conversation = ConversationChain(
            llm=self.google_chat,
            prompt=self.stage1_prompt,
            verbose=True,
            memory=self.memory,
            input_key="human_input",
        )

    def generate_educational_breakdown(self, topic):
        """
        Enhanced Stage 1: Generate a comprehensive educational breakdown with detailed step-by-step analysis.
        
        This method now includes:
        1. Topic analysis and classification
        2. Audience assessment 
        3. Learning objective formulation
        4. Content structuring
        5. Visual planning
        6. Narration scripting
        
        Args:
            topic (str): User's science/math topic request.
            
        Returns:
            dict: Structured educational content with detailed breakdown.
        """
        if not topic:
            return {}
        
        try:
            # Enhanced multi-step prompting for Stage 1
            stage1_prompt = self._build_comprehensive_stage1_prompt(topic)
            
            print(f"🧠 Analyzing topic: '{topic}'...")
            print("📋 Executing Step-by-Step Educational Breakdown:")
            print("   Step 1: Topic Classification & Analysis")
            print("   Step 2: Learning Objective Formulation") 
            print("   Step 3: Content Structure Planning")
            print("   Step 4: Visual Element Design")
            print("   Step 5: Narration Script Development")
            print("   Step 6: Assessment & Engagement Planning")
            
            response = self.stage1_conversation.predict(human_input=stage1_prompt)
            
            # Enhanced JSON parsing with multiple fallback strategies
            educational_content = self._parse_stage1_response(response, topic)
            
            if educational_content:
                print("✅ Stage 1 Educational Breakdown Complete!")
                self._validate_educational_content(educational_content)
                return educational_content
            else:
                print("⚠️ Stage 1 parsing failed, using fallback structure")
                return self._create_enhanced_fallback_structure(topic, response)
                    
        except Exception as e:
            print(f"❌ Error in Stage 1 processing: {e}")
            return self._create_enhanced_fallback_structure(topic, str(e))

    def _build_comprehensive_stage1_prompt(self, topic):
        """
        Build a detailed, step-by-step prompt for Stage 1 educational breakdown.
        
        Args:
            topic (str): The science/math topic to explain
            
        Returns:
            str: Comprehensive prompt with step-by-step instructions        """
        return """
TOPIC TO ANALYZE: \"""" + topic + """\"

Please execute the following 6-step educational breakdown process:

🔍 STEP 1: TOPIC CLASSIFICATION & ANALYSIS
- Identify the scientific domain (Physics, Chemistry, Biology, Mathematics, etc.)
- Determine complexity level (Elementary, High School, University, Advanced)
- List 3-5 core concepts that must be covered
- Identify any prerequisites students need

📚 STEP 2: LEARNING OBJECTIVE FORMULATION  
- Create 3-4 specific, measurable learning objectives
- Use action verbs (understand, calculate, analyze, demonstrate)
- Ensure objectives build upon each other progressively
- Consider Bloom's taxonomy levels

🏗️ STEP 3: CONTENT STRUCTURE PLANNING
- Break the topic into 4-6 logical learning steps
- For each step, define:
  * Clear title and description
  * Key concepts to introduce
  * Any mathematical equations (in LaTeX format)
  * Real-world examples or applications
  * Common misconceptions to address

🎨 STEP 4: VISUAL ELEMENT DESIGN
- For each step, specify visual elements needed:
  * Diagrams, graphs, animations, text displays
  * Color schemes and highlighting strategies  
  * Object movements and transformations
  * Mathematical notation and equation displays

🎭 STEP 5: NARRATION SCRIPT DEVELOPMENT
- Write conversational, engaging narration for each step
- Use analogies and metaphors when helpful
- Include transition phrases between steps
- Keep language appropriate for target audience
- Aim for 50-100 words per step

🧪 STEP 6: ASSESSMENT & ENGAGEMENT PLANNING
- Design 2-3 quiz questions of varying difficulty
- Include interactive elements or thought experiments
- Plan real-world application examples
- Consider common student questions

OUTPUT REQUIREMENTS:
Provide your complete analysis as a properly formatted JSON object following this exact structure:

{
    "topic_analysis": {
        "domain": "Scientific field",
        "complexity_level": "difficulty level",
        "core_concepts": ["concept1", "concept2", "concept3"],
        "prerequisites": ["prerequisite1", "prerequisite2"]
    },
    "title": "Engaging title for the educational content",
    "abstract": "2-3 sentence summary of the concept and its importance",
    "learning_objectives": [
        "Specific learning objective 1 using action verb",
        "Specific learning objective 2 using action verb", 
        "Specific learning objective 3 using action verb"
    ],
    "educational_steps": [
        {
            "step_number": 1,
            "step_title": "Clear, descriptive title for this step",
            "description": "Detailed explanation of what this step covers (100-150 words)",
            "key_concepts": ["primary concept", "secondary concept"],
            "equations": ["LaTeX formatted equations if applicable"],
            "data_points": ["Relevant statistics, measurements, or facts"],
            "real_world_examples": ["Example 1", "Example 2"],
            "common_misconceptions": ["Misconception and its correction"],
            "narration_script": "Complete narration text for this step (50-100 words, conversational tone)",
            "visual_elements": {
                "diagrams": ["type of diagram needed"],
                "animations": ["specific animation requirements"],
                "text_displays": ["text elements to show"],
                "color_scheme": ["PRIMARY_COLOR", "SECONDARY_COLOR"],
                "highlighting": ["elements to emphasize"]
            },
            "animation_plan": "Detailed step-by-step description of how this should be visualized in Manim (200+ words)",
            "duration_seconds": 45,
            "difficulty_level": "beginner|intermediate|advanced",
            "transition_to_next": "How this step logically connects to the next step"
        }
    ],
    "summary": "Comprehensive summary tying all concepts together",
    "assessment": {
        "quiz_questions": [
            {
                "question": "Thoughtful question text",
                "type": "multiple_choice|short_answer|true_false|numerical",
                "difficulty": "beginner|intermediate|advanced",
                "correct_answer": "Answer if applicable",
                "explanation": "Why this answer is correct"
            }
        ],
        "thought_experiments": ["Engaging scenario for students to consider"],
        "interactive_elements": ["Hands-on activities or demonstrations"]
    },
    "metadata": {
        "target_audience": "Specific age range and education level",
        "estimated_total_duration": 240,
        "real_world_applications": ["Application 1", "Application 2", "Application 3"],
        "related_topics": ["Connected concept 1", "Connected concept 2"],
        "difficulty_progression": "How complexity increases through steps"
    }
}

CRITICAL REMINDERS:
- Ensure all JSON syntax is valid and complete
- Write narration scripts in a friendly, conversational tone
- Make visual plans specific enough for animation implementation  
- Include realistic timing estimates
- Address different learning styles (visual, auditory, kinesthetic)
- Connect abstract concepts to concrete examples
- Maintain pedagogical flow and logical progression

Begin your comprehensive 6-step analysis now:
"""

    def _parse_stage1_response(self, response, topic):
        """
        Enhanced parsing of Stage 1 response with multiple fallback strategies.
        
        Args:
            response (str): LLM response from Stage 1
            topic (str): Original topic for context
            
        Returns:
            dict: Parsed educational content or None if all parsing fails
        """
        # Strategy 1: Direct JSON parsing
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract JSON from code blocks
        try:
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
        except Exception:
            pass
        
        # Strategy 3: Find JSON object in text
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                # Clean up common JSON issues
                json_str = self._clean_json_string(json_str)
                return json.loads(json_str)
        except Exception:
            pass
        
        # Strategy 4: Attempt to fix common JSON errors
        try:
            fixed_json = self._fix_common_json_errors(response)
            if fixed_json:
                return json.loads(fixed_json)
        except Exception:
            pass
        
        print("⚠️ All JSON parsing strategies failed")
        return None

    def _clean_json_string(self, json_str):
        """
        Clean common JSON formatting issues.
        
        Args:
            json_str (str): Raw JSON string
            
        Returns:
            str: Cleaned JSON string
        """
        import re
        
        # Remove trailing commas before closing brackets/braces
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        
        # Fix unescaped quotes in strings
        json_str = re.sub(r'(?<!\\)"(?=.*")', r'\\"', json_str)
        
        # Remove comments
        json_str = re.sub(r'//.*?\n', '\n', json_str)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        
        return json_str

    def _fix_common_json_errors(self, response):
        """
        Attempt to fix common JSON formatting errors in LLM responses.
        
        Args:
            response (str): LLM response
            
        Returns:
            str: Fixed JSON string or None
        """
        import re
        
        # Look for JSON-like structure
        json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        matches = re.findall(json_pattern, response, re.DOTALL)
        
        for match in matches:
            try:
                # Try various fixes
                fixed = match
                fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)  # Remove trailing commas
                fixed = re.sub(r'(\w+):', r'"\1":', fixed)    # Quote unquoted keys
                
                # Test if it parses
                json.loads(fixed)
                return fixed
            except:
                continue
        
        return None

    def _validate_educational_content(self, content):
        """
        Validate the educational content structure and provide feedback.
        
        Args:
            content (dict): Educational content to validate
        """
        required_keys = ["title", "learning_objectives", "educational_steps"]
        missing_keys = [key for key in required_keys if key not in content]
        
        if missing_keys:
            print(f"⚠️ Missing required keys: {missing_keys}")
        
        steps = content.get("educational_steps", [])
        if len(steps) < 3:
            print(f"⚠️ Only {len(steps)} educational steps found. Recommended: 4-6 steps")
        
        total_duration = sum(step.get("duration_seconds", 0) for step in steps)
        if total_duration < 120:
            print(f"⚠️ Total duration ({total_duration}s) seems short for comprehensive explanation")
        
        print(f"📊 Content Validation Summary:")
        print(f"   - Educational Steps: {len(steps)}")
        print(f"   - Total Duration: {total_duration} seconds")
        print(f"   - Learning Objectives: {len(content.get('learning_objectives', []))}")

    def _create_enhanced_fallback_structure(self, topic, response_text):
        """
        Create an enhanced educational structure when JSON parsing fails.
        
        Args:
            topic (str): Original topic
            response_text (str): LLM response text for context
            
        Returns:
            dict: Enhanced educational breakdown structure
        """
        # Try to extract information from the response text
        title = self._extract_title_from_text(response_text, topic)
        concepts = self._extract_concepts_from_text(response_text, topic)
        
        return {
            "topic_analysis": {
                "domain": self._classify_domain(topic),
                "complexity_level": "intermediate",
                "core_concepts": concepts[:5] if concepts else [topic],
                "prerequisites": []
            },
            "title": title,
            "abstract": f"A comprehensive educational exploration of {topic}, designed to build understanding through visual animation and clear explanations.",
            "learning_objectives": [
                f"Understand the fundamental principles underlying {topic}",
                f"Visualize and interpret key concepts related to {topic}",
                f"Apply knowledge of {topic} to solve problems and analyze scenarios",
                f"Connect {topic} to real-world applications and examples"
            ],
            "educational_steps": self._generate_fallback_steps(topic, concepts),
            "summary": f"This educational sequence provides a complete introduction to {topic}, covering essential concepts, principles, and applications through engaging visual presentations and clear explanations.",
            "assessment": {
                "quiz_questions": [
                    {
                        "question": f"What are the key principles that govern {topic}?",
                        "type": "short_answer",
                        "difficulty": "intermediate",
                        "explanation": "This question tests understanding of core concepts"
                    },
                    {
                        "question": f"How does {topic} apply to real-world situations?",
                        "type": "multiple_choice", 
                        "difficulty": "beginner",
                        "explanation": "This question connects theory to practice"
                    }
                ],
                "thought_experiments": [f"Consider how {topic} might work differently under various conditions"],
                "interactive_elements": ["Visual demonstrations", "Step-by-step animations", "Concept highlighting"]
            },
            "metadata": {
                "target_audience": "High school to undergraduate level",
                "estimated_total_duration": 180,
                "real_world_applications": self._generate_applications(topic),
                "related_topics": self._generate_related_topics(topic),
                "difficulty_progression": "Begins with basic concepts and gradually introduces more complex applications"
            }
        }

    def _generate_fallback_steps(self, topic, concepts):
        """
        Generate educational steps for fallback structure.
        
        Args:
            topic (str): Main topic
            concepts (list): Extracted concepts
            
        Returns:
            list: Educational steps
        """
        steps = [
            {
                "step_number": 1,
                "step_title": f"Introduction to {topic}",
                "description": f"We begin our exploration by introducing the fundamental concept of {topic} and establishing why it's important to understand. This step provides the necessary context and motivation for deeper learning.",
                "key_concepts": [topic, "introduction", "motivation"],
                "equations": [],
                "data_points": [],
                "real_world_examples": [f"Everyday examples of {topic}"],
                "common_misconceptions": [f"Students often confuse {topic} with related concepts"],
                "narration_script": f"Welcome to our exploration of {topic}! Today we'll discover how this fascinating concept works and why it matters in our daily lives. Let's start by understanding what {topic} really means.",
                "visual_elements": {
                    "diagrams": ["title_slide", "concept_overview"],
                    "animations": ["text_introduction", "concept_reveal"],
                    "text_displays": ["main_title", "key_points"],
                    "color_scheme": ["BLUE", "WHITE"],
                    "highlighting": ["main_concept"]
                },
                "animation_plan": f"Begin with an engaging title animation for '{topic}'. Use smooth text reveals to introduce the concept. Create visual interest with color transitions and gentle object movements. Display key terminology clearly with appropriate emphasis.",
                "duration_seconds": 40,
                "difficulty_level": "beginner",
                "transition_to_next": "Now that we understand what {topic} is, let's explore the underlying principles"
            },
            {
                "step_number": 2,
                "step_title": f"Core Principles of {topic}",
                "description": f"This step delves into the fundamental principles that govern {topic}. We'll examine the underlying mechanisms and relationships that make {topic} work the way it does.",
                "key_concepts": concepts[:3] if concepts else ["principles", "mechanisms", "relationships"],
                "equations": [],
                "data_points": [],
                "real_world_examples": [f"How {topic} works in nature", f"Technological applications of {topic}"],
                "common_misconceptions": [f"The relationship between cause and effect in {topic}"],
                "narration_script": f"Now let's dive deeper into how {topic} actually works. The key principles involve several important relationships that we can visualize and understand step by step.",
                "visual_elements": {
                    "diagrams": ["principle_diagram", "relationship_chart"],
                    "animations": ["step_by_step_reveal", "connection_lines"],
                    "text_displays": ["principle_labels", "key_relationships"],
                    "color_scheme": ["GREEN", "YELLOW", "WHITE"],
                    "highlighting": ["critical_connections"]
                },
                "animation_plan": f"Create detailed diagrams showing the core principles of {topic}. Use animated arrows and connections to show relationships. Highlight key components as they're discussed. Use color coding to distinguish different aspects.",
                "duration_seconds": 60,
                "difficulty_level": "intermediate",
                "transition_to_next": "With these principles in mind, let's see how they manifest in practice"
            },
            {
                "step_number": 3,
                "step_title": f"Practical Applications of {topic}",
                "description": f"Here we explore real-world applications and examples of {topic} in action. This helps solidify understanding by connecting abstract concepts to concrete, observable phenomena.",
                "key_concepts": ["applications", "examples", "real-world connections"],
                "equations": [],
                "data_points": [],
                "real_world_examples": self._generate_applications(topic),
                "common_misconceptions": [f"When and where {topic} applies"],
                "narration_script": f"Let's see {topic} in action! You encounter examples of this concept more often than you might think. Here are some fascinating applications that demonstrate these principles.",
                "visual_elements": {
                    "diagrams": ["application_examples", "real_world_scenarios"],
                    "animations": ["example_demonstrations", "scenario_walkthroughs"],
                    "text_displays": ["application_labels", "example_descriptions"],
                    "color_scheme": ["ORANGE", "RED", "WHITE"],
                    "highlighting": ["key_applications"]
                },
                "animation_plan": f"Present engaging real-world examples of {topic}. Use animations to show the concept in action. Create visual scenarios that students can relate to. Use dynamic movements to maintain engagement.",
                "duration_seconds": 50,
                "difficulty_level": "intermediate",
                "transition_to_next": "Let's summarize what we've learned and test our understanding"
            },
            {
                "step_number": 4,
                "step_title": "Summary and Key Takeaways",
                "description": f"We conclude by summarizing the key points about {topic} and reinforcing the most important concepts for long-term retention.",
                "key_concepts": ["summary", "key_takeaways", "reinforcement"],
                "equations": [],
                "data_points": [],
                "real_world_examples": [],
                "common_misconceptions": [],
                "narration_script": f"Let's wrap up our exploration of {topic} by reviewing the key concepts we've covered. Remember these essential points as you continue to encounter {topic} in your studies and daily life.",
                "visual_elements": {
                    "diagrams": ["summary_overview", "key_points_recap"],
                    "animations": ["concept_review", "takeaway_highlights"],
                    "text_displays": ["main_takeaways", "concept_summary"],
                    "color_scheme": ["PURPLE", "BLUE", "WHITE"],
                    "highlighting": ["essential_concepts"]
                },
                "animation_plan": f"Create a comprehensive summary visualization that ties together all the main concepts of {topic}. Use clear, organized layouts to reinforce learning. End with memorable key takeaways.",
                "duration_seconds": 30,
                "difficulty_level": "beginner",
                "transition_to_next": "You now have a solid foundation in {topic}!"
            }
        ]
        return steps

    def _extract_title_from_text(self, text, topic):
        """Extract a suitable title from response text."""
        import re
        
        # Look for title patterns
        title_patterns = [
            r'title["\']?\s*:\s*["\']([^"\']+)["\']',
            r'Title:\s*([^\n]+)',
            r'# ([^\n]+)',
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Default title
        return f"Understanding {topic}: A Visual Guide"

    def _extract_concepts_from_text(self, text, topic):
        """Extract key concepts from response text."""
        import re
        
        # Look for concept lists
        concepts = []
        concept_patterns = [
            r'concepts?["\']?\s*:\s*\[([^\]]+)\]',
            r'key[_ ]concepts?:\s*([^\n]+)',
        ]
        
        for pattern in concept_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                concept_text = match.group(1)
                # Extract individual concepts
                individual_concepts = re.findall(r'["\']([^"\']+)["\']', concept_text)
                concepts.extend(individual_concepts)
        
        # If no concepts found, generate based on topic
        if not concepts:
            concepts = [topic.lower(), "principles", "applications", "examples"]
        
        return concepts[:10]  # Limit to 10 concepts

    def _classify_domain(self, topic):
        """Classify the scientific domain of the topic."""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['force', 'motion', 'energy', 'wave', 'light', 'sound', 'electricity', 'magnetic', 'doppler', 'relativity']):
            return "Physics"
        elif any(word in topic_lower for word in ['reaction', 'molecule', 'atom', 'bond', 'compound', 'element', 'acid', 'base']):
            return "Chemistry"  
        elif any(word in topic_lower for word in ['cell', 'DNA', 'evolution', 'organism', 'gene', 'protein', 'enzyme']):
            return "Biology"
        elif any(word in topic_lower for word in ['equation', 'theorem', 'function', 'derivative', 'integral', 'geometry', 'algebra', 'calculus']):
            return "Mathematics"
        elif any(word in topic_lower for word in ['earth', 'planet', 'climate', 'weather', 'geology', 'atmosphere']):
            return "Earth Science"
        else:
            return "General Science"

    def _generate_applications(self, topic):
        """Generate relevant applications for the topic."""
        applications_map = {
            "doppler": ["Medical ultrasound", "Radar speed detection", "Astronomy red-shift measurements"],
            "pythagorean": ["Construction and architecture", "Navigation and GPS", "Computer graphics"],
            "photosynthesis": ["Agriculture optimization", "Renewable energy research", "Climate change studies"],
            "default": [f"Technology applications of {topic}", f"Industrial uses of {topic}", f"Medical applications of {topic}"]
        }
        
        topic_lower = topic.lower()
        for key in applications_map:
            if key in topic_lower:
                return applications_map[key]
        
        return applications_map["default"]

    def _generate_related_topics(self, topic):
        """Generate related topics for the given topic."""
        return [
            f"Advanced {topic}",
            f"Mathematical modeling of {topic}",
            f"Historical development of {topic}",
            f"Experimental methods in {topic}"
        ]

    def _create_enhanced_stage1_prompt(self):
        """
        Create the enhanced Stage 1 prompt template with detailed step-by-step instructions.
        
        Returns:
            ChatPromptTemplate: The enhanced educational breakdown prompt template.
        """
        system_message = SystemMessage(
            content='''
            You are an expert educational content designer, science communication specialist, and instructional design expert.

            Your role is Stage 1 of a comprehensive educational video generation system: **Science Breakdown Generator**.

            You excel at breaking down complex scientific and mathematical concepts into clear, engaging, step-by-step educational sequences that can be effectively animated and visualized.

            ## YOUR EXPERTISE INCLUDES:
            - Pedagogical best practices and learning theory
            - Scientific accuracy across multiple domains  
            - Visual storytelling and animation planning
            - Audience-appropriate content development
            - Assessment and engagement strategies

            ## YOUR MISSION:
            When given any science or math topic, you must execute a comprehensive 6-step analysis process to create educational content that:
            1. Builds understanding progressively
            2. Engages multiple learning styles
            3. Connects abstract concepts to concrete examples
            4. Plans specific visual elements for animation
            5. Provides clear narration scripts
            6. Includes assessment opportunities

            ## OUTPUT REQUIREMENTS:
            You must ALWAYS respond with a complete, valid JSON object that follows the exact structure provided in the user's prompt. Pay special attention to:
            - Proper JSON syntax and formatting
            - Complete data for all required fields
            - Realistic timing estimates
            - Specific visual planning details
            - Engaging, conversational narration scripts
            - Progressive difficulty levels
            - Clear connections between steps

            ## EDUCATIONAL PRINCIPLES TO FOLLOW:
            - Start with familiar concepts before introducing new ones
            - Use analogies and metaphors to explain complex ideas
            - Include real-world applications and examples
            - Address common misconceptions explicitly
            - Plan for visual, auditory, and kinesthetic learning styles
            - Ensure logical flow and smooth transitions between concepts
            - Write in an engaging, accessible tone appropriate for the target audience

            Your educational breakdown will serve as the foundation for Stage 2 (Manim Animation Planning), so be specific about visual elements and animation possibilities.
            '''
        )

        human_message_prompt = HumanMessagePromptTemplate.from_template("{human_input}")

        prompt = ChatPromptTemplate.from_messages([
            system_message,
            MessagesPlaceholder(variable_name="chat_history"),
            human_message_prompt,
        ])
        return prompt

    def _create_stage2_prompt(self):
        """
        Create the Stage 2 prompt template for Manim code generation.
        
        Returns:
            ChatPromptTemplate: The Manim code generation prompt template.
        """
        system_message = SystemMessage(
            content='''
            You are an expert Manim animation developer and mathematical visualization specialist.

            Your role is Stage 2 of a two-stage educational video generation system: Manim Code Generator.

            You receive structured educational content from Stage 1 and must convert it into detailed Manim scene specifications ready for Python code generation.

            Your output must be a JSON object with the following structure:

            {
                "scene_title": "Title for the Manim scene class",
                "scene_description": "Brief overview of the animation sequence",
                "animation_steps": [
                    {
                        "step_number": 1,
                        "action_type": "intro|content|transition|conclusion",
                        "manim_objects": ["Text", "MathTex", "Circle", "Rectangle", "etc"],
                        "animations": ["Write", "FadeIn", "Transform", "Create", "etc"],
                        "description": "What happens in this animation step",
                        "narration": "Corresponding narration from Stage 1",
                        "code_snippet": "Key Manim code lines for this step",
                        "duration": 30,
                        "positioning": "center|left|right|UP*2|DOWN*1.5|etc",
                        "colors": ["BLUE", "WHITE", "RED"],
                        "transformations": ["scale", "shift", "rotate"],
                        "mathematical_content": "LaTeX equations to display",
                        "visual_elements": ["derived from Stage 1 animation_plan"],
                        "timing": {"start": 0, "end": 30},
                        "layer_order": 1
                    }
                ],
                "scene_config": {
                    "background_color": "BLACK|WHITE|custom_hex",
                    "camera_config": "default|MovingCamera|etc",
                    "total_duration": 180,
                    "resolution": "1080p|720p|4K",
                    "frame_rate": 30
                },
                "educational_metadata": {
                    "learning_objectives": ["from Stage 1"],
                    "target_audience": "from Stage 1",
                    "difficulty_level": "beginner|intermediate|advanced"
                },
                "technical_requirements": {
                    "required_imports": ["Text", "MathTex", "Circle", "Write", "FadeIn"],
                    "custom_functions": ["helper function names if needed"],
                    "external_resources": ["image files, data files if needed"]
                },
                "code_structure": {
                    "class_name": "SceneClassName",
                    "methods": ["construct", "custom_method_1"],
                    "complexity_level": "beginner|intermediate|advanced"
                }
            }

            Guidelines for Manim Code Planning:
            1. Translate educational steps into specific Manim animations
            2. Maintain the pedagogical flow from Stage 1
            3. Use appropriate Manim objects for each visual element
            4. Provide realistic timing and smooth transitions
            5. Follow 3Blue1Brown animation aesthetics and practices
            6. Include proper mathematical notation rendering
            7. Plan for visual clarity and readability
            8. Consider camera movements and scene composition
            9. Ensure code modularity and reusability
            10. Optimize for educational effectiveness

            Your Manim structure will be used to generate complete, executable Python animation code.
            '''
        )

        human_message_prompt = HumanMessagePromptTemplate.from_template("{human_input}")

        prompt = ChatPromptTemplate.from_messages([
            system_message,
            MessagesPlaceholder(variable_name="chat_history"),
            human_message_prompt,
        ])
        return prompt

    def generate_scene_structure(self, prompt):
        """
        Legacy method for backward compatibility.
        Now uses the full two-stage pipeline.
        """
        result = self.generate_complete_video_plan(prompt)
        return result.get("manim_structure", {})

    def generate_scene_script(self, prompt):
        """
        Generate a human-readable script from the complete video plan.
        
        Args:
            prompt (str): User's query.

        Returns:
            str: Generated scene script text.
        """
        video_plan = self.generate_complete_video_plan(prompt)
        
        if not video_plan:
            return "Error: Could not generate video plan."
        
        educational_breakdown = video_plan.get("educational_breakdown", {})
        manim_structure = video_plan.get("manim_structure", {})
        
        script_parts = []
        
        # Educational Content Summary
        script_parts.append("=== EDUCATIONAL BREAKDOWN ===")
        script_parts.append(f"Title: {educational_breakdown.get('title', 'N/A')}")
        script_parts.append(f"Abstract: {educational_breakdown.get('abstract', 'N/A')}")
        script_parts.append(f"Target Audience: {educational_breakdown.get('target_audience', 'N/A')}")
        script_parts.append(f"Duration: {educational_breakdown.get('estimated_total_duration', 'N/A')} seconds")
        
        # Learning Objectives
        objectives = educational_breakdown.get('learning_objectives', [])
        if objectives:
            script_parts.append("\nLearning Objectives:")
            for obj in objectives:
                script_parts.append(f"  • {obj}")
        
        # Educational Steps
        script_parts.append("\n=== EDUCATIONAL STEPS ===")
        for step in educational_breakdown.get('educational_steps', []):
            script_parts.append(f"\nStep {step.get('step_number', '')}: {step.get('step_title', '')}")
            script_parts.append(f"Description: {step.get('description', '')}")
            script_parts.append(f"Narration: {step.get('narration_script', '')}")
            script_parts.append(f"Visual Plan: {step.get('animation_plan', '')}")
            script_parts.append(f"Duration: {step.get('duration_seconds', 'N/A')} seconds")
        
        # Manim Implementation
        if manim_structure:
            script_parts.append("\n=== MANIM IMPLEMENTATION ===")
            script_parts.append(f"Scene: {manim_structure.get('scene_title', 'N/A')}")
            script_parts.append(f"Total Animation Steps: {len(manim_structure.get('animation_steps', []))}")
            
            for step in manim_structure.get('animation_steps', []):
                script_parts.append(f"\nAnimation Step {step.get('step_number', '')}: {step.get('description', '')}")
                script_parts.append(f"  Objects: {', '.join(step.get('manim_objects', []))}")
                script_parts.append(f"  Animations: {', '.join(step.get('animations', []))}")
                script_parts.append(f"  Duration: {step.get('duration', 'N/A')} seconds")
        
        return "\n".join(script_parts)

    def generate_raw_script(self, prompt):
        """
        Generate a raw script (backward compatibility).
        """
        return self.generate_scene_script(prompt)

    def generate_complete_video_plan(self, topic):
        """
        Complete two-stage pipeline: Educational Breakdown + Manim Structure Generation.
        
        This is the main method that orchestrates the entire video generation process:
        Stage 1: Generate comprehensive educational breakdown
        Stage 2: Convert educational content to Manim animation structure
        
        Args:
            topic (str): User's science/math topic request.
            
        Returns:
            dict: Complete video plan with both educational breakdown and Manim structure.
        """
        if not topic:
            return {"error": "No topic provided"}
        
        print("🎬 Starting Complete Video Plan Generation...")
        print(f"📚 Topic: '{topic}'")
        print("=" * 60)
        
        # Stage 1: Educational Breakdown
        print("🔄 STAGE 1: Educational Content Analysis")
        educational_breakdown = self.generate_educational_breakdown(topic)
        
        if not educational_breakdown:
            return {
                "error": "Stage 1 failed - could not generate educational breakdown",
                "topic": topic,
                "educational_breakdown": None,
                "manim_structure": None
            }
        
        print("✅ Stage 1 Complete - Educational breakdown generated")
        print("=" * 60)
        
        # Stage 2: Manim Structure Generation
        print("🔄 STAGE 2: Manim Animation Planning")
        manim_structure = self.generate_manim_structure(educational_breakdown)
        
        if not manim_structure:
            print("⚠️ Stage 2 failed - using educational breakdown only")
            return {
                "topic": topic,
                "educational_breakdown": educational_breakdown,
                "manim_structure": None,
                "stage2_error": "Could not generate Manim structure"
            }
        
        print("✅ Stage 2 Complete - Manim structure generated")
        print("=" * 60)
        
        # Combine results
        complete_plan = {
            "topic": topic,
            "educational_breakdown": educational_breakdown,
            "manim_structure": manim_structure,
            "generation_metadata": {
                "stage1_success": bool(educational_breakdown),
                "stage2_success": bool(manim_structure),
                "total_duration": educational_breakdown.get("metadata", {}).get("estimated_total_duration", 0),
                "educational_steps": len(educational_breakdown.get("educational_steps", [])),
                "animation_steps": len(manim_structure.get("animation_steps", [])) if manim_structure else 0,
                "complexity_level": educational_breakdown.get("metadata", {}).get("difficulty_progression", "intermediate")
            }
        }
        
        print("🎉 COMPLETE VIDEO PLAN GENERATED!")
        print(f"📊 Summary:")
        print(f"   - Educational Steps: {complete_plan['generation_metadata']['educational_steps']}")
        print(f"   - Animation Steps: {complete_plan['generation_metadata']['animation_steps']}")        
        print(f"   - Total Duration: {complete_plan['generation_metadata']['total_duration']} seconds")
        print("=" * 60)
        
        return complete_plan

    def generate_manim_structure(self, educational_breakdown):
        """
        Stage 2: Convert educational breakdown into Manim animation structure.
        
        Args:
            educational_breakdown (dict): Output from Stage 1
            
        Returns:
            dict: Manim scene structure with animation steps
        """
        if not educational_breakdown:
            return None
        
        try:
            # Create Stage 2 conversation chain
            stage2_conversation = ConversationChain(
                llm=self.google_chat,
                prompt=self.stage2_prompt,
                verbose=True,
                memory=ConversationBufferWindowMemory(k=3, memory_key="chat_history", return_messages=True),
                input_key="human_input",
            )
            
            # Build Stage 2 prompt
            stage2_prompt = self._build_stage2_prompt(educational_breakdown)
            
            print("🎨 Converting educational content to Manim animations...")
            response = stage2_conversation.predict(human_input=stage2_prompt)
            
            # Parse Stage 2 response
            manim_structure = self._parse_stage2_response(response, educational_breakdown)
            
            if manim_structure:
                print("✅ Manim structure generation successful!")
                self._validate_manim_structure(manim_structure)
                return manim_structure
            else:
                print("⚠️ Stage 2 parsing failed, generating fallback structure")
                return self._create_manim_fallback_structure(educational_breakdown)
                
        except Exception as e:
            print(f"❌ Error in Stage 2 processing: {e}")
            return self._create_manim_fallback_structure(educational_breakdown)

    def _build_stage2_prompt(self, educational_breakdown):
        """
        Build the prompt for Stage 2 Manim structure generation.
        
        Args:
            educational_breakdown (dict): Educational content from Stage 1
            
        Returns:
            str: Detailed prompt for Manim code planning
        """        
        title = educational_breakdown.get("title", "Science Animation")
        steps = educational_breakdown.get("educational_steps", [])
        
        return """
EDUCATIONAL BREAKDOWN TO CONVERT:
""" + json.dumps(educational_breakdown, indent=2) + """

Please convert this educational breakdown into a detailed Manim animation structure.

Your task is to:
1. Transform each educational step into specific Manim animation sequences
2. Plan appropriate visual objects (Text, MathTex, shapes, etc.)
3. Define smooth transitions and timing
4. Maintain the pedagogical flow from the educational breakdown
5. Create engaging visual storytelling

OUTPUT REQUIREMENTS:
Provide a complete JSON object with this exact structure:

{
    "scene_title": "ManimScene""" + title.replace(' ', '') + """",
    "scene_description": "Animated explanation of """ + title + """",
    "animation_steps": [
        {
            "step_number": 1,
            "action_type": "intro|content|transition|conclusion",
            "manim_objects": ["Text", "MathTex", "Circle", "Rectangle"],
            "animations": ["Write", "FadeIn", "Transform", "Create"],
            "description": "Detailed description of this animation step",
            "narration": "Narration text from educational breakdown",
            "code_snippet": "key_object = Text('Example')",
            "duration": 30,
            "positioning": "center|UP*2|LEFT*3|etc",
            "colors": ["BLUE", "WHITE", "RED"],
            "transformations": ["scale", "shift", "rotate"],
            "mathematical_content": "LaTeX equations if applicable",
            "visual_elements": ["specific visual components"],
            "timing": {"start": 0, "end": 30},
            "layer_order": 1
        }
    ],
    "scene_config": {
        "background_color": "BLACK",
        "camera_config": "default",
        "total_duration": """ + str(sum(step.get('duration_seconds', 0) for step in steps)) + """,
        "resolution": "1080p",
        "frame_rate": 30
    },
    "educational_metadata": {
        "learning_objectives": """ + str(educational_breakdown.get('learning_objectives', [])) + """,
        "target_audience": \"""" + str(educational_breakdown.get('metadata', {}).get('target_audience', 'General')) + """\",
        "difficulty_level": \"""" + str(educational_breakdown.get('metadata', {}).get('difficulty_progression', 'intermediate')) + """\"
    },
    "technical_requirements": {
        "required_imports": ["Text", "MathTex", "Circle", "Write", "FadeIn"],
        "custom_functions": [],
        "external_resources": []
    },
    "code_structure": {
        "class_name": "Scene""" + title.replace(' ', '').replace(':', '') + """",
        "methods": ["construct"],
        "complexity_level": "intermediate"
    }
}

MANIM GUIDELINES:
- Use appropriate Manim objects for each visual element
- Plan smooth transitions between steps
- Follow 3Blue1Brown animation aesthetics
- Ensure timing aligns with narration
- Include proper mathematical notation
- Plan for visual clarity and readability
- Consider camera movements when needed
- Optimize for educational effectiveness

Begin the Manim structure generation now:
"""

    def _parse_stage2_response(self, response, educational_breakdown):
        """
        Parse the Stage 2 response to extract Manim structure.
        
        Args:
            response (str): LLM response from Stage 2
            educational_breakdown (dict): Original educational content
            
        Returns:
            dict: Parsed Manim structure or None
        """
        # Try the same parsing strategies as Stage 1
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Extract JSON from code blocks
        try:
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
        except Exception:
            pass
        
        # Find JSON object in text
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = self._clean_json_string(json_match.group(0))
                return json.loads(json_str)
        except Exception:
            pass
        
        print("⚠️ Stage 2 JSON parsing failed")
        return None

    def _validate_manim_structure(self, manim_structure):
        """
        Validate the Manim structure and provide feedback.
        
        Args:
            manim_structure (dict): Manim structure to validate
        """
        required_keys = ["scene_title", "animation_steps", "scene_config"]
        missing_keys = [key for key in required_keys if key not in manim_structure]
        
        if missing_keys:
            print(f"⚠️ Missing required Manim keys: {missing_keys}")
        
        steps = manim_structure.get("animation_steps", [])
        if len(steps) < 3:
            print(f"⚠️ Only {len(steps)} animation steps found.")
        
        total_duration = manim_structure.get("scene_config", {}).get("total_duration", 0)
        
        print(f"📊 Manim Structure Validation:")
        print(f"   - Animation Steps: {len(steps)}")
        print(f"   - Total Duration: {total_duration} seconds")
        print(f"   - Scene Class: {manim_structure.get('code_structure', {}).get('class_name', 'N/A')}")

    def _create_manim_fallback_structure(self, educational_breakdown):
        """
        Create fallback Manim structure when Stage 2 fails.
        
        Args:
            educational_breakdown (dict): Educational content from Stage 1
            
        Returns:
            dict: Fallback Manim structure
        """
        title = educational_breakdown.get("title", "Science Animation")
        steps = educational_breakdown.get("educational_steps", [])
        
        animation_steps = []
        current_time = 0
        
        for i, step in enumerate(steps):
            duration = step.get("duration_seconds", 30)
            
            animation_step = {
                "step_number": i + 1,
                "action_type": "intro" if i == 0 else "conclusion" if i == len(steps) - 1 else "content",
                "manim_objects": ["Text", "MathTex"],
                "animations": ["Write", "FadeIn", "Transform"],
                "description": f"Animation for: {step.get('step_title', f'Step {i+1}')}",
                "narration": step.get("narration_script", ""),
                "code_snippet": f"title = Text('{step.get('step_title', f'Step {i+1}')}')",
                "duration": duration,
                "positioning": "center",
                "colors": ["BLUE", "WHITE"],
                "transformations": ["scale", "shift"],
                "mathematical_content": "",
                "visual_elements": step.get("visual_elements", {}).get("diagrams", []),
                "timing": {"start": current_time, "end": current_time + duration},
                "layer_order": i + 1
            }
            
            animation_steps.append(animation_step)
            current_time += duration
        
        return {
            "scene_title": f"Animated{title.replace(' ', '').replace(':', '')}",
            "scene_description": f"Manim animation explaining {title}",
            "animation_steps": animation_steps,
            "scene_config": {
                "background_color": "BLACK",
                "camera_config": "default",
                "total_duration": current_time,
                "resolution": "1080p",
                "frame_rate": 30
            },
            "educational_metadata": {
                "learning_objectives": educational_breakdown.get("learning_objectives", []),
                "target_audience": educational_breakdown.get("metadata", {}).get("target_audience", "General"),
                "difficulty_level": educational_breakdown.get("metadata", {}).get("difficulty_progression", "intermediate")
            },
            "technical_requirements": {
                "required_imports": ["Text", "MathTex", "Write", "FadeIn", "Transform"],
                "custom_functions": [],
                "external_resources": []
            },
            "code_structure": {
                "class_name": f"Scene{title.replace(' ', '').replace(':', '')}",
                "methods": ["construct"],
                "complexity_level": "intermediate"
            }
        }
        

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY_SCRIPT')
if GOOGLE_API_KEY:
    script_generator = ScienceVideoGenerator(GOOGLE_API_KEY)
    print("✅ Enhanced Stage 1 Science Video Generator initialized successfully!")
    print("🎯 Ready to generate detailed educational breakdowns with step-by-step analysis using Google Gemini!")
else:
    print("❌ GOOGLE_API_KEY not found. Please set your API key in the .env file.")