"""
Agente de IA - Política de Envíos NovaExpress
Challenge Alura - Agente con LangChain + Cohere + FAISS + Streamlit
"""

import os
import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ─────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────
COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
DOCUMENTO_PATH = "Politica de Envios de NovaExpress.pdf"

# ─────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────
def leer_pdf(ruta: str) -> str:
    reader = PdfReader(ruta)
    paginas = [p.extract_text() for p in reader.pages if p.extract_text()]
    return "\n".join(paginas)

@st.cache_resource
def inicializar_agente():
    texto = leer_pdf(DOCUMENTO_PATH)

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    fragmentos = splitter.create_documents([texto])

    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model="embed-multilingual-v3.0"
    )
    base_vectorial = FAISS.from_documents(fragmentos, embeddings)

    llm = ChatCohere(
        cohere_api_key=COHERE_API_KEY,
        model="command-r-08-2024",
        temperature=0
    )

    retriever = base_vectorial.as_retriever(search_kwargs={"k": 3})

    template = """Usá el siguiente contexto para responder la pregunta en español.
Si no encontrás la respuesta en el contexto, decí que no tenés esa información.

Contexto:
{context}

Pregunta: {question}

Respuesta:"""

    prompt = PromptTemplate.from_template(template)

    def formatear_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    agente = (
        {"context": retriever | formatear_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return agente

# ─────────────────────────────────────────
# INTERFAZ STREAMLIT
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Agente NovaExpress",
    page_icon="🚚",
    layout="centered"
)

st.title("🚚 Agente de Políticas de Envíos")
st.caption("Consultá el documento oficial de NovaExpress en lenguaje natural.")

st.info("⏳ Cargando el agente por primera vez, esto puede tardar unos segundos...")
agente = inicializar_agente()
st.success("✅ Agente listo. ¡Hacé tu pregunta!")

# Ejemplos de preguntas
with st.expander("💡 Ver ejemplos de preguntas"):
    ejemplos = [
        "¿Cuántos intentos de entrega realiza NovaExpress?",
        "¿Cuál es el plazo para reclamar por daño visible?",
        "¿Cómo se calcula el peso volumétrico?",
        "¿Qué materiales están prohibidos para enviar?",
        "¿Hasta qué hora debo registrar mi pedido para que salga el mismo día?",
        "¿Cuál es el costo de envío para un paquete de 3 kg a zona interior?",
    ]
    for e in ejemplos:
        st.markdown(f"- {e}")

# Historial de conversación
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    with st.chat_message(msg["rol"]):
        st.write(msg["contenido"])

# Input del usuario
pregunta = st.chat_input("Escribí tu pregunta sobre las políticas de NovaExpress...")

if pregunta:
    with st.chat_message("user"):
        st.write(pregunta)
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

    with st.chat_message("assistant"):
        with st.spinner("Buscando respuesta..."):
            respuesta = agente.invoke(pregunta)
        st.write(respuesta)
    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})

st.markdown("---")
st.caption("Agente construido con LangChain + Cohere + FAISS · Challenge Alura")
