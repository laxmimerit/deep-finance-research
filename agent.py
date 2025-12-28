import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()


from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI

from scripts.rag_tools import hybrid_search, live_finance_researcher, think_tool
from deepagents import create_deep_agent

from scripts.deep_prompts import DEEP_RESEARCHER_INSTRUCTIONS, DEEP_ORCHESTRATOR_INSTRUCTIONS


# ## Create Research Sub-Agent

# Get current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Create research sub-agent with isolated context
research_sub_agent = {
    "name": "financial-research-agent",
    "description": "Delegate financial research to this sub-agent. Give it one specific research task at a time.",
    "system_prompt": DEEP_RESEARCHER_INSTRUCTIONS.format(date=current_date),
    "tools": [hybrid_search, live_finance_researcher, think_tool],
}


# Initialize model
model = ChatGoogleGenerativeAI(model='gemini-3-flash-preview')

# Tools for the main agent (orchestrator level)
tools = [hybrid_search, live_finance_researcher, think_tool]

# Create the deep agent with memory and secure file backend
agent = create_deep_agent(
    model=model,
    tools=tools,
    system_prompt=DEEP_ORCHESTRATOR_INSTRUCTIONS,
    subagents=[research_sub_agent]
)


