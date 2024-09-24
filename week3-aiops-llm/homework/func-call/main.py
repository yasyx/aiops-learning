from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories.file import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
from tools import all_tools,all_tools_map

load_dotenv()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert in the field of cloud-native technology, and you have an in-depth understanding of cloud-native related technologies. Please answer my question in {language}.",
        ),
        SystemMessage(content="This is an example conversation."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


def get_message_history(session_id: str) -> BaseChatMessageHistory:
   return FileChatMessageHistory(session_id)


model = ChatOpenAI(
    model="gpt-4o-mini",
)

model = model.bind_tools(all_tools)

chain = prompt | model


msg_with_his = RunnableWithMessageHistory(
    chain,
    get_session_history=get_message_history,
    input_messages_key="messages",
)

res= msg_with_his.invoke(
    {
        "messages": [
            HumanMessage("What is my k8s version ? and show me the pod list."),
        ],
        "language": "Chinese",
    },
    config={"configurable": {"session_id": "session_id_654783"}},
)

tool_msgs = []

if res.tool_calls :
    for tool_call in res.tool_calls:
        slected_tool = all_tools_map[tool_call["name"].lower()]
        tool_msg = slected_tool.invoke(tool_call)
        tool_msgs.append(tool_msg)


print(tool_msgs)

res= msg_with_his.invoke(
    {
        "messages": tool_msgs,
        "language": "Chinese",
    },
    config={"configurable": {"session_id": "session_id_654783"}},
)

print(res)