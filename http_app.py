from __future__ import annotations

import os
from typing import Any, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from agent_manager_runtime import AgentManagerRuntime

load_dotenv()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


def create_app(llm: Optional[Any] = None) -> FastAPI:
    runtime = AgentManagerRuntime(llm=llm)
    app = FastAPI(title="LangChain Anthropic Agent")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/chat", response_model=ChatResponse)
    async def chat(request: ChatRequest) -> ChatResponse:
        agent = runtime.create_agent()
        return ChatResponse(response=agent.chat(request.message))

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("http_app:app", host=host, port=port, reload=True)
