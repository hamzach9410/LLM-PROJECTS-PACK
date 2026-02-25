# 🎮 Agent X vs Agent O: AI Tic-Tac-Toe Game

Developed by **Ali Hamza** | AI/ML/DL Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ali%20Hamza-blue?logo=linkedin)](https://www.linkedin.com/in/ali-hamza-ai-ml-dl-engineer/)
[![Email](https://img.shields.io/badge/Email-ihamzaali06%40gmail.com-red?logo=gmail)](mailto:ihamzaali06@gmail.com)

---

## 📌 Overview

An interactive **AI vs AI Tic-Tac-Toe** game where two autonomous agents powered by different language models compete against each other. Built on the **Agno Agent Framework** with a Streamlit interface, real-time board visualization, and full game state management.

Choose any two AI models to battle it out — GPT-4o vs Claude, Gemini vs Llama, or any combination!

---

## ✨ Features

| Feature                    | Description                                                   |
| -------------------------- | ------------------------------------------------------------- |
| 🤖 **Multi-Model Support** | GPT-4o, Claude 3.7, Gemini, Llama 3, o3-mini and more         |
| 🧑‍⚖️ **Referee Agent**       | Coordinates the game, validates moves, and determines outcome |
| ♟️ **Move Validation**     | Full legal move enforcement and invalid move prevention       |
| 📊 **Move History**        | Board state visualization after every move                    |
| 🎯 **Win Detection**       | Detects win, draw, and invalid moves in real-time             |
| 🖥️ **Streamlit UI**        | Interactive board with model selection per player             |
| ⚡ **Agno Framework**      | Built on the fast, flexible Agno Agent Framework              |

---

## 🏗️ Architecture

```
┌────────────────────────────────────────────────┐
│                 Streamlit UI                    │
│   (Model Selection + Board View + History)      │
└────────────────────┬───────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
  ┌──────▼──────┐         ┌──────▼──────┐
  │  Player X   │         │  Player O   │
  │ (Any Model) │◄───────►│ (Any Model) │
  └──────┬──────┘         └──────┬──────┘
         │    strategic moves    │
         └──────────┬────────────┘
                    │
           ┌────────▼────────┐
           │  Master/Referee  │  ← Coordinates turns,
           │     Agent        │    validates moves,
           └────────┬─────────┘    tracks game state
                    │
           ┌────────▼────────┐
           │   Game Engine   │  ← 3x3 board, win detection
           └─────────────────┘
```

### Supported Models

| Provider      | Models                                                                 |
| ------------- | ---------------------------------------------------------------------- |
| **OpenAI**    | `gpt-4o`, `o3-mini`                                                    |
| **Anthropic** | `claude-3-5-sonnet`, `claude-3-7-sonnet`, `claude-3-7-sonnet-thinking` |
| **Google**    | `gemini-2.0-flash`, and other Gemini variants                          |
| **Groq**      | `llama-3.3-70b` and other Llama models                                 |

---

## 🚀 How to Get Started

### 1. Clone the Repository

```bash
git clone https://github.com/hamzach9410/LLM-PROJECTS-PACK.git
cd LLM-PROJECTS-PACK/advanced_ai_agents/autonomous_game_playing_agent_apps/ai_tic_tac_toe_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys

Create a `.env` file in the project directory:

```env
# Required for OpenAI models
OPENAI_API_KEY=your_openai_api_key_here

# Optional — add keys for the models you want to use
ANTHROPIC_API_KEY=your_anthropic_api_key_here   # Claude models
GOOGLE_API_KEY=your_google_api_key_here         # Gemini models
GROQ_API_KEY=your_groq_api_key_here             # Llama models
```

> **Note:** You only need keys for the models you select in the game.

### 4. Run the Game

```bash
streamlit run app.py
```

Open [localhost:8501](http://localhost:8501) in your browser.

---

## 🕹️ How It Works

1. **Select Models** — Choose any two AI models for Player X and Player O from the sidebar
2. **Start Game** — Click Start and watch the agents battle in real time
3. **Each Turn:**
   - The active player agent receives the current board state and valid moves
   - It analyses the position and returns a move in `row col` format (e.g., `1 2`)
   - The Referee Agent validates and applies the move
4. **End Condition** — Game auto-detects **win**, **draw**, or **illegal move**
5. **Move History** — Full board history is displayed after the game ends

---

## 📁 Project Structure

```
ai_tic_tac_toe_agent/
├── app.py           # Streamlit UI and game loop
├── agents.py        # Agent definitions and model factory
├── utils.py         # Board logic, move validation, game state
├── requirements.txt # Dependencies
└── README.md
```

---

## 📦 Requirements

```
agno
streamlit
python-dotenv
openai
anthropic
google-generativeai
groq
```

---

## 👨‍💻 About the Developer

**Ali Hamza** is an AI/ML/DL Engineer specialized in building intelligent autonomous agents and AI-powered applications.

- 🔗 [LinkedIn](https://www.linkedin.com/in/ali-hamza-ai-ml-dl-engineer/)
- 📧 [ihamzaali06@gmail.com](mailto:ihamzaali06@gmail.com)
- 🐙 [GitHub](https://github.com/hamzach9410)
