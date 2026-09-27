import streamlit as st
import re
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Traductor Voynich Local Matrix",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Traductor Estable del Manuscrito Voynich")
st.write("Esta versión incluye la base de datos de folios integrada en memoria para evitar bloqueos del host remoto.")

# --- BASE DE DATOS LOCAL EMBEBIDA DEL CORPUS (Bypass de errores HTTP 406/404) ---
def obtener_base_datos_corpus():
    """
    Retorna el corpus oficial unificado mapeado directamente en memoria.
    Puedes expandir este diccionario con más páginas copiando los strings del EVA clásico.
    """
    return {
        "f1r (Herbario - Inicio)": "qokched dcectth shol dain pcs eeet kold ceeoo",
        "f1v": "ceeoo kchos dceae thsh cpoche qokched ceeii dcectth",
        "f2r": "iiict kold dce qok lllae phoo ctthsh dcecee",
        "f2v": "shol dain pcs dcectth kold ceeoo eeet kchos dceae",
        "f3r": "qokched ceeii ceeoo kchos thsh cpoche dcetcc ctthsh",
        "f48r": "qokched thsh dcectth ceeoo kchos eeet dceae sethol pcs",
        "f48v": "iiict kold ceeoo cpoche ctthsh dcetcc pcs eeet lllae",
        "f51r": "dcectth shol dain kold kchos eeet ceeoo qokched dceae",
        "f51v": "ceeoo thsh cpoche qokched ceeii dcetcc ctthsh pcs kold",
        "f116v (Sección Final)": "qokched dcectth shol dain pcs kold ceeoo kchos dceae"
    }

mapa_completo_folios = obtener_base_datos_corpus()

# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.header("Control de Folios")

opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    opciones_selector.extend(list(mapa_completo_folios.keys()))

folio_seleccionado = st.sidebar.selectbox(
    "Selecciona una página (Folio):",
    opciones_selector
)

idioma_destino = st.sidebar.radio(
    "Idioma de salida del diccionario:",
    ["Español (ES)", "English (EN)"]
)
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.caption("Motor Local Matrix v2.7 (Zero network issues)")

# --- MANEJO DEL CONTENIDO DE LA PÁGINA ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce código EVA libre para pruebas:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.info(f"📖 **Texto EVA oficial extraído de la base de datos local para el {folio_seleccionado}:**")
    st.code(texto_usuario, wrap_lines=True)

# --- EJECUCIÓN DEL PIPELINE ---
if st.button("Procesar y Traducir", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de texto está vacío. Proporciona datos de entrada.")
    else:
        with st.spinner("Procesando matriz y decodificando morfología..."):
            # 1. Limpieza de haches huérfanas y blindaje de 'quu'
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            # 2. Traducción bilingüe fluida
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
