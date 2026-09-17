from __future__ import annotations

from typing import Any, Optional

from fastapi import FastAPI
from pydantic import BaseModel

from agent_manager_runtime import AgentManagerRuntime


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
