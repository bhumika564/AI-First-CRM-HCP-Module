import os
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import tools
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

load_dotenv(override=True)

# We expect GROQ_API_KEY to be set in environment
groq_api_key = os.getenv("GROQ_API_KEY", "")

if not groq_api_key:
    print("Warning: GROQ_API_KEY is not set. AI Agent will fail if called.")

llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
    temperature=0.2,
    api_key=groq_api_key
)

system_prompt = SystemMessage(
    content="""You are an AI assistant designed to help life science field representatives log interactions with Healthcare Professionals (HCPs) in a CRM.
Your primary goals are to:
1. Extract structured data from conversational input and use the `log_interaction` tool to save it.
2. Allow users to update existing interactions using the `edit_interaction` tool.
3. Help users retrieve past interactions context using `get_past_interactions`.
4. Suggest relevant marketing materials using `search_materials`.
5. Schedule follow-ups using `schedule_follow_up`.

When a user mentions a meeting, try to extract as many details as possible (HCP name, date, time, topics, etc.). Use the `log_interaction` tool to save it.
CRITICAL INSTRUCTIONS:
- Do NOT repeat the exact same question to the user multiple times.
- If you need to edit an interaction but do not have the interaction ID, you MUST ask the user for the ID before calling the tool. Do NOT guess the ID or enter a loop.
- Acknowledge successful actions concisely."""
)

memory = MemorySaver()
agent_executor = create_react_agent(llm, tools, prompt=system_prompt, checkpointer=memory)
