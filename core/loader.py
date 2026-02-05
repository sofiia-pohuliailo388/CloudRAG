import io
import uuid
import fitz
import pandas as pd
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class CloudDataLoader:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200, 
            chunk_overlap=150,
            separators=["\n\n", "\n", ".", " "]
        )

    def get_chunks(self, file_bytes, file_key):
        ext = file_key.split('.')[-1].lower()
        text = ""
        
        if ext == 'pdf':
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = "\n".join([p.get_text() for p in doc])
        elif ext in ['docx', 'doc']:
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([p.text for p in doc.paragraphs])
        elif ext in ['xlsx', 'xls']:
            df = pd.read_excel(io.BytesIO(file_bytes))
            text = df.to_csv(index=False, sep=" ")

        raw_chunks = self.splitter.split_text(text)
        
        processed_chunks = []
        for i, chunk in enumerate(raw_chunks):
            processed_chunks.append({
                "chunk_id": str(uuid.uuid4()), 
                "file_name": file_key,
                "chunk_index": i,
                "content": chunk.strip(),
                "metadata": {"source": file_key, "format": ext}
            })
        return processed_chunks