import streamlit as st
from datetime import datetime
import shelve
import base64

# --- 1. PERSISTENCIA ---
def cargar_datos_disco():
    with shelve.open("bazar_goth_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_goth_db") as db:
        db["bloques_db"] = datos

if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# --- 2. CSS TÉTRICO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .shein-card { background: rgba(10, 10, 10, 0.7); border: 1px solid #4a0072; border-radius: 15px; padding: 15px; margin-bottom: 15px; }
    h1, h3 { color: #b39ddb !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. UI ---
st.markdown("<h1 style='text-align:center;'>🌙 BAZAR NOCTURNAL GOTH</h1>", unsafe_allow_html=True)
tab_bazar, tab_anunciarse = st.tabs(["🛍️ Catálogo", "💜 Registro"])

with tab_bazar:
    bloques = {k: v for k, v in st.session_state.bloques_db.items() if v.get('estado') == "🟢 ACTIVO"}
    cols = st.columns(3)
    for i, (id_b, info) in enumerate(bloques.items()):
        with cols[i % 3]:
            html_img = ""
            # Recuperamos los bytes guardados
            for b64_str in info.get('imagenes_b64', []):
                html_img += f'<img src="data:image/png;base64,{b64_str}" style="width:50px; margin:2px; border-radius:5px;">'
            
            st.markdown(f"""
                <div class="shein-card">
                    <h3>{info['vendedor']}</h3>
                    <p>{info['articulos']}</p>
                    {html_img}
                </div>
            """, unsafe_allow_html=True)

with tab_anunciarse:
    with st.form("registro", clear_on_submit=True):
        nombre = st.text_input("Nombre")
        articulos = st.text_area("Artículos")
        fotos = st.file_uploader("Fotos", accept_multiple_files=True)
        
        if st.form_submit_button("Subir"):
            # Convertimos a base64 ANTES de guardar en el disco
            lista_b64 = [base64.b64encode(f.read()).decode() for f in fotos]
            
            id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
            st.session_state.bloques_db[id_b] = {
                "vendedor": nombre, "articulos": articulos, 
                "imagenes_b64": lista_b64, "estado": "🟢 ACTIVO"
            }
            guardar_datos_disco(st.session_state.bloques_db)
            st.rerun()
