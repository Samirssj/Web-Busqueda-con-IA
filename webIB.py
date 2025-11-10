import streamlit as st
import google.generativeai as genai
from datetime import datetime

# =============== CONFIGURACIÓN ===============
# Clave segura (usa Secrets en Streamlit Cloud)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(
    page_title="🤖 Jarvis - Asistente IA",
    page_icon="🤖",
    layout="wide"
)

# =============== ESTILOS ===============
st.markdown("""
    <style>
        body {
            background-color: #f5f5f7;
            color: #1d1d1f;
            font-family: 'SF Pro Display', sans-serif;
        }
        .chat-box {
            background-color: white;
            padding: 1.2rem;
            border-radius: 15px;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            max-width: 80%;
        }
        .user {
            background-color: #007aff;
            color: white;
            margin-left: auto;
        }
        .assistant {
            background-color: #e5e5ea;
            color: #000;
            margin-right: auto;
        }
    </style>
""", unsafe_allow_html=True)

# =============== FUNCIONES ===============
def obtener_respuesta(prompt):
    """Obtiene respuesta del modelo de Gemini"""
    try:
        respuesta = model.generate_content(prompt)
        return respuesta.text.strip()
    except Exception as e:
        return f"⚠️ Error al conectar con el servidor: {e}"

# =============== INTERFAZ ===============
st.title("🤖 Jarvis - Asistente con IA")
st.caption("Potenciado por Google Gemini")

# Inicializar sesión de chat
if "chat" not in st.session_state:
    st.session_state.chat = []
if "last_prompt" not in st.session_state:
    st.session_state.last_prompt = None

# Botones de control
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🗑️ Limpiar chat"):
        st.session_state.chat.clear()
        st.session_state.last_prompt = None

# Mostrar historial
for msg in st.session_state.chat:
    clase = "user" if msg["user"] else "assistant"
    st.markdown(f"<div class='chat-box {clase}'>{msg['text']}</div>", unsafe_allow_html=True)

# Entrada de usuario
prompt = st.chat_input("Escribe tu mensaje...")

# Procesar entrada
if prompt and prompt != st.session_state.last_prompt:
    st.session_state.last_prompt = prompt
    st.session_state.chat.append({"text": prompt, "user": True})

    respuesta = obtener_respuesta(prompt)
    st.session_state.chat.append({"text": respuesta, "user": False})

    # 🔹 Forzar renderizado sin error
    st.session_state.last_prompt = None
    st.experimental_set_query_params(refresh=datetime.now().timestamp())
