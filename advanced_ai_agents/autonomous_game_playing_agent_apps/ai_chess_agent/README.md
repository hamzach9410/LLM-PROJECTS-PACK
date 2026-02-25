# ♜ Agent White vs Agent Black: AI Chess Game

Developed by **Ali Hamza** | AI/ML/DL Engineer

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ali%20Hamza-blue?logo=linkedin)](https://www.linkedin.com/in/ali-hamza-ai-ml-dl-engineer/)
[![Email](https://img.shields.io/badge/Email-ihamzaali06%40gmail.com-red?logo=gmail)](mailto:ihamzaali06@gmail.com)

---

### 🎓 FREE Step-by-Step Tutorial

**👉 [Click here to follow the complete step-by-step tutorial](https://www.theunwindai.com/p/build-a-multi-agent-chess-game)** — learn how to build this from scratch with detailed code walkthroughs, explanations, and best practices.

---

## 📌 Overview

An advanced **AI Chess Game** where two autonomous agents powered by GPT-4o-mini play chess against each other. Built using **Microsoft AutoGen (AG2)** multi-agent framework with a Streamlit interface, complete move validation, and full game state management.

Both agents independently analyze the board, fetch legal moves, and make strategic decisions — no human input required!

---

## ✨ Features

| Feature                          | Description                                              |
| -------------------------------- | -------------------------------------------------------- |
| 🤖 **Multi-Agent System**        | Two GPT-4o-mini agents (White & Black) play autonomously |
| 🧑‍⚖️ **Game Master Agent**         | Validates all moves and manages game state               |
| ♟️ **Full Chess Rules**          | Complete legal move enforcement via `python-chess`       |
| 📊 **Move History**              | Visualizes every board state after each move             |
| 🎯 **Check/Checkmate Detection** | Automatically detects check, checkmate, and stalemate    |
| 🖥️ **Streamlit UI**              | Clean web interface with configurable turns              |
| 🔒 **Secure API Key Input**      | API key entered safely via sidebar                       |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Streamlit UI                        │
│          (API Key + Turn Config + Board View)        │
└──────────────────────┬──────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           │                       │
    ┌──────▼──────┐         ┌──────▼──────┐
    │ Agent White │         │ Agent Black │
    │ (GPT-4o-mini)│◄──────►│ (GPT-4o-mini)│
    └──────┬──────┘         └──────┬──────┘
           │   calls tools         │
           └──────────┬────────────┘
                      │
              ┌───────▼────────┐
              │   Game Master  │  ← Proxy Agent (no LLM)
              │  (Validator)   │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │  python-chess  │  ← Board State & Legal Moves
              └────────────────┘
```

### Agent Roles

| Agent           | Model          | Role                                           |
| --------------- | -------------- | ---------------------------------------------- |
| **Agent White** | GPT-4o-mini    | Strategic decision-maker for white pieces      |
| **Agent Black** | GPT-4o-mini    | Tactical opponent for black pieces             |
| **Game Master** | No LLM (Proxy) | Validates moves, enforces rules, manages turns |

---

## 🚀 How to Get Started

### 1. Clone the Repository

```bash
git clone https://github.com/hamzach9410/LLM-PROJECTS-PACK.git
cd LLM-PROJECTS-PACK/advanced_ai_agents/autonomous_game_playing_agent_apps/ai_chess_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Your OpenAI API Key

- Sign up at [platform.openai.com](https://platform.openai.com/) and obtain your API key.

### 4. Run the App

```bash
streamlit run ai_chess_agent.py
```

### 5. Play!

1. Enter your **OpenAI API key** in the sidebar
2. Set the **number of turns** (5-10 for demo, 200+ for full game)
3. Click **Start Game** and watch the AI agents battle it out!
4. After the game, scroll down to see the full **Move History** with board positions

---

## ⚙️ How It Works

1. **Agent Black** initiates the game by challenging Agent White
2. Each agent's turn:
   - Calls `available_moves()` to fetch all legal moves from the Game Master
   - Analyses the board position strategically
   - Calls `execute_move(move)` with their chosen UCI-format move
3. **Game Master** validates every move against `python-chess` rules
4. The board is updated and visualized after each move
5. Game auto-detects **checkmate**, **stalemate**, **insufficient material**, and **check**

---

## ⚠️ Important Notes

> **API Usage**: A complete chess game takes 200+ turns and can consume significant API credits. For demo purposes, **5-10 turns** is recommended.

> **Move Format**: Agents use UCI format (e.g., `e2e4`, `g1f3`) internally — this is handled automatically.

---

## 📦 Requirements

```
pyautogen
chess
streamlit
```

---

## 👨‍💻 About the Developer

**Ali Hamza** is an AI/ML/DL Engineer specialized in building intelligent autonomous agents and AI-powered applications.

- 🔗 [LinkedIn](https://www.linkedin.com/in/ali-hamza-ai-ml-dl-engineer/)
- 📧 [ihamzaali06@gmail.com](mailto:ihamzaali06@gmail.com)
- 🐙 [GitHub](https://github.com/hamzach9410)
