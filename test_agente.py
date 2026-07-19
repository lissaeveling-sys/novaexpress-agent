"""
test_agente.py — Prueba rápida del agente sin interfaz gráfica.
Ejecutar con: python test_agente.py
"""

import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings, ChatCohere
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

COHERE_API_KEY = os.environ.get("COHERE_API_KEY", "tu-api-key-aqui")
DOCUMENTO_PATH = "Politica de Envios de NovaExpress.pdf"

def leer_pdf(ruta):
    reader = PdfReader(ruta)
    paginas = [p.extract_text() for p in reader.pages if p.extract_text()]
    return "\n".join(paginas)

print("📄 Cargando documento...")
texto = leer_pdf(DOCUMENTO_PATH)

print("🔢 Generando embeddings...")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
fragmentos = splitter.create_documents([texto])
embeddings = CohereEmbeddings(cohere_api_key=COHERE_API_KEY, model="embed-multilingual-v3.0")
base_vectorial = FAISS.from_documents(fragmentos, embeddings)

print("🤖 Construyendo agente...")
llm = ChatCohere(cohere_api_key=COHERE_API_KEY, model="command-r-08-2024", temperature=0)
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

preguntas = [
    "¿Cuántos intentos de entrega realiza NovaExpress?",
    "¿Cuál es el plazo para reclamar por daño visible?",
    "¿Cómo se calcula el peso volumétrico?",
    "¿Qué materiales están prohibidos para enviar?",
    "¿Hasta qué hora debo registrar mi pedido para que salga el mismo día?",
]

print("\n" + "="*60)
print("PRUEBAS DEL AGENTE")
print("="*60)

for pregunta in preguntas:
    print(f"\n❓ {pregunta}")
    respuesta = agente.invoke(pregunta)
    print(f"✅ {respuesta}")
    print("-"*60)
