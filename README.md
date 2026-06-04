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
| Backend | Python, FastAPI, SQLAlchemy |
| API | REST, Pydantic (request/response validation) |
| Orchestration | LangGraph (stateful, checkpointed) |
| LLM | Anthropic API (Claude Sonnet) |
| Database | SQLite |
| Frontend | React 19, TypeScript, React Router 7 |

## Architecture

The backend exposes a REST API via three FastAPI routers (`characters`, `scenarios`, `sessions`). All request and response bodies are validated with Pydantic schemas. SQLAlchemy models back a SQLite database that persists characters, scenarios, relationship dynamics, and accumulated behavioral notes.

Session interactions run through a LangGraph state machine with two conditional nodes: `generate_response` (calls LLM with full character context + behavioral notes) and `process_feedback` (extracts corrections and writes them back as notes). LangGraph's SqliteSaver checkpoints every state transition, enabling rewind.

## Project structure

```
rehearsal/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI routers (characters, scenarios, sessions)
│   │   ├── models/       # SQLAlchemy ORM models
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── graph/        # LangGraph nodes, graph definition, state
│   │   ├── database.py   # SQLite engine and session factory
│   │   ├── config.py     # Settings (loaded from .env)
│   │   └── main.py       # App entrypoint with CORS middleware
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── components/   # React components (Library, Session)
    │   ├── api/          # Typed fetch wrappers
    │   └── main.tsx      # Entrypoint
    ├── package.json
    └── tsconfig.json
```

## Roadmap

### Done
- [x] SQLAlchemy models for characters, scenarios, relationship dynamics, and behavioral notes
- [x] LangGraph state machine with two conditional nodes (roleplay and feedback extraction)
- [x] Session rewind via SqliteSaver checkpointing on every state transition
- [x] Behavioral notes persisted and injected into subsequent prompts so corrections accumulate
- [x] Claude tool-use enforced on both nodes for structured JSON output
- [x] Full CRUD REST API for characters and scenarios
- [x] Session endpoints: start, send message, submit feedback, retrieve state
- [x] Session UI: dual-mode input, narrative history, uncertainty panel, keyboard shortcuts

### In Progress
- [ ] TypeScript API client for character and scenario endpoints (session client already complete)
- [ ] Library UI: character and scenario browsing, creation, and management
- [ ] Scenario composition: assign characters and define per-pair relationship dynamics

### Planned
- [ ] Session listing, resumption, and deletion
- [ ] Streaming LLM responses
- [ ] Scenario editing: add or remove characters and update relationship dynamics after creation

---

## Setup

### Backend

```bash
cd backend
python -m venv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env 
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```
