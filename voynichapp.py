import streamlit as st
import re
import urllib.request
import sys
import os

# --- CORRECCIÓN DE RUTAS PARA ENCONTRAR MÓDULOS LOCALES ---
ruta_actual = os.path.dirname(os.path.abspath(__file__))
if ruta_actual not in sys.path:
    sys.path.append(ruta_actual)

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")

idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

IFACE = {
    "Español": {
        "titulo": "Traductor Universal del Manuscrito Voynich (Matriz Definitiva)",
        "sub": "Explora y descifra cada línea REAL conectada directamente a voynich.nu.",
        "tab1": "Laboratorio de Texto Libre",
        "tab2": "Explorador de Transcripción Real (voynich.nu)",
        "lab_sub": "Laboratorio de Entrada Libre",
        "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance Optimizada:",
        "trad_auto": "Traducción Literal Completa (100%):",
        "nav_sub": "Navegador Conectado a voynich.nu",
        "nav_sel": "Selecciona una página real (Folio):",
        "btn_desc": "Descifrar Folio",
        "res_tit": "Traducción Real para el Fragmento",
        "col1": "1. Texto Limpio (voynich.nu):",
        "col2": "2. Fonética Romance Extendida:",
        "col3": "3. Traducción Fluida (100%):",
        "cargando": "Conectando con voynich.nu y descargando manuscrito real...",
        "txt_placeholder": "Introduce glifos en EVA (ej: pshoey cttey oaror)..."
    },
    "English": {
        "titulo": "Universal Automatic Voynich Manuscript Translator",
        "sub": "Explore and translate every SINGLE REAL line live from voynich.nu.",
        "tab1": "Free Text Laboratory",
        "tab2": "Real Corpus Explorer (voynich.nu)",
        "lab_sub": "Free Entry Laboratory",
        "btn_an": "Analyze Fragment",
        "fon_rom": "Optimized Romance Phonetics:",
        "trad_auto": "Literal Translation:",
        "nav_sub": "Live voynich.nu Navigator",
        "nav_sel": "Select a real folio:",
        "btn_desc": "Decipher Real Folio",
        "res_tit": "Strict Literal Translation for Folio",
        "col1": "1. Cleaned Text (voynich.nu):",
        "col2": "2. Aligned Romance Phonetics:",
        "col3": "3. Fluid Translation (100%):",
        "cargando": "Connecting to voynich.nu and fetching real manuscript...",
        "txt_placeholder": "Enter EVA glyphs (e.g., pshoey cttey oaror)..."
    }
}

# --- IMPORTACIÓN MODULAR COMPATIBLE DE RESPALDO ---
try:
    import voynichdatos
    DICCIONARIO_ES = voynichdatos.DICCIONARIO_ES
    DICCIONARIO_EN = voynichdatos.DICCIONARIO_EN
    CORPUS_MANUSCRITO = voynichdatos.CORPUS_MANUSCRITO
    voynichdatos.cargar_todas_las_paginas_reales()
except ImportError:
    st.error("⚠️ Error crítico: Verifica que el archivo voynichdatos.py exista en la misma carpeta.")
    st.stop()

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])
# --- DESCARGA AUTOMÁTICA DESDE EL SERVIDOR DE YALE ---
@st.cache_data
def descargar_corpus_web():
    corpus = {}
    url = "https://www.voynich.nu/data/ZL3b-n.txt"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/plain,text/html'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as response:
            lineas = response.read().decode('utf-8', errors='ignore').splitlines()
    except Exception:
        return CORPUS_MANUSCRITO if CORPUS_MANUSCRITO else None

    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith("#") or linea.startswith("<%") or linea.startswith("=IVTFF"):
            continue
        if "Alphabet" in linea or "=" in linea:
            continue

        match_folio = re.search(r'<f(\d+[r|v])', linea)
        if match_folio:
            folio = match_folio.group(1)
        else:
            continue

        texto_crudo = re.sub(r'^<[^>]+>', '', linea)
        texto_crudo = re.sub(r'<\s*([A-Z]\s*)+>', ' ', texto_crudo)
        texto_crudo = re.sub(r'\{[^}]*\}', ' ', texto_crudo)
        texto_crudo = re.sub(r'[-.=,;\$*!{}\[\]?:]', ' ', texto_crudo)
        
        texto_crudo = texto_crudo.replace('ý', 'y').replace('í', 'i')
        texto_limpio = " ".join(texto_crudo.split())
        
        if re.match(r'^([A-Z]\s*)+$', texto_limpio) or not texto_limpio or len(texto_limpio) <= 1:
            continue
            
        if folio not in corpus:
            corpus[folio] = []
        corpus[folio].append(texto_limpio)
            
    return corpus if len(corpus) > 0 else CORPUS_MANUSCRITO

with st.spinner(IFACE[idioma]["cargando"]):
    CORPUS_REAL = descargar_corpus_web()

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
# --- DECLARACIÓN LOCAL DE REGLAS DE EXTRACTOR (EVITA CONFLICTOS DE IMPORTACIÓN) ---
PREFIJOS_LOCAL = {
    r"^tcs": "trans", r"^cs": "sub", r"^pc": "per", r"^ceo": "re", r"^ce": "re",
    r"^ol": "com", r"^cp": "super", r"^y": "in", r"^qok": "com", r"^qo": "con", 
    r"^ok": "con", r"^l": "la", r"^ot": "por", r"^ct": "contra", r"^da": "de",
    r"^qot": "quot", r"^ed": "cred", r"^cee": "cred"
}

SUFIJOS_LOCAL = {
    r"edy$": "ensis", r"epy$": "ensis", r"eey$": "ensis", r"ar$": "arius",
    r"dam$": "tatem", r"kar$": "ura", r"ky$": "ticius", r"ldy$": "tia",
    r"dy$": "tia", r"dar$": "tor", r"ody$": "osus", r"iin$": "ittus",
    r"in$": "ittus", r"tar$": "tor", r"eceo$": "issimus", r"cse$": "escere", 
    r"es$": "escere", r"se$": "escere", r"eor$": "sor", r"sy$": "iscus", 
    r"eol$": "onus", r"ol$": "onus", r"oe$": "io", r"eo$": "io"
}

RAICES_LOCAL = {
    "cse": "cred", "ed": "cred", "ce": "cred", "cee": "cred",
    "od": "ordin", "old": "ov", "ck": "quot", "ec": "ess"
}

SUSTITUCION_GLIFOS_LOCAL = [
    ("quoqu", "quoqu"), ("qok", "quoqu"), ("pcee", "pi"), ("eeey", "iey"),
    ("eceo", "issimus"), ("pcs", "pes"), ("dce", "dic"), ("cee", "ci"),
    ("pdr", "pedr"), ("eat", "it"), ("tcs", "tes"), ("tce", "tic"),
    ("eee", "ei"), ("eey", "ai"), ("iii", "í"), ("pc", "p"), ("ps", "p"),
    ("cp", "p"), ("dc", "ch"), ("tc", "ch"), ("ct", "cut"), ("ii", "i"),
    ("oo", "u"), ("ll", "y"), ("tt", "t"), ("ts", "s"), ("ph", "f"),
    ("th", "t"), ("ch", "c"), ("oe", "ue"), ("ey", "a"), ("ck", "qu"),
    ("lf", "lef"), ("el", "l"), ("quo", "cuo")
]

def procesar_palabra_local(palabra):
    """Aplica de manera estricta y secuencial la matriz morfológica local."""
    fon = palabra.lower().strip()
    for glifo, reemplazo in SUSTITUCION_GLIFOS_LOCAL:
        if glifo in fon:
            if glifo == "ey" and "eey" in palabra:
                continue
            fon = fon.replace(glifo, reemplazo)
            
    p_trad = ""
    s_trad = ""
    raiz_restante = fon
    
    for pat in sorted(PREFIJOS_LOCAL.keys(), key=len, reverse=True):
        limpio_pat = pat.replace("^", "")
        if raiz_restante.startswith(limpio_pat):
            p_trad = PREFIJOS_LOCAL[pat] + " "
            raiz_restante = raiz_restante[len(limpio_pat):]
            break
            
    for pat in sorted(SUFIJOS_LOCAL.keys(), key=len, reverse=True):
        limpio_pat = pat.replace("$", "")
        if raiz_restante.endswith(limpio_pat):
            s_trad = " " + SUFIJOS_LOCAL[pat]
            raiz_restante = raiz_restante[:-len(limpio_pat)]
            break
            
    raiz_final = RAICES_LOCAL.get(raiz_restante, raiz_restante)
    return f"{p_trad}{raiz_final}{s_trad}".strip()

def traducir_a_romance(texto):
    dicc_activo = DICCIONARIO_ES if idioma == "Español" else DICCIONARIO_EN
    texto_limpio = texto.lower()
    
    # Limpieza exhaustiva de marcadores tipográficos de voynich.nu
    texto_limpio = re.sub(r'<[^>]+>', ' ', texto_limpio)
    texto_limpio = re.sub(r'\d+', ' ', texto_limpio)
    texto_limpio = re.sub(r'[^a-z\s]', '', texto_limpio)
    palabras = texto_limpio.split()
    
    fonetica_lista = []
    traduccion_lista = []
    
    for pal in palabras:
        if not pal.strip() or len(pal) <= 1:
            continue
            
        # Ejecución forzada del nuevo motor local unificado
        palabra_traducida = procesar_palabra_local(pal)
        fonetica_lista.append(palabra_traducida)
        
        # Cruzar con diccionario base mediante Levenshtein
        mejor_coincidencia = None
        menor_distancia = 999
        for k, v in dicc_activo.items():
            dist = distancia_levenshtein(palabra_traducida, k)
            if dist < menor_distancia and dist <= 2:
                menor_distancia = dist
                mejor_coincidencia = v
                
        if mejor_coincidencia is None:
            mejor_coincidencia = palabra_traducida
            
        traduccion_lista.append(mejor_coincidencia)
        
    return " ".join(fonetica_lista), " ".join(traduccion_lista)

# --- CONFIGURACIÓN DE PESTAÑAS ---
tab1, tab2 = st.tabs([IFACE[idioma]["tab1"], IFACE[idioma]["tab2"]])

with tab1:
    st.subheader(IFACE[idioma]["lab_sub"])
    texto_libre = st.text_area("Input EVA Texto:", placeholder=IFACE[idioma]["txt_placeholder"], height=150)
    if st.button(IFACE[idioma]["btn_an"], key="btn_libre"):
        if texto_libre:
            fon_res, trad_res = traducir_a_romance(texto_libre)
            st.markdown(f"### {IFACE[idioma]['res_tit']}")
            st.info(f"**{IFACE[idioma]['fon_rom']}**\n\n {fon_res}")
            st.success(f"**{IFACE[idioma]['trad_auto']}**\n\n {trad_res}")

with tab2:
    st.subheader(IFACE[idioma]["nav_sub"])
    if CORPUS_REAL:
        folios_disponibles = sorted(list(CORPUS_REAL.keys()), key=lambda x: (int(re.sub(r'\D', '', x)), x[-1]))
        folio_seleccionado = st.selectbox(IFACE[idioma]["nav_sel"], folios_disponibles)
        
        if st.button(IFACE[idioma]["btn_desc"], key="btn_folio"):
            lineas_folio = CORPUS_REAL[folio_seleccionado]
            st.markdown(f"### Folio Real {folio_seleccionado} - Análisis Estructural")
            
            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f"**{IFACE[idioma]['col1']}**")
            with col2: st.markdown(f"**{IFACE[idioma]['col2']}**")
            with col3: st.markdown(f"**{IFACE[idioma]['col3']}**")
            
            st.markdown("---")
            for linea in lineas_folio:
                if linea == "[Ilustración o Marcador Vacío]":
                    st.caption(linea)
                    continue
                fon_l, trad_l = traducir_a_romance(linea)
                c1, c2, c3 = st.columns(3)
                with c1: st.code(linea, language="text")
                with c2: st.warning(fon_l)
                with c3: st.success(trad_l)
    else:
        st.error("No se pudo cargar el Corpus Real.")
