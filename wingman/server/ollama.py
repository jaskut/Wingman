from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

llm = Ollama(model="llama2")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of your ability."),
    MessagesPlaceholder(variable_name="messages"),
])

chain = prompt | llm 