# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ThreadWeaver is a full-stack AI chat application with a FastAPI backend and React + Vite frontend. The backend integrates with Anthropic's Claude API for chat functionality, Supabase for database operations, and supports LangChain/LangGraph for potential agentic workflows.

I'm aiming to build and deploy my first ever full stack ai application. ive never developed an app before so im trying to gain firsthand experience. ## App overview ### VISION Create a unified assistant that understands your personal workspaces (Slack, Notion, WhatsApp Business) and acts as a **single hub** for both **retrieval**( finding info) and **action** (performing tasks). Goal: **Streamline** work scattered across platforms into **one intelligent interface**. ### CORE PROBLEM Too many different points of communication/storage for users to have to constantly be checking in order to stay up to date with the latest processes I want to learn building something genuinely useful while using the latest AI techinques to retrieve information + perform actions with different popular integrations ### MVP GOAL user should be able to hook up integrations interact with ai chat interface with retrieval capability with slack, notion, whatsapp business UI : one conversation window with a chat button ### USER FLOW user logins in through oauth email login. first they select which of 3 integrations they want to include (cards) prompted to login for respecitive services (potential option to give ai chat some kind of global context) opens straight to chat interface to start chatting with both ### TECH STACK frontend → next js + tailwind css backend → FastAPI for agentic process + data validation backend → node js for other backend stuff (don’t know too much yet) database → supabase (eventually maybe alloydb) ai → gemini + openai deployment → vecerl or gcp docker for containerization to work across multiple machines easily # IMPORTANT I want you to act as a mentor/teacher. I DO NOT want you coding big blocks of code, i want you to help me think through design decisions and help me out when I'm stuck.

## Architecture

### Backend (threadweaver-backend/)
- **Framework**: FastAPI with uvicorn
- **Configuration**: Centralized in `config.py` using Pydantic Settings with `.env` file
- **Database**: Supabase client initialized at startup in `main.py`
- **LLM Integration**: Anthropic Claude via `app/services/llm_chat_service.py`
- **API Structure**: Routers in `app/api/` (currently `/api/v1/chat`)
- **Schemas**: Pydantic models in `app/schemas/requests.py` for request/response validation
- **Placeholder directories**: `app/agents/` and `app/prompts/` prepared for future LangGraph agent implementation

### Frontend (threadweaver-frontend/)
- **Framework**: React 18 with Vite
- **Styling**: Tailwind CSS with PostCSS
- **HTTP Client**: Axios for API communication
- **Development**: Vite dev server with HMR

### Key Architectural Patterns
1. **Singleton Database Client**: `supabase_client` instantiated once in `app/db/supabase_client.py`, initialized at app startup
2. **Centralized Configuration**: All environment variables managed through `config.py` with Pydantic validation
3. **Service Layer**: Business logic isolated in `app/services/` (e.g., `LLMChatService`)
4. **Router Pattern**: API endpoints organized by domain with prefixed routers included in `main.py`

## Development Commands

### Backend Setup and Running
```bash
cd threadweaver-backend

# Create virtual environment (first time only)
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run development server
python main.py
# or with uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup and Running
```bash
cd threadweaver-frontend

# Install dependencies
npm install

# Run development server (default port 5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Environment Configuration
Create `threadweaver-backend/.env` with:
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key  # For embeddings
LANGSMITH_API_KEY=your_langsmith_key  # Optional
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
```

## API Endpoints

### Chat Endpoint
- **POST** `/api/v1/chat`
- **Request**: `ChatRequest` with list of `ChatMessage` objects
- **Response**: `ChatResponse` with assistant message and query_used
- **Implementation**: Currently sends only first user message to Claude (see `llm_chat_service.py:27`)

### Health Check
- **GET** `/health` - Returns app status, name, and version
- **GET** `/` - Welcome message

## Important Implementation Details

### LLM Chat Service
- Uses Anthropic's `claude-sonnet-4-20250514` model
- Service is **synchronous** but method signature is `async` (note: this inconsistency should be addressed)
- Currently only processes first message from request array (see `app/services/llm_chat_service.py:20`)

### Database Connection
- Supabase client connects at startup via `@app.on_event("startup")` in `main.py:48`
- Connection tested against `users` table during startup (see `supabase_client.py:61`)
- App will raise exception and fail to start if Supabase connection fails

### Configuration System
- `config.py` provides centralized settings with `config` singleton
- Includes helper method `get_embedding_model()` for OpenAI embeddings (returns `text-embedding-3-small` by default)
- All sensitive values loaded from `.env` with Pydantic validation

### CORS Configuration
- Configured in `main.py:28` to allow all methods/headers
- Origins controlled via `config.cors_origins`
- Default allows `http://localhost:3000` (update for Vite's port 5173 if needed)

## Code Organization Standards

- **Logging**: Use module-level `logger = logging.getLogger(__name__)` pattern
- **Type Hints**: Use throughout, including `Optional` and union types (e.g., `Client | None`)
- **Schemas**: All request/response models use Pydantic with Field descriptions
- **Error Handling**: Log errors before raising HTTPException in API routes
