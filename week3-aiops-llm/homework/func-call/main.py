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


def chat_with_tools(msg: HumanMessage) -> any:
    print(f"向ChatGPT发送消息：《{msg.content}》\n================================================================")
    
    res= msg_with_his.invoke(
        {
            "messages": [
                msg,
            ],
            "language": "Chinese",
        },
        config={"configurable": {"session_id": "session_id_654783"}},
    )

    tool_msgs = []
    # print(res.tool_calls)
    if res.tool_calls :
        for tool_call in res.tool_calls:
            print(f"1. 命中{tool_call["name"]}方法，其参数为：{tool_call["args"]},ID为：{tool_call["id"]}\n")
            slected_tool = all_tools_map[tool_call["name"].lower()]
            
            tool_msg = slected_tool.invoke(tool_call)
            tool_msgs.append(tool_msg)


    print(f"3. 将tool类型的消息返回至LLM解析，其内容为：{tool_msgs}\n")

    res= msg_with_his.invoke(
        {
            "messages": tool_msgs,
            "language": "Chinese",
        },
        config={"configurable": {"session_id": "session_id_654783"}},
    )
    
    print(f"4. ChatGPT返回：{res.content}\n\n")
    return res


# 帮我修改 gateway 的配置，vendor 修改为 alipay
chat_with_tools(HumanMessage(content="帮我修改 gateway 的配置，vendor 修改为 alipay"))


# 帮我重启 gateway 服务
chat_with_tools(HumanMessage(content="帮我重启 gateway 服务"))


# 帮我部署一个 deployment，镜像是 nginx
chat_with_tools(HumanMessage(content="帮我部署一个 deployment，镜像是 nginx"))


