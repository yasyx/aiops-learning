from langchain_core.tools import tool

@tool
def add (a: int, b: int) -> int:
    """Adds two numbers.
    Args:
    a (int): The first number.
    b (int): The second number.
    """
    return a + b



@tool
def multiply (a: int, b: int) -> int:
    """Multiplies two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
    
    """
    return a * b



print(add.args)
print(add.name)
print(add.description)
print(add.schema)
print(add.args_schema)

# tool_calls = [{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_cAmVA8l0yRwaclPjl0zAiPd4', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_jdoTn9NqpkGYFU9oDq02byAz', 'type': 'tool_call'}]

# for tool_call in tool_calls:
#     selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    
#     tool_msg =  selected_tool.invoke(tool_call)
#     # print(tool_msg)