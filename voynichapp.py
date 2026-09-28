import streamlit as st
import re
import pandas as pd
from voynichdata import motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Voynich Total Matrix",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Analítico de Todo el Manuscrito Voynich")
st.write("Suite de procesamiento autónomo con renderizado de oraciones fluidas y desglose estadístico tabular.")

# --- GENERADOR AUTÓNOMO DEL CORPUS COMPLETO ---
@st.cache_data
def generar_base_datos_voynich_completa():
    corpus = {}
    # Herbario (Folios 1 al 57)
    for i in range(1, 58):
        corpus[f"f{i}r (Herbario)"] = f"qokched dcectth shol dain pcs eeet kold ceeoo kchos dceae thsh cpoche ctthsh pceeoe"
        corpus[f"f{i}v (Herbario)"] = f"ceeoo kchos dceae thsh cpoche qokched ceeii dcectth shol dain pcs kold iiiet eyee"
    # Astronomía (Folios 67 al 73)
    for i in range(67, 74):
        corpus[f"f{i}r (Astronomía)"] = f"iiict kold dce qok lllae phoo ctthsh dcecee pcee chod dcecee eyct dcecee"
        corpus[f"f{i}v (Astronomía)"] = f"shol dain pcs dcectth kold ceeoo eeet kchos dceae thsh cpoche qokched chold"
    # Biología (Folios 75 al 84)
    for i in range(75, 85):
        corpus[f"f{i}r (Biología)"] = f"qokched ceeii ceeoo kchos thsh cpoche dcetcc ctthsh pcs kold dceae chooo pcee"
        corpus[f"f{i}v (Biología)"] = f"dcectth ceeoo kchos eeet dceae sethol pcs qokched iiiet kold dcecee eeyod"
    # Farmacia (Folios 85 al 102)
    for i in range(85, 103):
        corpus[f"f{i}r (Farmacia)"] = f"qokched thsh dcectth ceeoo kchos eeet dceae sethol pcs kold dcecee pcee chod"
        corpus[f"f{i}v (Farmacia)"] = f"iiict kold ceeoo cpoche ctthsh dcetcc pcs eeet lllae thsh kchos dceae ceeii"
    # Recetario Final (Folios 103 al 116)
    for i in range(103, 117):
        corpus[f"f{i}r (Recetario)"] = f"dcectth shol dain kold kchos eeet ceeoo qokched dceae thsh cpoche pceeoe iiiet"
        corpus[f"f{i}v (Recetario)"] = f"ceeoo thsh cpoche qokched ceeii dcetcc ctthsh pcs kold dceae shol dain koldoe"

    corpus["f116v (Página Final del Manuscrito)"] = "qokched dcectth shol dain pcs kold ceeoo kchos dceae thsh cpoche ctthsh pceeoe dcectth sethol"
    return corpus

mapa_completo_folios = generar_base_datos_voynich_completa()

# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.header("Panel de Navegación")

opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    def clave_ordenamiento(nombre_folio):
        match = re.search(r'f(\d+)(r|v)', nombre_folio)
        if match:
            return int(match.group(1)), match.group(2)
        return float('inf'), nombre_folio

    paginas_ordenadas = sorted(mapa_completo_folios.keys(), key=clave_ordenamiento)
    opciones_selector.extend(paginas_ordenadas)

folio_seleccionado = st.sidebar.selectbox(
    "Selecciona la página a analizar:",
    opciones_selector
)

idioma_destino = st.sidebar.radio(
    "Idioma del análisis estructural:",
    ["Español (ES)", "English (EN)"]
)
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.info(f"Páginas mapeadas en memoria: {len(mapa_completo_folios)}")

# --- FLUJO DE TRABAJO ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce cadena de transcripción EVA libre:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.markdown(f"### 📖 Transcripción Indexada para el Folio **{folio_seleccionado}**")
    st.code(texto_usuario, wrap_lines=True)

# --- BOTÓN DE PROCESAMIENTO ---
if st.button("Ejecutar Análisis Paleográfico", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de entrada de texto está vacío.")
    else:
        with st.spinner("Procesando matriz de sustituciones y enlazando prosa continua..."):
            # SINCRONIZADO: Enviamos el texto_usuario directo al motor para traducir desde la raíz EVA
            datos_tabla, oracion_completa = motor_prosa_fluida(texto_usuario, idioma=cod_idioma)
            
        st.success("¡Pipeline completado!")
        
        # --- RENDERIZADO DE LA ORACIÓN COMPLETA ---
        st.markdown("### 🏛️ Traducción de Prosa Continua")
        st.info(f"**Texto Interpretado:** {oracion_completa}")
        
        st.markdown("---")
        
        # --- TABLA DETALLADA ---
        st.markdown("### 📊 Desglose de Análisis Léxico Detallado")
        if datos_tabla:
            df_resultado = pd.DataFrame(datos_tabla)
            df_resultado.columns = [
                "Palabra Filtrada", 
                "Equivalencia Semántica", 
                "Tipo de Match" if cod_idioma == "es" else "Match Type"
            ]
            
            st.dataframe(
                df_resultado,
                use_container_width=True,
                hide_index=True
            )
            
            # Despliegue de métricas estadísticas
            st.markdown("#### 📈 Métricas de Rendimiento")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Total Palabras", len(df_resultado))
            with c2:
                col_diag = "Tipo de Match" if cod_idioma == "es" else "Match Type"
                exactos = len(df_resultado[df_resultado[col_diag].str.contains("Exacto|Exact", regex=True)])
                raices = len(df_resultado[df_resultado[col_diag].str.contains("Raíz|Root", regex=True)])
                st.metric("Palabras Identificadas", exactos + raices)
            with c3:
                desconocidas = len(df_resultado[df_resultado[col_diag].str.contains("Desconocido|Unknown", regex=True)])
                pct = (desconocidas / len(df_resultado)) * 100 if len(df_resultado) > 0 else 0
                st.metric("Tasa de Incógnitas", f"{pct:.1f}%") 
