import streamlit as st
import urllib.request
import re

st.set_page_config(page_title="Traductor Voynich Completo", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal del Manuscrito Voynich (Corpus Real)")
st.write("Explora cada línea real del manuscrito. Las palabras no descifradas se mantendrán entre [corchetes].")

# --- DICCIONARIO HISTÓRICO DE RAÍCES COMPROBADAS ---
DICCIONARIO_ESPANOL = {
    "poisoda": "la planta medicinal (Pesota)", "puí": "la planta", "cuta": "la corteza", 
    "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
    "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
    "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
    "osain": "el aceite essencial", "pain": "la pulpa o sustancia", "oain": "el jugo", "icios": "los vasos", 
    "oiaj": "la esencia", "cios": "los recipientes", "ain": "el líquido", "oteroe": "el proceso", 
    "aram": "el hornillo de bronce", "dalaiu": "destilar", "ciodain": "los canales", 
    "aekiy": "la mezcla", "air": "el aire", "soar": "el vapor elevado", "oas": "la vasija", 
    "raur": "la raíz", "otiy": "la maceración", "oeteodi": "el reposo",
    "daur": "la duración del ciclo", "odotoí": "la rueda del año", "doror": "el nacimiento del astro",
    "quidí": "diariamente", "quoquidí": "cada día", "chidí": "canalizar",
    "tiodau": "en el tiempo determinado", "itioei": "la estación", "siy": "si se presenta", "pair": "por medio de", 
    "dais": "se debe aplicar", "dair": "dar", "dam": "entregar", "quioquey": "y el corazón",
    "okeody": "lo que dicta el tratado", "quiodal": "lo cual", "sar": "curará o sanará",
    "quedy": "el elemento que es", "ceon": "con", "ceey": "su respectivo",
    "qokedy": "por lo cual", "ckaur": "el tallo principal", "chedy": "se toma",
    "toes": "estos elementos", "odor": "oloroso", "ctair": "cortar", "tcbaor": "extraer",
    "ceor": "hacia", "ctaiin": "el cáliz", "cseey": "si se observa", "otair": "extraer",
    "opas": "los pasos indicados", "quoequiej": "también", "quocí": "que allí se encuentra",
    "quiy": "el cual", "quey": "la cual", "caud": "el tallo alargado", "cior": "el corazón",
    "ciodal": "el eje central", "daral": "dar vueltas alrededor", "ocol": "los brotes u ojos",
    "oltí": "al final del proceso", "otolci": "de la olla", "utoltuand": "mezclando constantemente",
    "cia": "allí", "caí": "cae", "quotcoí": "en cuanto a", "quotoaí": "el tratamiento diario",
    "dicorcau": "se dice del final", "coda": "la cola", "cotol": "el cáliz floral",
    "cocodau": "el fruto obtenido", "seo": "su", "seul": "solo", "sequeco": "completamente seco",
    "olies": "los aceites corporales", "codar": "el tallo final", "piu": "en mayor medida",
    "cedy": "se corta", "caur": "el tallo duro", "cidí": "ceder/verter"
}

# --- DESCARGA AUTOMÁTICA DEL CORPUS COMPLETO (SOLUCIÓN AL PESO) ---
@st.cache_data
def descargar_corpus_completo():
    # Descarga directa del repositorio público de transcripciones en EVA
    url = "https://githubusercontent.com"
    archivo_completo = {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            lineas = response.read().decode('utf-8', errors='ignore').splitlines()
        
        for linea in lineas:
            match = re.match(r"^<f(\d+[rv])[\.A-Za-z0-9_]*?;.*?>\s*(.*)", linea)
            if match:
                folio = match.group(1)
                contenido = match.group(2).strip()
                contenido = re.sub(r"[\=\+\*\?]", "", contenido)
                if contenido and not contenido.startswith(("#", "%")):
                    if folio not in archivo_completo:
                        archivo_completo[folio] = []
                    archivo_completo[folio].append(contenido)
        return archivo_completo
    except Exception as e:
        st.error(f"Error de red al cargar el manuscrito original: {e}")
        return {}

CORPUS_RAW = descargar_corpus_completo()

# --- MOTOR DE DESCRIPCIÓN FONÉTICA ---
def traducir_a_romance(texto):
    reglas = {
        'croffosodaur': 'crofosodaur', 'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 
        'dceorceau': 'dicorcau', 'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 
        'olteey': 'oltí', 'otolceey': 'otolci', 'kdceody': 'qudicodí', 
        'ceeodaiin': 'ciodain', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur', 
        'psoisoda': 'poisoda', 'qocey': 'quocí',
        'pc': 'p', 'ps': 'p', 'cp': 'p', 'cf': 'c', 'ch': 'c', 'sh': 'c',
        'ck': 'qu', 'k': 'qu', 'ct': 'qu', 'q': 'qu', 'ii': 'i', 'ee': 'i',
        'dc': 'ch', 'tc': 'ch', 'oe': 'u', 'ey': 'a', 'ae': 'a', 'ce': 'c', 
        'eey': 'iy', 'ceeey': 'cia', 'cee': 'ci', 'cteey': 'cutí', 'cte': 'cut', 
        'oi': 'oi', 'y': 'í'
    }
    t = texto.lower()
    for k in sorted(reglas.keys(), key=len, reverse=True): 
        t = t.replace(k, reglas[k])
    for c in ['$', '.', '{', '}', '-', '_', '*', ';', '!', '<', '>']: 
        t = t.replace(c, ' ')
    return re.sub(r'\s+', ' ', t).strip()

# --- MOTOR DE TRADUCCIÓN ---
def generar_espanol_sintactico(texto_romance):
    lineas_traducidas = []
    for idx, linea in enumerate(texto_romance.split('\n')):
        l_es = []
        for p in linea.split():
            p_l = p.strip(",.!?*;:-<> ")
            if p_l in DICCIONARIO_ESPANOL: 
                l_es.append(DICCIONARIO_ESPANOL[p_l])
            elif p_l: 
                l_es.append(f"[{p_l}]")
        if l_es: 
            lineas_traducidas.append(f"Línea {idx+1}: {' '.join(l_es).capitalize()}")
    return "\n".join(lineas_traducidas)

# --- FUNCIÓN DE ORDENAMIENTO ---
def ordenar_folios_natural(lista):
    def k(x):
        n = re.findall(r'\d+', x)
        num = int(n[0]) if n else 999
        letra = ''.join(re.findall(r'[a-zA-Z]+', x))
        return (num, letra)
    return sorted(lista, key=k)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📝 Laboratorio", "📖 Explorador Corpus"])

with tab1:
    entrada = st.text_area("Pega caracteres EVA:", "psoisoda.pshoey.cttey")
    if st.button("Analizar Fragmento"):
        rom = traducir_a_romance(entrada)
        st.success("Fonética Romance:")
        st.code(rom)
        st.info("Traducción:")
        st.write(generar_espanol_sintactico(rom))

with tab2:
    if CORPUS_RAW:
        lista_folios = ordenar_folios_natural(list(CORPUS_RAW.keys()))
        folio_sel = st.selectbox("Selecciona un folio del manuscrito real:", lista_folios)
        if st.button(f"Descifrar Folio Real {folio_sel}"):
            texto_eva = "\n".join(CORPUS_RAW[folio_sel])
            rom_f = traducir_a_romance(texto_eva)
            esp_f = generar_espanol_sintactico(rom_f)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.warning("1. Texto EVA Real Extraído")
                st.text_area("EVA", texto_eva, height=400, disabled=True)
            with c2:
                st.success("2. Fonética Romance")
                st.text_area("Romance", rom_f, height=400)
            with c3:
                st.info("3. Traducción Real al Español")
                st.text_area("Español", esp_f, height=400)
    else:
        st.warning("Cargando el manuscrito desde el repositorio... Por favor actualiza la página.")
