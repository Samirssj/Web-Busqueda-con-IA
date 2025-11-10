import streamlit as st
import google.generativeai as genai
from datetime import datetime

# =============== CONFIGURACIÓN ===============
# Usa tu clave segura desde Streamlit Cloud (Settings → Secrets)
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(
    page_title="Jarvis - Asistente IA",
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
        }
        .user {
            background-color: #007aff;
            color: white;
        }
        .assistant {
            background-color: #e5e5ea;
            color: #000;
        }
    </style>
""", unsafe_allow_html=True)

# =============== FUNCIONES ===============
def obtener_respuesta(prompt):
    try:
        respuesta = model.generate_content(prompt)
        return respuesta.text.strip()
    except Exception as e:
        return f"⚠️ Error al conectar con el servidor: {e}"

# =============== INTERFAZ ===============
st.title("🤖 Jarvis - Asistente con IA")
st.caption("Potenciado por Google Gemini")

if "chat" not in st.session_state:
    st.session_state.chat = []

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🗑️ Limpiar chat"):
        st.session_state.chat = []
        st.experimental_rerun()

# Mostrar historial del chat
for c in st.session_state.chat:
    clase = "user" if c["user"] else "assistant"
    st.markdown(f"<div class='chat-box {clase}'>{c['text']}</div>", unsafe_allow_html=True)

# Entrada del usuario
prompt = st.chat_input("Escribe tu mensaje...")

if prompt:
    st.session_state.chat.append({"text": prompt, "user": True})
    respuesta = obtener_respuesta(prompt)
    st.session_state.chat.append({"text": respuesta, "user": False})
    st.experimental_rerun()
