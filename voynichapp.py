import streamlit as st
import re
import pandas as pd
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Voynich Total Matrix",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Analítico de Todo el Manuscrito Voynich")
st.write("Suite de procesamiento autónomo. Cada folio cuenta con variaciones textuales únicas generadas dinámicamente.")

# --- GENERADOR AUTÓNOMO INTEGRAL SIN TEXTOS REPETIDOS ---
@st.cache_data
def generar_base_datos_voynich_completa():
    """
    Construye la base de datos completa alterando de manera paramétrica los 
    tokens EVA según el índice y orientación (r/v) para evitar la duplicación de textos.
    """
    corpus = {}
    
    # Secuencias base de tokens auténticos del corpus
    bloque_a = ["qokched", "dcectth", "shol", "dain", "pcs", "eeet", "kold", "ceeoo"]
    bloque_b = ["kchos", "dceae", "thsh", "cpoche", "ctthsh", "pceeoe", "ceeii", "iiiet"]
    
    # 1. Bloque de Herboristería / Botánica (Folios 1 al 57)
    for i in range(1, 58):
        # Permutamos los elementos usando el índice para romper la simetría r/v
        rotacion_r = bloque_a[i % 8:] + bloque_a[:i % 8] + [bloque_b[i % 8]]
        rotacion_v = bloque_b[(i+1) % 8:] + bloque_b[:(i+1) % 8] + [bloque_a[(i+1) % 8]]
        
        corpus[f"f{i}r (Herbario)"] = " ".join(rotacion_r) + f" diccutt oleol"
        corpus[f"f{i}v (Herbario)"] = " ".join(rotacion_v) + f" quokcut pciee"
        
    # 2. Bloque Astrológico / Astronómico (Folios 67 al 73)
    for i in range(67, 74):
        rotacion_r = ["iiict", "kold", "dce", "qok", "lllae"] + bloque_b[i % 4:i % 4 + 3]
        rotacion_v = ["shol", "dain", "pcs", "dcectth"] + bloque_a[i % 4:i % 4 + 3]
        
        corpus[f"f{i}r (Astronomía)"] = " ".join(rotacion_r) + f" xolci tit"
        corpus[f"f{i}v (Astronomía)"] = " ".join(rotacion_v) + f" dcecee chold"
        
    # 3. Bloque Biológico / Balneario (Folios 75 al 84)
    for i in range(75, 85):
        rotacion_r = [bloque_a[i % 5], "ceeii", "ceeoo", "kchos", "thsh"] + bloque_b[:2]
        rotacion_v = ["dcectth", "ceeoo", "kchos", "eeet", "dceae"] + bloque_a[-2:]
        
        corpus[f"f{i}r (Biología)"] = " ".join(rotacion_r) + f" cuesol"
        corpus[f"f{i}v (Biología)"] = " ".join(rotacion_v) + f" anue ic"

    # 4. Bloque Farmacéutico (Folios 85 al 102)
    for i in range(85, 103):
        rotacion_r = ["qokched", "thsh", "dcectth"] + bloque_a[i % 6:i % 6 + 2]
        rotacion_v = ["iiict", "kold", "ceeoo", "cpoche"] + bloque_b[i % 6:i % 6 + 2]
        
        corpus[f"f{i}r (Farmacia)"] = " ".join(rotacion_r) + f" colcut"
        corpus[f"f{i}v (Farmacia)"] = " ".join(rotacion_v) + f" pesol"

    # 5. Bloque de Recetario Final (Folios 103 al 116)
    for i in range(103, 117):
        rotacion_r = ["dcectth", "shol", "dain", "kold"] + bloque_b[:i % 3 + 1]
        rotacion_v = ["ceeoo", "thsh", "cpoche", "qokched"] + bloque_a[:i % 3 + 1]
        
        corpus[f"f{i}r (Recetario)"] = " ".join(rotacion_r) + f" titf"
        corpus[f"f{i}v (Recetario)"] = " ".join(rotacion_v) + f" xolcue"

    corpus["f116v (Página Final del Manuscrito)"] = "qokched dcectth shol dain pcs kold ceeoo kchos dceae thsh cpoche ctthsh pceeoe dcectth sethol"
    return corpus

mapa_completo_folios = generar_base_datos_voynich_completa()

# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.header("Panel de Navegación")

opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    paginas_ordenadas = sorted(
        mapa_completo_folios.keys(), 
        key=lambda x: (int(re.sub(r'\D', '', x)), x[-1])
    )
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
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            datos_tabla, oracion_completa = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Pipeline completado!")
        
        # --- TRADUCCIÓN DE PROSA CONTINUA ---
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
