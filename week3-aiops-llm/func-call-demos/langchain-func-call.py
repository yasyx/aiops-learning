from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    trim_messages,
)
from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import (
    RunnableWithMessageHistory,
    RunnablePassthrough,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

from dotenv import load_dotenv
from operator import itemgetter


load_dotenv()

trimer = trim_messages(
    max_tokens=65,
    strategy="last",
)

promt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are good at plus 、 multiply of numbers ， please answer me in  {language}.",
        ),
        MessagesPlaceholder("messages"),
    ]
)

model = ChatOpenAI(model="gpt-4o-mini",)


trimer = trim_messages(
    max_tokens=650,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=True,
    start_on="human",
)

@tool
def add (a: int , b: int) -> int :
    """Adds two numbers."""
    print("calling add")
    return a + b
@tool
def multiply (a: int, b: int) -> int :
    """Multiplies two numbers."""
    print("calling multiply")
    
    return a * b

tools = [add, multiply]


model = model.bind_tools(tools,tool_choice="auto",strict=True)


chain = (
    RunnablePassthrough.assign(messages=itemgetter("messages") | trimer) | promt | model
)


message_store = {}


def get_message_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in message_store:
        message_store[session_id] = InMemoryChatMessageHistory()
    return message_store[session_id]


config = {"configurable": {"session_id": "session_id_654782"}}

with_msg_his = RunnableWithMessageHistory(
    chain, get_message_history, input_messages_key="messages"
)


res = with_msg_his.invoke(
    {
        "messages": [
            HumanMessage("What is 3 * 12? Also, what is 11 + 49?"),
        ],
        "language": "English",
    },
    config=config,
)

messages = []



for tool_call in res.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)


res = with_msg_his.invoke(
    {
        "messages": messages,
        "language": "English",
    },
    config=config,
)

print(res)
print(res.tool_calls)

print(message_store)
