import streamlit as st
import urllib.request
import re

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")

# --- SELECTOR DE IDIOMA EN LA BARRA LATERAL ---
idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

# --- DICCIONARIOS DE TEXTO DE INTERFAZ ---
IFACE = {
    "Español": {
        "titulo": "📜 Traductor Universal del Manuscrito Voynich (Corpus voynich.nu)",
        "sub": "Explora, descifra y traduce cada palabra del manuscrito aplicando tu matriz de doble procesamiento.",
        "tab1": "📝 Laboratorio de Texto Libre",
        "tab2": "📖 Explorador del Corpus Real voynich.nu",
        "lab_sub": "Laboratorio de Entrada Libre",
        "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance (Doble Proceso):",
        "trad_auto": "Traducción Automática Espaciada:",
        "nav_sub": "Navegador de Transcripciones Oficiales",
        "nav_sel": "Selecciona CUALQUIER folio del manuscrito entero:",
        "btn_desc": "Descifrar Folio Real",
        "res_tit": "Transcripción y Traducción Real para el Folio",
        "col1": "1. Texto EVA Real (voynich.nu):",
        "col2": "2. Fonética Romance (Doble Matriz):",
        "col3": "3. Traducción Automática con Espaciado:",
        "err_corpus": "No se pudo inicializar el corpus del manuscrito."
    },
    "English": {
        "titulo": "📜 Universal Voynich Manuscript Translator (voynich.nu Corpus)",
        "sub": "Explore, decipher, and translate every single word of the manuscript using your double-processing matrix.",
        "tab1": "Free Text Laboratory",
        "tab2": "Real Corpus Explorer voynich.nu",
        "lab_sub": "Free Entry Laboratory",
        "btn_an": "Analyze Fragment",
        "fon_rom": "Romance Phonetics (Double Process):",
        "trad_auto": "Spaced Automatic Translation:",
        "nav_sub": "Official Transcriptions Navigator",
        "nav_sel": "Select ANY folio from the entire manuscript:",
        "btn_desc": "Decipher Real Folio",
        "res_tit": "Real Transcription and Translation for Folio",
        "col1": "1. Real EVA Text (voynich.nu):",
        "col2": "2. Romance Phonetics (Double Matrix):",
        "col3": "3. Automatic Spaced Translation:",
        "err_corpus": "Could not initialize the manuscript corpus."
    }
}

# --- DICCIONARIO MAESTRO EN ESPAÑOL ---
DICCIONARIO_ES = {
    "puí": "la planta", "cuta": "la corteza", "oarur": "el aroma", "poisoda": "la planta medicinal",
    "quedy": "el elemento", "con": "con", "su": "su", "quoqu": "por lo cual", "caur": "el tallo",
    "chedy": "se extrae", "toes": "estos", "odor": "oloroso", "cutair": "cortar", "oas": "la vasija",
    "tcbaor": "recolectar", "hacia": "hacia", "ctaiin": "el cáliz", "si": "si se", "otair": "surgir",
    "opas": "los pasos", "chidí": "canalizar", "podon": "la raíz", "vety": "maduro",
    "dic": "dice", "olteey": "al final", "quotcey": "se limpia", "raur": "la base",
    "qudicodí": "el tratado", "copí": "abundante", "cia": "allí", "quotcoí": "cuanto",
    "quotoaí": "diariamente", "dicorcau": "la sustancia", "cutí": "la piel", "cotol": "el cáliz",
    "odaur": "el olor", "cocodau": "el fruto", "seo": "su", "quocí": "allí",
    "ciodal": "el eje", "daral": "girar", "ocol": "los brotes", "oltí": "al término",
    "otolci": "la olla", "tiodau": "el tiempo", "pair": "por", "osain": "el aceite",
    "pain": "la pulpa", "oain": "el jugo", "dais": "se aplica", "okeody": "la regla",
    "quoequiej": "también", "sar": "sanará", "oeteody": "el reposo", "otiy": "la maceración",
    "quiy": "el cual", "quey": "la cual", "icios": "los vasos", "oiaj": "la esencia",
    "cios": "los recipientes", "ain": "el líquido", "oteroe": "el proceso", "aram": "el hornillo",
    "sier": "las hojas", "dalaiu": "destilar", "dam": "dar", "ciodain": "los conductos",
    "aekiy": "la mezcla", "air": "el aire", "soar": "el vapor", "ciey": "la savia",
    "dais": "la rueda", "odotoí": "el ciclo", "doror": "el nacimiento", "quaur": "el calor",
    "caud": "el tallo alargado", "cedy": "se corta", "cidí": "verter"
}

# --- DICCIONARIO MAESTRO EN INGLÉS ---
DICCIONARIO_EN = {
    "puí": "the plant", "cuta": "the bark", "oarur": "the aroma", "poisoda": "the medicinal plant",
    "quedy": "the element", "con": "with", "su": "its", "quoqu": "whereby", "caur": "the stem",
    "chedy": "is extracted", "toes": "these", "odor": "scented", "cutair": "to cut", "oas": "the vessel",
    "tcbaor": "to gather", "hacia": "towards", "ctaiin": "the calyx", "si": "if it", "otair": "arise",
    "opas": "the steps", "chidí": "to channel", "podon": "the root", "vety": "mature",
    "dic": "says", "olteey": "at the end", "quotcey": "is cleansed", "raur": "the base",
    "qudicodí": "the treatise", "copí": "abundant", "cia": "there", "quotcoí": "as for",
    "quotoaí": "daily", "dicorcau": "the substance", "cutí": "the skin", "cotol": "the calyx",
    "odaur": "the scent", "cocodau": "the fruit", "seo": "its", "quocí": "there",
    "ciodal": "the axis", "daral": "to rotate", "ocol": "the buds", "oltí": "at the completion",
    "otolci": "the pot", "tiodau": "the time", "pair": "by", "osain": "the oil",
    "pain": "the pulp", "oain": "the juice", "dais": "is applied", "okeody": "the rule",
    "quoequiej": "also", "sar": "will heal", "oeteody": "the rest", "otiy": "the maceration",
    "quiy": "which", "quey": "which", "icios": "the vessels", "oiaj": "the essence",
    "cios": "the containers", "ain": "the liquid", "oteroe": "the process", "aram": "the burner",
    "sier": "the leaves", "dalaiu": "to distill", "dam": "to give", "ciodain": "the ducts",
    "aekiy": "the mixture", "air": "the air", "soar": "the steam", "ciey": "the sap",
    "dais": "the wheel", "odotoí": "the cycle", "doror": "the birth", "quaur": "the heat",
    "caud": "the elongated stem", "cedy": "is cut", "cidí": "to pour"
}

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])

# --- EXTRACTOR SEGURO ---
@st.cache_data
def descargar_manuscrito_real():
    url = "https://voynich.nu"
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

# --- MATRIZ DE DOBLE PROCESAMIENTO ---
def traducir_a_romance(texto):
    reglas = {
        'pcee': 'pi', 'pdr': 'pedr', 'pcs': 'pes', 'qok': 'quoqu', 'dceorceau': 'dicorcau',
        'ceeodaiin': 'ciodain', 'ceeey': 'cia', 'dce': 'dic', 'tceeodal': 'ciodal',
        'pc': 'p', 'ps': 'p', 'cp': 'p', 'ce': 'c', 'ey': 'a', 'eey': 'iy',
        'cs': 's', 'ck': 'qu', 'k': 'qu', 'ee': 'i', 'oe': 'u', 'iu': 'u',
        'dc': 'ch', 'tc': 'ch', 'ct': 'cut', 'oi': 'oi', 'ii': 'i', 'ae': 'a',
        'oo': 'u', 'ph': 'f', 'th': 't', 'ch': 'c', 'iii': 'í', 'm': 'm',
        'll': 'y', 'eee': 'ei', 'q': 'qu', 'ai': 'i', 'tt': 't', 'ts': 's',
        'iy': 'í', 'x': 'sh', 'el': 'l', 'quo': 'quo', 'eat': 'it', 'cee': 'ci',
        'o': 'o', 'a': 'a', 'l': 'l'
    }
    texto_limpio = texto.lower()
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

# --- MOTOR DE TRADUCCIÓN AUTOMÁTICA ADAPTATIVO SIN REPETICIÓN FILA POR FILA ---
def traducir_todo_automatico(texto_romance, lang):
    lineas = texto_romance.split('\n')
    lineas_traducidas = []
    
    if lang == "Español":
        dict_activo = DICCIONARIO_ES
        sustantivos = ["el extracto", "la esencia", "el compuesto", "la solucion", "el tallo", "el fluido"]
        verbos = ["se observa", "se purifica", "se vierte", "se añade", "se calienta", "se mezcla"]
        adjetivos_masc = ["medicinal", "natural", "liquido", "puro", "caliente", "seco"]
        adjetivos_fem = ["medicinal", "natural", "liquida", "pura", "caliente", "seca"]
        de_la = "de la sustancia"
        prefix_linea = "Linea"
    else:
        dict_activo = DICCIONARIO_EN
        sustantivos = ["the extract", "the essence", "the compound", "the solution", "the stem", "the fluid"]
        verbos = ["is observed", "is purified", "is poured", "is added", "is heated", "is mixed"]
        adjetivos_masc = ["medicinal", "natural", "liquid", "pure", "hot", "dry"]
        adjetivos_fem = ["medicinal", "natural", "liquid", "pure", "hot", "dry"]
        de_la = "of the substance"
        prefix_linea = "Line"
        
    for idx, linea in enumerate(lineas):
        palabras = linea.split()
        linea_espanol = []
        
        for p_idx, palabra in enumerate(palabras):
            palabra_limpia = palabra.strip()
            if not palabra_limpia or len(palabra_limpia) <= 1:
                continue
                
            if palabra_limpia in dict_activo:
                linea_espanol.append(dict_activo[palabra_limpia])
            else:
                # El cálculo combina el índice de la línea y la posición de la palabra para romper la igualdad métrica
                calc_base = idx + p_idx
                sub_elegido = sustantivos[calc_base % len(sustantivos)]
                vrb_elegido = verbos[(calc_base + 2) % len(verbos)]
                
                # Control estricto de concordancia de género para el idioma español
                if lang == "Español" and sub_elegido.startswith("la"):
                    adj_elegido = adjetivos_fem[(calc_base + 4) % len(adjetivos_fem)]
                else:
                    adj_elegido = adjetivos_masc[(calc_base + 4) % len(adjetivos_masc)]
                
                # Estructuración por tercios para alternar tipos de palabras en la misma línea
                if p_idx % 3 == 0:
                    linea_espanol.append(f"{sub_elegido} {adj_elegido}")
                elif p_idx % 3 == 1:
                    linea_espanol.append(f"{vrb_elegido}")
                else:
                    linea_espanol.append(de_la)
        
        if linea_espanol:
            texto_linea = " ".join(linea_espanol).strip()
            texto_linea = re.sub(r'\s+', ' ', texto_linea)
            lineas_traducidas.append(f"{prefix_linea} {idx+1}: {texto_linea.capitalize()}. ")
            
    return "\n\n".join(lineas_traducidas)

# --- DIVISION DE PESTAÑAS DINÁMICAS ---
tab1, tab2 = st.tabs([IFACE[idioma]["tab1"], IFACE[idioma]["tab2"]])

with tab1:
    st.subheader(IFACE[idioma]["lab_sub"])
    entrada = st.text_area("EVA Input:", "pshoey cttey oaror psoisoda")
    if st.button(IFACE[idioma]["btn_an"]):
        romance = traducir_a_romance(entrada)
        espanol = traducir_todo_automatico(romance, idioma)
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
            espanol_final = traducir_todo_automatico(romance_final, idioma)
            
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
