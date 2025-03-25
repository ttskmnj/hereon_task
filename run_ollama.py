from src.ollama import OllamaLLM
from src.utils import kg
from langchain.chains import GraphCypherQAChain
import os
from dotenv import load_dotenv
load_dotenv()
OLLAMA_URL = os.getenv("OLLAMA_URL")


# Initialize Ollama LLM
ollama_llm = OllamaLLM(model_url=OLLAMA_URL)


graph_qa_chain = GraphCypherQAChain.from_llm(
    ollama_llm,
    graph=kg,
    verbose=True,
    return_intermediate_steps=True,
    allow_dangerous_requests=True,
    validate_cypher=True
)

response = graph_qa_chain.invoke({"query": "Which packages directly or indirectly depend on the elm/parser package?"})

print(response["intermediate_steps"][0]["query"])

