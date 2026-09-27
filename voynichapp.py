import streamlit as st
import re
import os
import pandas as pd
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Local Voynich",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Analítico de Todo el Manuscrito Voynich")
st.write("Esta suite procesa las **240 páginas completas** del corpus local organizando las equivalencias fonéticas en tablas ordenadas.")

# --- COMPONENTE: PARSER INTELIGENTE CON TOLERANCIA A EXTENSIONES MALA NOMBRE ---
@st.cache_data(show_spinner=True)
def cargar_y_parsear_corpus_local():
    """
    Busca variaciones del archivo de texto en el directorio actual para mitigar 
    problemas de extensiones ocultas o nombres duplicados en sistemas operativos.
    """
    # Lista de nombres alternativos comunes que Windows o el usuario suelen crear sin querer
    posibles_nombres = ["voyn_101.txt", "voyn_101", "voyn_101.txt.txt", "voyn_101.TXT"]
    nombre_valido = None
    
    for nombre in posibles_nombres:
        if os.path.exists(nombre):
            nombre_valido = nombre
            break
            
    # Si no se encuentra con los nombres exactos, busca cualquier archivo que contenga 'voyn'
    if not nombre_valido:
        for archivo in os.listdir('.'):
            if 'voyn' in archivo.lower() and archivo.endswith(('.txt', '')):
                nombre_valido = archivo
                break

    if not nombre_valido:
        return {}
        
    diccionario_folios = {}
    try:
        with open(nombre_valid, "r", encoding="utf-8", errors="ignore") as f:
            folio_actual = None
            for linea in f:
                linea_str = linea.strip()
                if not linea_str or linea_str.startswith("#"):
                    continue
                
                # Captura marcas oficiales de folios (<f1r.1>, etc.)
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
                    
            return {folio: " ".join(lineas_pag) for folio, lineas_pag in diccionario_folios.items()}
    except Exception:
        return {}

# Carga de la base de datos local
mapa_completo_folios = cargar_y_parsear_corpus_local()

# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.header("Panel de Navegación")

opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    paginas_ordenadas = sorted(
        mapa_completo_folios.keys(), 
        key=lambda x: (int(re.sub(r'\D', '', x)), x[-1])
    )
    opciones_selector.extend(paginas_ordenadas)
else:
    st.sidebar.error("⚠️ No se detectó el archivo del corpus. Asegúrate de colocar el archivo de texto en la misma carpeta del proyecto.")

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
st.sidebar.info(f"Páginas indexadas: {len(mapa_completo_folios) if mapa_completo_folios else 0}")

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
