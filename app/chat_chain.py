# app/chat_chain.py
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda
from core.acronyms import expander

# local, free model (install Ollama and pull a model first)
#   ollama pull qwen2.5:7b-instruct
llm = ChatOllama(model="qwen2.5:7b-instruct", temperature=0)

prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant for Sofrecom. Be concise and accurate.

User:
{query}
""")

def _preprocess(inputs: dict) -> dict:
    # 👇 expand acronyms ONCE AND FOR ALL, transparently
    q = inputs.get("query", "")
    return {"query": expander.expand(q)}

chain = RunnableLambda(_preprocess) | prompt | llm

def answer(text: str) -> str:
    return chain.invoke({"query": text}).content

if __name__ == "__main__":
    print(answer("When will SP release? وهل ATF مطلوب؟"))
