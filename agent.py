import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

import os
import sqlite3
from datetime import datetime

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver

from scripts.rag_tools import hybrid_search, live_finance_researcher, think_tool

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend

from scripts.deep_prompts import DEEP_RESEARCHER_INSTRUCTIONS, DEEP_ORCHESTRATOR_INSTRUCTIONS

# ## Initialize Memory and File Backend

# create sqlite db dir
os.makedirs('data', exist_ok=True)

# Secure filesystem backend for research outputs
RESEARCH_OUTPUT_DIR = os.path.join(os.getcwd(),"research_outputs")


def get_research_backend(user_id, thread_id):

    USER_OUTPUT_DIR = os.path.join(RESEARCH_OUTPUT_DIR, user_id, thread_id)
    
    os.makedirs(USER_OUTPUT_DIR, exist_ok=True)

    print(f"Writing research files to: {USER_OUTPUT_DIR}")

    # Create filesystem backend with virtual_mode=True for security
    backend = FilesystemBackend(
        root_dir=USER_OUTPUT_DIR,
        virtual_mode=True  # Prevents agent from accessing files outside sandbox
    )

    return backend

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

# ## Initialize LLM and Create DeepAgent

# Initialize model
model = ChatGoogleGenerativeAI(model='gemini-3-flash-preview')

# Tools for the main agent (orchestrator level)
tools = [hybrid_search, live_finance_researcher, think_tool]

def get_deep_agent(user_id, thread_id):

    # # SQLite checkpointer for agent memory
    # conn = sqlite3.connect('data/deep_agent_finance_researcher.db', check_same_thread=False)
    # checkpointer = SqliteSaver(conn=conn)

    backend = get_research_backend(user_id, thread_id)

    # Create the deep agent with memory and secure file backend
    agent = create_deep_agent(
        model=model,
        tools=tools,
        system_prompt=DEEP_ORCHESTRATOR_INSTRUCTIONS,
        subagents=[research_sub_agent],
        # checkpointer=checkpointer,  # SQLite memory
        backend=backend,  # Secure filesystem with virtual_mode=True
    )

    return agent

user_id = 'kgptalkie'
thread_id = 'sessions1'
agent = get_deep_agent(user_id, thread_id)