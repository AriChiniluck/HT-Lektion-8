from functools import lru_cache

from langchain.agents import create_agent
from langchain_core.tools import tool

from config import RESEARCH_SYSTEM_PROMPT, build_chat_model
from tools import web_search, read_url, knowledge_search


def _content_to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(text)
            elif isinstance(item, str):
                parts.append(item)
        return "".join(parts)
    return str(content) if content else ""


@lru_cache(maxsize=1)
def get_research_agent():
    return create_agent(
        model=build_chat_model(temperature=0.2),
        tools=[web_search, read_url, knowledge_search],
        system_prompt=RESEARCH_SYSTEM_PROMPT,
    )


@tool
def research(plan: str) -> str:
    """Execute the research plan and return concise findings with sources."""
    plan_text = str(plan or "").strip()
    if not plan_text:
        return "Research plan is empty."

    research_request = (
        "Execute the following research plan and gather evidence.\n\n"
        f"Research plan:\n{plan_text}\n\n"
        "Important: answer in the same language as the user's request, consult the local knowledge base first for course topics, and keep source metadata in the form 'Source / page / Relevance' when available."
    )
    try:
        result = get_research_agent().invoke(
            {"messages": [{"role": "user", "content": research_request}]},
            config={"recursion_limit": 17},
        )
    except Exception as exc:
        return f"Research agent failed: {exc}"
    )

    messages = result.get("messages", [])
    if not messages:
        return "Researcher did not return any findings."

    return _content_to_text(getattr(messages[-1], "content", ""))
