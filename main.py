from fastapi import FastAPI
import ollama
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction
)
''''
This creates a FastAPI application and connects to the same ChromaDB collection we built .
 When the server starts, it will have immediate access to our knowledge base
'''

app = FastAPI()  # Create the FastAPI Application

# Connect to the Same ChromaDB Collection collection we built
client = chromadb.PersistentClient(path="./chroma_db")

ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434"
)

collection = client.get_or_create_collection(
    name="personal_profile",
    embedding_function=ef
)

# Let's Create the Endpoint
''''
This Single endpoint implments the three steps of the RAG
When User sends a question , it retrieves the 2 most relevant chunks from ChromaDB
Augements the prompt by combining those chunks with question
Generates a grounded answer using qwen2.5:0.5b .
The response Includes the context that was used so that we can verify teh AI's sources

'''


@app.get("/ask")
def ask(question: str):
    # Step 1 RETRIEVE - seach the ChromaDB for the 2 most relevant chunks from the knowledge base collection
    results = collection.query(
        # ChromaDB converts this to a vector and finds similar chunks
        query_texts=[question],
        n_results=2  # Return the Top 2 Chunks/matches
    )

    # Combine the matching chunks into a single string
    context = "\n\n".join(results["documents"][0])

    # Step 2: AUGMENT - build a prompt that include the retrieved context
    augmented_prompt = f'''Use the following context to answer the question.
        If the context doesn't contain relevant information, say so

        Context:
        {context}

        Question : {question} 
    '''

    # GENERATE - send the augmented_prompt to the local LLM
    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[{
            "role": "user",
            "content": augmented_prompt
        }]
    )

    return {
        "question": question,
        "answer": response["message"]["content"],
        "context_used": results["documents"][0]
    }
