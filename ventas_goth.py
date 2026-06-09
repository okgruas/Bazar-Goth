import streamlit as st
from datetime import datetime
import shelve

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
    /* Fondo Radial Tétrico */
    .stApp { 
        background: radial-gradient(circle at center, #2a0845 0%, #050505 70%) !important; 
        color: #d1d1d1 !important; 
    }
    
    .fb-header-container { 
        background: rgba(0, 0, 0, 0.6); 
        border: 2px solid #5d0f75; 
        box-shadow: 0 0 20px rgba(93, 15, 117, 0.5);
        border-radius: 20px; 
        padding: 25px; 
        margin-bottom: 30px; 
        text-align: center; 
    }
    
    .shein-card { 
        background: rgba(10, 10, 10, 0.7); 
        border: 1px solid #4a0072; 
        border-radius: 15px; 
        padding: 15px; 
        margin-bottom: 15px; 
        backdrop-filter: blur(5px);
    }
    
    .pago-card { 
        background: rgba(30, 0, 45, 0.5); 
        border: 1px solid #8a2be2; 
        padding: 15px; 
        border-radius: 10px; 
        margin: 10px 0; 
        color: #e0e0e0;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>textarea { 
        background: #000 !important; 
        color: #fff !important; 
        border: 1px solid #5d0f75 !important; 
    }
    
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
            st.markdown(f"""
                <div class="shein-card">
                    <h3>{info_b['vendedor']}</h3>
                    <p style="font-size: 12px; color: #9575cd;">📍 {info_b['zona']}</p>
                    <div style="font-size: 13px; max-height: 100px; overflow-y: auto;">{info_b['articulos']}</div>
                </div>
            """, unsafe_allow_html=True)

# --- PESTAÑA REGISTRO ---
with tab_anunciarse:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    st.markdown("**Costo por bloque: $25 MXN con una vigencia automática de 15 días.**")
    
    with st.form("form_goth", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre / Tienda *")
            whatsapp = st.text_input("WhatsApp *")
        with col2:
            zona = st.text_input("Punto de Entrega *")
            cat = st.radio("Categoría *", ["K-Pop", "Mi Clóset"], horizontal=True)
        
        lista = st.text_area("Artículos y Precios *")
        fotos = st.file_uploader("📸 Fotos de artículos (Hasta 15)", type=["jpg", "png"], accept_multiple_files=True)
        
        st.markdown("""
            <div class="pago-card">
                <p><strong>Titular: Yajaira Leija (Capitana Albatros)</strong></p>
                <p>🏦 Pago: NU MÉXICO | CLABE: 0123 4567 8901 2345 67</p>
            </div>
        """, unsafe_allow_html=True)
        
        comprobante = st.file_uploader("Subir Comprobante *", type=["jpg", "png"])
        
        if st.form_submit_button("Subir Bloque"):
            if nombre and whatsapp and zona and lista and comprobante and len(fotos) <= 15:
                id_b = f"GOTH-{datetime.now().strftime('%M%S')}"
                st.session_state.bloques_db[id_b] = {
                    "vendedor": nombre, "whatsapp": whatsapp, "zona": zona,
                    "articulos": lista, "imagenes": fotos, "estado": "⏳ En espera", "categoria": cat
                }
                guardar_datos_disco(st.session_state.bloques_db)
                st.success("¡Solicitud enviada, Capitana!")
            else:
                st.error("Verifica campos obligatorios y máximo 15 fotos.")

# --- PESTAÑA ADMIN ---
with tab_admin:
    clave = st.text_input("Clave Admin:", type="password")
    if clave == "bazar123":
        for id_b, info in st.session_state.bloques_db.items():
            st.write(f"{info['vendedor']} - {info['estado']}")
            if st.button(f"Activar {id_b}"):
                st.session_state.bloques_db[id_b]['estado'] = "🟢 ACTIVO"
                guardar_datos_disco(st.session_state.bloques_db)
                st.rerun()
            
