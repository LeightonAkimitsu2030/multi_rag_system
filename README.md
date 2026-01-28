# Multi-RAG System

A multi-source RAG (Retrieval-Augmented Generation) system powered by Google Gemini.

## Setup Instructions

### 1. Install Dependencies

Dependencies are managed with `uv`. If you don't have it installed:

```bash
pip install uv
```

Then install project dependencies:

```bash
uv sync
```

### 2. Configure API Keys

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

Then edit `.env` and add your API keys:

```
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

**Get your keys from:**
- **Google API Key**: https://ai.google.dev/
- **Tavily API Key**: https://tavily.com/

### 3. Run the Application

```bash
uv run python main/app.py
```

The Flask web server will start on `http://localhost:5000`

## Features

- **Gemini Integration**: Uses Google's Gemini LLM for intelligent responses
- **Multi-Source RAG**: Combines local document retrieval with web search
- **LangGraph Workflow**: State-based conversation flow
- **Web Interface**: Simple Flask-based chat interface

## Project Structure

```
main/
├── app.py                          # Flask application entry point
├── config.py                       # Configuration
├── vector_db.py                    # Vector database setup
├── chatbot/
│   └── backend.py                 # ChatbotManager
└── lang_graphs_policy/
    ├── tavily_search.py           # Web search integration
    ├── workflow_graphs.py          # LangGraph workflow
    └── lookup_policy/             # RAG policy
```

## Troubleshooting

**Error: "Your default credentials were not found"**
- Make sure `GOOGLE_API_KEY` is set in your `.env` file
- Restart the application after updating the `.env` file

**Error: "No module named..."**
- Run `uv sync` to ensure all dependencies are installed

**Python 3.9 end-of-life warning**
- Consider upgrading to Python 3.10 or 3.11 for better support
