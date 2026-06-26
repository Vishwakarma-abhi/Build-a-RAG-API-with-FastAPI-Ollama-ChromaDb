
''''
This loads your profile.txt file and splits it into chunks by paragraph.
 Smaller chunks help the AI find the most relevant section rather 
 than dumping the entire document into the prompt.
 Why do we split documents into chunks?

'''
import chromadb
from chromadb.utils.embedding_functions.ollama_embedding_function import (
    OllamaEmbeddingFunction
)

# Load the Document
with open("profile.txt", "r") as f:
    text = f.read()

# Split the text in the document into chunks by paragraph - each blank lin becomes a split point
# # w check if there is any whitespaces we remove it and also keep spliting it in para
chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

print(f"Loaded {len(chunks)} chunks from profile.txt")

# --------------------------- #
''''
💡 What does this code do?
This creates a ChromaDB database that saves to disk, connects it to nomic-embed-text for generating embeddings,
 and creates a collection called personal_profile. A collection is like a table in a relational database.

Here's how the pieces fit together: the OllamaEmbeddingFunction tells
ChromaDB to call your local Ollama server whenever it needs to convert text into vectors. 
ChromaDB handles the storage and search, 
but Ollama's nomic-embed-text model does the actual embedding work behind the scenes.
'''
# Initlize the ChromaDB - PersistentClient saves data to disk so it survives restart
client = chromadb.PersistentClient(path="./chroma_db")

# Connect to the Ollama 's Embedding Model to convert text into vectors
ef = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434",  # Ollama's default local address
)

# Create ( or resuse a collection )- like a table in a database
collection = client.get_or_create_collection(
    name="personal_profile",
    embedding_function=ef
)

# ------------------- #
''''💡 What does this code do?
When you call collection.add(), ChromaDB automatically sends each chunk to nomic-embed-text, 
converts it into a vector, and stores both the text and vector together.
'''
# Add chunks into the collection - ChromaDB automatically generates embeddings
collection.add(
    ids=[f"chunk{i}" for i in range(len(chunks))],  # Unique ids for each chunk
    documents=chunks,  # The actual document
    metadatas=[{"source": "profile", "chunk_index": i}
               for i in range(len(chunks))]
)

print(f"Added {len(chunks)} chunks to the 'personal_profile' collection")
print("Knowledge base built Succesfully ")
