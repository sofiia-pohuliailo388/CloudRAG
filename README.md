# 📚 Analytical System: Ayn Rand Archive

A pet project — a RAG-based chatbot that loads files from cloud storage, converts them into a vector database, and answers user questions based on the content.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Web interface | Streamlit |
| Vector database | Qdrant |
| Embeddings | Cohere |
| Answer generation | Google Gemini |
| Cloud file storage | Cloudflare R2 |

---

## ⚙️ How It Works
Files in Cloudflare R2 (PDF, DOCX, TXT...)
↓
Split into chunks
↓
Cohere converts to vectors
↓
Stored in Qdrant vector DB
↓
User asks a question in Streamlit
↓
Most relevant chunks are retrieved
↓
Google Gemini generates the answer

---

## ✨ Features

- Supports multiple file formats from cloud storage
- Semantic search across documents
- Chat interface with conversation history
- Powered by state-of-the-art embedding and generation models

---
