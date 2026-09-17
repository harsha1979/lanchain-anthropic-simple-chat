import os
from typing import Any, Optional

from langchain_core.messages import HumanMessage


class SimpleChatAgent:
    def __init__(self, llm: Optional[Any] = None, model: Optional[str] = None, system_prompt: str = "You are a helpful assistant."):
        self.system_prompt = system_prompt
        self.model = model or os.getenv(
            "ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        self.base_url = os.getenv(
            "ANTHROPIC_API_URL") or os.getenv("ANTHROPIC_BASE_URL")

        if llm is not None:
            self.llm = llm
            return

        try:
            from langchain_anthropic import ChatAnthropic
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError(
                "langchain-anthropic is required. Install dependencies with: pip install -r requirements.txt"
            ) from exc

        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Export it before running the agent or inject a custom llm in the runtime."
            )

        self.llm = ChatAnthropic(
            model=self.model,
            api_key=api_key,
            base_url=self.base_url,
            default_headers={"API-Key": api_key, "Authorization": ""},
        )

    def _normalize_content(self, content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for item in content:
                if isinstance(item, dict):
                    if "text" in item:
                        parts.append(str(item["text"]))
                    elif "content" in item:
                        parts.append(self._normalize_content(item["content"]))
                else:
                    parts.append(self._normalize_content(item))
            return "".join(parts)
        if hasattr(content, "text"):
            return str(content.text)
        return str(content)

    def chat(self, message: str) -> str:
        if not message or not message.strip():
            return ""

        response = self.llm.invoke([HumanMessage(content=message)])
        if hasattr(response, "content"):
            return self._normalize_content(response.content)
        if isinstance(response, str):
            return response
        return str(response)
