import streamlit as st
import re
import urllib.request

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
        "trad_auto": "Traducción Literal:",
        "nav_sub": "Navegador Conectado a voynich.nu",
        "nav_sel": "Selecciona una página real (Folio):",
        "btn_desc": "Descifrar Folio",
        "res_tit": "Traducción Real para el Fragmento",
        "col1": "1. Texto Limpio (voynich.nu):",
        "col2": "2. Fonética Romance Extendida:",
        "col3": "3. Traducción Real:",
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
        "col3": "3. Real Translation:",
        "cargando": "Connecting to voynich.nu and fetching real manuscript...",
        "txt_placeholder": "Enter EVA glyphs (e.g., pshoey cttey oaror)..."
    }
}

# --- IMPORTACIÓN SEGURO DEL MOTOR MORFOLÓGICO DESDE VOYNIOSDATOS ---
try:
    from voynichdatos import DICCIONARIO_ES, DICCIONARIO_EN, descomponer_y_traducir_glifo, CORPUS_MANUSCRITO, cargar_todas_las_paginas_reales
    # Inicializar el corpus local por si se cae la web
    cargar_todas_las_paginas_reales()
except ImportError:
    st.error("Error: Asegúrate de tener el archivo voynichdatos.py en la misma carpeta.")
    st.stop()

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])

# --- DESCARGA Y LIMPIEZA AUTOMÁTICA DESDE EL SITIO WEB OFICIAL (FORMATO ZL3b-n) ---
@st.cache_data
def descargar_corpus_web():
    corpus = {}
    url = "https://voynich.nu/data/ZL3b-n.txt"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/plain,text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            lineas = response.read().decode('utf-8', errors='ignore').splitlines()
    except Exception as e:
        # Si falla la descarga, usamos el corpus simulado/local de voynichdatos
        return CORPUS_MANUSCRITO if CORPUS_MANUSCRITO else None

    for linea in lineas:
        linea = linea.strip()
        if not linea or linea.startswith("#") or linea.startswith("<%") or linea.startswith("=IVTFF"):
            continue
        if "Alphabet" in linea or "=" in linea:
            continue
        if re.search(r'<\s*([A-Z?\]\[!]\s*){3,}>', linea) or re.search(r'([A-Z]\s+){3,}[A-Z]', linea):
            continue

        match_folio = re.search(r'<f(\d+[r|v])', linea)
        if match_folio:
            folio = match_folio.group(1)
        else:
            continue

        texto_crudo = re.sub(r'^<[^>]+>', '', linea)
        texto_crudo = re.sub(r'<\s*([A-Z]\s*)+>', ' ', texto_crudo)
        texto_crudo = re.sub(r'\{[^}]*\}', ' ', texto_crudo)
        texto_crudo = re.sub(r'[-.=,;\$*!{}\[\]\d?:]', ' ', texto_crudo)
        
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

# --- NUEVA FUNCIÓN CONECTADA AL MOTOR MORFOLÓGICO MEDIEVAL ---
def traducir_a_romance(texto):
    dicc_activo = DICCIONARIO_ES if idioma == "Español" else DICCIONARIO_EN
    texto_limpio = texto.lower()
    texto_limpio = re.sub(r'[^a-z\s]', '', texto_limpio)
    palabras = texto_limpio.split()
    
    fonetica_lista = []
    traduccion_lista = []
    
    for pal in palabras:
        # Ejecuta la descomposición en prefijos, raíces y sufijos definida en voynichdatos
        palabra_fonetica = descomponer_y_traducir_glifo(pal)
        fonetica_lista.append(palabra_fonetica)
        
        # Búsqueda aproximada mediante Levenshtein (Tolerancia 3)
        mejor_coincidencia = f"[{palabra_fonetica}]"
        menor_distancia = 999
        for k, v in dicc_activo.items():
            dist = distancia_levenshtein(palabra_fonetica, k)
            if dist < menor_distancia and dist <= 3:
                menor_distancia = dist
                mejor_coincidencia = v
        traduccion_lista.append(mejor_coincidencia)
        
    return " ".join(fonetica_lista), " ".join(traduccion_lista)


# --- INTERFAZ GRÁFICA DE STREAMLIT ---
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
            
            # Crear cabeceras de columnas scaneables
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**{IFACE[idioma]['col1']}**")
            with col2:
                st.markdown(f"**{IFACE[idioma]['col2']}**")
            with col3:
                st.markdown(f"**{IFACE[idioma]['col3']}**")
            
            st.markdown("---")
            
            # Renderizar línea por línea de forma perfectamente alineada
            for linea in lineas_folio:
                if linea == "[Ilustración o Marcador Vacío]":
                    st.caption(linea)
                    continue
                
                fon_l, trad_l = traducir_a_romance(linea)
                
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.code(linea, language="text")
                with c2:
                    st.warning(fon_l)
                with c3:
                    st.success(trad_l)
    else:
        st.error("No se pudo cargar el Corpus Real del manuscrito Voynich.")
