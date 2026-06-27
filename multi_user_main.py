from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction
)

app = FastAPI()


# Conenct to the Chroma DB Collection we built
client = chromadb.PersistentClient(path="./chroma_db")

ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434"
)

collection = client.get_or_create_collection(
    name="personal_profile",
    embedding_function=ef
)

# Define the expected shape of incoming data for the POST Endpoint

''''
💡 What does this code do?
The DocumentSubmission class defines the expected shape of incoming data.
 FastAPI uses this to validate request bodies and auto-generate documentation. 
 The endpoint chunks the submitted profile the same way build_knowledge_base.py does, 
but attaches the user's name as metadata on each chunk. 
This user_name metadata is the key to the whole multi-user system.

'''


class DocumentSubmission(BaseModel):
    user_name: str  # Who this Profile belongs to
    content: str  # The Profile Text to store


@app.post("/documents")
def add_document(submission: DocumentSubmission):
    # Split the submitted profile into chunks by paragraph
    chunks = [chunk.strip()
              for chunk in submission.content.split("\n\n") if chunk.strip()]

    # Store each chunk in ChromaDB with the user's name attached as metadata
    collection.add(
        ids=[f"{submission.user_name}-chunk{i}" for i in range(len(chunks))],
        documents=chunks,
        metadatas=[
            {"source": "profile", "user_name": submission.user_name, "chunk_index": i}
            for i in range(len(chunks))
        ]
    )

    return {
        "message": f"Added {len(chunks)} chunks for user '{submission.user_name}' .",
        "user_name": submission.user_name,
        "chunks_added": len(chunks)
    }


''''
💡 What does this code do?
The DocumentSubmission class defines the expected shape of incoming data. 
FastAPI uses this to validate request bodies and auto-generate documentation.
 The endpoint chunks the submitted profile the same way build_knowledge_base.py does, 
but attaches the user's name as metadata on each chunk. 
This user_name metadata is the key to the whole multi-user system.
'''


@app.get("/ask")
def ask(question: str, user: str = None):
    # Build the Query parameters
    query_params = {
        "query_texts": [question],
        "n_results": 2
    }

    # If a User name was provided , only search that user's chunks
    if user:
        query_params["where"] = {"user_name": user}
        # chromaDb metadata Filter

    # Step 1 RETRIEVE = search ChromaDB for the most relevant chunks
    results = collection.query(**query_params)
    context = "\n\n".join(results["documents"][0])

    # Step 2 AUGMENT - build the prompt that includes the rerieved context
    augmented_prompt = f"""User the Following context to answer the question 
    If the context doesn't contain relevant information , say so

    Context:
    {context}

    Question: {question} """

    # Step 3 - GENERATE - send the augmented prompt to the local LLM
    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[
            {
                "role": "user",
                "content": augmented_prompt
            }
        ]
    )

    # Return the answer along with metadata about the query
    return {
        "question": question,
        "answer": response["message"]["content"],
        "context_used": results["documents"][0],
        "filtered_by_user": user
    }
