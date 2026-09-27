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
    # Genera matemáticamente las páginas del manuscrito (1r, 1v... hasta 116v)
    for i in range(1, 117):
        folios.append(f"f{i}r")
        folios.append(f"f{i}v")
    return folios

# --- COMPONENTE: WEB SCRAPING CON FILTRADO DE METADATA ---
@st.cache_data(show_spinner=False)
def descargar_folio_online(folio):
    """
    Descarga dinámicamente un folio desde la nube y lo formatea para la URL con zfill
    """
    match = re.match(r"f(\d+)([rv])", folio)
    if not match:
        return f"Error: Formato de folio inválido ({folio})"
        
    num_pagina = match.group(1)
    lado = match.group(2)
    
    # voynich.nu requiere tres dígitos obligatorios (ej: f001r_tr.txt, f116v_tr.txt)
    url = f"https://voynich.nu{num_pagina.zfill(3)}{lado}_tr.txt"
    
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            lineas = respuesta.text.split("\n")
            texto_pag = []
            for linea in lineas:
                # Ignorar comentarios internos del repositorio
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
            return f"Error 404: El folio {folio} no está disponible en este formato interlineal."
    except Exception as e:
        return f"Error de red: No se pudo conectar al host ({str(e)})"

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
st.sidebar.caption("Desarrollado con arquitectura cloud dinámica y optimizador de n-gramas v2.2")

# --- CONTROL DEL FLUJO DE DATOS ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce código EVA libre para pruebas:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    with st.spinner(f"Consumiendo datos académicos del Folio {folio_seleccionado}..."):
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
            # Paso 1: Ejecutar tu matriz libre del bug quu
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            # Paso 2: Pasar el idioma dinámico seleccionado al motor
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
