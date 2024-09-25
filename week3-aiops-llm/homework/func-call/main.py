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
            "You are a k8s manager, you can help me manager k8s cluster. Please answer my question in {language}.",
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


def chat_with_tools(msgs: HumanMessage) -> any:
    print(f"向ChatGPT发送消息：{msgs}")
    
    res= msg_with_his.invoke(
        {
            "messages": [
                msgs,
            ],
            "language": "Chinese",
        },
        config={"configurable": {"session_id": "session_id_654783"}},
    )

    tool_msgs = []
    # print(res.tool_calls)
    if res.tool_calls :
        for tool_call in res.tool_calls:
            print(f"命中{tool_call["name"]}方法，其参数为：{tool_call["args"]},ID为：{tool_call["id"]}")
            slected_tool = all_tools_map[tool_call["name"].lower()]
            
            tool_msg = slected_tool.invoke(tool_call)
            tool_msgs.append(tool_msg)


    print(f"将tool类型的消息返回至LLM解析，其内容为：{tool_msgs}")

    res= msg_with_his.invoke(
        {
            "messages": tool_msgs,
            "language": "Chinese",
        },
        config={"configurable": {"session_id": "session_id_654783"}},
    )
    
    return res


# 帮我修改 gateway 的配置，vendor 修改为 alipay

print(f"ChatGPT返回：{chat_with_tools(HumanMessage(content="帮我修改 gateway 的配置，vendor 修改为 alipay")).content}")

print("================================================================")
# 帮我重启 gateway 服务
print(f"ChatGPT返回：{chat_with_tools(HumanMessage(content="帮我重启 gateway 服务")).content}")

print("================================================================")
# 帮我部署一个 deployment，镜像是 nginx
print(f"ChatGPT返回：{chat_with_tools(HumanMessage(content="帮我部署一个 deployment，镜像是 nginx")).content}")


