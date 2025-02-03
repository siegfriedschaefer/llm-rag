from pprint import pprint
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

messages = [AIMessage(content=f"Sie studieren also die heimische Vogelwelt?", name="Model")]
messages.append(HumanMessage(content=f"Ja, das stimmt.",name="Heidi"))
messages.append(AIMessage(content=f"Grossartig. Was genau interessiert Sie?", name="Model"))
messages.append(HumanMessage(content=f"Ich würde gerne wissen, welche Vogelart im Kraichgau heimisch ist.", name="Heidi"))

def multipy(a, b):
    return a * b


chat = ChatOpenAI(model="gpt-4o")
chat_with_tools = chat.bind_tools([multipy])
tool_call = chat_with_tools.invoke([HumanMessage(content=f"Was ist 2 plus 3,name='Heidi'")])
# result = chat.invoke([HumanMessage(content=f"Was ist 2 mal 3,name='Heidi'")])
# pprint(result)
pprint(tool_call)

