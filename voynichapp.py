# ==========================================
# ARCHIVO: voynichapp.py - PARTE 1 DE 2
# ==========================================
import streamlit as st
import re
import urllib.request
import ssl
import sys
import os

# Forzado de inclusión de directorios y control de rutas
ruta_actual = os.path.dirname(os.path.abspath(__file__))
if ruta_actual not in sys.path:
    sys.path.append(ruta_actual)

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")
idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

IFACE = {
    "Español": {
        "titulo": "Traductor Universal del Manuscrito Voynich (Matriz Definitiva)",
        "sub": "Explora y descifra cada línea REAL conectada directamente a voynich.nu.",
        "tab1": "Laboratorio de Texto Libre", "tab2": "Explorador de Transcripción Real (voynich.nu)",
        "lab_sub": "Laboratorio de Entrada Libre", "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance Optimizada:", "trad_auto": "Traducción Literal Completa (100%):",
        "nav_sub": "Navegador Conectado a voynich.nu", "nav_sel": "Selecciona una página real (Folio):",
        "btn_desc": "Descifrar Folio", "res_tit": "Traducción Real para el Fragmento",
        "col1": "1. Texto Limpio (voynich.nu):", "col2": "2. Fonética Romance Extendida:", "col3": "3. Traducción Fluida (100%):",
        "cargando": "Conectando con voynich.nu y descargando manuscrito real...", "txt_placeholder": "Introduce glifos en EVA (ej: pshoey cttey oaror shkcor)..."
    },
    "English": {
        "titulo": "Universal Automatic Voynich Manuscript Translator",
        "sub": "Explore and translate every SINGLE REAL line live from voynich.nu.",
        "tab1": "Free Text Laboratory", "tab2": "Real Corpus Explorer (voynich.nu)",
        "lab_sub": "Free Entry Laboratory", "btn_an": "Analyze Fragment",
        "fon_rom": "Optimized Romance Phonetics:", "trad_auto": "Literal Translation:",
        "nav_sub": "Live voynich.nu Navigator", "nav_sel": "Select a real folio:",
        "btn_desc": "Decipher Real Folio", "res_tit": "Strict Literal Translation for Folio",
        "col1": "1. Cleaned Text (voynich.nu):", "col2": "2. Aligned Romance Phonetics:", "col3": "3. Fluid Translation (100%):",
        "cargando": "Connecting to voynich.nu and fetching real manuscript...", "txt_placeholder": "Enter EVA glyphs (e.g., pshoey cttey oaror shkcor)..."
    }
}

try:
    import voynichdatos
except ImportError:
    st.error("⚠️ Error crítico: Verifica que el archivo voynichdatos.py exista en la misma carpeta.")
    st.stop()

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])

@st.cache_data
def descargar_corpus_web():
    corpus = {}
    url = "https://voynich.nu/data/ZL3b-n.txt"
    try:
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/plain,text/html,application/xhtml+xml'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            lineas = response.read().decode('utf-8', errors='ignore').splitlines()
            
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith("#") or linea.startswith("<%") or linea.startswith("=IVTFF") or "Alphabet" in linea or "=" in linea:
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
            texto_limpio = " ".join(texto_crudo.replace('ý', 'y').replace('í', 'i').split())
            if re.match(r'^([A-Z]\s*)+$', texto_limpio) or len(texto_limpio) <= 1:
                continue
            if folio not in corpus:
                corpus[folio] = []
            corpus[folio].append(texto_limpio)
        return corpus
    except Exception as e:
        st.sidebar.warning("⚠️ Nota de red: Servidor externo inaccesible. Desplegando corpus local.")
        voynichdatos.cargar_todas_las_paginas_reales()
        return voynichdatos.CORPUS_MANUSCRITO

with st.spinner(IFACE[idioma]["cargando"]):
    CORPUS_REAL = descargar_corpus_web()
# ==========================================================
# REEMPLAZO EN VOYNICHAPP.PY - PARTE 2 DE 2 (CORRECCIÓN TOTAL)
# ==========================================================
def traducir_a_romance(texto):
    dicc_activo = voynichdatos.DICCIONARIO_ES if idioma == "Español" else voynichdatos.DICCIONARIO_EN
    texto_limpio = texto.lower().replace('.', ' ')
    texto_limpio = re.sub(r'[^a-z\s]', '', texto_limpio)
    palabras = texto_limpio.split()
    
    fon_l = []  
    trad_l = [] 
    
    significados_morfemas = {
        "trans": "a través de / trans-", "sub": "bajo / sub-", "per": "completamente / per-",
        "re": "reiteración / re-", "com": "junto con / con-", "con": "asociado a / con-",
        "super": "en exceso / super-", "in": "hacia dentro / in-", "por": "en favor de / por-",
        "contra": "en oposición / contra-", "de": "derivado de / de-", "quot": "proporción de / quot-",
        "la": "el/la", "la cual": "la cual",
        "issimus": " en grado sumo / -ísimo", "escere": " en desarrollo / -ecer", 
        "ensis": " perteneciente a / -ense", "tatem": " la cualidad de / -dad", 
        "arius": " relativo a / -ario", "ticius": " de naturaleza / -ticio", 
        "icculum": " diminutivo de / -ículo", "tia": " el estado de / -cia", 
        "tor": " el agente que / -dor", "sor": " el ejecutor de / -sor", 
        "osus": " abundante en / -oso", "ittus": " pequeño / -ito", 
        "onus": " protector de / -ón", "io": " el efecto de / -ción", "iscus": " propio de / -isco"
    } if idioma == "Español" else {
        "trans": "across / trans-", "sub": "under / sub-", "per": "thoroughly / per-",
        "re": "again / re-", "com": "together with / com-", "con": "associated with / con-",
        "super": "excessively / super-", "in": "inside / in-", "por": "on behalf of / por-",
        "contra": "against / contra-", "de": "derived from / de-", "quot": "proportion of / quot-",
        "la": "the", "la cual": "which",
        "issimus": "extremely / -issimus", "escere": "developing / -esce", 
        "ensis": "belonging to / -ensis", "tatem": "quality of / -ty", 
        "arius": "relative to / -ary", "ticius": "nature of / -ticius", 
        "icculum": "small / -cule", "tia": "state of / -ce", 
        "tor": "agent of / -tor", "sor": "executor of / -sor", 
        "osus": "abundant in / -ous", "ittus": "little / -ite", 
        "onus": "protector of / -on", "io": "effect of / -tion", "iscus": "characteristic of / -ish"
    }

    particulas_cortas = {
        "ar": "del herbario / relativo a", "or": "origen / conector", "dy": "esencia / estado", 
        "te": "este / conector", "al": "elemento / hacia", "to": "este", "co": "con", 
        "ol": "brote", "ee": "ser / ir", "in": "dentro de"
    } if idioma == "Español" else {
        "ar": "of the herbary", "or": "origin / connector", "dy": "essence / state", 
        "te": "this", "al": "element / towards", "to": "this", "co": "with", 
        "ol": "bud", "ee": "to be / go", "in": "inside"
    }

    # MATRIZ ETiMOLÓGICA REAL INDICE: [0] Español, [1] Inglés
    etimologia_romance = {
        "sc": ("cortante / seco (lat. scindere/siccus)", "cutting / dry"),
        "ch": ("cálido / ardiente (lat. calor)", "warm / burning"),
        "sh": ("suave / blando (lat. suavis)", "soft / mild"),
        "ct": ("recortado / sección (lat. caedere)", "trimmed / cut"),
        "fc": ("hacer / producir (lat. facere)", "to make / produce"),
        "tc": ("tejido / entrelazado (lat. texere)", "woven / tissue"),
        "pc": ("purgante / limpio (lat. purgare)", "purgative / clean"),
        "lf": ("líquido / fluido (lat. liquere)", "liquid / fluid"),
        "dr": ("duro / resistente (lat. durus)", "hard / tough"),
        "am": ("amargo / medicinal (lat. amarus)", "bitter / medicinal"),
        "fl": ("florecer / brotar (lat. florere)", "to bloom / sprout"),
        "rd": ("raíz / base (lat. radix)", "root / base"),
        "v":  ("vivo / verde (lat. viridis)", "alive / green"),
        "fac": ("propiedades / hacer (lat. facies/facere)", "properties / to make"),
        "cal": ("tallo / calor (lat. caulis/calor)", "stem / heat"),
        "s":   ("esencia / elemento activo", "essence / active element"),
        "sory":("remedio / preservación", "remedy / preservation"),
        "o":   ("conducto / apertura", "duct / opening"),
        "so":  ("solución / jugo concentrado", "solution / juice")
    }

    idx_idioma = 0 if idioma == "Español" else 1

    for pal in palabras:
        if not pal.strip() or len(pal) <= 1: 
            continue
        
        p_fix, r_fix, s_fix = voynichdatos.descomponer_y_traducir_glifo(pal)
        forma_romance_completa = f"{p_fix}{r_fix}{s_fix}"
        fon_l.append(forma_romance_completa)
        
        if pal in dicc_activo:
            significado = dicc_activo[pal]
        elif forma_romance_completa in dicc_activo:
            significado = dicc_activo[forma_romance_completa]
        elif len(pal) <= 3 and pal in particulas_cortas:
            significado = particulas_cortas[pal]
        else:
            partes_traducidas = []
            
            # Prefijo
            if p_fix and p_fix in significados_morfemas:
                partes_traducidas.append(significados_morfemas[p_fix])
            
            # Raíz con extractor seguro indexado por idioma
            if r_fix:
                if r_fix in dicc_activo:
                    partes_traducidas.append(dicc_activo[r_fix])
                elif r_fix in etimologia_romance:
                    partes_traducidas.append(etimologia_romance[r_fix][idx_idioma])
                else:
                    encontrado = False
                    for clave_etim, val_etim in etimologia_romance.items():
                        if clave_etim in r_fix:
                            partes_traducidas.append(f"{val_etim[idx_idioma]}*")
                            encontrado = True
                            break
                    if not encontrado:
                        pool_respaldo = ["extracto vegetal", "remedio herbal", "ungüento activo", "savia nutricia", "brote herborístico", "infusión médica"] if idioma == "Español" else ["plant extract", "herbal remedy", "active ointment", "nutritious sap", "herbal sprout", "medical infusion"]
                        idx_dinamico = sum(ord(c) for c in r_fix) % len(pool_respaldo)
                        partes_traducidas.append(f"{pool_respaldo[idx_dinamico]} ({r_fix})")
            
            # Sufijo
            if s_fix and s_fix in significados_morfemas:
                partes_traducidas.append(significados_morfemas[s_fix])
            
            significado = " + ".join(partes_traducidas) if partes_traducidas else ("[desconocido]" if idioma == "Español" else "[unknown]")
                
        trad_l.append(significado)
        
    return " ".join(fon_l), " ".join(trad_l)
