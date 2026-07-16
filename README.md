# 🚚 Agente de IA — Políticas de Envíos NovaExpress

Agente de inteligencia artificial capaz de responder preguntas en lenguaje natural sobre el documento oficial de Política de Envíos de la empresa NovaExpress. Proyecto desarrollado como parte del **Challenge Alura — Agente de IA**.

---

## 📋 Descripción General

Este proyecto implementa un agente conversacional que permite a cualquier colaborador consultar las políticas internas de envíos de NovaExpress sin necesidad de abrir ni buscar manualmente dentro del documento. El usuario escribe una pregunta en lenguaje natural y el agente devuelve una respuesta precisa basada en el contenido del documento oficial.

---

## 🏗️ Arquitectura de la Solución

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────────┐
│  Documento      │────▶│  Procesamiento RAG   │────▶│  Agente Conversac.  │
│  .pdf           │     │                      │     │                     │
│  (NovaExpress)  │     │  1. Lectura (pypdf)  │     │  LangChain          │
└─────────────────┘     │  2. Chunking         │     │  + Cohere LLM       │
                        │  3. Embeddings       │     │  (command-r-08-2024)│
                        │  4. FAISS Vector DB  │     │                     │
                        └──────────────────────┘     └─────────────────────┘
                                                               │
                                                               ▼
                                                      ┌─────────────────────┐
                                                      │  Interfaz Web       │
                                                      │  Gradio             │
                                                      │  (puerto 7860)      │
                                                      └─────────────────────┘
```

**Patrón utilizado: RAG (Retrieval Augmented Generation)**

1. El documento `.pdf` es leído y su texto extraído con `pypdf`.
2. El texto se divide en fragmentos (*chunks*) de 500 caracteres con un solapamiento de 50.
3. Cada fragmento se convierte en un vector numérico (*embedding*) usando el modelo `embed-multilingual-v3.0` de Cohere.
4. Los vectores se almacenan en una base de datos vectorial local con **FAISS**.
5. Cuando el usuario hace una pregunta, se buscan los 3 fragmentos más relevantes (*retrieval*) y se envían al modelo `command-r-08-2024` de Cohere junto con la pregunta para generar la respuesta.
6. La interfaz web está construida con **Gradio** y corre en el puerto 7860.

---

## 🛠️ Tecnologías y Herramientas

| Herramienta | Versión | Uso |
|---|---|---|
| Python | 3.10+ | Lenguaje principal |
| LangChain | 0.3.7 | Framework del agente RAG |
| Cohere (command-r-08-2024) | 5.11.0 | Modelo de lenguaje (LLM) |
| Cohere Embeddings | embed-multilingual-v3.0 | Vectorización del texto |
| FAISS | 1.9.0 | Base de datos vectorial local |
| PyPDF | 5.x | Lectura del documento .pdf |
| Gradio | 5.6.0 | Interfaz web del agente |
| Oracle Cloud (OCI) | — | Deploy en la nube |

---

## 📁 Estructura del Repositorio

```
novaexpress-agent/
│
├── novaexpress_agent.ipynb                    # Notebook con el agente en Google Colab
├── app.py                                     # Aplicación principal con interfaz Gradio
├── test_agente.py                             # Script de prueba sin interfaz gráfica
├── requirements.txt                           # Dependencias del proyecto
├── setup_oci.sh                               # Script de instalación para OCI
├── Politica de Envios de NovaExpress.pdf      # Documento fuente
└── README.md                                  # Este archivo
```

---

## ▶️ Instrucciones para Ejecutar el Proyecto

### Prerrequisitos

- Python 3.10 o superior instalado.
- Una API key gratuita de Cohere (obtenela en [dashboard.cohere.com](https://dashboard.cohere.com)).

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/novaexpress-agent.git
cd novaexpress-agent
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar la API key

**Opción A — Variable de entorno (recomendada):**
```bash
export COHERE_API_KEY="tu-api-key-aqui"   # Linux / macOS / OCI
set COHERE_API_KEY="tu-api-key-aqui"      # Windows
```

**Opción B — Directamente en el código:**  
Editá la línea 13 de `app.py` y reemplazá `"tu-api-key-aqui"` por tu clave.

### 4. Ejecutar la aplicación

```bash
python app.py
```

Abrí tu navegador en: `http://localhost:7860`

### Ejecutar solo las pruebas (sin interfaz)

```bash
python test_agente.py
```

---

## 💬 Ejemplos de Preguntas y Respuestas

**Pregunta:** ¿Cuántos intentos de entrega realiza NovaExpress antes de devolver el paquete?  
**Respuesta del agente:** NovaExpress realiza un máximo de dos (2) intentos de entrega. Si el segundo intento falla, el paquete regresa al centro de distribución más cercano, donde permanece en resguardo durante un plazo máximo de 5 días hábiles.

---

**Pregunta:** ¿Cuál es el plazo para reclamar por daño visible en un envío?  
**Respuesta del agente:** El destinatario debe reportar la anomalía en el momento exacto de la entrega al repartidor, o dentro de las 24 horas posteriores a la entrega.

---

**Pregunta:** ¿Cómo se calcula el peso volumétrico de un paquete?  
**Respuesta del agente:** El peso volumétrico se calcula con la fórmula: (Largo × Ancho × Alto en cm) dividido 5000. Si el resultado supera el peso real, se factura el peso volumétrico.

---

**Pregunta:** ¿Qué materiales están prohibidos para enviar?  
**Respuesta del agente:** NovaExpress prohíbe el transporte de sustancias explosivas, gases comprimidos, líquidos inflamables (como perfumes con alto porcentaje de alcohol o combustibles), armas de fuego y bienes perecederos sin cadena de frío controlada.

---

**Pregunta:** ¿Cuál es el costo de envío para un paquete de 3 kg a zona interior?  
**Respuesta del agente:** Según la tabla de tarifas, un paquete en el rango de 2.1 kg a 5.0 kg hacia zona interior tiene un costo base de Gs. 38.000.

---

**Pregunta:** ¿Hasta qué hora debo registrar mi pedido para que salga el mismo día?  
**Respuesta del agente:** Las solicitudes de recolección creadas antes de las 14:00 horas se procesan y despachan el mismo día.

---

## ☁️ Deploy en Oracle Cloud (OCI)

La aplicación fue desplegada en una instancia **OCI Compute** (VM.Standard.E2.1.Micro — capa gratuita).

**Pasos del deploy:**
1. Crear una instancia Ubuntu 22.04 en OCI Free Tier.
2. Conectarse por SSH y clonar el repositorio.
3. Instalar dependencias con `pip install -r requirements.txt`.
4. Configurar la variable de entorno `COHERE_API_KEY`.
5. Abrir el puerto 7860 en las reglas del Security List de OCI.
6. Ejecutar `python app.py` (o con `nohup` para que corra en segundo plano).

> 📸 *Ver captura de pantalla en la sección de evidencias del repositorio.*

---

## 👤 Autor

Desarrollado como parte del **Challenge Alura — Agente de IA**
