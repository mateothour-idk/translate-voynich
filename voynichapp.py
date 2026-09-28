# voynichapp.py
import streamlit as st
import re
import pandas as pd
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Voynich NLP Dinámico",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Automatizado NLP - Manuscrito Voynich")
st.write("Procesamiento dinámico sin diccionario estático basado en traducción estadística de Latín Romance.")

@st.cache_data
def generar_base_datos_voynich_real():
    """
    Base de datos simplificada con las transcripciones auténticas (EVA) 
    de los folios que estuvimos analizando en tus pruebas.
    """
    corpus = {
        "f48r (Herbario - Planta Alargada)": "pceeoe ceodar olees ceepy cseol cseckeeeo otolcseey ceeor ceeokeey",
        "f48v (Herbario - Planta Lobulada)": "tcseor olcse qodaiin qokeeor sy oraiin ykeeol oiteeody cteeey",
        "f1r (Página de Apertura)": "pchod fchy tcheor odaiin yoles cseor ceeor cseody",
    }
    return corpus

mapa_completo_folios = generar_base_datos_voynich_real()

st.sidebar.header("Panel de Navegación")
opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    paginas_ordenadas = sorted(mapa_completo_folios.keys())
    opciones_selector.extend(paginas_ordenadas)

folio_seleccionado = st.sidebar.selectbox("Selecciona la página a analizar:", opciones_selector)
idioma_destino = st.sidebar.radio("Idioma de destino:", ["Español (ES)", "English (EN)"])
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.info(f"Páginas cargadas en el corpus: {len(mapa_completo_folios)}")

if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area("Introduce cadena de transcripción EVA libre:", placeholder="Ejemplo: pceeoe ceodar olees...")
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.markdown(f"### 📖 Transcripción Real del Folio **{folio_seleccionado}**")
    st.code(texto_usuario, wrap_lines=True)

if st.button("Ejecutar Análisis Paleográfico y Traducción AI", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de entrada de texto está vacío.")
    else:
        with st.spinner("Conectando con el motor NLP de traducción automática de Latín..."):
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            datos_tabla, oracion_completa = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Análisis dinámico completado!")
        st.markdown("### 🏛️ Traducción de Prosa Continua (Contextual)")
        st.info(f"**Texto Interpretado por IA:** {oracion_completa}")
        st.markdown("---")
        st.markdown("### 📊 Desglose de Análisis Léxico Detallado")
        
        if datos_tabla:
            df_resultado = pd.DataFrame(datos_tabla)
            # Sincronizado exactamente con las llaves de tu nuevo voynichdata.py
            df_resultado.columns = ["Palabra Filtrada", "Equivalencia Semántica", "Tipo de Match"]
            st.dataframe(df_resultado, use_container_width=True, hide_index=True)
            
            st.markdown("#### 📈 Métricas de Rendimiento Dinámico")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Total Palabras Analizadas", len(df_resultado))
            with c2:
                st.metric("Tipo de Motor", "Google Translator API (La -> Target)")
