import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

google_ef  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=API_KEY)


chroma_client = chromadb.PersistentClient(path="chroma_persistent_storage")
collection_name = "document_qa_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name, embedding_function=google_ef
)


def load_documents_from_directory(directory_path):
    print("==== Loading documents from directory ====")
    documents = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    documents.append({"id": filename, "text": file.read()})
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")
                
    return documents


def split_text(text, chunk_size=1000, chunk_overlap=20):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - chunk_overlap
        
    return chunks



directory_path = "./Docs"
documents = load_documents_from_directory(directory_path)

print(f"Loaded {len(documents)} documents")

chunked_documents = []
for doc in documents:
    chunks = split_text(doc["text"])
    for i, chunk in enumerate(chunks):
        chunked_documents.append({"id": f"doc{doc['id']}_chunk{i+1}", "text": chunk})

print(f"Split documents into {len(chunked_documents)} chunks")
        
for chunk in chunked_documents:
    chunk_text = chunk["text"]
    print(f"Embedding chunk {chunk['id']}...")
    embedded_chunk_text = google_ef([chunk_text])[0]
    chunk["embedding"] = embedded_chunk_text


print("==== All chunks embedded ====")

for chunk in chunked_documents:
    collection.upsert(
        ids=[chunk["id"]], 
        documents=[chunk["text"]],
        embeddings=[chunk["embedding"]]
    )
    
print("==== All chunks Upserted to collection ====")


def query( question, n_results = 2 ):
    results = collection.query(query_texts=question, n_results=n_results)
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    return relevant_chunks



def askQuestion( question ):
    relevant_chunks = query( question )
    context = "\n\n".join(relevant_chunks)
    
    prompt = str(
            "You are an assistant for question-answering tasks. Use the following pieces of "
            "retrieved context to answer the question. If you don't know the answer, say that you "
            "don't know. Use three sentences maximum and keep the answer concise."
            "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    chat = model.start_chat(
        history = [
            { "role" : "model" , "parts" : [prompt] },
            { "role" : "user" , "parts" : ["Give me precise answer of my previous question"] }
        ]
    )
    
    result = chat.send_message('Give me precise answer of my previous question')
    return result.text


question = "What is databricks?"
answer = askQuestion(question)
print(f"Answer to question '{question}': {answer}")
