from langchain_community.llms import Ollama

llm = Ollama(model="llama2:13b")

llm.invoke("Tell me a joke")
