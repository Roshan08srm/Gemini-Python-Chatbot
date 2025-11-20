# Gemini-Python-Chatbot
A simple Python-based command-line chatbot built with the Google GenAI SDK (Gemini API) and featuring conversational memory.

A simple, command-line chatbot application built in **Python** that demonstrates integration with the **Google Gemini API** using the official `google-genai` SDK.

This project utilizes the `gemini-2.5-flash` model and implements a **stateful chat session**, ensuring the model retains context and conversational memory across multiple user turns.

---

## ✨ Features

* **Conversational Memory:** Maintains context throughout the dialogue using `client.chats.create()`.
* **Gemini 2.5 Flash:** Interacts with the latest high-performance, cost-effective multimodal model.
* **Command Line Interface:** Simple, accessible text-based interaction.
* **Robust Error Handling:** Includes checks for API key initialization and runtime errors.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following:

1.  **Python 3.8+** installed.
2.  A **Gemini API Key** obtained from Google AI Studio.

---

## 🚀 Setup and Installation

### 1. Install the SDK

Open your terminal (PowerShell) and install the required Google GenAI SDK:

```bash
pip install google-genai
