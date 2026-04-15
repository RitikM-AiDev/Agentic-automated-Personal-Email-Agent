from langchain_openai import ChatOpenAI
from langgraph.graph.message import Annotated,add_messages,TypedDict
import os 
from dotenv import load_dotenv  
load_dotenv()
llm = ChatOpenAI(
    model="gemini-2.5-flash-lite",
    base_url=os.getenv("GEMINI_BASE_URL"),
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.0
)
class State(TypedDict):
    history : Annotated[list,add_messages]
    user_input : str
    subject : str
    content : str
    to_email : str
    human_opinion : str
    human_needed : str