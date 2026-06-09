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
        <p style='font-style: italic; color: #9575cd;'>Tu estilo, nuestra esencia</p>
    </div>
""", unsafe_allow_html=True)

tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Catálogo", "💜 Registro", "🔐 Admin"])

# --- PESTAÑA CATALOGO ---
with tab_bazar:
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    cols = st.columns(3)
    for i, (id_b, info_b) in enumerate(bloques_activos.items()):
        with cols[i % 3]:
            # Mostrar imágenes guardadas
            img_html = ""
            if 'fotos_b64' in info_b:
                for img_data in info_b['fotos_b64']:
                    img_html += f'<img src="data:image/png;base64,{img_data}" style="width:40px; margin:2px;">'
            
            st.markdown(f"""
                <div class="shein-card">
                    <h3>{info_b['vendedor']}</h3>
                    <p style="font-size: 12px; color: #9575cd;">📍 {info_b['zona']}</p>
                    <div style="font-size: 13px; max-height: 100px; overflow-y: auto;">{info_b['articulos']}</div>
                    <div>{img_html}</div>
                </div>
            """, unsafe_allow_html=True)

# --- PESTAÑA REGISTRO ---
with tab_anunciarse:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    with st.form("form_goth", clear_on_submit=True):
        nombre = st.text_input("Nombre / Tienda *")
        whatsapp = st.text_input("WhatsApp *")
        zona = st.text_input("Punto de Entrega *")
        lista = st.text_area("Artículos y Precios *")
        fotos = st.file_uploader("📸 Fotos", accept_multiple_files=True)
        
        if st.form_submit_button("Subir Bloque"):
            # Conversión a base64
            fotos_b64 = [base64.b64encode(f.read()).decode() for f in fotos]
            id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
            st.session_state.bloques_db[id_b] = {
                "vendedor": nombre, "whatsapp": whatsapp, "zona": zona,
                "articulos": lista, "fotos_b64": fotos_b64, "estado": "⏳ En espera"
            }
            guardar_datos_disco(st.session_state.bloques_db)
            st.success("¡Solicitud enviada!")

# --- PESTAÑA ADMIN ---
with tab_admin:
    clave = st.text_input("Clave Admin:", type="password")
    if clave == "bazar123":
        for id_b, info in st.session_state.bloques_db.items():
            if st.button(f"Activar {info['vendedor']}"):
                st.session_state.bloques_db[id_b]['estado'] = "🟢 ACTIVO"
                guardar_datos_disco(st.session_state.bloques_db)
                st.rerun()                    if b.get('portada_b64'):
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
