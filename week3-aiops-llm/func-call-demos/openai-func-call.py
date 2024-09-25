from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()


model = OpenAI()


def addInt(a: int, b: int) -> int:
    """Adds two int."""
    res = a + b + 1
    print("Calling addInt result is : ", res)
    return res


def addStr(a: str, b: str) -> str:
    """Adds two str."""
    res = f"{a}  {b}  yasyx!"
    print("Calling addStr result is : ", res)
    return res



tools = [
    {
        "type": "function",
        "function": {
            "name": "addInt",
            "description": "Add two integer",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}},
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
    
    {
        "type": "function",
        "function": {
            "name": "addStr",
            "description": "Add two string",
            "parameters": {
                "type": "object",
                "properties": {"a": {"type": "string"}, "b": {"type": "string"}},
                "required": ["a", "b"],
                "additionalProperties": False,
            },
        },
    },
]


all_messages = [
    {"role": "system", "content": "You are a helpful assistant. you can‘t modify the result if the function result is wrong."},
    # {
    #     "role": "user",
    #     "content": "What refusal mean in Chinese?",
    # },
    {
        "role": "user",
        "content": "1 + 2 = ?, and how about I + am = ?",
    },
]


completions = model.chat.completions.create(
    model="gpt-4o-mini",
    tools=tools,
    tool_choice="auto",
    messages=all_messages,
)

all_messages.append(completions.choices[0].message)

tool_calls = completions.choices[0].message.tool_calls
if tool_calls :
    for t in tool_calls:
        if t.function.name == "addStr":
            args = json.loads(t.function.arguments)
            all_messages.append(
                {
                    "role": "tool",
                    "content": f"The result of {args.get('a')} + {args.get('b')} is {addStr(args.get('a'), args.get('b'))}",
                    "tool_call_id": t.id,
                }
            )
        if t.function.name == "addInt":
            args = json.loads(t.function.arguments)
            all_messages.append(
                {
                    "role": "tool",
                    "content": f"The result of {args.get('a')} + {args.get('b')} is {addInt(args.get('a'), args.get('b'))}",
                    "tool_call_id": t.id,
                }
            )    


completions = model.chat.completions.create(
    model="gpt-4o-mini",
    tools=tools,
    tool_choice="auto",
    messages=all_messages,
)


print(completions.choices[0].message)
