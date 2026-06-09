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

# --- 3. CSS (Manteniendo tu estilo original) ---
st.markdown("""
    <style>
    .stApp { background: #050505 !important; color: #e0e0e0 !important; }
    .fb-header-container { background: rgba(20, 20, 20, 0.8); border: 1px solid #9d50bb; border-radius: 20px; padding: 20px; margin-bottom: 30px; }
    .shein-card { background: rgba(255, 255, 255, 0.03); border: 1px solid #9d50bb; border-radius: 12px; padding: 15px; margin-bottom: 15px; }
    h1, h2, h3 { color: #9d50bb !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. ENCABEZADO ---
st.markdown("""
    <div class="fb-header-container">
        <h1 style='text-align:center;'>🌙 BAZAR NOCTURNAL GOTH</h1>
        <p style='text-align:center; font-style: italic;'>Tu estilo, nuestra esencia</p>
    </div>
""", unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Catálogo Goth", "💜 Registrar Espacio", "🔐 Admin"])

# --- PESTAÑA CATÁLOGO (Visualización de fotos) ---
with tab_bazar:
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    cols = st.columns(3)
    for i, (id_b, info_b) in enumerate(bloques_activos.items()):
        with cols[i % 3]:
            # Renderizado de Portada y Perfil (Facebook Style)
            portada_b64 = info_b.get('portada_b64', '')
            perfil_b64 = info_b.get('perfil_b64', '')
            
            # Renderizado de hasta 15 fotos de prendas
            fotos_html = "".join([f'<img src="data:image/png;base64,{b}" style="width:50px; margin:2px;">' for b in info_b.get('fotos_prendas_b64', [])])
            
            st.markdown(f"""
                <div class="shein-card">
                    <img src="data:image/png;base64,{portada_b64}" style="width:100%; border-radius:10px;">
                    <img src="data:image/png;base64,{perfil_b64}" style="width:60px; border-radius:50%; margin-top:-30px; margin-left:10px; border:3px solid #050505;">
                    <h3>{info_b['vendedor']}</h3>
                    <p>📍 {info_b['zona']}</p>
                    <div>{info_b['articulos']}</div>
                    <div style="margin-top:10px;">{fotos_html}</div>
                </div>
            """, unsafe_allow_html=True)

# --- PESTAÑA REGISTRO ---
with tab_anunciarse:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    st.markdown("Costo por bloque: $25 MXN con una vigencia automática de 15 días.")
    with st.form("form_goth", clear_on_submit=True):
        nombre = st.text_input("Nombre / Tienda *")
        whatsapp = st.text_input("WhatsApp *")
        zona = st.text_input("Punto de Entrega *")
        
        # Nuevos campos de carga
        foto_portada = st.file_uploader("🖼️ Foto de Portada", type=["jpg", "png"])
        foto_perfil = st.file_uploader("👤 Foto de Perfil", type=["jpg", "png"])
        
        lista = st.text_area("Artículos y Precios *")
        fotos_prendas = st.file_uploader("📸 Fotos de prendas (Hasta 15)", type=["jpg", "png"], accept_multiple_files=True)
        
        if st.form_submit_button("Subir Bloque"):
            # Conversión a b64
            p_b64 = base64.b64encode(foto_portada.read()).decode() if foto_portada else ""
            pe_b64 = base64.b64encode(foto_perfil.read()).decode() if foto_perfil else ""
            f_b64 = [base64.b64encode(f.read()).decode() for f in fotos_prendas]
            
            id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
            st.session_state.bloques_db[id_b] = {
                "vendedor": nombre, "whatsapp": whatsapp, "zona": zona,
                "articulos": lista, "portada_b64": p_b64, "perfil_b64": pe_b64,
                "fotos_prendas_b64": f_b64, "estado": "⏳ En espera"
            }
            guardar_datos_disco(st.session_state.bloques_db)
            st.success("¡Enviado, Capitana!")

# --- PESTAÑA ADMIN ---
with tab_admin:
    clave = st.text_input("Clave Admin:", type="password")
    if clave == "bazar123":
        for id_b, info in st.session_state.bloques_db.items():
            if st.button(f"Activar {info['vendedor']}"):
                st.session_state.bloques_db[id_b]['estado'] = "🟢 ACTIVO"
                guardar_datos_disco(st.session_state.bloques_db)
                st.rerun()
