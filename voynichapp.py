import streamlit as st
import requests
import re
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

st.set_page_config(
    page_title="Traductor Voynich Unificado",
    page_icon="📜",
    layout="centered"
)

st.title("📜 Traductor Dinámico de Todo el Manuscrito Voynich")
st.write("Esta herramienta descarga el corpus completo unificado evitando bloqueos de servidor (Fix 406).")

# --- DESCARGA E INDEXACIÓN DEL CORPUS COMPLETO (CON HEADERS ANTI-BOT) ---
@st.cache_data(show_spinner=True)
def descargar_y_parsear_corpus():
    url_maestra = "https://voynich.nu"
    diccionario_folios = {}
    
    # CABECERAS CRÍTICAS: Evitan que el servidor tire Error 406 (Not Acceptable)
    cabeceras = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
    }
    
    try:
        # Hacemos la petición inyectando el agente de usuario simulado
        respuesta = requests.get(url_maestra, headers=cabeceras, timeout=15)
        
        if respuesta.status_code == 200:
            lineas = respuesta.text.split("\n")
            folio_actual = None
            
            for linea in lineas:
                linea_str = linea.strip()
                if not linea_str or linea_str.startswith("#"):
                    continue
                
                # Buscar marcas de folio interlineales como <f1r.1> o <f48r.1>
                match_folio = re.search(r"<f(\d+[rv])", linea_str)
                if match_folio:
                    folio_actual = f"f{match_folio.group(1)}"
                    if folio_actual not in diccionario_folios:
                        diccionario_folios[folio_actual] = []
                
                # Limpiar metadatos internos de las líneas y comentarios
                limpio = re.sub(r'<[^>]+>', '', linea_str)
                limpio = re.sub(r'\{[^}]+\}', '', limpio)
                limpio = re.sub(r'\[[^\]]+\]', '', limpio)
                limpio = limpio.replace(".", " ").replace(",", " ").strip()
                
                if folio_actual and limpio:
                    diccionario_folios[folio_actual].append(limpio)
            
            return {folio: " ".join(lineas_pag) for folio, lineas_pag in diccionario_folios.items()}
        else:
            st.error(f"Error del servidor al obtener el corpus (Código {respuesta.status_code}). El host rechazó los encabezados.")
            return {}
    except Exception as e:
        st.error(f"Fallo crítico de conexión con el repositorio: {str(e)}")
        return {}

# Ejecutar cargador en caché
mapa_completo_folios = descargar_y_parsear_corpus()

# --- CONFIGURACIÓN DE LA BARRA LATERAL ---
st.sidebar.header("Control de Folios")

opciones_selector = ["Manual (Texto Libre)"]
if mapa_completo_folios:
    paginas_ordenadas = sorted(
        mapa_completo_folios.keys(), 
        key=lambda x: (int(re.sub(r'\D', '', x)), x[-1])
    )
    opciones_selector.extend(paginas_ordenadas)
else:
    st.sidebar.warning("Modo de entrada manual activado debido al bloqueo del host.")

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
st.sidebar.caption("Motor Unificado de Corpus v2.6 (Headers Bypass)")

# --- MANEJO DEL CONTENIDO DE LA PÁGINA ---
if folio_seleccionado == "Manual (Texto Libre)":
    texto_usuario = st.text_area(
        "Introduce código EVA libre para pruebas:",
        placeholder="Ejemplo: qokched dcectth shol pcs..."
    )
else:
    texto_usuario = mapa_completo_folios.get(folio_seleccionado, "")
    st.info(f"📖 **Texto EVA oficial extraído de memoria para el Folio {folio_seleccionado}:**")
    st.code(texto_usuario, wrap_lines=True)

# --- EJECUCIÓN DEL PIPELINE ---
if st.button("Procesar y Traducir", type="primary"):
    if not texto_usuario.strip():
        st.warning("El búfer de texto está vacío. Proporciona datos de entrada.")
    else:
        with st.spinner("Procesando matriz y decodificando morfología..."):
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
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
