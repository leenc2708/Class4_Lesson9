This project is a minimal Streamlit app that accepts a system prompt, context, and question, validates inputs with Pydantic AI, and sends a structured request to OpenRouter to render a streaming LLM response in real time. It follows a functional, modular design with the RORO pattern and uses async I/O for network calls where appropriate. Langfuse provides end-to-end observability (traces, spans, prompt/version tracking, errors, and latency metrics) across the prompt construction and request lifecycle. Configure credentials via environment variables (e.g., OPENROUTER_API_KEY, LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY), then run the Streamlit app to iterate quickly on prompts and context while monitoring quality and performance.

## Implementation Checklist
- [x] Define `PromptInput` (system_prompt, context, question, model) with Pydantic v2
- [x] Validate inputs and `OPENROUTER_API_KEY` on “Start streaming”
- [ ] Use OpenAI-compatible client for OpenRouter:
  - [x] Configure base_url `https://openrouter.ai/api/v1`
  - [x] Supply API key and optional headers (`HTTP-Referer`, `X-Title`)
- [ ] Build messages:
  - [x] system: system_prompt
  - [x] user: `context + question` (context optional)
- [ ] Stream response:
  - [ ] `client.chat.completions.create(..., stream=True)`
  - [ ] Incrementally render tokens via `st.empty()` buffer
- [ ] Wire UI:
  - [ ] Hook “Start streaming” to trigger flow
  - [ ] “Clear” resets `st.session_state`
- [ ] Optional (default off): simple non-streaming PydanticAI mode for single-shot response
- [ ] Deprioritized for later: Langfuse, retries/backoff, token/latency metrics, advanced error mapping