# Rehearsal

A writing aid for developing fictional characters through interactive scenes. Define your characters, drop them into a scenario, play one yourself, and refine them through feedback until you know exactly who they are.

## What it does

Writers often know their characters in the abstract but struggle to hear their voice. Rehearsal lets you put characters in situations and interact with them directly. The scenes are throwaway. What persists is the character, refined through use.

- **Build characters** with personality, voice, backstory, motivations and fears
- **Set up scenarios** with situation context and relationship dynamics between characters
- **Play a character** and interact with the others, driven by an LLM
- **Give feedback** when the LLM gets something wrong, corrections are stored and remembered
- **Rewind** to any point in the session and try a different direction

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python, FastAPI, LangGraph |
| LLM | Anthropic API (Claude Sonnet) |
| Database | SQLite (dev) |
| Frontend | React, TypeScript |

## Project structure

```
rehearsal/
├── backend/
│   ├── app/
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic request/response shapes
│   │   ├── api/          # FastAPI routers
│   │   ├── graph/        # LangGraph nodes and graph definition
│   │   ├── database.py   # SQLite engine and session
│   │   ├── config.py     # Settings
│   │   └── main.py       # App entrypoint
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/   # React components
    │   ├── api/          # Typed fetch wrappers
    │   └── main.tsx      # Entrypoint
    ├── package.json
    └── tsconfig.json
```

## Setup

### Backend

```bash
cd backend
python -m venv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # add your Anthropic API key
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Environment variables

```
ANTHROPIC_API_KEY=your-key-here
```

## Status

Early development.
