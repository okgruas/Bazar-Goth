import streamlit as st
import shelve
import base64
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Bazar Nocturnal Goth", page_icon="🌙", layout="wide")

# --- PERSISTENCIA ---
def cargar_db():
    return shelve.open("bazar_goth_db", writeback=True)

# --- CSS (Estilo Facebook para fotos + Estilo Goth) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .fb-card { background: rgba(0, 0, 0, 0.6); border: 2px solid #5d0f75; border-radius: 15px; overflow: hidden; margin-bottom: 20px; padding: 0; }
    .portada { width: 100%; height: 180px; object-fit: cover; }
    .perfil { width: 100px; height: 100px; border-radius: 50%; border: 4px solid #000; margin-top: -50px; margin-left: 20px; }
    .info { padding: 15px; }
    h1 { color: #b39ddb !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🌙 BAZAR NOCTURNAL GOTH</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

# --- CATALOGO ---
with tab1:
    with cargar_db() as db:
        bloques = db.get("bloques", [])
        cols = st.columns(3)
        for i, b in enumerate(bloques):
            if b.get('estado') == "🟢 ACTIVO":
                with cols[i % 3]:
                    st.markdown(f"""
                        <div class="fb-card">
                            <img src="data:image/png;base64,{b['portada']}" class="portada">
                            <img src="data:image/png;base64,{b['perfil']}" class="perfil">
                            <div class="info">
                                <h3>{b['vendedor']}</h3>
                                <p>📍 {b['zona']}</p>
                                <p>🛍️ {b['articulos']}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    # Galería de artículos
                    for img in b.get('fotos_articulos', []):
                        st.image(base64.b64decode(img), width=80)

# --- REGISTRO ---
with tab2:
    st.markdown("### 💜 Registra tu Bloque de Anuncios")
    st.info("Costo por bloque: $25 MXN | Vigencia: 15 días")
    with st.form("registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre / Tienda *")
        zona = col2.text_input("Punto Seguro de Entrega *")
        wapp = col1.text_input("WhatsApp (10 dígitos) *")
        cat = col2.radio("Categoría *", ["K-Pop", "Mi Clóset"])
        articulos = st.text_area("Artículos y Precios *")
        
        # Fotos de estilo FB
        portada = st.file_uploader("🖼️ Foto de Portada (Estilo FB)", type=['jpg', 'png'])
        perfil = st.file_uploader("👤 Foto de Perfil", type=['jpg', 'png'])
        fotos_art = st.file_uploader("📸 Fotos de artículos (Hasta 15)", accept_multiple_files=True)
        
        pago = st.file_uploader("💸 Subir Comprobante de Pago *", type=['jpg', 'png'])

        if st.form_submit_button("Subir Bloque para Validación"):
            # Conversión a base64
            p_b64 = base64.b64encode(portada.read()).decode() if portada else ""
            pe_b64 = base64.b64encode(perfil.read()).decode() if perfil else ""
            f_b64 = [base64.b64encode(f.read()).decode() for f in fotos_art]
            
            with cargar_db() as db:
                lista = db.get("bloques", [])
                lista.append({
                    "vendedor": nombre, "zona": zona, "articulos": articulos,
                    "portada": p_b64, "perfil": pe_b64, "fotos_articulos": f_b64,
                    "estado": "⏳ En espera"
                })
                db["bloques"] = lista
            st.success("¡Registro enviado! Será activado pronto.")

# --- ADMIN ---
with tab3:
    if st.text_input("Clave Admin", type="password") == "bazar123":
        with cargar_db() as db:
            lista = db.get("bloques", [])
            for i, b in enumerate(lista):
                if b['estado'] == "⏳ En espera":
                    if st.button(f"Validar y Activar: {b['vendedor']}", key=str(i)):
                        lista[i]['estado'] = "🟢 ACTIVO"
                        db["bloques"] = lista
                        st.rerun()
