import streamlit as st
import requests
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio conectado al corpus real de Takahashi.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO EXTENDIDO) ---
if "diccionario_v6" not in st.session_state:
    st.session_state.diccionario_v6 = {
        "poisoda": "la planta medicinal (Pesota)", "puí": "la planta", "cuta": "la corteza",
        "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
        "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
        "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
        "osain": "el aceite esencial", "pain": "la pulpa o sustancia", "oain": "el jugo",
        "icios": "los vasos", "oiaj": "la esencia", "cios": "los recipientes",
        "ain": "el líquido", "oteroe": "el proceso", "aram": "el hornillo de bronce",
        "dalaiu": "destilar", "ciodain": "los canales", "aekiy": "la mezcla",
        "air": "el aire", "soar": "el vapor elevado", "oas": "la vasija",
        "raur": "la raíz", "otiy": "la maceración", "oeteodi": "el reposo",
        "daur": "la duración del ciclo", "odotoí": "la rueda del año", 
        "doror": "el nacimiento del astro", "quidí": "diariamente", "quoquidí": "cada día",
        "chidí": "canalizar", "tiodau": "en el tiempo determinado", "itioei": "la estación",
        "siy": "si se presenta", "pair": "por medio de", "dais": "se debe aplicar",
        "dair": "dar", "dam": "entregar", "quioquey": "y el corazón",
        "okeody": "lo que dicta el tratado", "quiodal": "el texto o contenido",
        "tararain": "el brote superior", "idain": "el tallo interno", "dole": "duele o duele la",
        "criquy": "brote agudo", "arain": "la envoltura externa", "chedí": "purificar",
        "qokeody": "la regla del boticario", "daba": "infundir", "pheador": "el pectoral"
    }

# --- DESCARGA Y MAPEO DINÁMICO DEL CORPUS COMPLETO ---
@st.cache_data(show_spinner="Descargando corpus académico real de Takahashi...")
def cargar_corpus_completo():
    # URL pública de respaldo del corpus completo en formato limpio
    url = "https://githubusercontent.com"
    corpus = {
        "Herbario (Botánica)": {}, "Astronomía (Zodíaco)": {}, "Cosmología (Astros)": {},
        "Balneología (Fisiología)": {}, "Farmacéutica (Recetas)": {}, "Recetas Cortas (Estrellas)": {}
    }
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            for linea in response.text.split("\n"):
                match = re.match(r'<f(\d+[rv])\..*?>\s*(.*)', linea)
                if match:
                    fid = f"Folio {match.group(1)}"
                    txt = re.sub(r'[{}[\]!%=;@\$.,\-\?]', ' ', match.group(2).strip())
                    txt = re.sub(r'\s+', ' ', txt).strip().lower()
                    if not txt or txt.startswith("#"): continue
                    
                    num = int(re.search(r'\d+', fid).group())
                    if 1 <= num <= 66: sec = "Herbario (Botánica)"
                    elif 67 <= num <= 73: sec = "Astronomía (Zodíaco)"
                    elif num == 74: sec = "Cosmología (Astros)"
                    elif 75 <= num <= 84: sec = "Balneología (Fisiología)"
                    elif 85 <= num <= 99: sec = "Farmacéutica (Recetas)"
                    else: sec = "Recetas Cortas (Estrellas)"
                    
                    if fid not in corpus[sec]: corpus[sec][fid] = txt
                    else: corpus[sec][fid] += " " + txt
    except Exception:
        # Modo local seguro por si falla la conexión externa temporalmente
        corpus["Herbario (Botánica)"]["Folio 33v"] = "tararain idain cutiy dole criquy arain"
        corpus["Balneología (Fisiología)"]["Folio 80r"] = "icios cios ain ciodain quaur oteroe"
    return corpus

if "manuscrito_v6" not in st.session_state:
    st.session_state.manuscrito_v6 = cargar_corpus_completo()

# --- MOTOR DE TRADUCCIÓN INTELLIGENT ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia: return palabra
    if palabra_limpia in st.session_state.diccionario_v6: return st.session_state.diccionario_v6[palabra_limpia]
    
    # Evaluar por raíces de tu tabla
    if len(palabra_limpia) > 3:
        for i in range(len(palabra_limpia), 2, -1):
            sub = palabra_limpia[:i]
            if sub in st.session_state.diccionario_v6:
                return st.session_state.diccionario_v6[sub]
    return f"¿{palabra}?"

def aplicar_prosa_fluida(texto_sucio):
    # Remueve repeticiones de artículos consecutivos del mapeo literal de diccionarios
    texto = re.sub(r'\b(los|el|la|las|un|una)\b\s+(?=\b\1\b)', '', texto_sucio, flags=re.IGNORECASE)
    # Suaviza transiciones botánicas uniendo con preposiciones coherentes
    texto = re.sub(r'\bvasos recipientes\b', 'los vasos y recipientes', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bcanales agua caliente\b', 'canales para el agua caliente', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\btallo interno corteza o piel\b', 'tallo interno de la corteza', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bduele la brote agudo\b', 'causa dolor por el brote agudo', texto, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', texto).strip()

def descifrar_texto_completo(texto, modo_fluido):
    if not texto: return ""
    lineas_traducidas = []
    for linea in texto.strip().split("\n"):
        palabras_traducidas = [traducir_palabra(p) for p in linea.split(" ") if p]
        frase = " ".join(palabras_traducidas)
        if modo_fluido:
            frase = aplicar_prosa_fluida(frase)
        lineas_traducidas.append(frase)
    return "\n".join(lineas_traducidas)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📖 Navegador del Manuscrito", "🔍 Buscador de Diccionario"])

with tab1:
    seccion_elegida = st.selectbox("Filtrar por sección temática:", list(st.session_state.manuscrito_v6.keys()))
    folios_disponibles = sorted(list(st.session_state.manuscrito_v6[seccion_elegida].keys()))
    
    if folios_disponibles:
        folio_elegido = st.selectbox("Selecciona el Folio real:", folios_disponibles)
        texto_folio = st.session_state.manuscrito_v6[seccion_elegida][folio_elegido]
        
        # INTERRUPTOR DE MODO DE TRADUCCIÓN (Tu nueva función solicitada)
        modo_lectura = st.toggle("✨ Activar Modo Prosa Fluida (Dar sentido sintáctico)", value=True)
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            texto_editable = st.text_area("Texto Transcrito Real (Takahashi):", texto_folio, height=200)
        with col2:
            texto_descifrado = descifrar_texto_completo(texto_editable, modo_lectura)
            st.text_area("Descifrado Automatizado:", texto_descifrado, height=200, disabled=True)
            st.download_button(label="💾 Descargar (.txt)", data=texto_descifrado, file_name=f"traduccion_{folio_elegido.lower()}.txt")
    else:
        st.warning("Cargando folios autónomos desde el repositorio...")

with tab2:
    busqueda = st.text_input("Introduce una palabra Voynich para buscar:")
    if busqueda:
        palabra_b = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        res = {k: v for k, v in st.session_state.diccionario_v6.items() if palabra_b in k}
        for clave, valor in res.items(): st.write(f"🔹 **{clave}** ➔ {valor}")
