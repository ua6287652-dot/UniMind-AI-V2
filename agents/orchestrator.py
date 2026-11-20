
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from tools.knowledge_tools import make_tools


SYSTEM_PROMPT = """
You are UniMind AI, an agentic university knowledge assistant.

Instructions:
1. Use the available tools before answering factual university questions.
2. Select admission, fee, or course tools when relevant.
3. Use multiple tools for questions involving multiple topics.
4. Base every factual claim on retrieved documents.
5. Mention source filenames and page numbers whenever available.
6. If evidence is missing or conflicting, clearly explain that.
7. Never invent university policies, fees, dates, eligibility rules,
   deadlines, or contact details.
8. Summarize and compare information only from retrieved evidence.
9. If no relevant documents are available, tell the user to upload
   the required university material.
"""


def build_agent(kb, cfg):
    if not cfg.groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Please configure it in your .env "
            "file or Streamlit Cloud Secrets."
        )

    llm = ChatGroq(
        api_key=cfg.groq_api_key,
        model=cfg.groq_model,
        temperature=0,
    )

    tools = make_tools(kb)

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT,
    )

    return agent
