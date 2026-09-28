# voynichapp.py
import streamlit as st
import re
import pandas as pd
import urllib.request
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Intérprete Voynich Total Global",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Intérprete Automatizado NLP - Todo el Manuscrito Voynich Real")
st.write("Procesamiento dinámico sin diccionarios fijos. Descarga el corpus original completo de investigación y traduce vía IA.")

@st.cache_data(show_spinner=False)
def descargar_corpus_voynich_real():
    """
    Descarga en tiempo real la transcripción paleográfica real completa del 
    manuscrito (v01 de Landini) y limpia los códigos de línea.
    """
    url_corpus = "https://www.voynich.nu/data/ZL3b-n.txt"
    corpus = {}
    
    try:
        # Solicitud HTTP al repositorio histórico oficial de datos Voynich
        req = urllib.request.Request(url_corpus, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            lineas = response.read().decode('utf-8').splitlines()
            
        for linea in lineas:
            linea = linea.strip()
            # Estructura del corpus oficial: <f48r.P1.L1> texto_eva
            if linea.startswith("<f") and ">" in linea:
                partes = linea.split(">")
                etiqueta = partes[0].replace("<", "")
                texto_eva = partes[1].strip()
                
                # Extraer el identificador del folio (ej. 'f48r' desde 'f48r.1')
                identificador_folio = etiqueta.split(".")[0]
                
                # Limpiar comentarios internos del transcriptor (ej. =; % etc)
                texto_eva = re.sub(r';.*$', '', texto_eva) # Quita comentarios finales
                texto_eva = re.sub(r'[{}]', '', texto_eva)   # Quita indicadores ilegibles
                
                if texto_eva.strip():
                    if identificador_folio in corpus:
                        corpus[identificador_folio] += " " + texto_eva
                    else:
                        corpus[identificador_folio] = texto_eva
                        
    except Exception as e:
        st.sidebar.error(f"No se pudo descargar el corpus online: {e}. Usando respaldo local.")
        # Copia de respaldo automática con tus folios de prueba por si falla internet
        corpus = {
            "f48r": "pceeoe ceodar olees ceepy cseol cseckeeeo otolcseey ceeor ceeokeey",
            "f48v": "tcseor olcse qodaiin qokeeor sy oraiin ykeeol oiteeody cteeey",
            "f1r": "pchod fchy tcheor odaiin yoles cseor ceeor cseody"
        }
    return corpus

# Inicializar y descargar la base de datos completa real
with st.spinner("Descargando transcriptor oficial de folios reales desde el repositorio..."):
    mapa_completo_folios = descargar_corpus_voynich_real()

st.sidebar.header("Panel de Navegación")
opciones_selector = ["Manual (Texto Libre)"]

if mapa_completo_folios:
    # Ordenar los folios reales numéricamente (f1r, f1v, f2r...)
    def ordenar_clave(clave):
        numeros = re.findall(r'\d+', clave)
        num = int(numeros[0]) if numeros else 0
        letra = clave[-1] if clave else ''
        return (num, letra)
        
    paginas_ordenadas = sorted(mapa_completo_folios.keys(), key=ordenar_clave)
    opciones_selector.extend(paginas_ordenadas)

folio_seleccionado = st.selectbox("Selecciona la página REAL del manuscrito a analizar:", opciones_selector)

idioma_destino = st.sidebar.radio("Idioma de traducción de la IA:", ["Español (ES)", "English (EN)"])
cod_idioma = "es" if "Español" in idioma_destino else "en"

st.sidebar.markdown("---")
st.sidebar.info(f"Páginas reales mapeadas en vivo: {len(mapa_completo_folios)}")

if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area("Introduce cadena de transcripción EVA libre:", placeholder="Ejemplo: pceeoe ceodar olees...")
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.markdown(f"### 📖 Transcripción Cruda Original (EVA) del Folio **{folio_seleccionado}**")
    st.code(texto_usuario, wrap_lines=True)

if st.button("Ejecutar Análisis Paleográfico y Traducción AI", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de entrada de texto está vacío.")
    else:
        with st.spinner("Procesando dos capas de sustitución y conectando con el motor NLP..."):
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            datos_tabla, oracion_completa = motor_prosa_fluida(texto_filtrado, idioma=cod_idioma)
            
        st.success("¡Pipeline dinámico completado con éxito!")
        
        st.markdown("### 🏛️ Traducción de Prosa Continua Contextual")
        st.write("La IA intenta conectar tus raíces convertidas en Latín para armar una frase con sentido:")
        st.info(f"**Texto Interpretado final:** {oracion_completa}")
        
        st.markdown("---")
        st.markdown("### 📊 Desglose de Análisis Léxico Detallado")
        
        if datos_tabla:
            df_resultado = pd.DataFrame(datos_tabla)
            df_resultado.columns = ["Palabra Filtrada", "Equivalencia Semántica", "Tipo de Match"]
            st.dataframe(df_resultado, use_container_width=True, hide_index=True)
            
            st.markdown("#### 📈 Métricas de Rendimiento Dinámico")
            c1, c2 = st.columns(2)
            with c1:
                st.metric("Total Palabras Analizadas en la Página", len(df_resultado))
            with c2:
                st.metric("Motor Lingüístico", f"Google API NLP (Latín -> {cod_idioma.upper()})")
