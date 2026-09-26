import streamlit as st
import urllib.request
import re
import json

st.set_page_config(page_title="Traductor Universal Voynich Completo", page_icon="📜", layout="wide")

st.title("📜 Traductor Universal del Manuscrito Voynich (Corpus Real)")
st.write("Explora, descifra y traduce cada línea real del manuscrito. Las palabras no descifradas se mantendrán limpias entre [corchetes].")

# --- DICCIONARIO HISTÓRICO DE RAÍCES COMPROBADAS ---
DICCIONARIO_ESPANOL = {
    "poisoda": "la planta medicinal (Pesota)", "puí": "la planta", "cuta": "la corteza", 
    "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
    "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
    "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
    "osain": "el aceite esencial", "pain": "la pulpa o sustancia", "oain": "el jugo", "icios": "los vasos", 
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

# --- EXTRACTOR OPTIMIZADO DESDE REPOSITORIO DE TEXTO PLANO ---
@st.cache_data
def descargar_manuscrito_completo():
    url = "https://voynich.nu"
    archivo_completo = {}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=12) as response:
            lineas = response.read().decode('utf-8', errors='ignore').splitlines()
        
        for linea in lineas:
            match = re.match(r"^<f(\d+[rv]\d*)[\.A-Za-z0-9_]*?>\s*(.*)", linea)
            if match:
                folio = match.group(1)
                contenido = match.group(2).strip()
                
                if contenido and not contenido.startswith(("%", "#")):
                    contenido = re.sub(r"[\=\+\*\?\-\{\}]", "", contenido)
                    
                    if folio not in archivo_completo:
                        archivo_completo[folio] = []
                    archivo_completo[folio].append(contenido)
        return archivo_completo
    except Exception as e:
        st.error(f"Error al conectar con la base de datos de Voynich.nu: {e}")
        return {}

CORPUS_MANUSCRITO = descargar_manuscrito_completo()

# --- MOTOR DE DESCRIPCIÓN FONÉTICA ---
def traducir_a_romance(texto):
    reglas = {
        'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 'dceorceau': 'dicorcau',
        'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 'olteey': 'oltí',
        'otolceey': 'otolci', 'kdceody': 'qudicodí', 'ceeodaiin': 'ciodain',
        'croffosodaur': 'crofosodaur', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'qocey': 'quocí', 'dce': 'dic', 'cee': 'ci', 'eey': 'iy', 'ceeey': 'cia',
        'cteey': 'cutí', 'cte': 'cut', 
        'pc': 'p', 'ps': 'p', 'cp': 'p', 'cf': 'c', 'ch': 'c', 'sh': 'c',
        'ck': 'qu', 'k': 'qu', 'ct': 'qu', 'ii': 'i', 'ee': 'i',
        'ce': 'c', 'ey': 'a', 'oe': 'u', 'oi': 'oi', 'ae': 'a', 'dc': 'ch', 'tc': 'ch', 'q': 'qu',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur', 'psoisoda': 'poisoda', 'y': 'í'
    }
    texto_limpio = texto.lower()
    
    # 1. Aplicar reglas fonéticas antes de quitar separadores de palabras
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
        
    # 2. Reemplazar caracteres académicos y separadores por espacios limpios
    for caracter in ['$', '.', '{', '}', '-', '_', '*', ';', '!']:
        texto_limpio = texto_limpio.replace(caracter, ' ')
        
    # 3. Colapsar espacios duplicados para que split() no procese vacíos
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio)
    
    return texto_limpio

# --- MOTOR DE TRADUCCIÓN LIMPIO Y DIRECTO ---
def generar_espanol_sintactico(texto_romance):
    lineas = texto_romance.split('\n')
    lineas_traducidas = []
    
    for idx, linea in enumerate(lineas):
        palabras = linea.split()
        linea_espanol = []
        
        for palabra in palabras:
            palabra_limpia = palabra.strip(",.!?*;:- ")
            if not palabra_limpia:
                continue
                
            if palabra_limpia in DICCIONARIO_ESPANOL:
                linea_espanol.append(DICCIONARIO_ESPANOL[palabra_limpia])
            else:
                linea_espanol.append(f"[{palabra_limpia}]")
        
        if linea_espanol:
            texto_linea = " ".join(linea_espanol).capitalize()
            lineas_traducidas.append(f"Línea {idx+1}: {texto_linea}")
            
    return "\n".join(lineas_traducidas)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📝 Laboratorio de Texto Libre", "📖 Explorador del Corpus Real (1r a 116v)"])

with tab1:
    st.subheader("Laboratorio de Entrada Libre")
    entrada = st.text_area("Pega caracteres EVA aquí:", "psoisoda.pshoey.cttey")
    if st.button("Analizar Fragmento"):
        romance = traducir_a_romance(entrada)
        espanol = generar_espanol_sintactico(romance)
        c1, c2 = st.columns(2)
        with c1:
            st.success("Fonética Romance:")
            st.code(romance)
        with c2:
            st.info("Traducción:")
            st.write(espanol)

with tab2:
    st.subheader("Navegador de Transcripciones Académicas")
    if CORPUS_MANUSCRITO:
        lista_folios = sorted(list(CORPUS_MANUSCRITO.keys()), key=lambda x: (int(''.join(filter(str.isdigit, x))), x[-1]))
        folio_sel = st.selectbox("Selecciona un folio real para extraer e interpretar su contenido de internet:", lista_folios)
        
        if st.button(f"Descifrar Folio Real {folio_sel}"):
            lineas_eva = CORPUS_MANUSCRITO[folio_sel]
            texto_eva_completo = "\n".join(lineas_eva)
            
            romance_final = traducir_a_romance(texto_eva_completo)
            espanol_final = generar_espanol_sintactico(romance_final)
            
            st.write("---")
            st.markdown(f"### Transcripción y Descifrado Real para el Folio {folio_sel}")
            
            col_eva, col_rom, col_esp = st.columns(3)
            with col_eva:
                st.warning("1. Texto EVA Real Extraído:")
                st.text_area("EVA", texto_eva_completo, height=450, disabled=True)
            with col_rom:
                st.success("2. Fonética Romance (Tu Matriz):")
                st.text_area("Romance", romance_final, height=450)
            with col_esp:
                st.info("3. Traducción Real al Español:")
                st.text_area("Español", espanol_final, height=450)
    else:
        st.warning("No se pudo cargar la base de datos remota debido a restricciones de conexión.")
