from langchain_openai import ChatOpenAI

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda

from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

from ..tools import tools, is_client_side
from .. import config

tool_calls_client = []

def peek(x):
    print("---")
    print(x.__repr__())
    print("---")
    return x

def chain_start(x):
    global tool_calls_client
    tool_calls_client = []
    if 'input' in x.keys():
        x['chat_history'].append(HumanMessage(x.pop('input')))
    return x

def chain_end(x):
    global tool_calls_client
    x['tool_calls'] = tool_calls_client
    if tool_calls_client and 'messages' in x.keys():
        x['messages'][-1].tool_calls = tool_calls_client
    for i, message in enumerate(x["messages"]):
        if message.type == "AIMessageChunk":
            args = message.dict()
            args.pop('type', 'example')
            x["messages"][i] = AIMessage.construct(**args)
        if message.type == "function":
            args = message.dict()
            args.pop('type')
            args['tool_call_id']=x["messages"][i-1].tool_calls[0]['id']
            x["messages"][i] = ToolMessage.construct(**args)


    return x

def fil(x):
    global tool_calls_client
    if x.tool_calls:
        tool_calls_client = [tool for tool in x.tool_calls if is_client_side(tool['name'])]
        x.tool_calls = [tool for tool in x.tool_calls if not is_client_side(tool['name'])]

        x.additional_kwargs['tool_calls'] = x.tool_calls
    return x

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            config.system_description,
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

model = ChatOpenAI(model=config.openai_model)
model_with_tools = model.bind_tools(tools)

agent = (
    { "chat_history": lambda x: x["chat_history"], "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]) }
    | prompt 
    | model_with_tools
    | RunnableLambda(fil)
    | OpenAIToolsAgentOutputParser()
)
chain = RunnableLambda(chain_start) | AgentExecutor(agent=agent, tools=tools, verbose=True) | RunnableLambda(chain_end)

if __name__ == "__main__":
    messages = [HumanMessage("What's the weather in Berlin today?")]
    for chunk in chain.stream({"chat_history":messages}):
        messages += chunk["messages"]
    print(chain.invoke({"chat_history": messages}))