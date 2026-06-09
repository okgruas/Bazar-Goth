import streamlit as st
from datetime import datetime
import shelve
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Bazar Nocturnal Goth", page_icon="🌙", layout="wide")

# --- CSS GOTH (Tu esencia original) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .fb-header-container { background: rgba(0, 0, 0, 0.6); border: 2px solid #5d0f75; box-shadow: 0 0 20px rgba(93, 15, 117, 0.5); border-radius: 20px; padding: 25px; margin-bottom: 30px; text-align: center; }
    .shein-card { background: rgba(10, 10, 10, 0.7); border: 1px solid #4a0072; border-radius: 15px; padding: 15px; margin-bottom: 15px; backdrop-filter: blur(5px); }
    h1, h2, h3 { color: #b39ddb !important; text-shadow: 0 0 10px rgba(179, 157, 219, 0.5); }
    </style>
""", unsafe_allow_html=True)

# --- ENCABEZADO ---
st.markdown("""
    <div class="fb-header-container">
        <h1>🌙 BAZAR NOCTURNAL GOTH</h1>
        <p style='font-style: italic; color: #9575cd;'>Tu estilo, nuestra esencia</p>
    </div>
""", unsafe_allow_html=True)

# --- PERSISTENCIA ---
def get_db():
    return shelve.open("bazar_goth_db", writeback=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

# --- LÓGICA DE VIZUALIZACIÓN ---
with tab_bazar:
    with get_db() as db:
        bloques = db.get("bloques", [])
        cols = st.columns(3)
        for i, b in enumerate(bloques):
            if b.get('estado') == "🟢 ACTIVO":
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="shein-card">
                            <h3>{b['vendedor']}</h3>
                            <p>📍 {b['zona']}</p>
                            <p>{b['articulos']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    # Mostrar las fotos convertidas correctamente
                    for img_b64 in b.get('fotos_b64', []):
                        st.image(base64.b64decode(img_b64), width=100)

with tab_anunciarse:
    with st.form("registro", clear_on_submit=True):
        nombre = st.text_input("Nombre / Tienda")
        zona = st.text_input("Zona")
        articulos = st.text_area("Artículos")
        fotos = st.file_uploader("📸 Fotos", accept_multiple_files=True)
        
        if st.form_submit_button("Subir Bloque"):
            fotos_b64 = [base64.b64encode(f.read()).decode() for f in fotos]
            with get_db() as db:
                lista = db.get("bloques", [])
                lista.append({"vendedor": nombre, "zona": zona, "articulos": articulos, "fotos_b64": fotos_b64, "estado": "⏳ En espera"})
                db["bloques"] = lista
            st.success("¡Solicitud enviada!")

with tab_admin:
    if st.text_input("Clave", type="password") == "bazar123":
        with get_db() as db:
            lista = db.get("bloques", [])
            for i, b in enumerate(lista):
                if b['estado'] == "⏳ En espera" and st.button(f"Activar {b['vendedor']}", key=str(i)):
                    lista[i]['estado'] = "🟢 ACTIVO"
                    db["bloques"] = lista
                    st.rerun()
