import streamlit as st
import re
import os

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")

idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

IFACE = {
    "Español": {
        "titulo": "Traductor Universal del Manuscrito Voynich (Matriz Definitiva)",
        "sub": "Explora y descifra cada línea REAL de voynich.nu aplicando tu matriz fonética.",
        "tab1": "Laboratorio de Texto Libre",
        "tab2": "Explorador del Corpus Real (voyn_101.txt)",
        "lab_sub": "Laboratorio de Entrada Libre",
        "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance Optimizada:",
        "trad_auto": "Traducción Literal:",
        "nav_sub": "Navegador de Folios Reales",
        "nav_sel": "Selecciona un folio real:",
        "btn_desc": "Descifrar Folio",
        "res_tit": "Traducción Real para el Folio",
        "col1": "1. Texto Real (voynich.nu):",
        "col2": "2. Fonética Romance:",
        "col3": "3. Traducción Real:"
    },
    "English": {
        "titulo": "Universal Automatic Voynich Manuscript Translator",
        "sub": "Explore and translate every SINGLE REAL line from voynich.nu using your matrix.",
        "tab1": "Free Text Laboratory",
        "tab2": "Real Corpus Explorer (voyn_101.txt)",
        "lab_sub": "Free Entry Laboratory",
        "btn_an": "Analyze Fragment",
        "fon_rom": "Optimized Romance Phonetics:",
        "trad_auto": "Literal Translation:",
        "nav_sub": "Real Folios Navigator",
        "nav_sel": "Select a real folio:",
        "btn_desc": "Decipher Real Folio",
        "res_tit": "Strict Literal Translation for Folio",
        "col1": "1. Real Text (voynich.nu):",
        "col2": "2. Aligned Romance Phonetics:",
        "col3": "3. Real Translation:"
    }
}

# Traemos tus diccionarios desde tu otro archivo
try:
    from voynichdatos import DICCIONARIO_ES, DICCIONARIO_EN
except ImportError:
    DICCIONARIO_ES = {"pui": "la planta", "cuta": "la corteza"}
    DICCIONARIO_EN = {"pui": "the plant", "cuta": "the bark"}

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])

# --- LEER EL ARCHIVO REAL DE VOYNICH.NU ---
@st.cache_data
def cargar_corpus_real():
    corpus = {}
    archivo = "voyn_101.txt"
    
    if not os.path.exists(archivo):
        return None
        
    with open(archivo, "r", encoding="utf-8", errors="ignore") as f:
        for linea in f:
            linea = linea.strip()
            # Salta comentarios de voynich.nu
            if not linea or linea.startswith("#") or linea.startswith("<%"):
                continue
            
            # Formato típico: <f1r.P1.1;H> pshoey cttey oaror
            match = re.match(r"^<f(\d+[r|v])\..*?>\s+(.*)\$", linea)
            if match:
                folio = match.group(1)
                texto_linea = match.group(2)
                # Limpia caracteres raros de transcripción
                texto_linea = re.sub(r'[-.=,;]', ' ', texto_linea)
                texto_linea = re.sub(r'[*!{}]', '', texto_linea)
                texto_linea = " ".join(texto_linea.split())
                
                if texto_linea:
                    if folio not in corpus:
                        corpus[folio] = []
                    corpus[folio].append(texto_linea)
    return corpus

CORPUS_REAL = cargar_corpus_real()

def distancia_levenshtein(s1, s2):
    if len(s1) < len(s2): return distancia_levenshtein(s2, s1)
    if len(s2) == 0: return len(s1)
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

def traducir_a_romance(texto):
    dicc_activo = DICCIONARIO_ES if idioma == "Español" else DICCIONARIO_EN
    texto_limpio = texto.lower()
    texto_limpio = re.sub(r'[^a-z0-9\s]', '', texto_limpio)
    palabras = texto_limpio.split()
    
    fonetica_lista = []
    traduccion_lista = []
    
    for pal in palabras:
        fon = pal
        
        # TUS REGLAS FONÉTICAS ESTRICTAS
        fon = re.sub(r'qok', 'quoqu', fon)
        fon = re.sub(r'pcee', 'pi', fon)
        fon = re.sub(r'pcs', 'pes', fon)
        fon = re.sub(r'iii', 'í', fon)
        fon = re.sub(r'eee', 'ei', fon)
        fon = re.sub(r'eey', 'ai', fon)
        fon = re.sub(r'pc|ps|cp', 'p', fon)
        fon = re.sub(r'dce', 'dic', fon)
        fon = re.sub(r'cee', 'ci', fon)
        fon = re.sub(r'pdr', 'pedr', fon)
        fon = re.sub(r'eat', 'it', fon)
        fon = re.sub(r'dc|tc', 'ch', fon)
        fon = re.sub(r'ct', 'cut', fon)
        fon = re.sub(r'ii', 'i', fon)
        fon = re.sub(r'oo', 'u', fon)
        fon = re.sub(r'll', 'y', fon)
        fon = re.sub(r'tt', 't', fon)
        fon = re.sub(r'ts', 's', fon)
        fon = re.sub(r'ph', 'f', fon)
        fon = re.sub(r'th', 't', fon)
        fon = re.sub(r'ch', 'c', fon)
        if 'eey' not in pal: fon = re.sub(r'ey', 'a', fon)
        fon = re.sub(r'oe', 'ue', fon)
        fon = re.sub(r'iu', 'u', fon)
        fon = re.sub(r'oi', 'oy', fon)
        fon = re.sub(r'ae', 'a', fon)
        fon = re.sub(r'ai', 'i', fon)
        fon = re.sub(r'iy', 'í', fon)
        fon = re.sub(r'quo', 'cuo', fon)
        fon = re.sub(r'ck|k|q', 'qu', fon)
        fon = re.sub(r'x', 'sh', fon)
        fon = re.sub(r'el', 'l', fon)
        
        if fon.startswith('y'): fon = 'i' + fon[1:]
        if fon.endswith('y'): fon = fon[:-1] + 'í'
            
        fonetica_lista.append(fon)
        
        if fon in dicc_activo:
            traduccion_lista.append(dicc_activo[fon])
        else:
            mejor_coincidencia = None
            distancia_minima = float('inf')
            for clave in dicc_activo.keys():
                dist = distancia_levenshtein(fon, clave)
                if dist < distancia_minima:
                    distancia_minima = dist
                    mejor_coincidencia = clave
            if distancia_minima <= 2 and mejor_coincidencia:
                traduccion_lista.append(dicc_activo[mejor_coincidencia] + "*")
            else:
                traduccion_lista.append(f"[{pal}]")
                
    return " ".join(fonetica_lista), " ".join(traduccion_lista)

tab1, tab2 = st.tabs([IFACE[idioma]["tab1"], IFACE[idioma]["tab2"]])

with tab1:
    st.subheader(IFACE[idioma]["lab_sub"])
    area_texto = st.text_area("Input EVA:", value="pshoey cttey oaror")
    if st.button(IFACE[idioma]["btn_an"]):
        fon, trad = traducir_a_romance(area_texto)
        st.markdown(f"**{IFACE[idioma]['fon_rom']}** `{fon}`")
        st.success(f"**{IFACE[idioma]['trad_auto']}** {trad}")

with tab2:
    st.subheader(IFACE[idioma]["nav_sub"])
    
    if CORPUS_REAL is None:
        st.error("Error: Sube el archivo 'voyn_101.txt' a tu repositorio de GitHub para ver las páginas reales.")
    else:
        folios_ordenados = sorted(list(CORPUS_REAL.keys()), key=lambda x: (int(re.sub(r'\D', '', x)), x[-1]))
        folio_sel = st.selectbox(IFACE[idioma]["nav_sel"], folios_ordenados)
        
        if st.button(IFACE[idioma]["btn_desc"]):
            st.markdown(f"### {IFACE[idioma]['res_tit']} {folio_sel}")
            lineas = CORPUS_REAL[folio_sel]
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**{IFACE[idioma]['col1']}**")
                for l in lineas: st.write(l)
            with col2:
                st.markdown(f"**{IFACE[idioma]['col2']}**")
                for l in lineas:
                    fon, _ = traducir_a_romance(l)
                    st.write(fon)
            with col3:
                st.markdown(f"**{IFACE[idioma]['col3']}**")
                for l in lineas:
                    _, trad = traducir_a_romance(l)
                    st.write(trad)
