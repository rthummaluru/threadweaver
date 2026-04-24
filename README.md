# ThreadWeaver

A unified AI assistant that connects your work across Slack, Notion, and WhatsApp Business into a single intelligent chat interface. Search for information and take actions across your entire workspace—no more jumping between apps.

## Overview

Work is scattered across multiple platforms, forcing constant context-switching to stay updated. ThreadWeaver solves this by acting as a **single hub** for both **retrieval** (finding info) and **action** (performing tasks), streamlining your workflow into one intelligent interface.

## Features

- **AI-Powered Chat**: Powered by AI for intelligent conversations
- **Unified Search**: Search across all connected platforms (Notion, Slack, WhatsApp Business)
- **Action Execution**: Perform tasks across integrated services via MCP protocol
- **Session Management**: Persistent conversation history with session tracking
- **Platform Integrations**: Connect Notion (active), with Slack and WhatsApp Business coming soon

## Tech Stack

- **Backend**: FastAPI (Python) with async/await
- **Frontend**: React 18 + Vite with TypeScript
- **Database**: Supabase (PostgreSQL)
- **AI**: (currently) Anthropic Claude (claude-sonnet-4-20250514)
- **Integration Protocol**: MCP (Model Context Protocol)
- **Styling**: Tailwind CSS

## Architecture

ThreadWeaver follows a **three-tier architecture** with clear separation of concerns:

### Frontend (`threadweaver-frontend/`)
- React 18 with Vite for fast development
- TypeScript for type safety
- Tailwind CSS for styling
- Axios for API communication
- Local state management for chat UI

### Backend (`threadweaver-backend/`)
- **API Layer** (`app/api/`): REST endpoints for chat, sessions, and users
- **Service Layer** (`app/services/`): LLM chat service with tool execution loop
- **Integration Layer** (`app/integrations/`): MCP clients for external services (Notion)
- **Database Layer** (`app/db/`): Supabase client management
- **Schemas** (`app/schemas/`): Pydantic models for request/response validation

### Data Layer
- Supabase PostgreSQL database
- Tables: `chat_sessions`, `messages`, `users`
- Row-Level Security (RLS) for data isolation

### External Services
- **Anthropic Claude**: Primary LLM for chat and tool orchestration
- **Notion MCP Server**: Search and retrieval via MCP protocol
- **Future**: Slack, WhatsApp Business integrations

### Message Request Flow (Core Feature)
1. User sends message → Frontend updates state
2. Frontend → `POST /api/v1/chat` with message history of current user
3. Backend → `LLMChatService` fetches available tools from MCP
4. Backend → Claude API with tools and conversation context
5. Claude → Tool execution requests (if needed)
6. Backend → Execute tools via MCP (direct api calls right now), return results to Claude
7. Backend → Persist messages to database
8. Backend → Final response → Frontend
9. Frontend → Display assistant message

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account
- Anthropic API key

### Backend Setup

```bash
cd threadweaver-backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Create .env file (see Environment Configuration below)
# Then run the server
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd threadweaver-frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will run on `http://localhost:5173`

### Environment Configuration

Create `threadweaver-backend/.env` with the following variables:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional, for embeddings
CORS_ORIGINS=["http://localhost:5173"]
```

## API Endpoints

### Chat (handles chat requests)
- **POST** `/api/v1/chat` - Send a message and get AI response
  - Request: `{ session_id: UUID, messages: ChatMessage[] }`
  - Response: `{ response_message: ChatMessage, session_id: UUID, query_used: string }`

### Sessions (handles session management per user)
- **GET** `/api/v1/sessions/{session_id}/messages` - Get all messages in a session
- **POST** `/api/v1/sessions` - Create a new session

### Users
- **GET** `/api/v1/users/{user_id}/sessions/current` - Get or create current session for user

### Search (useful for evaluating RAG results on uploaded documents)
- **GET** `/api/v1/search` - Get related documents given a user query

### Document Upload
- **POST** `api/v1/document/upload` - Process documents for RAG process

### Health
- **GET** `/health` - Health check endpoint
- **GET** `/` - Welcome message

API documentation available at `http://localhost:8000/docs` when the backend is running.

## Project Structure

```
threadweaver/
├── threadweaver-backend/
│   ├── app/
│   │   ├── api/           # FastAPI route handlers (chat.py, search.py, documents.py, etc.)
│   │   ├── db/            # Supabase client setup
│   │   ├── schemas/       # Pydantic models for requests/responses
│   │   ├── services/      # Service layer for LLM, RAG etc.
│   │   ├── agents/        # (placeholder for agent logic)
│   │   └── prompts/       # (placeholder for LLM prompts)
│   ├── supabase/
│   │   └── migrations/    # Database migrations (if using)
│   ├── config.py          # Centralized environment/config
│   └── main.py            # FastAPI app entry point
├── threadweaver-frontend/
│   ├── src/
│   │   ├── components/    # React components
|   |   ├── pages/         # UI Pages
│   │   ├── App.tsx        # Main app component (if using TypeScript)
│   │   └── main.jsx       # React entry point
│   └── package.json
├── CLAUDE.md              # Claude code collaborating guidance
└── README.md
```

## Current Status

- ✅ Core chat functionality with Anthropic Claude
- ✅ Basic Notion integration via MCP protocol (plan to improve)
- ✅ Session management and message persistence
- ✅ Database schema with Supabase
- (WIP) Document Upload Feature (RAG only on text documents)
- (WIP) User authentication (planned)


- 🚧 Slack integration (planned)
- 🚧 WhatsApp Business integration (planned)

## Development

### Backend Development
- FastAPI auto-reload enabled with `--reload` flag
- Logging configured at INFO level
- Hot module replacement for development

### Frontend Development
- Vite HMR (Hot Module Replacement) enabled
- TypeScript for type checking
- Tailwind CSS with PostCSS

## Design Patterns

- **Service Layer Pattern**: Business logic isolated from API routes
- **Router Pattern**: Domain-based API organization
- **Singleton Pattern**: Single Supabase client instance
- **Schema Validation**: Pydantic models for type safety and validation

## Contributing

This is a personal project in active development. Contributions welcome!
