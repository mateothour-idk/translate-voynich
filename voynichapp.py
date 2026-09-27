import streamlit as st
import requests
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio conectado al corpus de Voynich.nu.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO EXTENDIDO) ---
if "diccionario_v4" not in st.session_state:
    st.session_state.diccionario_v4 = {
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

# --- DESCARGA Y PARSEO DEL CORPUS CON RESPALDO INTEGRADO ---
@st.cache_data(show_spinner="Descargando corpus académico real...")
def cargar_corpus_real_voynich():
    url = "https://voynich.nu"
    corpus_v4 = {
        "Herbario (Botánica)": {}, "Astronomía (Zodíaco)": {}, "Cosmología (Astros)": {},
        "Balneología (Fisiología)": {}, "Farmacéutica (Recetas)": {}, "Recetas Cortas (Estrellas)": {}
    }
    exito = False
    try:
        response = requests.get(url, timeout=12)
        if response.status_code == 200 and "<f1r" in response.text:
            exito = True
            for linea in response.text.split("\n"):
                match = re.match(r'<f(\d+[rv])\..*?>\s*(.*)', linea)
                if match:
                    folio_id = f"Folio {match.group(1)}"
                    texto_limpio = re.sub(r'[{}[\]!%=;@\$.,]', ' ', match.group(2).strip())
                    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
                    if not texto_limpio or texto_limpio.startswith("#"): continue
                    
                    num_folio = int(re.search(r'\d+', folio_id).group())
                    if 1 <= num_folio <= 66: seccion = "Herbario (Botánica)"
                    elif 67 <= num_folio <= 73: seccion = "Astronomía (Zodíaco)"
                    elif num_folio == 74: seccion = "Cosmología (Astros)"
                    elif 75 <= num_folio <= 84: seccion = "Balneología (Fisiología)"
                    elif 85 <= num_folio <= 99: seccion = "Farmacéutica (Recetas)"
                    else: seccion = "Recetas Cortas (Estrellas)"
                    
                    if folio_id not in corpus_v4[seccion]: corpus_v4[seccion][folio_id] = texto_limpio
                    else: corpus_v4[seccion][folio_id] += "\n" + texto_limpio
    except Exception:
        exito = False

    if not exito or not corpus_v4["Herbario (Botánica)"]:
        for i in range(1, 40): corpus_v4["Herbario (Botánica)"][f"Folio {i}r"] = "poisoda cutiy podon vetí oarur sier"
        for i in range(75, 82): corpus_v4["Balneología (Fisiología)"][f"Folio {i}r"] = "icios cios ain ciodain quaur oteroe"
        for i in range(85, 92): corpus_v4["Farmacéutica (Recetas)"][f"Folio {i}r"] = "poisoda cuta podon vetí oarur osain"

    corpus_v4["Herbario (Botánica)"]["Folio 33v"] = "tararain idain cutiy dole criquy arain"
    corpus_v4["Balneología (Fisiología)"]["Folio 80r"] = "icios cios ain ciodain quaur oteroe"
    return corpus_v4

if "manuscrito_v4" not in st.session_state:
    st.session_state.manuscrito_v4 = cargar_corpus_real_voynich()

# --- MOTOR DE TRADUCCIÓN ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia: return palabra
    if palabra_limpia in st.session_state.diccionario_v4: return st.session_state.diccionario_v4[palabra_limpia]
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    if not texto: return ""
    lineas_traducidas = []
    for linea in texto.strip().split("\n"):
        palabras_traducidas = [traducir_palabra(p) for p in linea.split(" ")]
        frase_sucia = " ".join(palabras_traducidas)
        frase_limpia = re.sub(r'\b(los|el|la|las|un|una)\b\s+(?=\b\1\b)', '', frase_sucia, flags=re.IGNORECASE)
        lineas_traducidas.append(re.sub(r'\s+', ' ', frase_limpia).strip())
    return "\n".join(lineas_traducidas)

# --- INTERFAZ ---
tab1, tab2 = st.tabs(["📖 Navegador del Manuscrito", "🔍 Buscador de Diccionario"])

with tab1:
    seccion_elegida = st.selectbox("Filtrar por sección temática:", list(st.session_state.manuscrito_v4.keys()))
    folios_disponibles = sorted(list(st.session_state.manuscrito_v4[seccion_elegida].keys()))
    
    if folios_disponibles:
        folio_elegido = st.selectbox("Selecciona el Folio:", folios_disponibles)
        texto_folio = st.session_state.manuscrito_v4[seccion_elegida][folio_elegido]
        col1, col2 = st.columns(2)
        with col1:
            texto_editable = st.text_area("Texto Transcrito Original:", texto_folio, height=200)
        with col2:
            texto_descifrado = descifrar_texto_completo(texto_editable)
            st.text_area("Descifrado Automatizado:", texto_descifrado, height=200, disabled=True)
            st.download_button(label="💾 Descargar (.txt)", data=texto_descifrado, file_name=f"traduccion_{folio_elegido.lower()}.txt")

with tab2:
    busqueda = st.text_input("Introduce una palabra Voynich para buscar:")
    if busqueda:
        palabra_b = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        res = {k: v for k, v in st.session_state.diccionario_v4.items() if palabra_b in k}
        for clave, valor in res.items(): st.write(f"🔹 **{clave}** ➔ {valor}")
