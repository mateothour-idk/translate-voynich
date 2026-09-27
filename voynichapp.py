import streamlit as st
import requests
import re
import pandas as pd
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Voynich Data Direct",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Conectado a Voynich.nu/data/")
st.write("Esta suite descarga el archivo unificado oficial y mapea todas las páginas automáticamente en una tabla ordenada.")

# --- DESCARGA E INDEXACIÓN USANDO EL ARCHIVO DEL DICTECTORIO /DATA/ ---
@st.cache_data(show_spinner=True)
def descargar_y_parsear_corpus_data():
    """
    Se conecta a la ruta exacta del directorio de voynich.nu usando cabeceras
    completas de navegador para evitar bloqueos por seguridad anti-bots (Error 406).
    """
    url_data = "https://www.voynich.nu/data/voyn_101.txt"
    diccionario_folios = {}
    
    # Cabeceras completas imitando a Google Chrome para saltar el firewall corporativo
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive"
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
                
                # Captura marcas oficiales de folios del archivo como <f1r.1> o <f102v.1>
                match_folio = re.search(r"<f(\d+[rv])", linea_str)
                if match_folio:
                    folio_actual = f"f{match_folio.group(1)}"
                    if folio_actual not in diccionario_folios:
                        diccionario_folios[folio_actual] = []
                
                # Limpieza de metadatos estructurales de la línea
                limpio = re.sub(r'<[^>]+>', '', linea_str)
                limpio = re.sub(r'\{[^}]+\}', '', limpio)
                limpio = re.sub(r'\[[^\]]+\]', '', limpio)
                limpio = limpio.replace(".", " ").replace(",", " ").strip()
                
                if folio_actual and limpio:
                    diccionario_folios[folio_actual].append(limpio)
            
            # Combinar todas las líneas recolectadas por cada folio
            return {folio: " ".join(lineas_pag) for folio, lineas_pag in diccionario_folios.items()}
        else:
            st.sidebar.error(f"El servidor respondió con código {respuesta.status_code}.")
            return {}
    except Exception as e:
        st.sidebar.error(f"Error de red: {str(e)}")
        return {}

# Ejecutar el extractor en caché
mapa_completo_folios = descargar_y_parsear_corpus_data()

# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.header("Panel de Navegación")

opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    # Ordenar lógicamente todas las páginas extraídas (1r, 1v, 2r...)
    paginas_ordenadas = sorted(
        mapa_completo_folios.keys(), 
        key=lambda x: (int(re.sub(r'\D', '', x)), x[-1])
    )
    opciones_selector.extend(paginas_ordenadas)
else:
    st.sidebar.warning("⚠️ No se pudo inicializar el árbol de folios. Activa el modo manual.")

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
st.sidebar.info(f"Páginas indexadas de voyn_101: {len(mapa_completo_folios) if mapa_completo_folios else 0}")

# --- FLUJO DE TRABAJO ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce cadena de transcripción EVA libre:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.markdown(f"### 📖 Transcripción Cruda Indexada del Folio **{folio_seleccionado}**")
    st.code(texto_usuario, wrap_lines=True)

# --- BOTÓN DE PROCESAMIENTO Y TABULACIÓN ---
if st.button("Ejecutar Análisis Paleográfico", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de entrada de texto está vacío.")
    else:
        with st.spinner("Procesando matriz de sustituciones y ordenando datos..."):
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            datos_tabla = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Pipeline completado!")
        st.markdown("### 📊 Desglose de Análisis Léxico Ordenado")
        
        if datos_tabla:
            # Creación del DataFrame de Pandas
            df_resultado = pd.DataFrame(datos_tabla)
            
            # Renombrar columnas para la visualización final scannable
            df_resultado.columns = [
                "Palabra Filtrada", 
                "Equivalencia Semántica", 
                "Tipo de Match" if cod_idioma == "es" else "Match Type"
            ]
            
            # Renderizar la tabla limpia ordenada sin índices sueltos
            st.dataframe(
                df_resultado,
                use_container_width=True,
                hide_index=True
            )
            
            # Despliegue de métricas estadísticas ordenadas por debajo
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
        else:
            st.info("El filtrado dio un resultado vacío.")
