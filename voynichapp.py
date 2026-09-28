import streamlit as st
import urllib.request
import re

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")

idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

IFACE = {
    "Español": {
        "titulo": "📜 Traductor Universal del Manuscrito Voynich (Corpus voynich.nu)",
        "sub": "Explora y traduce cada línea real del manuscrito aplicando tu matriz de doble procesamiento estricto.",
        "tab1": "📝 Laboratorio de Texto Libre",
        "tab2": "📖 Explorador del Corpus Real voynich.nu",
        "lab_sub": "Laboratorio de Entrada Libre",
        "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance (Doble Proceso):",
        "trad_auto": "Traducción Estricta Basada en Glosario:",
        "nav_sub": "Navegador de Transcripciones Oficiales",
        "nav_sel": "Selecciona CUALQUIER folio del manuscrito entero:",
        "btn_desc": "Descifrar Folio Real",
        "res_tit": "Transcripción y Traducción Real para el Folio",
        "col1": "1. Texto EVA Real (voynich.nu):",
        "col2": "2. Fonética Romance (Doble Matriz):",
        "col3": "3. Traducción Real al Español:",
        "err_corpus": "No se pudo inicializar el corpus del manuscrito."
    },
    "English": {
        "titulo": "📜 Universal Voynich Manuscript Translator (voynich.nu Corpus)",
        "sub": "Explore and translate every single line of the manuscript using your strict double-processing matrix.",
        "tab1": "Free Text Laboratory",
        "tab2": "Real Corpus Explorer voynich.nu",
        "lab_sub": "Free Entry Laboratory",
        "btn_an": "Analyze Fragment",
        "fon_rom": "Romance Phonetics (Double Process):",
        "trad_auto": "Strict Glossary-Based Translation:",
        "nav_sub": "Official Transcriptions Navigator",
        "nav_sel": "Select ANY folio from the entire manuscript:",
        "btn_desc": "Decipher Real Folio",
        "res_tit": "Real Transcription and Translation for Folio",
        "col1": "1. Real EVA Text (voynich.nu):",
        "col2": "2. Romance Phonetics (Double Matrix):",
        "col3": "3. Real Translation to English:",
        "err_corpus": "Could not initialize the manuscript corpus."
    }
}

DICCIONARIO_ES = {
    "pui": "la planta", "cuta": "la corteza", "oarur": "el aroma", "poisoda": "la planta medicinal",
    "quedy": "el elemento", "con": "con", "su": "su", "quoqu": "por lo cual", "caur": "el tallo",
    "chedy": "se extrae", "toes": "estos", "odor": "oloroso", "cutair": "cortar", "oas": "la vasija",
    "tcbaor": "recolectar", "hacia": "hacia", "ctaiin": "el cáliz", "si": "si se", "otair": "surgir",
    "opas": "los pasos", "chidi": "canalizar", "podon": "la raíz", "vety": "maduro",
    "dic": "dice", "olteey": "al final", "quotcey": "se limpia", "raur": "la base",
    "qudicodi": "el tratado", "copi": "abundante", "cia": "allí", "quotcoi": "cuanto",
    "quotoai": "diariamente", "dicorcau": "la sustancia", "cuti": "la piel", "cotol": "el cáliz",
    "odaur": "el olor", "cocodau": "el fruto", "seo": "su", "quoci": "allí",
    "ciodal": "el eje", "daral": "girar", "ocol": "los brotes", "olti": "al término",
    "otolci": "la olla", "tiodau": "el tiempo", "pair": "por", "osain": "el aceite",
    "pain": "la pulpa", "oain": "el jugo", "dais": "se aplica", "okeody": "la regla",
    "quoequiej": "también", "sar": "sanará", "oeteody": "el reposo", "otiy": "la maceración",
    "quiy": "el cual", "quey": "la cual", "icios": "los vasos", "oiaj": "la esencia",
    "cios": "los recipientes", "ain": "el líquido", "oteroe": "el proceso", "aram": "el hornillo",
    "sier": "las hojas", "dalaiu": "destilar", "dam": "dar", "ciodain": "los conductos",
    "aekiy": "la mezcla", "air": "el aire", "soar": "el vapor", "ciey": "la savia",
    "dais": "la rueda", "odotoi": "el ciclo", "doror": "el nacimiento", "quaur": "el calor",
    "caud": "el tallo alargado", "cedy": "se corta", "cidí": "verter"
}

DICCIONARIO_EN = {
    "pui": "the plant", "cuta": "the bark", "oarur": "the aroma", "poisoda": "the medicinal plant",
    "quedy": "the element", "con": "with", "su": "its", "quoqu": "whereby", "caur": "the stem",
    "chedy": "is extracted", "toes": "these", "odor": "scented", "cutair": "to cut", "oas": "the vessel",
    "tcbaor": "to gather", "hacia": "towards", "ctaiin": "the calyx", "si": "if it", "otair": "arise",
    "opas": "the steps", "chidi": "to channel", "podon": "the root", "vety": "mature",
    "dic": "says", "olteey": "at the end", "quotcey": "is cleansed", "raur": "the base",
    "qudicodi": "the treatise", "copi": "abundant", "cia": "there", "quotcoi": "as for",
    "quotoai": "daily", "dicorcau": "the substance", "cuti": "the skin", "cotol": "the calyx",
    "odaur": "the scent", "cocodau": "the fruit", "seo": "its", "quoci": "there",
    "ciodal": "the axis", "daral": "to rotate", "ocol": "the buds", "olti": "at the completion",
    "otolci": "the pot", "tiodau": "the time", "pair": "by", "osain": "the oil",
    "pain": "the pulp", "oain": "the juice", "dais": "is applied", "okeody": "the rule",
    "quoequiej": "also", "sar": "will heal", "oeteody": "the rest", "otiy": "the maceration",
    "quiy": "which", "quey": "which", "icios": "the vessels", "oiaj": "the essence",
    "cios": "the containers", "ain": "the liquid", "oteroe": "the process", "aram": "the burner",
    "sier": "the leaves", "dalaiu": "to distill", "dam": "to give", "ciodain": "the ducts",
    "aekiy": "the mixture", "air": "the air", "soar": "the steam", "ciey": "the sap",
    "dais": "the wheel", "odotoi": "the cycle", "doror": "the birth", "quaur": "the heat",
    "caud": "the elongated stem", "cedy": "is cut", "cidí": "to pour"
}

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])

@st.cache_data
def descargar_manuscrito_real():
    url = "https://www.voynich.nu/data/ZL3b-n.txt"
    archivo_completo = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/plain,text/html,*/*'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            lineas = response.read().decode('utf-8', errors='ignore').splitlines()
        
        for linea in lineas:
            match = re.match(r"^<f(\d+[rv])\b.*?>\s*(.*)", linea)
            if match:
                folio = match.group(1)
                contenido = match.group(2).strip()
                contenido = re.sub(r"\{.*?\}", "", contenido)
                contenido = re.sub(r";\w+", "", contenido)
                contenido = re.sub(r"[\=\+\-\_\,\.\;\:\(\)\d+]", "", contenido)
                
                if contenido and not contenido.startswith(("#", "%", "<")):
                    if folio not in archivo_completo:
                        archivo_completo[folio] = []
                    archivo_completo[folio].append(contenido)
        return archivo_completo
    except Exception:
        return {"1r": ["pshoey cttey oaror psoisoda kedy ceon ceey qokedy ckaur chedy toes"]}

CORPUS_MANUSCRITO = descargar_manuscrito_real()

def traducir_a_romance(texto):
    reglas = {
        'pcee': 'pi', 'pdr': 'pedr', 'pcs': 'pes', 'qok': 'quoqu', 'dceorceau': 'dicorcau',
        'ceeodaiin': 'ciodain', 'ceeey': 'cia', 'dce': 'dic', 'tceeodal': 'ciodal',
        'pc': 'p', 'ps': 'p', 'cp': 'p', 'ce': 'c', 'ey': 'a', 'eey': 'iy',
        'cs': 's', 'ck': 'qu', 'k': 'qu', 'ee': 'i', 'oe': 'u', 'iu': 'u',
        'dc': 'ch', 'tc': 'ch', 'ct': 'cut', 'oi': 'oi', 'ii': 'i', 'ae': 'a',
        'oo': 'u', 'ph': 'f', 'th': 't', 'ch': 'c', 'iii': 'i', 'm': 'm',
        'll': 'y', 'eee': 'ei', 'q': 'qu', 'ai': 'i', 'tt': 't', 'ts': 's',
        'iy': 'i', 'x': 'sh', 'el': 'l', 'quo': 'quo', 'eat': 'it', 'cee': 'ci',
        'o': 'o', 'a': 'a', 'l': 'l', 'y': 'i', 'í': 'i', 'ó': 'o'
    }
    texto_limpio = texto.lower()
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

def generar_espanol_sintactico(texto_romance, lang):
    lineas = texto_romance.split('\n')
    lineas_traducidas = []
    
    dict_activo = DICCIONARIO_ES if lang == "Español" else DICCIONARIO_EN
    prefix_linea = "Linea" if lang == "Español" else "Line"
        
    for idx, linea in enumerate(lineas):
        palabras = linea.split()
        linea_espanol = []
        
        for palabra in palabras:
            palabra_limpia = palabra.strip(",.!?*;:- ")
            # Ecualizar tildes y caracteres finales de control de coincidencia
            palabra_normalizada = palabra_limpia.replace("í", "i").replace("ó", "o").replace("y", "i")
            if not palabra_normalizada:
                continue
                
            if palabra_normalizada in dict_activo:
                linea_espanol.append(dict_activo[palabra_normalizada])
            else:
                linea_espanol.append(f"[{palabra_limpia}]")
        
        if linea_espanol:
            texto_linea = " ".join(linea_espanol).strip()
            texto_linea = re.sub(r'\s+', ' ', texto_linea)
            lineas_traducidas.append(f"{prefix_linea} {idx+1}: {texto_linea.capitalize()}. ")
            
    return "\n\n".join(lineas_traducidas)

tab1, tab2 = st.tabs([IFACE[idioma]["tab1"], IFACE[idioma]["tab2"]])

with tab1:
    st.subheader(IFACE[idioma]["lab_sub"])
    entrada = st.text_area("EVA Input:", "pshoey cttey oaror psoisoda")
    if st.button(IFACE[idioma]["btn_an"]):
        romance = traducir_a_romance(entrada)
        espanol = generar_espanol_sintactico(romance, idioma)
        c1, c2 = st.columns(2)
        with c1:
            st.success(IFACE[idioma]["fon_rom"])
            st.code(romance)
        with c2:
            st.info(IFACE[idioma]["trad_auto"])
            st.write(espanol)

with tab2:
    st.subheader(IFACE[idioma]["nav_sub"])
    if CORPUS_MANUSCRITO:
        lista_folios = sorted(list(CORPUS_MANUSCRITO.keys()), key=lambda x: (int(''.join(filter(str.isdigit, x))), x[-1]))
        folio_sel = st.selectbox(IFACE[idioma]["nav_sel"], lista_folios)
        
        if st.button(f"{IFACE[idioma]['btn_desc']} {folio_sel}"):
            lineas_eva = CORPUS_MANUSCRITO[folio_sel]
            texto_eva_completo = "\n".join(lineas_eva)
            
            romance_final = traducir_a_romance(texto_eva_completo)
            espanol_final = generar_espanol_sintactico(romance_final, idioma)
            
            st.write("---")
            st.markdown(f"### {IFACE[idioma]['res_tit']} {folio_sel}")
            
            col_eva, col_rom, col_esp = st.columns(3)
            with col_eva:
                st.warning(IFACE[idioma]["col1"])
                st.text_area("EVA", texto_eva_completo, height=450, disabled=True)
            with col_rom:
                st.success(IFACE[idioma]["col2"])
                st.text_area("Romance", romance_final, height=450)
            with col_esp:
                st.info(IFACE[idioma]["col3"])
                st.text_area("Translation", json_fix := espanol_final, height=450)
    else:
        st.warning(IFACE[idioma]["err_corpus"])
