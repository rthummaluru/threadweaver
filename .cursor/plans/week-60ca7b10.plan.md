<!-- 60ca7b10-b293-4a9f-a8ff-08874b37ad1c 54325d95-bd46-44d8-82ab-230bf53d6de9 -->
# Next Week Threadweaver Plan

1. Solidify request/response contracts

   - Add required metadata to `app/schemas/requests.py` (session id, tool traces)
   - Update `app/api/chat.py` to validate and log richer payloads for debugging
   - Prepare clients to send structured messages for multi-turn threads
```25:27:threadweaver-backend/app/schemas/requests.py
# TO BE IMPLEMENTED: session_id: str = Field(..., description="The session id")
```


2. Persist chat threads in Supabase

   - Model thread, message, and tool-call tables; add lightweight migration docs/config
   - Extend `app/db/supabase_client.py` helpers for inserts and history fetches
   - Save each turn (prompt, response, tool invocations) before returning to the caller

3. Improve tool execution loop in `LLMChatService`

   - Cache `list_tools` results per request, guard against network timeouts
   - Normalize tool responses (e.g., JSON parsing) before passing back to Claude
   - Add tracing/logging around `response.stop_reason` handling for bug triage
```124:171:threadweaver-backend/app/services/llm_chat_service.py
response = self.client.messages.create(...)
... while response.stop_reason == "tool_use":
    ... tool_results.append({ ... })
```


4. Surface chat history & health endpoints

   - Add read-only API route for prior sessions and tool-call logs
   - Expose Notion MCP / Supabase health diagnostics under `/health`
   - Document usage in `README.md`, including environment setup & sample curl calls

5. Establish baseline tests & observability

   - Write unit tests for schema validation and tool-loop branching
   - Add integration smoke test that mocks Anthropic and Notion MCP
   - Configure structured logging + basic metrics (latency counters)

### To-dos

- [ ] Add session metadata and validation enhancements to chat schemas and API layer
- [ ] Design Supabase tables and persistence helpers; store chat turns persistently
- [ ] Improve LLMChatService tool execution flow and logging
- [ ] Add history/health endpoints and update documentation
- [ ] Create unit/integration tests and logging/metrics setup