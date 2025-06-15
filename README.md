<div align="center">

# 🧬 EduGen 🎬
### AI-Powered Science Education Video Generator

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Manim-Community-orange.svg" alt="Manim">
  <img src="https://img.shields.io/badge/AI-Powered-green.svg" alt="AI">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

<p align="center">
  🔬 <strong>Physics</strong> • 
  🧪 <strong>Chemistry</strong> • 
  🧬 <strong>Biology</strong> • 
  🌍 <strong>Earth Science</strong> • 
  📊 <strong>Mathematics</strong> • 
  💻 <strong>Computer Science</strong>
</p>

---

*A sophisticated system that leverages Large Language Models (LLMs) and the Manim animation framework to automatically create compelling educational science videos with professional-quality visualizations.*

</div>

## 🚀 Features

### ✨ Intelligent Two-Stage AI Pipeline
1. **Scientific Content Generator**: Creates pedagogically structured, curriculum-aligned scientific explanations
2. **Manim Animation Generator**: Transforms educational content into executable, visually appealing animation code

### 🎯 Core Capabilities
- **Science-Optimized Content Generation**: Domain-specific prompts tailored for various scientific disciplines
- **Structured Educational Output**: JSON-formatted content with visual descriptions, timing, and learning objectives
- **Professional Scientific Visualizations**: Manim-powered animations optimized for scientific concepts
- **Complete Automated Pipeline**: End-to-end generation and rendering of educational science videos
- **Adaptive Complexity Levels**: Content generation for K-12, undergraduate, and advanced levels

### 🔬 Supported Scientific Domains
- **Physics**: Mechanics, Thermodynamics, Electromagnetism, Quantum Physics, Optics
- **Chemistry**: Atomic Structure, Chemical Bonding, Reactions, Organic Chemistry, Biochemistry
- **Biology**: Cell Biology, Genetics, Evolution, Ecology, Human Anatomy & Physiology
- **Earth Science**: Geology, Meteorology, Oceanography, Environmental Science
- **Mathematics**: Algebra, Geometry, Calculus, Statistics, Applied Mathematics
- **Computer Science**: Algorithms, Data Structures, Programming Concepts

## 🏗️ Architecture

```
User Input → Content Generator → Manim Code Generator → Animation Renderer → Final Video
```

### Stage 1: Educational Content Generator
- **Input**: Scientific topic (e.g., "Photosynthesis", "Newton's Laws", "DNA Replication")
- **Output**: Structured JSON with:
  - Step-by-step explanations
  - Visual descriptions
  - Scientific diagrams and models needed
  - Timing information
  - Mathematical equations (when applicable)
  - Key concepts and terminology

### Stage 2: Manim Animation Generator  
- **Input**: Structured educational content
- **Output**: Complete, executable Manim Python code
- **Features**: Scientific visualizations, animations, proper timing, educational appeal

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/EduGen.git
   cd EduGen
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies**
   ```bash
   # LaTeX (for mathematical notation and scientific formulas)
   sudo apt install texlive-full ffmpeg  # Ubuntu/Debian
   # brew install --cask mactex ffmpeg    # macOS
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## 🔧 Configuration

Create a `.env` file with your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here  # Optional fallback
```

## 🎮 Usage

### Web Interface (Streamlit)
```bash
streamlit run app.py
```

Then navigate to `http://localhost:8501` and:
1. Enter a scientific topic
2. Select complexity level and domain
3. Generate structured content
4. Generate Manim animation code
5. Render and download animation

### Programmatic Usage

```python
from script_generator import script_generator
from manim_code_generator import manim_code_generator
from animation_creator import create_animation_from_code

# Generate structured content
content = script_generator.generate_script("Explain cellular respiration")

# Generate Manim code
manim_code = manim_code_generator.generate_manim_code(content)

# Create animation
video_path = create_animation_from_code(manim_code)
```

## 📁 Project Structure

```
EduGen/
├── script_generator.py          # Stage 1: Educational content generation
├── manim_code_generator.py      # Stage 2: Manim code generation
├── animation_creator.py         # Animation rendering
├── app.py                       # Web interface
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
└── media/                       # Generated content storage
```

## 🎨 Example Output Structure

### Generated Content (Stage 1)
```json
{
  "title": "Photosynthesis: Converting Light to Chemical Energy",
  "introduction": "Let's explore how plants transform sunlight into the energy that powers life on Earth...",
  "explanation_steps": [
    {
      "step": 1,
      "narration": "Photosynthesis begins when chloroplasts in plant cells absorb sunlight",
      "visual_description": "Show a plant cell with highlighted chloroplasts, with light rays entering",
      "scientific_objects": ["plant_cell", "chloroplasts", "sunlight", "labels"],
      "duration": 6,
      "key_equation": "6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂",
      "emphasis_points": ["chloroplasts", "light absorption"],
      "learning_objective": "Understand where photosynthesis occurs in plant cells"
    }
  ],
  "complexity_level": "high_school",
  "scientific_domain": "biology",
  "total_duration": 120,
  "prerequisites": ["basic cell structure", "chemical equations"],
  "key_vocabulary": ["chloroplast", "photosynthesis", "glucose", "carbon dioxide"]
}
```

### Generated Manim Code (Stage 2)
```python
from manim import *

class PhotosynthesisScene(Scene):
    def construct(self):
        # Create plant cell with chloroplasts
        cell = Circle(radius=2, color=GREEN).set_fill(GREEN, opacity=0.2)
        chloroplasts = VGroup(*[
            Circle(radius=0.3, color=DARK_GREEN).set_fill(DARK_GREEN, opacity=0.7)
            for _ in range(6)
        ]).arrange_in_grid(2, 3, buff=0.3).move_to(cell.get_center())
        
        # Add title
        title = Text("Photosynthesis", font_size=48, color=GREEN)
        title.to_edge(UP)
        
        # Create sunlight rays
        sun_rays = VGroup(*[
            Arrow(start=UP*3 + LEFT*i, end=cell.get_top() + LEFT*i*0.3, 
                  color=YELLOW, stroke_width=4)
            for i in range(-2, 3)
        ])
        
        # Animation sequence
        self.play(Write(title), run_time=2)
        self.play(Create(cell), run_time=2)
        self.play(Create(chloroplasts), run_time=2)
        self.play(Create(sun_rays), run_time=1.5)
        
        # Show the chemical equation
        equation = MathTex(
            "6CO_2 + 6H_2O + \\text{light} \\rightarrow C_6H_{12}O_6 + 6O_2",
            font_size=36
        ).to_edge(DOWN)
        
        self.play(Write(equation), run_time=3)
        self.wait(3)
```

## 🚧 Development Status

### Phase 1 ✅ (Completed)
- [x] Enhanced script generator with science-specific prompts
- [x] Two-stage LLM pipeline
- [x] Manim code generator
- [x] Improved Streamlit interface

### Phase 2 🔄 (In Progress)
- [ ] Scientific object library (molecules, cells, atoms, etc.)
- [ ] Advanced error handling and validation
- [ ] Real-time animation preview
- [ ] Multi-domain content integration

### Phase 3 📋 (Planned)
- [ ] Interactive scientific simulations
- [ ] Voice narration integration
- [ ] Curriculum alignment features
- [ ] Assessment question generation

## 🎯 Key Benefits

- **Educators**: Create engaging science content without animation expertise
- **Students**: Access high-quality visual explanations for complex scientific concepts
- **Researchers**: Communicate findings through compelling visualizations
- **Content Creators**: Produce professional educational videos efficiently

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Built with ❤️ for science education*