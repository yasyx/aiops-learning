from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.chat_history import InMemoryChatMessageHistory


model = ChatOpenAI(
    model="gpt-4o-mini",
)