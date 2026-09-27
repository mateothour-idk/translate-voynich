import streamlit as st
import requests  # Preparado para cuando conectes el raspado de folios completos
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Traductor Voynich Matrix",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Traductor Adaptativo del Manuscrito Voynich")

# --- NUEVA FUNCIÓN: PARA EXTRAER CUALQUIER PÁGINA (Estructura base) ---
def obtener_texto_folio_voynich(folio):
    """
    Función para automatizar la traducción de todas las páginas desde voynich.nu.
    Por ahora devuelve un mock-up, pero puedes activarla con requests.
    """
    # Ejemplo de URL: f"http://voynich.nu"
    # Aquí iría tu scraping por expresiones regulares para limpiar los comentarios del corpus.
    mock_corpus = {
        "f1r": "qokched dcectth shol dain pcs eeet",
        "f1v": "ceeoo kchos dceae thsh cpoche",
        "f2r": "iiict kold dce qok lllae phoo"
    }
    return mock_corpus.get(folio, "qokched dcectth shol")

# --- BARRA LATERAL (CONTROLES DE PÁGINAS E IDIOMA) ---
st.sidebar.header("Configuración del Intérprete")

# Selector de todas las páginas del Manuscrito
folio_seleccionado = st.sidebar.selectbox(
    "Selecciona la página (Folio):",
    ["Manual (Texto Libre)", "f1r (Herbario - Inicio)", "f1v", "f2r"]
)

# Selector de Idioma de Salida solicitado
idioma_destino = st.sidebar.radio(
    "Idioma del resultado:",
    ["Español (ES)", "English (EN)"],
    index=0
)
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.caption("Modificaciones de matriz v2.1 (Fix quu bug)")

# --- ÁREA DE TRABAJO PRINCIPAL ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce texto en EVA:",
        placeholder="Ejemplo: qokched dcectth shol..."
    )
else:
    # Carga automáticamente el texto de la página seleccionada
    texto_usuario = obtener_texto_folio_voynich(folio_seleccionado.split()[0])
    st.info(f"**Texto oficial en EVA cargado para el Folio {folio_seleccionado}:**")
    st.code(texto_usuario)

if st.button("Procesar y Traducir", type="primary"):
    if not texto_usuario.strip():
        st.warning("No hay texto para procesar.")
    else:
        with st.spinner("Procesando matriz..."):
            # 1. Aplicamos la matriz blindada contra el bug "quu"
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            
            # 2. Pasamos el idioma seleccionado al motor
            traduccion_final = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Completado!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧪 Texto Tras la Matriz")
            st.info(f"`{texto_filtrado}`")
        with col2:
            title_lang = "Prosa Romance" if cod_idioma == "es" else "Estimated Romance Prose"
            st.markdown(f"### 🏛️ {title_lang}")
            st.write(traduccion_final)
