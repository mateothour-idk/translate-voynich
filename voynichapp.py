import streamlit as st
import requests
import re
import pandas as pd

# Importación de tus lógicas desde el archivo voynichdata.py
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Voynich Data Direct",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Conectado a Voynich.nu/data/")
st.write("Esta suite descarga el archivo unificado oficial y mapea todas las páginas automáticamente en una tabla ordenada.")

# --- DESCARGA E INDEXACIÓN AUTOMÁTICA DEL CORPUS REMOTO ---
@st.cache_data(show_spinner=True)
def descargar_y_parsear_corpus_data():
    """
    Se conecta directamente al archivo voyn_101.txt de voynich.nu simulando
    una petición web para evitar restricciones del cortafuegos del servidor.
    """
    url_data = "https://www.voynich.nu/data/voyn_101.txt"
    diccionario_folios = {}
    
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/plain,text/html"
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
                
                # Rastrea marcas oficiales del tipo <f1r.1> o <f102v.12>
                match_folio = re.search(r"<f(\d+[rv])", linea_str)
                if match_folio:
                    folio_actual = f"f{match_folio.group(1)}"
                    if folio_actual not in diccionario_folios:
                        diccionario_folios[folio_actual] = []
                
                # Limpieza estándar de caracteres de control propios del transcriptor
                limpio = re.sub(r'<[^>]+>', '', linea_str)
                limpio = re.sub(r'\{[^}]+\}', '', limpio)
                limpio = re.sub(r'\[[^\]]+\]', '', limpio)
                limpio = limpio.replace(".", " ").replace(",", " ").strip()
                
                if folio_actual and limpio:
                    diccionario_folios[folio_actual].append(limpio)
            
            return {folio: " ".join(lineas_pag) for folio, lineas_pag in diccionario_folios.items()}
        else:
            st.sidebar.error(f"El servidor remoto devolvió el estado: {respuesta.status_code}.")
            return {}
    except Exception as e:
        st.sidebar.error(f"Fallo en la comunicación remota: {str(e)}")
        return {}

# Ejecución del crawler optimizado
mapa_completo_folios = descargar_y_parsear_corpus_data()

# --- CONFIGURACIÓN DE LA INTERFAZ DE NAVEGACIÓN LATERAL ---
st.sidebar.header("Panel de Navegación")

opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    paginas_ordenadas = sorted(
        mapa_completo_folios.keys(), 
        key=lambda x: (int(re.sub(r'\D', '', x)), x[-1])
    )
    opciones_selector.extend(paginas_ordenadas)
else:
    st.sidebar.warning("⚠️ No hay conexión al servidor remoto. Se forzó el modo manual.")

folio_seleccionado = st.sidebar.selectbox(
    "Selecciona la página a analizar:",
    opciones_selector
)

idioma_destino = st.sidebar.radio(
    "Idioma de la traducción final:",
    ["Español (ES)", "English (EN)"]
)
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.info(f"Páginas indexadas de voyn_101: {len(mapa_completo_folios) if mapa_completo_folios else 0}")

# --- ENRUTAMIENTO DE DATOS ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce cadena de transcripción EVA libre:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.markdown(f"### 📖 Transcripción Cruda Indexada del Folio **{folio_seleccionado}**")
    st.code(texto_usuario, wrap_lines=True)

# --- INICIO DEL PIPELINE DE PALEOGRAFÍA ---
if st.button("Ejecutar Análisis Paleográfico", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de entrada de texto está vacío.")
    else:
        with st.spinner("Procesando matriz de sustituciones y ordenando datos..."):
            # Paso 1: Ejecutar tu filtrado jerárquico por capas
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            # Paso 2: Ejecutar el diccionario semántico dual
            datos_tabla = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Pipeline completado!")
        st.markdown("### 📊 Desglose de Análisis Léxico Ordenado")
        
        if datos_tabla:
            df_resultado = pd.DataFrame(datos_tabla)
            
            # Formateo visual dinámico de los encabezados según el idioma
            if cod_idioma == "es":
                df_resultado.columns = ["Morfología Filtrada", "Interpretación / Semántica", "Diagnóstico"]
            else:
                df_resultado.columns = ["Filtered Morphology", "Interpretation / Semantics", "Diagnostic"]
            
            st.dataframe(
                df_resultado,
                use_container_width=True,
                hide_index=True
            )
            
            # --- SECCIÓN DE MÉTRICAS DESCRIPTIVAS EN TIEMPO REAL ---
            st.markdown("#### 📈 Métricas de Rendimiento" if cod_idioma == "es" else "#### 📈 Performance Metrics")
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
        else:
            st.info("El filtrado dio un resultado vacío.")
