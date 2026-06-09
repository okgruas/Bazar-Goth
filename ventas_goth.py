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

# Función auxiliar para convertir imagen a base64
def img_to_base64(img_file):
    return base64.b64encode(img_file.read()).decode()

# --- 3. CSS GOTH TÉTRICO ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .shein-card { background: rgba(10, 10, 10, 0.8); border: 1px solid #4a0072; border-radius: 15px; padding: 0; overflow: hidden; margin-bottom: 20px; }
    .portada { width: 100%; height: 150px; object-fit: cover; }
    .perfil { width: 80px; height: 80px; border-radius: 50%; border: 4px solid #050505; margin-top: -40px; margin-left: 20px; }
    .info-container { padding: 15px; }
    h3 { margin-top: 5px; color: #b39ddb !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. ENCABEZADO ---
st.markdown("<h1 style='text-align:center; color:#b39ddb;'>🌙 BAZAR NOCTURNAL GOTH</h1>", unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

# --- PESTAÑA CATALOGO ---
with tab_bazar:
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    cols = st.columns(3)
    for i, (id_b, info_b) in enumerate(bloques_activos.items()):
        with cols[i % 3]:
            # Recuperar imágenes guardadas
            p_b64 = info_b.get('portada_b64', '')
            pe_b64 = info_b.get('perfil_b64', '')
            fotos_b64 = info_b.get('fotos_b64', [])
            
            fotos_html = "".join([f'<img src="data:image/png;base64,{f}" style="width:50px; height:50px; margin:2px; object-fit:cover;">' for f in fotos_b64])
            
            st.markdown(f"""
                <div class="shein-card">
                    <img src="data:image/png;base64,{p_b64}" class="portada">
                    <img src="data:image/png;base64,{pe_b64}" class="perfil">
                    <div class="info-container">
                        <h3>{info_b['vendedor']}</h3>
                        <p style="font-size: 12px; color: #9575cd;">📍 {info_b['zona']}</p>
                        <div style="font-size: 13px; max-height: 80px; overflow-y: auto;">{info_b['articulos']}</div>
                        <div style="margin-top:10px;">{fotos_html}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# --- PESTAÑA REGISTRO ---
with tab_anunciarse:
    with st.form("form_goth", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre / Tienda *")
        whatsapp = col2.text_input("WhatsApp *")
        zona = st.text_input("Punto de Entrega *")
        
        c1, c2 = st.columns(2)
        foto_portada = c1.file_uploader("🖼️ Foto Portada", type=["jpg", "png"])
        foto_perfil = c2.file_uploader("👤 Foto Perfil", type=["jpg", "png"])
        
        lista = st.text_area("Artículos y Precios *")
        fotos = st.file_uploader("📸 Fotos artículos (Hasta 15)", type=["jpg", "png"], accept_multiple_files=True)
        
        if st.form_submit_button("Subir Bloque"):
            if nombre and foto_portada and foto_perfil:
                # Procesar imágenes a base64
                p_b64 = img_to_base64(foto_portada)
                pe_b64 = img_to_base64(foto_perfil)
                f_b64 = [base64.b64encode(f.read()).decode() for f in fotos]
                
                id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
                st.session_state.bloques_db[id_b] = {
                    "vendedor": nombre, "whatsapp": whatsapp, "zona": zona,
                    "articulos": lista, "portada_b64": p_b64, "perfil_b64": pe_b64,
                    "fotos_b64": f_b64, "estado": "⏳ En espera"
                }
                guardar_datos_disco(st.session_state.bloques_db)
                st.success("¡Solicitud enviada, Capitana!")

# --- PESTAÑA ADMIN ---
with tab_admin:
    clave = st.text_input("Clave Admin:", type="password")
    if clave == "bazar123":
        for id_b, info in st.session_state.bloques_db.items():
            if st.button(f"Activar {info['vendedor']}", key=id_b):
                st.session_state.bloques_db[id_b]['estado'] = "🟢 ACTIVO"
                guardar_datos_disco(st.session_state.bloques_db)
                st.rerun()
