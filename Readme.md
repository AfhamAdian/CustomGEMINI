# Document QA System with ChromaDB and Google Generative AI

This repository provides a Python-based solution for building a document-based Question Answering (QA) system. It uses ChromaDB for document storage and Google Generative AI (Gemini 1.5 Flash) for embedding and answering questions.

---

## **Project Structure**

- **`main.py`**: The core implementation of the document loader, text chunking, embedding, and question-answering logic.
- **`Docs/`**: A directory where all text files to be indexed are stored.
- **`.env`**: Environment variables file containing sensitive information like the API key.

---

## **Setup and Installation**

### **1. Prerequisites**
- Python 3.8+
- pip (Python package manager)

### **2. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

### **3. Install Dependencies**
Install the required Python libraries:
```bash
pip install chromadb google-generativeai python-dotenv
```

### **4. Configure API Key**
1. Create a `.env` file in the root directory.
2. Add your Google Generative AI API key to the file:
   ```
   API_KEY=your-google-api-key
   ```

### **5. Prepare the Documents**
- Place all `.txt` files to be indexed in the `Docs/` directory.

---

## **Usage**

### **1. Run the Script**
```bash
python main.py
```

### **2. Features**
- **Document Loading**: The script reads all `.txt` files from the `Docs/` directory.
- **Text Chunking**: Splits documents into smaller chunks (default: 1000 characters with 20-character overlap).
- **Embedding**: Uses Google Generative AI to embed the chunks.
- **Document Storage**: Stores the chunks and embeddings in a persistent ChromaDB collection.
- **Question Answering**:
  - Queries the collection for the most relevant chunks.
  - Uses the Gemini model to generate concise answers based on the retrieved context.

---

## **Code Overview**

### **Functions**
1. **`load_documents_from_directory(directory_path)`**:
   - Loads all `.txt` files from the specified directory.

2. **`split_text(text, chunk_size=1000, chunk_overlap=20)`**:
   - Splits a document into smaller, overlapping chunks.

3. **`query(question, n_results=2)`**:
   - Queries the ChromaDB collection for the most relevant chunks.

4. **`askQuestion(question)`**:
   - Uses the context retrieved by `query()` to generate an answer using Google Generative AI.

### **Main Workflow**
1. Load `.txt` files from the `Docs/` directory.
2. Split each document into chunks.
3. Embed each chunk using Google Generative AI.
4. Store the chunks and embeddings in a ChromaDB collection.
5. Accept a user question, query relevant chunks, and generate an answer.

---

## **Example**

1. Add a `.txt` file in the `Docs/` directory (e.g., `example.txt`).
2. Run the script and ask a question:

```python
question = "What is Databricks?"
answer = askQuestion(question)
print(f"Answer: {answer}")
```

Output:
```
Answer: Databricks is a cloud-based platform for big data analytics and AI development.
```

---

## **Dependencies**
- `chromadb`: For persistent vector storage and retrieval.
- `google-generativeai`: To generate embeddings and provide intelligent responses.
- `dotenv`: For environment variable management.

---

## **Future Enhancements**
- Add support for non-text file formats (e.g., PDFs, Word documents).
- Implement better chunking strategies for improved relevance.
- Add a web or command-line interface for easier interaction.
- Explore alternate embedding methods for better accuracy.

---

## **License**
This project is open-source and available under the [MIT License](LICENSE).

---

## **Contributions**
Feel free to submit issues or pull requests to improve this project!
