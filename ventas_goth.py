import streamlit as st
from datetime import datetime
import shelve
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Bazar Nocturnal Goth", page_icon="🌙", layout="wide")

# --- 2. PERSISTENCIA ---
def get_db():
    return shelve.open("bazar_goth_db", writeback=True)

# --- 3. CSS GOTH (Mantenemos tu esencia) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .fb-card { background: rgba(0, 0, 0, 0.6); border: 1px solid #5d0f75; border-radius: 15px; padding: 0; overflow: hidden; margin-bottom: 20px; }
    .portada { width: 100%; height: 150px; object-fit: cover; }
    .perfil { width: 80px; height: 80px; border-radius: 50%; border: 4px solid #050505; margin-top: -40px; margin-left: 20px; }
    .info { padding: 15px; }
    h1 { color: #b39ddb !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌙 BAZAR NOCTURNAL GOTH</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

# --- CATALOGO ---
with tab1:
    with get_db() as db:
        bloques = db.get("bloques", [])
        cols = st.columns(3)
        for i, b in enumerate(bloques):
            if b['estado'] == "🟢 ACTIVO":
                with cols[i % 3]:
                    # Decodificar base64 a imagen
                    p_img = f"data:image/png;base64,{b['portada']}"
                    pe_img = f"data:image/png;base64,{b['perfil']}"
                    st.markdown(f"""
                        <div class="fb-card">
                            <img src="{p_img}" class="portada">
                            <img src="{pe_img}" class="perfil">
                            <div class="info">
                                <h3>{b['vendedor']}</h3>
                                <p>📍 {b['zona']}</p>
                                <p>{b['articulos']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

# --- REGISTRO ---
with tab2:
    with st.form("registro", clear_on_submit=True):
        nombre = st.text_input("Nombre / Tienda")
        zona = st.text_input("Zona de entrega")
        articulos = st.text_area("Artículos")
        f_portada = st.file_uploader("Foto Portada", type=['jpg', 'png'])
        f_perfil = st.file_uploader("Foto Perfil", type=['jpg', 'png'])
        
        if st.form_submit_button("Subir Bloque"):
            # Convertir a base64
            p_b64 = base64.b64encode(f_portada.read()).decode()
            pe_b64 = base64.b64encode(f_perfil.read()).decode()
            
            with get_db() as db:
                lista = db.get("bloques", [])
                lista.append({
                    "vendedor": nombre, "zona": zona, "articulos": articulos,
                    "portada": p_b64, "perfil": pe_b64, "estado": "⏳ En espera"
                })
                db["bloques"] = lista
            st.success("¡Enviado, Capitana!")

# --- ADMIN ---
with tab3:
    if st.text_input("Clave", type="password") == "bazar123":
        with get_db() as db:
            lista = db.get("bloques", [])
            for i, b in enumerate(lista):
                if b['estado'] == "⏳ En espera":
                    if st.button(f"Activar {b['vendedor']}", key=i):
                        lista[i]['estado'] = "🟢 ACTIVO"
                        db["bloques"] = lista
                        st.rerun()
