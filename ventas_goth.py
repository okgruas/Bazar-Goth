import streamlit as st
from datetime import datetime
import shelve
import base64

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Bazar Nocturnal", layout="wide")

def get_db():
    return shelve.open("bazar_db")

# --- CSS PARA EL ESTILO ROSA ---
st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { background-color: #ec407a; color: white; }
    h1, h2, h3 { color: #ec407a; }
    </style>
""", unsafe_allow_html=True)

# --- UI PRINCIPAL ---
st.markdown("<h1 style='text-align:center;'>🌙 BAZAR DIGITAL K-POP & CLÓSET</h1>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐"])

with tab1:
    st.subheader("🛒 Clósets y Productos Disponibles")
    with get_db() as db:
        bloques = db.get("bloques", [])
        for b in bloques:
            if b['estado'] == "ACTIVO":
                st.markdown(f"**🟢 ACTIVO** - {b['vendedor']}")
                st.write(f"Categoría: {b['categoria']} | Punto: {b['punto']}")
                st.info(b['productos'])
                
                st.write("📸 Fotos:")
                cols = st.columns(5)
                for idx, img_b64 in enumerate(b.get('fotos_b64', [])):
                    with cols[idx % 5]:
                        st.image(base64.b64decode(img_b64))
                
                st.link_button("Contactar por WhatsApp", f"https://wa.me/{b['whatsapp']}")
                st.divider()

with tab2:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    st.markdown("**Costo por bloque: $25 MXN con una vigencia automática de 15 días.**")
    
    with st.form("registro_form", clear_on_submit=True):
        st.markdown("### 👤 1. Datos de Contacto")
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre / Tienda *")
        punto = col2.text_input("Punto Seguro de Entrega *")
        wapp = col1.text_input("WhatsApp de Contacto *")
        cat = col2.radio("Categoría *", ["K-Pop (Photocards/Coleccionables)", "Mi Clóset (Ropa/Accesorios)"])
        
        st.markdown("### 🛍️ 2. Tus Artículos y Precios")
        productos = st.text_area("Lista tus productos (Uno por renglón, con precio) *")
        
        st.markdown("### 📸 3. Fotos de tus Artículos (Máximo 15)")
        fotos = st.file_uploader("Selecciona tus imágenes", accept_multiple_files=True)
        
        st.markdown("### 💳 4. Pago de Validación ($25 MXN)")
        st.info("🏦 BANCO: NU MÉXICO\n🔑 CLABE: 0123 4567 8901 2345 67\n👤 TITULAR: CAPITANA ALBATROS")
        comprobante = st.file_uploader("Sube la foto de tu comprobante de transferencia *")
        
        if st.form_submit_button("Enviar Registro"):
            if nombre and wapp and productos and fotos:
                fotos_b64 = [base64.b64encode(f.read()).decode() for f in fotos]
                nuevo_bloque = {
                    "vendedor": nombre, "whatsapp": wapp, "punto": punto,
                    "categoria": cat, "productos": productos, "fotos_b64": fotos_b64, "estado": "ESPERA"
                }
                with get_db() as db:
                    lista = db.get("bloques", [])
                    lista.append(nuevo_bloque)
                    db["bloques"] = lista
                st.success("¡Registro enviado, Capitana!")
            else:
                st.error("Por favor completa los campos obligatorios.")

with tab3:
    if "admin_autenticado" not in st.session_state:
        st.session_state.admin_autenticado = False

    if not st.session_state.admin_autenticado:
        pwd = st.text_input("Clave Admin", type="password")
        if st.button("Acceder"):
            if pwd == "admin123": # Puedes cambiar esta clave
                st.session_state.admin_autenticado = True
                st.rerun()
    else:
        st.write("Panel de Control Activo")
        with get_db() as db:
            bloques = db.get("bloques", [])
            for i, b in enumerate(bloques):
                if b['estado'] == "ESPERA":
                    if st.button(f"Activar: {b['vendedor']}", key=f"btn_{i}"):
                        bloques[i]['estado'] = "ACTIVO"
                        db["bloques"] = bloques
                        st.rerun()
