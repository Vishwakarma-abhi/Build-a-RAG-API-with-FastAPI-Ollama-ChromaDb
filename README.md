
# Build a RAG API with FastAPI

**Project Link:** [View Project](http://nextwork.ai/projects/ai-devops-api)

**Author:** Abhijeet Vishwakarma  
**Email:** jertbeats.music@gmail.com

---

---

## Introducing Today's Project!

In this project, I'm going to build a RAG - Pipeline using FastAPI  This will help me understand the core Concepts of Retrieval Augmented Generation Concepts , How to Build APIs using FastAPI Python Framework and How We convert Text data into Embeddings (i.e. Numerical Form of the data for effecient search based on similarity). I'm interested in this because I want to build a Project which has the foundation of RAG to be implemented .

### Key tools and concepts

The key tools I used include VS Code, Ollama, Git and Github Key concepts I learnt include RAG Core Concepts , How Data is stored and Retrieved from ChromaDB Collections how Multi-Tenancy / User RAG System Works.

### Challenges and wins

This project took me approximately 2 hours with Full Concept understanding. The most challenging part was understanding how collection were store in the chroma db  and embedding fn

---

## Performing RAG Manually

In this step, I'm going to understand How a RAG Pipeline Works Internally and Also Install required tools and dependencies for the project . We will also select embedding model that we are going to use for knowlege base and context both . The RAG stands for "Retrieval Augmented Generation" - from Its name we can we can define it a Generation Procedure where Some Context is fetched/Retrieved from the Knowledg base that we provide / user provide based before sending to LLM . This helps LLM to understand the User requirement fo precisely and help in producing effecient Outputs

![Image](http://nextwork.ai/compassionate_amber_agile_taranui/uploads/ai-devops-api_v3j7x5b9)

### Understanding the three parts of RAG

I performed RAG manually by. augmenting a Context to the original Question(Prompt) The three parts are
Retrieval (Context) data , Augmented data and generation based on the information

### Comparing the two AI models

The key difference is :
nomic-embed-text - It is a Model that convertes text into embeddings (numerical vector form) which helps in performing search based on similarity score of the vectors. It is not used to chat
wheras
qwen2.5:0.5b - It is a Light weight Large Language Model which is used to chat where user gives inputs and it generate output in the form of text as response It is trained using 500 million parameters


---

## Building a Personal Knowledge Base

In this step, I'm going to Write a personal Document which will be used as knowledge base for my LLM and to Build the context based on the user input . This Knowledge based of text will be converted into Embeddings using the nomic model . Emedding are the numerical representation of the data where text is in the form of Vectors(list of data points)

![Image](http://nextwork.ai/compassionate_amber_agile_taranui/uploads/ai-devops-api_g3h7m2r5)

### Creating the profile document

I included information about my personal things this will act a Knowlege base for the AI and we kept in the form of Vectors. 
SO Whenever User comes to the AI for asking something then We donot directly send the input we first check do we have anything reltaed / similar information in our knowledge base or not if yes then we create the context and then this context is attached to the requried input to make the AI aware that hey you can answer based on this information that I am providing you

This helps the AI To understand the user requirement in a more better manner .

### How semantic search finds relevant chunks

When I ask a question, ChromaDB takes the question and use the nomic-embed model to convert the question into vector then Chromadb find the chunks whose vectors are closed in that high dimensional space. This is Semantic Searchin action happens in the background.. Instead of matching keywords , it finds content with the closed meaning 

---

## Creating the RAG API with FastAPI

In this step, I'm going to build an API that will take user's question as input using FastAPI .  The API endpoint will be "/ask" . I'll test it using Swagger UI provided by the FastAPI Framework.

![Image](http://nextwork.ai/compassionate_amber_agile_taranui/uploads/ai-devops-api_j5m1r8t2)

### How the /ask endpoint works

This Single endpoint implments the three steps of the RAG
When User sends a question , it retrieves the 2 most relevant chunks from ChromaDB
Augements the prompt by combining those chunks with question
Generates a grounded answer using qwen2.5:0.5b .
The response Includes the context that was used so that we can verify teh AI's sources

### Testing with Swagger UI

I tested my API by asking "What are my hobbies ?"
 
The AI answered with   "answer": "Based on the information provided:\n\n1. Hiking: Yes, I enjoy hiking.\n2. Playing guitar: Yes, I play guitar.\n3. Reading sci-fi novels: Yes, I like reading science fiction and fantasy books.\n4. Solving a Rubik's cube in under a minute: Yes, I can solve the Rubik's cube with speed and accuracy.\n\nSo, my hobbies are hiking, playing guitar, reading science fiction novels, and solving the Rubik's cube in under a minute.",

 The context used was. - "context_used": [
    "For fun, I enjoy e.g., hiking, playing guitar, reading sci-fi novels.\nA fun fact about me is e.g., I once ran a marathon, I can solve a Rubik's cube in under a minute.",
    "My career goal is to become a e.g., DevOps engineer, cloud architect, AI engineer.\nI'm especially interested in e.g., automation, infrastructure as code, machine learning."
  ]

---

## Extending to a Multi-User AI Directory

In this project extension, I'm adding multi-user support because in the real world RAG Systems serve multiple users or data sources .Multi-tenancy means multiple user support teaches you dynamic document ingestion, metadata filtering in vector databases . 



![Image](http://nextwork.ai/compassionate_amber_agile_taranui/uploads/ai-devops-api_d5g9k3n7)

### Adding the POST /documents endpoint

In this project extension, I added a POST endpoint that that first split the cotnexts into paragraph and create chunks . Then These chunks are storeed in the chromadb collection for creating embeddings . Here when we are creating the collections for the chunks we create use username also appened in the ids of the chunk and also attached username in the metadata 

Metadata filtering allows to easily filter out chunks collections embedding and perform search for the context specific to the username provided by the user


![Image](http://nextwork.ai/compassionate_amber_agile_taranui/uploads/ai-devops-api_r8t2w6y1)

### Verifying multi-user filtering

In this project extension, I tested multi-user queries by building lot of users colllections with diffetent infomation The filter works because it seached teh username in the meta data of the collections which effeciently find that collection whose metadata contains that username 

---

## Wrapping Up

I did this project today to learn how to build a Multi - Tenancy RAG Pipeline

---

---
