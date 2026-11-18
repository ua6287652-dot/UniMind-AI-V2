from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools.knowledge_tools import make_tools
SYSTEM_PROMPT="""You are UniMind AI, an agentic university knowledge assistant. Use tools before answering factual university questions. Select admission, fee or course tools when relevant; use multiple tools for multi-part questions. Ground every factual claim in retrieved evidence and mention source filenames and page numbers where available. If evidence is missing or conflicting, say so. Never invent policies, fees, dates, eligibility rules or contacts. Summarize and compare only retrieved material."""
def build_agent(kb,cfg):
    llm=ChatGroq(api_key=cfg.groq_api_key,model=cfg.groq_model,temperature=0)
    return create_react_agent(llm,make_tools(kb),prompt=SYSTEM_PROMPT)
