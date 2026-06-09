import streamlit as st
from datetime import datetime
import shelve
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Bazar Nocturnal Goth", page_icon="🌙", layout="wide")

# --- 2. PERSISTENCIA ---
def cargar_datos_disco():
    with shelve.open("bazar_goth_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_goth_db") as db:
        db["bloques_db"] = datos

if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# --- 3. CSS GOTH TÉTRICO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .fb-header-container { background: rgba(0, 0, 0, 0.6); border: 2px solid #5d0f75; box-shadow: 0 0 20px rgba(93, 15, 117, 0.5); border-radius: 20px; padding: 25px; margin-bottom: 30px; text-align: center; }
    .shein-card { background: rgba(10, 10, 10, 0.7); border: 1px solid #4a0072; border-radius: 15px; padding: 15px; margin-bottom: 15px; backdrop-filter: blur(5px); }
    .pago-card { background: rgba(30, 0, 45, 0.5); border: 1px solid #8a2be2; padding: 15px; border-radius: 10px; margin: 10px 0; color: #e0e0e0; }
    .stTextInput>div>div>input, .stTextArea>div>textarea { background: #000 !important; color: #fff !important; border: 1px solid #5d0f75 !important; }
    h1, h2, h3 { color: #b39ddb !important; text-shadow: 0 0 10px rgba(179, 157, 219, 0.5); }
    </style>
""", unsafe_allow_html=True)

# --- 4. ENCABEZADO ---
st.markdown("""
    <div class="fb-header-container">
        <h1>🌙 BAZAR NOCTURNAL GOTH</h1>
    </div>
""", unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

# --- PESTAÑA CATALOGO ---
with tab_bazar:
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    cols = st.columns(3)
    for i, (id_b, info_b) in enumerate(bloques_activos.items()):
        with cols[i % 3]:
            # NUEVO: Mostrar fotos
            imgs = ""
            if 'fotos' in info_b:
                for f in info_b['fotos']:
                    b64 = base64.b64encode(f.getvalue()).decode()
                    imgs += f'<img src="data:image/png;base64,{b64}" width="50">'
            
            st.markdown(f"""
                <div class="shein-card">
                    <h3>{info_b['vendedor']}</h3>
                    <p>{info_b['zona']}</p>
                    {info_b['articulos']}
                    <br>{imgs}
                </div>
            """, unsafe_allow_html=True)

# --- PESTAÑA REGISTRO ---
with tab_anunciarse:
    with st.form("form_goth", clear_on_submit=True):
        nombre = st.text_input("Nombre / Tienda *")
        whatsapp = st.text_input("WhatsApp *")
        zona = st.text_input("Punto de Entrega *")
        lista = st.text_area("Artículos y Precios *")
        fotos = st.file_uploader("📸 Fotos", accept_multiple_files=True)
        
        if st.form_submit_button("Subir Bloque"):
            id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
            st.session_state.bloques_db[id_b] = {
                "vendedor": nombre, "whatsapp": whatsapp, "zona": zona,
                "articulos": lista, "fotos": fotos, "estado": "⏳ En espera"
            }
            guardar_datos_disco(st.session_state.bloques_db)
            st.success("¡Solicitud enviada!")

# --- PESTAÑA ADMIN ---
with tab_admin:
    clave = st.text_input("Clave Admin:", type="password")
    if clave == "bazar123":
        for id_b, info in st.session_state.bloques_db.items():
            if st.button(f"Activar {info['vendedor']}", key=id_b):
                st.session_state.bloques_db[id_b]['estado'] = "🟢 ACTIVO"
                guardar_datos_disco(st.session_state.bloques_db)
                st.rerun()
