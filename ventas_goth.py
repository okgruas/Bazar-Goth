import streamlit as st
from datetime import datetime
import shelve
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Bazar Nocturnal Goth", page_icon="🌙", layout="wide")

# --- 2. PERSISTENCIA ---
def cargar_db():
    return shelve.open("bazar_goth_db", writeback=True)

# --- 3. CSS GOTH (Tu esencia original) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; color: #d1d1d1 !important; }
    .fb-header { background: rgba(0, 0, 0, 0.6); border: 2px solid #5d0f75; border-radius: 20px; padding: 25px; text-align: center; margin-bottom: 20px; }
    .card { background: rgba(10, 10, 10, 0.8); border: 1px solid #4a0072; border-radius: 15px; padding: 15px; margin-bottom: 15px; }
    h1, h2, h3 { color: #b39ddb !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. ENCABEZADO ---
st.markdown("""<div class="fb-header"><h1>🌙 BAZAR NOCTURNAL GOTH</h1><p>Tu estilo, nuestra esencia</p></div>""", unsafe_allow_html=True)

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
                        <div class="card">
                            <h3>{b['vendedor']}</h3>
                            <p>📍 {b['zona']}</p>
                            <p>{b['articulos']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    # Mostrar las fotos guardadas en base64
                    for img_b64 in b.get('fotos_b64', []):
                        st.image(base64.b64decode(img_b64), width=100)

# --- REGISTRO (Campos Rosa) ---
with tab2:
    with st.form("registro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre / Tienda *")
        zona = col2.text_input("Punto Seguro de Entrega *")
        wapp = col1.text_input("WhatsApp de Contacto *")
        cat = col2.radio("Categoría *", ["K-Pop", "Mi Clóset"])
        articulos = st.text_area("Lista tus productos (Uno por renglón con precio) *")
        fotos = st.file_uploader("📸 Fotos de artículos (Hasta 15)", accept_multiple_files=True)
        
        if st.form_submit_button("Subir Bloque"):
            if nombre and zona and articulos and fotos:
                fotos_b64 = [base64.b64encode(f.read()).decode() for f in fotos]
                with cargar_db() as db:
                    lista = db.get("bloques", [])
                    lista.append({
                        "vendedor": nombre, "zona": zona, "wapp": wapp, 
                        "articulos": articulos, "fotos_b64": fotos_b64, "estado": "⏳ En espera"
                    })
                    db["bloques"] = lista
                st.success("¡Solicitud enviada, Capitana!")
            else:
                st.error("Por favor completa todos los campos marcados con *")

# --- ADMIN ---
with tab3:
    if st.text_input("Clave Admin", type="password") == "bazar123":
        with cargar_db() as db:
            lista = db.get("bloques", [])
            for i, b in enumerate(lista):
                if b['estado'] == "⏳ En espera":
                    if st.button(f"Activar {b['vendedor']}", key=str(i)):
                        lista[i]['estado'] = "🟢 ACTIVO"
                        db["bloques"] = lista
                        st.rerun()
