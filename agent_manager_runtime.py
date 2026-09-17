from __future__ import annotations

from typing import Any, Optional

from agent import SimpleChatAgent


class AgentManagerRuntime:
    def __init__(self, llm: Optional[Any] = None, model: Optional[str] = None):
        self.llm = llm
        self.model = model

    def create_agent(self, llm: Optional[Any] = None, model: Optional[str] = None) -> SimpleChatAgent:
        return SimpleChatAgent(llm=llm or self.llm, model=model or self.model)
