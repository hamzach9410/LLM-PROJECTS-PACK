# 🎮 AI 3D PyGame Visualizer with DeepSeek R1

Developed by **Ali Hamza** | AI/ML/DL Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ali%20Hamza-blue?logo=linkedin)](https://www.linkedin.com/in/ali-hamza-ai-ml-dl-engineer/)
[![Email](https://img.shields.io/badge/Email-ihamzaali06%40gmail.com-red?logo=gmail)](mailto:ihamzaali06@gmail.com)

---

### 🎓 FREE Step-by-Step Tutorial

**👉 [Click here to follow the complete step-by-step tutorial](https://www.theunwindai.com/p/build-an-ai-3d-pygame-visualizer-with-deepseek-r1)** — learn to build this from scratch with detailed code walkthroughs, explanations, and best practices.

---

## 📌 Overview

This project demonstrates **DeepSeek R1's reasoning capabilities** for auto-generating interactive PyGame visualizations from plain English descriptions. It uses a **multi-agent pipeline** to:

1. Reason through the code using DeepSeek's R1 model
2. Extract clean, executable Python code via GPT-4o
3. Automatically open and run the code on **[Trinket.io](https://trinket.io/features/pygame)** via browser automation agents

---

## ✨ Features

| Feature                       | Description                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------ |
| 🤖 **DeepSeek R1 Reasoning**  | Uses `deepseek-reasoner` model for deep chain-of-thought code planning         |
| 🧹 **GPT-4o Code Extraction** | Cleanly extracts only the Python code from R1's verbose reasoning              |
| 🌐 **Browser Automation**     | Uses `browser-use` agents to navigate and run code on Trinket.io automatically |
| 🎮 **PyGame Visualization**   | See your generated game/animation running in real time online                  |
| 🖥️ **Streamlit UI**           | Clean, simple web interface for API keys + query input                         |
| 🔗 **Multi-Agent System**     | 4 specialized agents: Navigator, Coder, Executor, Viewer                       |

---

## 🏗️ Architecture

```
User Query (Natural Language)
        │
        ▼
┌──────────────────────┐
│  DeepSeek R1 Reasoner │  ← Generates reasoning + embedded code
└──────────┬───────────┘
           │ reasoning_content
           ▼
┌──────────────────────┐
│   GPT-4o (Agno Agent) │  ← Extracts clean Python code
└──────────┬───────────┘
           │ extracted_code
           ▼
┌──────────────────────────────────────────────┐
│           Browser-Use Multi-Agent System       │
│  ┌──────────┐  ┌────────┐  ┌──────────────┐  │
│  │ Navigator │→ │ Coder  │→ │   Executor   │  │
│  │(Open URL) │  │(Write) │  │  (Run Code)  │  │
│  └──────────┘  └────────┘  └──────────────┘  │
│                               ┌──────────┐    │
│                               │  Viewer  │    │
│                               │(Observe) │    │
│                               └──────────┘    │
└──────────────────────────────────────────────┘
           │
           ▼
   PyGame Runs on Trinket.io 🎮
```

---

## 🚀 How to Get Started

### 1. Clone the Repository

```bash
git clone https://github.com/hamzach9410/LLM-PROJECTS-PACK.git
cd LLM-PROJECTS-PACK/advanced_ai_agents/autonomous_game_playing_agent_apps/ai_3dpygame_r1
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Your API Keys

- **DeepSeek API Key** → Sign up at [platform.deepseek.com](https://platform.deepseek.com/)
- **OpenAI API Key** → Sign up at [platform.openai.com](https://platform.openai.com/)

### 4. Run the App

```bash
streamlit run ai_3dpygame_r1.py
```

### 5. Use It!

1. Enter your **DeepSeek** and **OpenAI** API keys in the sidebar
2. Type your PyGame idea (e.g., _"Create a particle explosion with colors"_)
3. Click **Generate Code** → See R1's reasoning + extracted Python code
4. Click **Generate Visualization** → Browser automation runs it on Trinket.io

---

## 💡 Example Queries

```
"Create a particle system simulation where 100 particles emit from the mouse position and respond to keyboard-controlled wind forces"

"Build a 3D rotating cube with colorful faces using PyGame"

"Simulate bouncing balls with realistic gravity and collision detection"

"Create a snake game with increasing speed and score display"
```

---

## 📦 Requirements

```
agno>=2.2.10
langchain-openai
browser-use
streamlit
```

---

## 🔄 How It Works (Step by Step)

1. **Query Input** — User types a natural language description of the desired visualization
2. **DeepSeek R1 Reasoning** — `deepseek-reasoner` model thinks through the code logic with full chain-of-thought reasoning
3. **Code Extraction** — GPT-4o agent extracts only the clean, runnable Python code (no markdown, no explanations)
4. **Browser Automation** — Four specialized `browser-use` agents work in sequence:
   - **Navigator** → Opens `trinket.io/features/pygame`
   - **Coder** → Waits for user to paste or inputs the code
   - **Executor** → Clicks the Run button
   - **Viewer** → Observes the running visualization
5. **Result** — The PyGame visualization runs live in the browser!

---

## 👨‍💻 About the Developer

**Ali Hamza** is an AI/ML/DL Engineer passionate about building intelligent systems and autonomous agents.

- 🔗 [LinkedIn](https://www.linkedin.com/in/ali-hamza-ai-ml-dl-engineer/)
- 📧 [ihamzaali06@gmail.com](mailto:ihamzaali06@gmail.com)
- 🐙 [GitHub](https://github.com/hamzach9410)
