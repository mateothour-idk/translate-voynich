import streamlit as st
import requests
import re
import pandas as pd

# Importación de las lógicas corregidas del pipeline
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Voynich Data Direct",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Conectado a Voynich.nu/data/")
st.write("Esta suite procesa el repositorio de Zandbergen-Landini (ZL3b-n.txt) indexando los folios bajo tu matriz de reglas.")

# --- DESCARGA AUTOMÁTICA DEL REPOSITORIO ZL3B-N (IVTFF) ---
@st.cache_data(show_spinner=True)
def descargar_y_parsear_corpus_data():
    """
    Se conecta a la URL de transcripción limpia de Landini usando cabeceras 
    estándar para saltar firewalls de servidores.
    """
    url_data = "https://www.voynich.nu/data/ZL3b-n.txt"
    diccionario_folios = {}
    
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/plain"
    }
    
    try:
        respuesta = requests.get(url_data, headers=cabeceras, timeout=15)
        if respuesta.status_code == 200:
            lineas = respuesta.text.split("\n")
            folio_actual = None
            
            for linea in lineas:
                linea_str = linea.strip()
                if not linea_str or linea_str.startswith("#"):
                    continue
                
                # Rastrea marcas oficiales del tipo <f1r>, <f102v> en formato IVTFF
                match_folio = re.search(r"<f(\d+[rv])>", linea_str)
                if match_folio:
                    folio_actual = f"f{match_folio.group(1)}"
                    if folio_actual not in diccionario_folios:
                        diccionario_folios[folio_actual] = []
                    continue
                
                # Omitir líneas de control de fin o marcas de página estructurales fuera de texto
                if linea_str.startswith("<") or linea_str.startswith("%") or linea_str.startswith("$"):
                    continue
                
                # Limpieza de caracteres analíticos especiales (=, :, -, %, $)
                limpio = re.sub(r'\{[^}]+\}', '', linea_str)
                limpio = re.sub(r'\[[^\]]+\]', '', limpio)
                limpio = limpio.replace(".", " ").replace(",", " ").replace("=", " ").replace("-", " ").strip()
                
                if folio_actual and limpio:
                    diccionario_folios[folio_actual].append(limpio)
            
            return {folio: " ".join(lineas_pag) for folio, lineas_pag in diccionario_folios.items()}
        else:
            return None
    except:
        return None

# Ejecutar el conector en caché
mapa_completo_folios = descargar_y_parsear_corpus_data()

# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.header("Panel de Navegación")

if mapa_completo_folios:
    st.sidebar.success("🌐 Conexión activa con ZL3b-n.txt")
    opciones_selector = ["Manual (Texto Libre)"]
    paginas_ordenadas = sorted(
        mapa_completo_folios.keys(), 
        key=lambda x: (int(re.sub(r'\D', '', x)), x[-1])
    )
    opciones_selector.extend(paginas_ordenadas)
else:
    st.sidebar.warning("⚠️ Servidor de voynich.nu inaccesible. Forzando modo manual.")
    opciones_selector = ["Manual (Texto Libre)"]

folio_seleccionado = st.sidebar.selectbox(
    "Selecciona la página a analizar:",
    opciones_selector
)

idioma_destino = st.sidebar.radio(
    "Idioma de la traducción final:",
    ["Español (ES)", "English (EN)"]
)
cod_idioma = "es" if "Español" in idioma_destino else "en"

# --- RENDERIZADO DEL ÁREA DE TRABAJO ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce cadena de transcripción EVA libre:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.markdown(f"### 📖 Transcripción Cruda Indexada del Folio **{folio_seleccionado}**")
    st.code(texto_usuario, wrap_lines=True)

# --- EJECUCIÓN DEL PIPELINE PALEOGRÁFICO ---
if st.button("Ejecutar Análisis Paleográfico", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de entrada de texto está vacío.")
    else:
        with st.spinner("Procesando matriz de sustituciones..."):
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            datos_tabla = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Pipeline completado!")
        st.markdown("### 📊 Desglose de Análisis Léxico Ordenado")
        
        if datos_tabla:
            df_resultado = pd.DataFrame(datos_tabla)
            
            if cod_idioma == "es":
                df_resultado.columns = ["Morfología Filtrada", "Interpretación / Semántica", "Diagnóstico"]
            else:
                df_resultado.columns = ["Filtered Morphology", "Interpretation / Semantics", "Diagnostic"]
            
            st.dataframe(df_resultado, use_container_width=True, hide_index=True)
            
            # Métricas en tiempo real
            st.markdown("#### 📈 Métricas" if cod_idioma == "es" else "#### 📈 Metrics")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Total Palabras" if cod_idioma == "es" else "Total Words", len(df_resultado))
            with c2:
                col_diag = "Diagnóstico" if cod_idioma == "es" else "Diagnostic"
                exactos = len(df_resultado[df_resultado[col_diag].str.contains("Exacto|Exact", regex=True)])
                raices = len(df_resultado[df_resultado[col_diag].str.contains("Raíz|Root", regex=True)])
                st.metric("Palabras Identificadas" if cod_idioma == "es" else "Identified Words", exactos + raices)
            with c3:
                desconocidas = len(df_resultado[df_resultado[col_diag].str.contains("Desconocido|Unknown", regex=True)])
                pct = (desconocidas / len(df_resultado)) * 100 if len(df_resultado) > 0 else 0
                st.metric("Tasa de Incógnitas" if cod_idioma == "es" else "Unknown Word Rate", f"{pct:.1f}%")
