import streamlit as st
import requests
import re
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Traductor Voynich Cloud",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Traductor Dinámico de Todo el Manuscrito Voynich")
st.write("Esta alternativa extrae las transcripciones oficiales en EVA directamente desde repositorios académicos en la nube.")

# --- GENERADOR AUTOMÁTICO DE FOLIOS ---
# Creamos la lista completa de las 240+ páginas del manuscrito de forma matemática
def generar_lista_folios():
    folios = ["Manual (Texto Libre)"]
    # El manuscrito va del folio 1 al 116 (con algunas páginas faltantes históricamente)
    for i in range(1, 117):
        folios.append(f"f{i}r")
        folios.append(f"f{i}v")
    return folios

# --- FUNCIÓN DE EXTRACCIÓN EN LA NUBE (WEB SCRAPING) ---
@st.cache_data(show_spinner=False)
def descargar_folio_online(folio):
    """
    Se conecta al repositorio y descarga el folio limpio.
    """
    # Usamos el espejo del corpus unificado Landini/Zandbergen/Currier
    url = f"https://voynich.nu{folio[1:-1]}{folio[-1]}_tr.txt"
    try:
        respuesta = requests.get(url, timeout=5)
        if respuesta.status_code == 200:
            lineas = respuesta.text.split("\n")
            texto_pag = []
            for linea in lineas:
                # Ignorar comentarios del corpus académico
                if not linea.strip() or linea.startswith("#"):
                    continue
                # Limpiar metadatos de las líneas (<f1r.P1.1>, etc.)
                limpio = re.sub(r'<[^>]+>', '', linea)
                limpio = re.sub(r'\{[^}]+\}', '', limpio)
                limpio = limpio.replace(".", " ").replace(",", " ").strip()
                if limpio:
                    texto_pag.append(limpio)
            return " ".join(texto_pag)
        else:
            # Fallback en caso de que la URL de voynich.nu varíe la sintaxis
            return f"Error: No se pudo obtener el folio {folio} (Código {respuesta.status_code})"
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# --- BARRA LATERAL CONTROLES ---
st.sidebar.header("Filtros del Manuscrito")

lista_folios = generar_lista_folios()
folio_seleccionado = st.sidebar.selectbox(
    "Selecciona cualquier página del libro:",
    lista_folios
)

idioma_destino = st.sidebar.radio(
    "Idioma del resultado:",
    ["Español (ES)", "English (EN)"]
)
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.caption("Alternativa Cloud sin archivos locales")

# --- FLUJO PRINCIPAL ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce texto libre en EVA:",
        placeholder="Ejemplo: qokched dcectth shol..."
    )
else:
    with st.spinner(f"Descargando datos oficiales del Folio {folio_seleccionado}..."):
        texto_usuario = descargar_folio_online(folio_seleccionado)
    
    if "Error" in texto_usuario:
        st.error(texto_usuario)
        texto_usuario = ""
    else:
        st.info(f"📖 **Texto EVA oficial descargado de internet para el Folio {folio_seleccionado}:**")
        st.code(texto_usuario, wrap_lines=True)

if st.button("Procesar y Traducir", type="primary"):
    if not texto_usuario.strip():
        st.warning("No hay texto disponible para traducir.")
    else:
        with st.spinner("Ejecutando matriz de sustitución..."):
            # Llama a tu voynichdata.py (que ya tiene corregido el bug 'quu' y el filtro de la 'h')
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            traduccion_final = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Operación completada con éxito!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧪 Reducción de Matriz")
            st.info(f"`{texto_filtrado}`")
        with col2:
            title_lang = "Prosa Romance" if cod_idioma == "es" else "Estimated Romance Prose"
            st.markdown(f"### 🏛️ {title_lang}")
            st.write(traduccion_final)
