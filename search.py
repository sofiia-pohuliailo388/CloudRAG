import streamlit as st
import cohere
import time
from google import genai
from qdrant_client import QdrantClient
from config import settings

qdrant = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
co = cohere.Client(api_key=settings.COHERE_API_KEY)
gemini = genai.Client(api_key=settings.GOOGLE_API_KEY)

st.set_page_config(page_title="Архів Айн Ренд", page_icon="📚")
st.title("📚 Аналітична система: Архів Айн Ренд")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Запитайте про твори Анни Рейд..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            emb_res = co.embed(
                texts=[prompt],
                model=settings.EMBEDDING_MODEL,
                input_type="search_query",
                embedding_types=["float"]
            )
            query_vector = emb_res.embeddings.float[0]

            search_result = qdrant.query_points(
                collection_name="personal_brain_cohere",
                query=query_vector,
                limit=10
            ).points
            
            raw_docs = [hit.payload["content"] for hit in search_result]
            
            rerank_hits = co.rerank(
                query=prompt, 
                documents=raw_docs, 
                top_n=3, 
                model="rerank-multilingual-v3.0"
            )
            
            context = "\n\n".join([raw_docs[hit.index] for hit in rerank_hits.results])

            response = gemini.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Ти експерт-аналітик. Твоя спеціалізація — твори Анни Рейд. "
                         f"Відповідай на основі наданого контексту. \n\n"
                         f"КОНТЕКСТ:\n{context}\n\nЗАПИТАННЯ:\n{prompt}"
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

            with st.expander("Використані джерела"):
                for hit in rerank_hits.results:
                    st.write(f"Релевантність: {hit.relevance_score:.2f}")
                    st.info(raw_docs[hit.index])

        except Exception as e:
            st.error(f" Виникла помилка: {e}")