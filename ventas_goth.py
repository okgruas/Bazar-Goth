import streamlit as st
from datetime import datetime
import shelve
import base64
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Bazar Nocturnal Goth",
    page_icon="🌙",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"

# --- 2. PERSISTENCIA REAL EN DISCO ---
def cargar_datos_disco():
    with shelve.open("bazar_permanente_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_permanente_db", writeback=True) as db:
        db["bloques_db"] = datos

if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# --- 3. CARGA DE IMÁGENES ---
def obtener_base64_de_imagen(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    return ""

img_portada_base64 = obtener_base64_de_imagen("portada1.png")
img_perfil_base64 = obtener_base64_de_imagen("portada2.png")

# --- 4. ESTILOS CSS (Bazar Nocturnal Goth) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .fb-header-container { background: rgba(0, 0, 0, 0.6); border: 2px solid #5d0f75; border-radius: 20px; padding: 20px; margin-bottom: 30px; }
    .gradient-title { color: #b39ddb !important; font-size: 35px !important; font-weight: bold; }
    .shein-card { background: rgba(20, 20, 20, 0.8); border: 1px solid #5d0f75; border-radius: 15px; padding: 15px; margin-bottom: 20px; color: #d1d1d1; }
    div.stButton > button { background-color: #5d0f75 !important; color: #ffffff !important; border: 1px solid #b39ddb !important; }
    </style>
""", unsafe_allow_html=True)

# --- 5. ENCABEZADO ---
st.markdown(f"""
    <div class="fb-header-container">
        <h1 class="gradient-title">🌙 BAZAR NOCTURNAL GOTH</h1>
        <p>Tu estilo, nuestra esencia</p>
    </div>
""", unsafe_allow_html=True)

# --- 6. PESTAÑAS ---
tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

with tab_bazar:
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v.get('estado') == "🟢 ACTIVO"}
    cols = st.columns(3)
    for i, (id_b, b) in enumerate(bloques_activos.items()):
        with cols[i % 3]:
            st.markdown(f"""
                <div class="shein-card">
                    <h3>{b['vendedor']}</h3>
                    <p>📍 {b['zona']}</p>
                    <p>{b['articulos']}</p>
                </div>
            """, unsafe_allow_html=True)

with tab_anunciarse:
    with st.form("form_anuncio", clear_on_submit=True):
        nombre = st.text_input("Nombre / Tienda *")
        wapp = st.text_input("WhatsApp *")
        zona = st.text_input("Punto de Entrega *")
        articulos = st.text_area("Artículos y Precios *")
        if st.form_submit_button("Subir Bloque"):
            id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
            st.session_state.bloques_db[id_b] = {
                "vendedor": nombre, "whatsapp": wapp, "zona": zona, 
                "articulos": articulos, "estado": "⏳ En espera", "fecha": datetime.now().strftime("%d/%m")
            }
            guardar_datos_disco(st.session_state.bloques_db)
            st.success("¡Registro enviado, Capitana!")

with tab_admin:
    if st.text_input("Clave Admin", type="password") == CONTRASENA_ADMIN:
        for id_b, b in st.session_state.bloques_db.items():
            if b['estado'] == "⏳ En espera":
                if st.button(f"Activar {b['vendedor']}", key=id_b):
                    st.session_state.bloques_db[id_b]['estado'] = "🟢 ACTIVO"
                    guardar_datos_disco(st.session_state.bloques_db)
                    st.rerun()
