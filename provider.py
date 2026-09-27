"""Model adapters: deterministic mock mode and OpenRouter-compatible mode."""
from __future__ import annotations
import json, os
from dataclasses import dataclass
from typing import Any

import requests

@dataclass
class ModelResponse:
    content: str
    tool_calls: list[dict[str, Any]]

class MockProvider:
    """A deterministic provider used for grading and offline demonstrations."""
    def complete(self, messages: list[dict[str, str]], tools: list[dict[str, Any]]) -> ModelResponse:
        prompt = messages[-1]["content"] if messages else ""
        if any(message.get("role") == "tool" for message in messages):
            return ModelResponse("The tool completed successfully; the task is complete.", [])
        if "hello.txt" in prompt.lower():
            return ModelResponse("I will create the requested file.", [{"name": "write_file", "arguments": {"path": "hello.txt", "content": "Hello harness\n"}}])
        return ModelResponse("Mock mode completed the request after inspecting the available tools.", [])

class OpenRouterProvider:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is required for live mode")

    def complete(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]]) -> ModelResponse:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json",
                     "HTTP-Referer": os.getenv("OPENROUTER_SITE_URL", "https://github.com"),
                     "X-Title": os.getenv("OPENROUTER_APP_NAME", "AI Harness Engineering")},
            json={"model": self.model, "messages": messages, "tools": tools, "tool_choice": "auto"}, timeout=90,
        )
        response.raise_for_status()
        message = response.json()["choices"][0]["message"]
        calls = []
        for call in message.get("tool_calls", []):
            calls.append({"name": call["function"]["name"], "arguments": json.loads(call["function"].get("arguments", "{}"))})
        return ModelResponse(message.get("content", ""), calls)
