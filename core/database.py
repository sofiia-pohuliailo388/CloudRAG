import uuid
import time
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models as qdrant_models
from config import settings

class DatabaseManager:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
        self.co = cohere.Client(api_key=settings.COHERE_API_KEY)
        self.collection_name = "personal_brain_cohere"
        self._setup_collection()

    def _setup_collection(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=qdrant_models.VectorParams(
                    size=settings.EMBEDDING_DIMENSION, 
                    distance=qdrant_models.Distance.COSINE
                )
            )

    def upload_chunks(self, chunks):
        batch_size = 20 
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            texts = [c["content"] for c in batch]
            
            print(f"Обробка пакету {i//batch_size + 1}... ({i}/{len(chunks)})")
            
            try:
                res = self.co.embed(
                    texts=texts,
                    model=settings.EMBEDDING_MODEL,
                    input_type="search_document",
                    embedding_types=["float"]
                )
                
                points = []
                for idx, chunk in enumerate(batch):
                    points.append(qdrant_models.PointStruct(
                        id=chunk["chunk_id"],
                        vector=res.embeddings.float[idx],
                        payload=chunk
                    ))

                self.client.upsert(collection_name=self.collection_name, points=points)
                
                time.sleep(10)
                
            except Exception as e:
                if "429" in str(e):
                    print(" Ліміт Cohere вичерпано. Пауза 60 секунд...")
                    time.sleep(60)
                else:
                    print(f" Помилка бази: {e}")
                    raise e