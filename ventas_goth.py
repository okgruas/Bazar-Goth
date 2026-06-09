import streamlit as st
from datetime import datetime
import shelve  # Base de datos física para que no se borre al dormirse la app
import base64
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title=“Nocturnal Clóset",
    page_icon="✨",
    layout="wide"
)

# ⚠️ CONFIGURACIÓN DE ADMINISTRADOR ⚠️
TELEFONO_ADMIN_WHATSAPP = "528143029578"
CONTRASENA_ADMIN = "bazar123"  # Puedes cambiarla aquí cuando quieras sin perder datos

# --- 2. PERSISTENCIA REAL EN DISCO ---
def cargar_datos_disco():
    with shelve.open("bazar_permanente_db") as db:
        return dict(db.get("bloques_db", {}))

def guardar_datos_disco(datos):
    with shelve.open("bazar_permanente_db") as db:
        db["bloques_db"] = datos

# Inicializar st.session_state leyendo directamente del disco permanente
if "bloques_db" not in st.session_state:
    st.session_state.bloques_db = cargar_datos_disco()

# --- 3. FUNCIÓN ULTRA-SEGURA PARA CARGAR IMÁGENES LOCALES (EVITA PANTALLA NEGRA) ---
def obtener_base64_de_imagen(nombre_archivo):
    try:
        rutas_a_probar = [
            nombre_archivo,
            os.path.join("static", nombre_archivo),
            os.path.join("app", "static", nombre_archivo),
            nombre_archivo.replace(".png", ".jpg"),
            nombre_archivo.replace(".png", ".jpeg"),
            nombre_archivo.upper(),
        ]
        
        for ruta in rutas_a_probar:
            if os.path.exists(ruta):
                with open(ruta, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode()
                    extension = "png" if ruta.lower().endswith(".png") else "jpeg"
                    return f"data:image/{extension};base64,{encoded_string}"
    except Exception:
        pass
    return ""

# Cargar imágenes locales de forma segura
img_portada_base64 = obtener_base64_de_imagen("portada1.png")
img_perfil_base64 = obtener_base64_de_imagen("portada2.png")

# --- 4. ESTILOS CSS CON EFECTO GLASSMORPHISM NEGRO/MORADO DEGRADADO ---
st.markdown("""
    <style>
    /* Fondo general de la App */
    .stApp {
        background: linear-gradient(135deg, #FFE5EC 0%, #FFB3C6 40%, #FF477E 100%) !important;
    }
    
    /* ========================================================
       ✨ CONTENEDOR DE PERFIL ESTILO FACEBOOK (GLASSMORPHISM MEJORADO)
       ======================================================== */
    .fb-header-container {
        position: relative;
        width: 100%;
        /* Degradado Glassmorphic translúcido de Negro a Morado con opacidad del 35% */
        background: linear-gradient(135deg, rgba(255, 179, 198, 0.35), rgba(187, 134, 252, 0.35)) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 24px;
        padding: 15px;
        box-shadow: 0 10px 32px 0 rgba(0, 0, 0, 0.12);
        margin-bottom: 30px;
        overflow: hidden;
    }
    
    /* Foto de portada con esquinas redondeadas */
    .fb-cover-wrapper {
        width: 100%;
        height: 280px;
        border-radius: 18px;
        overflow: hidden;
        position: relative;
    }
    .fb-cover-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Zona inferior del encabezado: Perfil y Títulos abajo de la foto */
    .fb-profile-row {
        display: flex;
        align-items: center;
        margin-top: -45px; /* Sube lo justo para la foto de perfil */
        padding: 0 40px 15px 40px;
        position: relative;
        z-index: 5;
    }
    
    /* Foto de Perfil Redonda con borde grueso blanco */
    .fb-profile-avatar {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        border: 5px solid #FFFFFF;
        box-shadow: 0px 6px 16px rgba(0,0,0,0.15);
        overflow: hidden;
        flex-shrink: 0;
        background-color: #FFFFFF;
    }
    .fb-profile-avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    /* Textos alineados abajo para que NUNCA tapen la portada en Computadora */
    .fb-profile-info {
        margin-left: 25px;
        margin-top: 50px; /* Empuja los textos hacia abajo fuera de la foto de portada */
    }
    
    /* ✨ TÍTULO CON DEGRADADO NEGRO Y MORADO ✨ */
    .gradient-title {
        font-size: 34px !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #FF1493, #9400D3) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        margin: 0 !important;
        filter: drop-shadow(1px 1px 1px rgba(255, 255, 255, 0.8));
    }
    
    /* 🔮 SUBTÍTULO CON EL MISMO DEGRADADO NEGRO Y MORADO 🔮 */
    .gradient-subtitle {
        font-size: 17px !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #FF1493, #9400D3) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        margin: 6px 0 0 0 !important;
        filter: drop-shadow(1px 1px 1px rgba(255, 255, 255, 0.8));
    }
    
    /* Ajustes adaptables perfectos para Celulares */
    @media (max-width: 768px) {
        .fb-cover-wrapper { height: 150px; }
        .fb-profile-row {
            flex-direction: column;
            align-items: center;
            margin-top: -55px;
            padding: 0 10px 10px 10px;
            text-align: center;
        }
        .fb-profile-avatar { width: 110px; height: 110px; border-width: 4px; }
        .fb-profile-info { margin-left: 0; margin-top: 15px; }
        .gradient-title { font-size: 24px !important; }
        .gradient-subtitle { font-size: 14px !important; }
    }
    
    /* ========================================================
       TARJETAS Y CONTENIDOS (ESTILO SHEIN / HIGHLIGHTS)
       ======================================================== */
    .stForm, .preview-container, .public-block, .admin-box {
        background-color: rgba(255, 255, 255, 0.98) !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 25px;
    }
    
    .shein-card {
        background-color: #FFFFFF !important;
        border: 2px solid #FFB3C6 !important;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    
    label, p, span, .stRadio p, h1, h2, h3, div[data-testid="stMarkdownContainer"] p {
        color: #1A1A1A !important;
        font-weight: bold !important;
    }
    
    textarea, input[type="text"], div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #FF477E !important;
        -webkit-text-fill-color: #1A1A1A !important;
        caret-color: #1A1A1A !important;
    }
    
    textarea::placeholder, div[data-testid="stTextArea"] textarea::placeholder {
        color: #888888 !important;
        -webkit-text-fill-color: #888888 !important;
        font-weight: normal !important;
        opacity: 0.7 !important;
    }
    
    div[data-testid="stFileUploader"] section {
        background-color: #FFF0F5 !important;
        border: 2px dashed #E6005C !important;
        border-radius: 10px !important;
    }
    div[data-testid="stFileUploader"] section * { color: #1A1A1A !important; }
    div[data-testid="stFileUploader"] button { background-color: #E6005C !important; color: #FFFFFF !important; }
    
    div[data-testid="stFormSubmitButton"] button, .stSubmitButton button, div.stSubmitButton > button {
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        box-shadow: 0px 6px 15px rgba(230, 0, 92, 0.4) !important;
    }
    div[data-testid="stFormSubmitButton"] button *, .stSubmitButton button *, div.stSubmitButton > button * {
        color: #FFFFFF !important;
        font-size: 20px !important;
        font-weight: 900 !important;
    }
    
    div[data-testid="stHorizontalBlock"] button, div[data-testid="element-container"] button {
        background-color: #E6005C !important;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 8px !important;
    }
    div[data-testid="stHorizontalBlock"] button *, div[data-testid="element-container"] button * { color: #FFFFFF !important; }

    div.stButton > button {
        background-color: #25D366 !important;
        color: #1A1A1A !important;
        border: 2px solid #FFFFFF !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        width: 100% !important;
        box-shadow: 0px 6px 18px rgba(37, 211, 102, 0.4) !important;
    }
    div.stButton > button * { color: #1A1A1A !important; font-size: 19px !important; font-weight: 900 !important; }
    
    .mini-foto img {
        max-height: 100px !important;
        object-fit: contain !important;
        border-radius: 6px;
        border: 1px solid #FFB3C6;
    }
    
    .articulos-box-shein {
        background-color: #F8F9FA !important;
        color: #1A1A1A !important;
        padding: 10px;
        border-radius: 6px;
        border-left: 4px solid #E6005C;
        font-size: 14px;
        white-space: pre-wrap;
        margin-bottom: 10px;
        max-height: 150px;
        overflow-y: auto;
    }
    
    .badge-activo-shein {
        background-color: #D4EDDA; color: #155724; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block;
    }
    
    .btn-wa-nativo {
        display: block;
        width: 100%;
        background-color: #25D366 !important;
        color: #1A1A1A !important;
        text-align: center;
        padding: 16px 32px;
        border-radius: 12px;
        font-size: 19px;
        font-weight: 900;
        text-decoration: none;
        border: 2px solid #FFFFFF;
        box-shadow: 0px 6px 18px rgba(37, 211, 102, 0.4);
        margin-top: 10px;
    }

    .seccion-quejas {
        text-align: center;
        font-size: 11px !important;
        color: #666666 !important;
        margin-top: 20px;
        font-weight: normal !important;
    }

    /* 🎨 RE-ESTILIZADO: AVISO DE SEGURIDAD MÁS TENUE Y EN ARMONÍA CON LA WEB */
    .alerta-seguridad-principal {
        background-color: rgba(255, 255, 255, 0.5) !important; /* Blanco translúcido tenue */
        color: #555555 !important; /* Gris oscuro elegante y suave */
        padding: 18px;
        border-radius: 14px;
        border-left: 5px solid #FFB3C6; /* Borde morado sutil */
        margin-bottom: 25px;
        backdrop-filter: blur(4px);
    }
    .alerta-seguridad-principal p { 
        color: #444444 !important; 
        font-size: 13.5px !important; 
        font-weight: normal !important; 
        margin: 0 !important; 
    }

    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] { display: flex !important; flex-direction: row !important; flex-wrap: wrap !important; gap: 10px !important; }
        div[data-testid="column"] { flex: 1 1 45% !important; min-width: 45% !important; }
        .shein-card { padding: 8px !important; margin-bottom: 10px !important; }
        .shein-card h4 { font-size: 13px !important; }
        .shein-card p, .articulos-box-shein { font-size: 11px !important; max-height: 90px !important; }
        div[data-testid="column"] div[data-testid="column"] { flex: 1 1 20% !important; min-width: 20% !important; }
        .mini-foto img { max-height: 45px !important; object-fit: cover !important; }
        .shein-card button { font-size: 11px !important; padding: 6px 4px !important; }
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. ENRENDERIZADO DEL ENCABEZADO MEJORADO CORREGIDO ---
fondo_portada_fallback = img_portada_base64 if img_portada_base64 else "linear-gradient(90deg, #FFB3C6, #FF8FAB)"
fondo_perfil_fallback = img_perfil_base64 if img_perfil_base64 else "linear-gradient(135deg, #FF477E, #FF8FAB)"

st.markdown(f"""
    <div class="fb-header-container">
        <div class="fb-cover-wrapper" style="background: {fondo_portada_fallback if not img_portada_base64 else 'none'};">
            {f'<img src="{img_portada_base64}" />' if img_portada_base64 else ''}
        </div>
        <div class="fb-profile-row">
            <div class="fb-profile-avatar" style="background: {fondo_perfil_fallback if not img_perfil_base64 else '#FFFFFF'}; display: flex; align-items: center; justify-content: center;">
                {f'<img src="{img_perfil_base64}" />' if img_perfil_base64 else '<span style="font-size:35px;">✨</span>'}
            </div>
            <div class="fb-profile-info">
                <h1 class="gradient-title">✨ BAZAR DIGITAL NOCTURNAL CLÓSET ✨</h1>
                <p class="gradient-subtitle">🛍️ Tu Estilo, Nuestra Esencia • Monterrey</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# --- 6. PESTAÑAS PRINCIPALES DE LA APLICACIÓN ---
tab_bazar, tab_anunciarse, tab_admin = st.tabs(["🛍️ Ver el Bazar / Clóset", "💜 Registrarse como Vendedora", "🔐"])

# ==========================================
# PESTAÑA 1: EL ESCAPARATE PÚBLICO
# ==========================================
with tab_bazar:
    st.markdown("""
        <div class="alerta-seguridad-principal">
            <p>
                ⚠️ <b>Aviso de Seguridad:</b> Recuerda realizar tus entregas únicamente en <b>lugares públicos y concurridos</b>. 
                Cada vendedora se hace completamente responsable de sus artículos, precios, acuerdos de entrega y citas correspondientes. 
                Este espacio funciona únicamente como catálogo digital, por lo que toda transacción y trato es totalmente ajeno a la aplicación.
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.subheader("🛒 Clósets y Productos Disponibles")
    bloques_activos = {k: v for k, v in st.session_state.bloques_db.items() if v['estado'] == "🟢 ACTIVO"}
    
    if not bloques_activos:
        st.info("No hay tienditas activas en este momento. Las publicaciones aprobadas aparecerán aquí de inmediato.")
    else:
        lista_bloques = list(bloques_activos.items())
        
        hora_actual = datetime.now().hour
        desplazamiento = hora_actual % len(lista_bloques)
        lista_rotada = lista_bloques[desplazamiento:] + lista_bloques[:desplazamiento]
        
        columnas_por_fila = 3
        
        for i in range(0, len(lista_rotada), columnas_por_fila):
            fila_bloques = lista_rotada[i:i+columnas_por_fila]
            cols = st.columns(columnas_por_fila)
            
            for idx_col, (id_b, info_b) in enumerate(fila_bloques):
                with cols[idx_col]:
                    texto_mensaje = "Hola, vengo del bazar digital de k-pop, me interesó alguno de tus artículos. ✨🛍️"
                    texto_codificado = texto_mensaje.replace(' ', '%20').replace('\n', '%0A')
                    url_wa_vendedor = f"https://wa.me/{info_b['whatsapp']}?text={texto_codificado}"

                    st.markdown(f"""
                        <div class="shein-card">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                                    <span class="badge-activo-shein">🟢 ACTIVO</span>
                                    <span style="font-size: 11px; color: #666666;">📅 {info_b['fecha']}</span>
                                </div>
                                <h4 style="margin: 0 0 5px 0; color:#D81159; font-size: 18px;">🛍️ Bazar de {info_b['vendedor']}</h4>
                                <p style="margin: 2px 0; color:#555555; font-size: 12px;">📂 <b>Categoría:</b> {info_b['categoria']}</p>
                                <p style="margin: 2px 0; color:#555555; font-size: 12px; margin-bottom: 10px;">📍 <b>Punto:</b> {info_b['zona']}</p>
                                <div class="articulos-box-shein">{info_b['articulos']}</div>
                            </div>
                    """, unsafe_allow_html=True)
                    
                    if info_b.get('imagenes'):
                        st.markdown("<span style='font-size:12px; color:#1A1A1A;'>📸 Fotos:</span>", unsafe_allow_html=True)
                        cols_img = st.columns(4)
                        for idx_img, img_file in enumerate(info_b['imagenes'][:4]):
                            with cols_img[idx_img % 4]:
                                st.markdown('<div class="mini-foto">', unsafe_allow_html=True)
                                st.image(img_file, use_container_width=True)
                                st.markdown('</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                            <div style="margin-top: 15px;">
                                <a href="{url_wa_vendedor}" target="_blank" style="text-decoration: none;">
                                    <button style="background-color:#E6005C; color:white; border:none; padding:10px 15px; font-weight:bold; border-radius:8px; cursor:pointer; width:100%; font-size:13px;">
                                        💬 Contactar por WhatsApp
                                    </button>
                                </a>
                                <div style="text-align: center; color: #D81159; font-weight: bold; font-size: 12px; margin-top: 8px; margin-bottom: 8px;">
                                    ✨ ¡Gracias por tu preferencia! ✨
                                </div>
                                <hr style="border: 0; height: 5px; background-color: #E6005C; margin: 0; border-radius: 5px;">
                            </div>
                        </div>
                        <br>
                    """, unsafe_allow_html=True)

# ==========================================
# PESTAÑA 2: REGISTRO DE VENDEDORAS
# ==========================================
with tab_anunciarse:
    st.subheader("💜 Registra tu Bloque de Anuncios")
    st.write("Costo por bloque: **$25 MXN** con una vigencia automática de 15 días.")
    
    if "pre_registro" not in st.session_state:
        st.session_state.pre_registro = None
    if "enviado_ok" not in st.session_state:
        st.session_state.enviado_ok = False

    with st.form("form_anuncio", clear_on_submit=True):
        st.markdown("### 👤 1. Datos de Contacto")
        col1, col2 = st.columns(2)
        with col1:
            nombre_vendedor = st.text_input("Nombre / Tienda *")
            whatsapp_vendedor = st.text_input("WhatsApp de Contacto * (10 dígitos)")
        with col2:
            zona_entrega = st.text_input("Punto Seguro de Entrega * (ej. Metro Cuauhtémoc)")
            tipo_articulo = st.radio("Categoría: *", [" El Vacío (Calzado/bolsas)”, "Mi Clóset (Ropa/Accesorios)"])
            
        st.markdown("---")
        st.markdown("### 🛍️ 2. Tus Artículos y Precios")
        lista_articulos = st.text_area(
            "Lista tus productos (Uno por renglón, con precio) *", 
            placeholder="Ejemplo:\n- Blusa Gotica Talla XL - $150\n- Zapatos Demonia Talla 5 - $25
        )
        
        st.markdown("### 📸 3. Fotos de tus Artículos (Máximo 15)")
        fotos_articulos = st.file_uploader("Selecciona tus imágenes:", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        
        st.markdown("---")
        st.markdown("### 💳 4. Pago de Validación ($25 MXN)")
        st.markdown("""
            <div style="background-color: #FFFFFF; padding: 20px; border-radius: 10px; border: 2px solid #D81159;">
                <p style="color: #D81159 !important; font-size: 17px !important; margin: 0 0 5px 0; font-weight: 900;">🏛️ BANCO: NU MÉXICO</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0 0 5px 0; font-family: monospace; font-weight: bold;">🔑 CLABE: 0123 4567 8901 2345 67</p>
                <p style="color: #1A1A1A !important; font-size: 17px !important; margin: 0; font-weight: bold;">👤 TITULAR: CAPITANA ALBATROS</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("")
        comprobante = st.file_uploader("Sube la foto de tu comprobante de transferencia *", type=["jpg", "png", "jpeg"])
        
        enviar_anuncio = st.form_submit_button("Subir Bloque de Anuncios para Validación")

        if enviar_anuncio:
            if fotos_articulos and len(fotos_articulos) > 15:
                st.error("No puedes subir más de 15 fotos.")
            elif not (nombre_vendedor and whatsapp_vendedor and zona_entrega and lista_articulos and comprobante):
                st.error("Por favor, llena todos los campos obligatorios (*) y carga tu comprobante.")
            else:
                id_transaccion = f"BZR-{datetime.now().strftime('%d%H%M%S')}"
                st.session_state.pre_registro = {
                    "id": id_transaccion,
                    "vendedor": nombre_vendedor,
                    "whatsapp": whatsapp_vendedor,
                    "zona": zona_entrega,
                    "categoria": tipo_articulo,
                    "articulos": lista_articulos,
                    "imagenes": fotos_articulos,
                    "estado": "⏳ En espera de verificación",
                    "fecha": datetime.now().strftime("%d/%m/%Y")
                }
                st.session_state.enviado_ok = False

    if st.session_state.pre_registro is not None:
        datos = st.session_state.pre_registro
        id_b = datos["id"]
        
        if id_b in st.session_state.bloques_db and st.session_state.bloques_db[id_b]['estado'] == "🟢 ACTIVO":
            st.session_state.pre_registro = None
            st.session_state.enviado_ok = False
            st.rerun()
        else:
            st.markdown('<div class="preview-container">', unsafe_allow_html=True)
            st.warning("⏳ Tu registro está en proceso de revisión. Por favor, realiza el paso final de WhatsApp en la parte de abajo.")
            
            st.markdown("### 👀 Detalles de tu Solicitud")
            col_p1, col_p2 = st.columns([1, 2])
            with col_p1:
                st.metric(label="Monto por Validar", value="$25 MXN")
                st.write(f"🆔 **ID Asignado:** `{id_b}`")
            with col_p2:
                st.write(f"👤 **Vendedora:** {datos['vendedor']}")
                st.write(f"📍 **Punto Seguro:** {datos['zona']}")
                st.write("**📝 Lista enviada:**")
                st.markdown(f'<div class="articulos-box-shein">{datos["articulos"]}</div>', unsafe_allow_html=True)
            
            if datos["imagenes"]:
                st.write("**📸 Imágenes cargadas con éxito:**")
                cols_prev = st.columns(6)
                for i, img in enumerate(datos["imagenes"]):
                    with cols_prev[i % 6]:
                        st.markdown('<div class="mini-foto">', unsafe_allow_html=True)
                        st.image(img, use_container_width=True)
                        st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📲 ¡Paso Final Obligatorio!")
            
            msg = (
                f"Hola, vengo de la página del Bazar.\n\n"
                f"👤 *Vendedora:* {datos['vendedor']}\n"
                f"🆔 *ID de Registro:* {id_b}\n\n"
                f"📎 *(Por favor, adjunta aquí la foto de tu comprobante antes de enviar el mensaje)*"
            )
            msg_encoded = msg.replace(' ', '%20').replace('\n', '%0A')
            url_wa = f"https://wa.me/528143029578?text={msg_encoded}"
            
            if not st.session_state.enviado_ok:
                if st.button("📲 Click Para Registrar y Preparar Envío de WhatsApp", key="btn_disparador_wa"):
                    st.session_state.bloques_db[id_b] = {
                        "vendedor": datos["vendedor"],
                        "whatsapp": datos["whatsapp"],
                        "zona": datos["zona"],
                        "categoria": datos["categoria"],
                        "articulos": datos["articulos"],
                        "imagenes": datos["imagenes"],
                        "estado": "⏳ En espera de verificación",
                        "fecha": datos["fecha"]
                    }
                    guardar_datos_disco(st.session_state.bloques_db)
                    st.session_state.enviado_ok = True
                    st.rerun()
            else:
                st.success("✅ ¡Datos registrados con éxito en el panel de administración!")
                st.markdown(f"""
                    <a class="btn-wa-nativo" href="{url_wa}" target="_blank">
                        🚀 ¡TODO LISTO! CLIC AQUÍ PARA CONFIRMAR TU PAGO VÍA WHATSAPP
                    </a>
                """, unsafe_allow_html=True)
                st.info("Al dar clic arriba se abrirá el chat. No olvides adjuntar foto del comprobante.")
                
            st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 🔐 PESTAÑA 3: PANEL DE CONTROL DE ADMINISTRADORA
# ==========================================
with tab_admin:
    st.subheader("🔐 Consola de Verificación")
    clave_ingresada = st.text_input("Introduce la Contraseña de Administradora:", type="password", key="tab_admin_key")
    
    if clave_ingresada == CONTRASENA_ADMIN:
        st.success("Acceso Autorizado - Modo Gestor")
        st.markdown("### 🛠️ Solicitudes del Sistema")
        
        if not st.session_state.bloques_db:
            st.info("No hay bloques registrados actualmente esperando acción en el sistema.")
        else:
            for b_id in list(st.session_state.bloques_db.keys()):
                b_info = st.session_state.bloques_db[b_id]
                
                st.markdown(f"""
                    <div class="admin-box">
                        <span style="color:#D81159;"><b>ID Solicitud:</b> {b_id}</span><br>
                        <b>Vendedora:</b> {b_info['vendedor']} | <b>Celular:</b> {b_info['whatsapp']}<br>
                        <b>Estado Actual:</b> <code>{b_info['estado']}</code>
                    </div>
                """, unsafe_allow_html=True)
                
                if b_info.get('imagenes'):
                    st.markdown("**📸 Fotos adjuntas por la vendedora:**")
                    cols_admin_img = st.columns(6)
                    for idx, img_obj in enumerate(b_info['imagenes']):
                        with cols_admin_img[idx % 6]:
                            st.markdown('<div class="mini-foto">', unsafe_allow_html=True)
                            st.image(img_obj, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                
                if b_info['estado'] == "⏳ En espera de verificación":
                    if st.button("🟢 Aceptar Bloque", key=f"tab_acc_{b_id}"):
                        st.session_state.bloques_db[b_id]['estado'] = "🟢 ACTIVO"
                        guardar_datos_disco(st.session_state.bloques_db)
                        st.toast(f"¡Bloque {b_id} activado con éxito!")
                        st.rerun()
                
                nuevo_texto = st.text_area(f"Modificar artículos de {b_id}:", value=b_info['articulos'], key=f"tab_edit_{b_id}")
                if nuevo_texto != b_info['articulos']:
                    st.session_state.bloques_db[b_id]['articulos'] = nuevo_texto
                    guardar_datos_disco(st.session_state.bloques_db)
                
                if st.button(f"🗑️ Eliminar permanentemente {b_id}", key=f"tab_del_{b_id}"):
                    del st.session_state.bloques_db[b_id]
                    guardar_datos_disco(st.session_state.bloques_db)
                    st.rerun()
                st.markdown("---")

# Sección de pie de página
st.markdown('<div class="seccion-quejas">Quejas, sugerencias y aclaraciones, con Capitana Albatros: 8143029578</div>', unsafe_allow_html=True)
