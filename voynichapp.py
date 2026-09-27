import streamlit as st
import requests
import re
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Traductor Voynich Cloud Pro",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Traductor Dinámico del Manuscrito Voynich")
st.write("Esta herramienta procesa el corpus en la nube mediante tu matriz adaptativa de reducción paleográfica.")

# --- COMPONENTE: GENERADOR AUTOMÁTICO DE FOLIOS DEL LIBRO ---
def generar_lista_folios():
    folios = ["Manual (Texto Libre)"]
    for i in range(1, 117):
        folios.append(f"f{i}r")
        folios.append(f"f{i}v")
    return folios

# --- COMPONENTE: WEB SCRAPING CON FILTRADO DE METADATA ---
@st.cache_data(show_spinner=False)
def descargar_folio_online(folio_raw):
    """
    Aísla completamente los parámetros numéricos y de orientación para blindar
    la construcción de la URL e impedir fusiones con el host.
    """
    # Forzar limpieza total de strings y extraer los tokens numéricos
    folio_limpio = str(folio_raw).strip().lower()
    match = re.search(r"f(\d+)([rv])", folio_limpio)
    
    if not match:
        return f"Error: Formato de folio inválido o no reconocido ({folio_raw})"
        
    num_pagina = match.group(1)
    lado = match.group(2)
    
    # Formatear el número con ceros a la izquierda (ej: '51' -> '051')
    num_tres_digitos = str(num_pagina).zfill(3)
    
    # Construcción estricta y hardcodeada de la ruta del archivo
    nombre_archivo = f"f{num_tres_digitos}{lado}_tr.txt"
    url_final = f"https://voynich.nu{nombre_archivo}"
    
    try:
        respuesta = requests.get(url_final, timeout=8)
        if respuesta.status_code == 200:
            lineas = respuesta.text.split("\n")
            texto_pag = []
            for linea in lineas:
                if not linea.strip() or linea.startswith("#"):
                    continue
                # Limpiar etiquetas xml/interlineales como <f1r.P1.1> o comentarios {}
                limpio = re.sub(r'<[^>]+>', '', linea)
                limpio = re.sub(r'\{[^}]+\}', '', limpio)
                limpio = limpio.replace(".", " ").replace(",", " ").strip()
                if limpio:
                    texto_pag.append(limpio)
            return " ".join(texto_pag)
        else:
            return f"Error 404: El folio no está disponible en el servidor (URL intentada: {url_final})"
    except Exception as e:
        return f"Error de red crítico: No se pudo resolver la conexión. URL intentada: {url_final}. Detalles: {str(e)}"

# --- CONFIGURACIÓN DE CONTROLES (BARRA LATERAL) ---
st.sidebar.header("Parámetros del Sistema")

lista_folios = generar_lista_folios()
folio_seleccionado = st.sidebar.selectbox(
    "Selecciona una página (Folio):",
    lista_folios
)

idioma_destino = st.sidebar.radio(
    "Idioma de salida del diccionario:",
    ["Español (ES)", "English (EN)"]
)
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.caption("Desarrollado con arquitectura cloud dinámica y optimizador de n-gramas v2.4")

# --- CONTROL DEL FLUJO DE DATOS ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce código EVA libre para pruebas:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    texto_usuario = descargar_folio_online(folio_seleccionado)
    
    if "Error" in texto_usuario:
        st.error(texto_usuario)
        texto_usuario = ""
    else:
        st.info(f"📖 **Texto EVA oficial extraído para el Folio {folio_seleccionado}:**")
        st.code(texto_usuario, wrap_lines=True)

# --- BOTÓN Y LÓGICA DE PROCESAMIENTO ---
if st.button("Procesar y Traducir", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de texto está vacío. Proporciona datos de entrada.")
    else:
        with st.spinner("Procesando matriz y decodificando morfología..."):
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            traduccion_final = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Pipeline completado!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧪 Reducción de Matriz")
            st.info(f"`{texto_filtrado}`")
        with col2:
            title_lang = "Prosa Romance Estimada" if cod_idioma == "es" else "Estimated Romance Prose"
            st.markdown(f"### 🏛️ {title_lang}")
            st.write(traduccion_final)
