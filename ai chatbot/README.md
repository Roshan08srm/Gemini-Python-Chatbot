# Gemini AI Space (Streamlit & SQLite Persistent Chatbot)

A premium, state-of-the-art web application built in **Python** that implements a conversational assistant powered by Google's Gemini models using the official `google-genai` SDK and **Streamlit**.

Unlike simple chat logs, this project features a full **SQLite database backend** to support multiple persistent conversation threads, sidebar navigation, auto-naming, and real-time response streaming.

---

## ✨ Features

* **🌌 Premium Dark Interface:** Custom HSL styling, gradient headers, sleek chat bubbles, and micro-animations for an outstanding user experience.
* **⚡ Live Response Streaming:** Renders response text word-by-word in real-time as Gemini generates it.
* **💾 Local SQLite Database Persistence:** Conversation logs are saved automatically to a local database (`chats.db`), keeping them safe even after app or server restarts.
* **📁 Sidebar Thread Management:**
  * **➕ New Chat:** Instantly provision a new clean chat canvas.
  * **Recent Chats Swapping:** Load and switch between past conversations with complete context recall.
  * **🗑️ Thread Deletion:** Delete individual conversation threads or clear the entire history.
* **🧠 Smart Auto-Naming:** New chats automatically rename themselves in the sidebar based on the topic of your first query.

---

## 🛠️ Prerequisites

Ensure you have the following:

1. **Python 3.8+** installed.
2. A **Gemini API Key** obtained from [Google AI Studio](https://aistudio.google.com/).

---

## 🚀 Setup and Installation

### 1. Install Dependencies

Open your terminal or PowerShell and install Streamlit and the official Google GenAI SDK:

```bash
pip install streamlit google-genai
```

### 2. Configure your API Key

Set your Gemini API key in your terminal context:

* **Windows (Command Prompt):**
  ```cmd
  set GEMINI_API_KEY="your-api-key-here"
  ```
* **Windows (PowerShell):**
  ```powershell
  $env:GEMINI_API_KEY="your-api-key-here"
  ```

### 3. Launch the Web App

Start the Streamlit server from the project directory:

```bash
streamlit run app.py
```

Open `http://localhost:8501` (or the port shown in your terminal) in your browser to start chatting!

---

## 📂 Project File Structure

```
├── .streamlit/
│   └── config.toml       # Custom dark theme colors & fonts
├── .gitignore            # Excludes caches, secrets, and local chats.db
├── app.py                # Main Streamlit frontend interface & session state
├── database.py           # SQLite database schema, operations & migrations
└── README.md             # Project documentation
```
