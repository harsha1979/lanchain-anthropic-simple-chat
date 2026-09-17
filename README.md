# LangChain Anthropic Chat Agent

This project provides a simple chat agent built with LangChain and Anthropic that can be:

- injected into the Agent Manager runtime with an LLM provider,
- used over HTTP via FastAPI,
- run locally in the terminal for interactive chat.

## Project structure

- `agent.py` — the reusable chat agent.
- `agent_manager_runtime.py` — runtime injection wrapper for the agent.
- `http_app.py` — HTTP API for the chat interface.
- `local_cli.py` — terminal chat loop.

## Setup

1. Copy `.env.example` to `.env` and set your Anthropic key.
2. Install dependencies:

   ```bash
   python -m venv .venv
   . .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Run the local terminal chat:

   ```bash
   python local_cli.py
   ```

4. Run the HTTP server:

   ```bash
   uvicorn http_app:app --reload --host 0.0.0.0 --port 8000
   ```

5. Send a chat request:

   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"Hello from the agent manager runtime"}'
   ```

## Runtime injection pattern

If the Agent Manager runtime already provides the LLM object, you can inject it directly:

```python
from agent import SimpleChatAgent
from agent_manager_runtime import AgentManagerRuntime

runtime = AgentManagerRuntime(llm=my_llm_instance)
agent = runtime.create_agent()
print(agent.chat("Hello"))
```

This keeps the same agent code usable in the runtime and in local terminal execution.
