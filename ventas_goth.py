import streamlit as st
from datetime import datetime
import shelve
import base64

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Bazar Digital", layout="wide")

# --- 2. PERSISTENCIA ---
def get_db():
    return shelve.open("bazar_db", writeback=True)

# --- 3. CSS (Estilo Rosa) ---
st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .card { border: 1px solid #ec407a; padding: 15px; border-radius: 15px; background: white; margin-bottom: 20px; }
    .portada { width: 100%; height: 150px; object-fit: cover; border-radius: 10px; }
    .perfil { width: 80px; height: 80px; border-radius: 50%; border: 3px solid white; margin-top: -40px; margin-left: 15px; }
    h1, h2, h3 { color: #ec407a; }
    </style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ ---
st.markdown("<h1 style='text-align:center;'>🌙 BAZAR DIGITAL K-POP & CLÓSET</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐 Admin"])

with tab1:
    st.subheader("🛒 Clósets Disponibles")
    with get_db() as db:
        bloques = db.get("bloques", [])
        for b in bloques:
            if b['estado'] == "ACTIVO":
                with st.container():
                    # Mostrar Portada y Perfil
                    if b.get('portada_b64'):
                        st.image(base64.b64decode(b['portada_b64']), use_container_width=True)
                    if b.get('perfil_b64'):
                        st.image(base64.b64decode(b['perfil_b64']), width=100)
                    
                    st.markdown(f"### {b['vendedor']}")
                    st.write(f"📍 Punto: {b['punto']} | Categoría: {b['categoria']}")
                    st.info(b['productos'])
                    
                    # Mostrar fotos de artículos
                    cols = st.columns(5)
                    for idx, img_b64 in enumerate(b.get('fotos_b64', [])):
                        with cols[idx % 5]:
                            st.image(base64.b64decode(img_b64))
                    
                    st.link_button("Contactar por WhatsApp", f"https://wa.me/{b['whatsapp']}")
                    st.divider()

with tab2:
    with st.form("registro_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre / Tienda *")
        punto = col2.text_input("Punto Seguro de Entrega *")
        wapp = col1.text_input("WhatsApp (ej: 52...) *")
        cat = col2.radio("Categoría *", ["K-Pop", "Mi Clóset"])
        
        portada = st.file_uploader("🖼️ Foto de Portada", type=['jpg', 'png'])
        perfil = st.file_uploader("👤 Foto de Perfil", type=['jpg', 'png'])
        productos = st.text_area("Lista tus productos *")
        fotos = st.file_uploader("📸 Fotos de artículos", accept_multiple_files=True)
        
        if st.form_submit_button("Enviar Registro"):
            # Convertir imágenes a base64 para guardarlas permanentemente
            p_b64 = base64.b64encode(portada.read()).decode() if portada else ""
            pe_b64 = base64.b64encode(perfil.read()).decode() if perfil else ""
            f_b64 = [base64.b64encode(f.read()).decode() for f in fotos]
            
            with get_db() as db:
                lista = db.get("bloques", [])
                lista.append({
                    "vendedor": nombre, "whatsapp": wapp, "punto": punto, "categoria": cat,
                    "productos": productos, "portada_b64": p_b64, "perfil_b64": pe_b64,
                    "fotos_b64": f_b64, "estado": "ESPERA"
                })
                db["bloques"] = lista
            st.success("¡Registro enviado, espera a que sea activado!")

with tab3:
    pwd = st.text_input("Clave Admin", type="password")
    if pwd == "admin123":
        with get_db() as db:
            bloques = db.get("bloques", [])
            for i, b in enumerate(bloques):
                if b['estado'] == "ESPERA":
                    if st.button(f"Activar: {b['vendedor']}", key=i):
                        bloques[i]['estado'] = "ACTIVO"
                        db["bloques"] = bloques
                        st.rerun()
