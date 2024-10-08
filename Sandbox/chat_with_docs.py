from customagents.DocsAgent import DocsAgent
from agentforge.utils.chroma_utils import ChromaUtils

docs_agent = DocsAgent()
kb = ChromaUtils()

while True:
    user_input = input("Welcome to the chat with docs!\nQuestion: ")
    results = kb.query_memory(collection_name="docs", query=user_input, num_results=5)
    print(results)
    response = docs_agent.run(docs=results['documents'], query=user_input)
    print(f"Agent: {response}")
    # print(f"Results: {results}")
