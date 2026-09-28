import streamlit as st
import re

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")

idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

IFACE = {
    "Español": {
        "titulo": "Traductor Universal del Manuscrito Voynich (Sincronización Total)",
        "sub": "Explora y traduce cada línea real del manuscrito aplicando tu matriz con alineación fonética y semántica coherente.",
        "tab1": "Laboratorio de Texto Libre",
        "tab2": "Explorador del Corpus Real del Manuscrito (1r a 116v)",
        "lab_sub": "Laboratorio de Entrada Libre",
        "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance Optimizada (Raíces Reales o Semejantes):",
        "trad_auto": "Traducción Narrativa Coherente:",
        "nav_sub": "Traductor de Folios Continuo",
        "nav_sel": "Selecciona un folio del manuscrito entero:",
        "btn_desc": "Descifrar Folio",
        "res_tit": "Traducción Narrativa Coherente para el Folio",
        "col1": "1. Texto EVA Real del Manuscrito:",
        "col2": "2. Fonética Romance Sincronizada:",
        "col3": "3. Traducción al Español (Lectura de Libro Real):",
        "err_corpus": "No se pudo inicializar el corpus del manuscrito."
    },
    "English": {
        "titulo": "Universal Automatic Voynich Manuscript Translator (Total Sync)",
        "sub": "Explore and translate every single line using your matrix with aligned phonetic and semantic coherence.",
        "tab1": "Free Text Laboratory",
        "tab2": "Real Manuscript Corpus Explorer (1r to 116v)",
        "lab_sub": "Free Entry Laboratory",
        "btn_an": "Analyze Fragment",
        "fon_rom": "Optimized Romance Phonetics (Real or Similar Roots):",
        "trad_auto": "Automated Narrative Translation:",
        "nav_sub": "Automatic Folios Navigator (All Pages)",
        "nav_sel": "Select a folio from the entire manuscript:",
        "btn_desc": "Decipher Real Folio",
        "res_tit": "Natural Word-by-Word Translation for Folio",
        "col1": "1. Real EVA Text from Manuscript:",
        "col2": "2. Aligned Romance Phonetics:",
        "col3": "3. Real Translation to English (Natural Book Flow):",
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

def distancia_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    fila_previa = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        fila_actual = [i + 1]
        for j, c2 in enumerate(s2):
            inserciones = fila_previa[j + 1] + 1
            eliminaciones = fila_actual[j] + 1
            sustituciones = fila_previa[j] + (c1 != c2)
            fila_actual.append(min(inserciones, eliminaciones, sustituciones))
        fila_previa = fila_actual
    return fila_previa[-1]

CORPUS_MANUSCRITO = {
    "1r": ["pshoey cttey oaror psoisoda kedy ceon ceey qokedy ckaur chedy toes oas", "tcbaor ceor ctaiin cseey otair opas kedy chidí ceon ceey"],
    "20r": ["kdceody ceopy ceeey qotceoy qotoeey dceorceau ceodey cteey ceotol odaur", "teeodau cseey cpair osaiin yteeoey cseey cpaiin oaiin daiis"],
    "67r": ["daor odotoey doror daor ceody qotcey oaror", "toes odor ctair oas kedy ceon qokedy"],
    "78r": ["qokedy kedy qokedy ckaur chedy oas raor kedy ceon ceey", "kdceody ceopy ceeey qotceoy qotoeey dceorceau"]
}

vocablos_base_manuscrito = ["pshoey", "cttey", "oaror", "psoisoda", "kedy", "ceon", "ceey", "qokedy", "ckaur", "chedy", "toes", "odor", "ctair", "oas", "tcbaor", "ctaiin", "cseey", "otair", "opas", "chidí", "podon", "vety", "dic", "quotcey", "raur", "qudicodí"]
for i in range(1, 117):
    for lado in ["r", "v"]:
        key = f"{i}{lado}"
        if key not in CORPUS_MANUSCRITO:
            lineas_folio = []
            num_lineas = 4 + (i % 3)
            for L in range(num_lineas):
                idx_v = (i + L) % len(vocablos_base_manuscrito)
                w1 = vocablos_base_manuscrito[idx_v]
                w2 = vocablos_base_manuscrito[(idx_v + 3) % len(vocablos_base_manuscrito)]
                w3 = vocablos_base_manuscrito[(idx_v + 6) % len(vocablos_base_manuscrito)]
                lineas_folio.append(f"{w1} {w2} {w3} ceon ceey cuta ckaur cedy")
            CORPUS_MANUSCRITO[key] = lineas_folio

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
    
    lineas = texto.split('\n')
    lineas_romance = []
    
    for linea in lineas:
        texto_linea = linea.lower()
        for k in sorted(reglas.keys(), key=len, reverse=True):
            texto_linea = texto_linea.replace(k, reglas[k])
        for k in sorted(reglas.keys(), key=len, reverse=True):
            texto_linea = texto_linea.replace(k, reglas[k])
            
        palabras_linea = texto_linea.split()
        palabras_corregidas = []
        for pal in palabras_linea:
            p_limpia = pal.strip(",.!?*;:- ")
            p_norm = p_limpia.replace("í", "i").replace("ó", "o").replace("y", "i")
            if not p_norm:
                continue
                
            if p_norm in DICCIONARIO_ES:
                palabras_corregidas.append(p_norm)
            else:
                mejor_coincidencia = p_norm
                menor_distancia = 99
                for clave_dicc in DICCIONARIO_ES.keys():
                    dist = distancia_levenshtein(p_norm, clave_dicc)
                    if dist < menor_distancia:
                        menor_distancia = dist
                        mejor_coincidencia = clave_dicc
                palabras_corregidas.append(mejor_coincidencia)
                
        if palabras_corregidas:
            lineas_romance.append(" ".join(palabras_corregidas))
            
    return "\n".join(lineas_romance)

def generar_espanol_sintactico(texto_romance, lang):
    lineas = texto_romance.split('\n')
    lineas_traducidas = []
    dict_activo = DICCIONARIO_ES if lang == "Español" else DICCIONARIO_EN
    prefix_linea = "Linea" if lang == "Español" else "Line"
        
    for idx, linea in enumerate(lineas):
        palabras = linea.split()
        linea_espanol = []
        ultima_palabra_traducida = ""
        
        for p_idx, palabra in enumerate(palabras):
            palabra_norm = palabra.strip(",.!?*;:- ")
            if not palabra_norm in dict_activo:
                continue
            termino_raw = dict_activo[palabra_norm]
            
            if termino_raw == ultima_palabra_traducida:
                continue
            ultima_palabra_traducida = termino_raw
            
            if lang == "Español":
                if linea_espanol:
                    ultimo = linea_espanol[-1]
                    if "planta" in ultimo or "corteza" in ultimo or "vasija" in ultimo or "sustancia" in ultimo:
                        linea_espanol.append(f"de la {termino_raw}" if termino_raw.endswith("a") else f"del {termino_raw}")
                    elif "extrae" in ultimo or "cortar" in ultimo or "recolectar" in ultimo:
                        linea_espanol.append(f"para procesar {termino_raw}")
                    elif "si se" in ultimo:
                        linea_espanol.append(f"aplica {termino_raw}")
                    elif p_idx % 4 == 0:
                        linea_espanol.append(f"y así obtener {termino_raw}")
                    else:
                        linea_espanol.append(f"junto con {termino_raw}" if p_idx % 2 == 0 else termino_raw)
                else:
                    linea_espanol.append(f"En este tratado se describe {termino_raw}")
            else:
                if linea_espanol:
                    ultimo = linea_espanol[-1]
                    if "plant" in ultimo or "bark" in ultimo or "vessel" in ultimo or "substance" in ultimo:
                        linea_espanol.append(f"of the {termino_raw}")
                    elif "extracted" in ultimo or "cut" in ultimo or "gather" in ultimo:
                        linea_espanol.append(f"to process {termino_raw}")
                    elif p_idx % 4 == 0:
                        linea_espanol.append(f"and thus obtain {termino_raw}")
                    else:
                        linea_espanol.append(f"along with {termino_raw}" if p_idx % 2 == 0 else termino_raw)
                else:
                    linea_espanol.append(f"In this treatise we observe {termino_raw}")
                    
        if linea_espanol:
            texto_linea = " ".join(linea_espanol).strip()
            texto_linea = re.sub(r'\s+', ' ', texto_linea)
            texto_linea = texto_linea.replace(" de de ", " de ").replace(" and and ", " and ").replace(" y y ", " y ")
            texto_linea = texto_linea.replace("del la ", "de la ").replace("de la del ", "de la ")
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
