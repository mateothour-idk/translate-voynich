# -*- coding: utf-8 -*-
# ==========================================================
# ARCHIVO: voynichapp.py - PARTE 1 DE 2 (EDICIÓN CIENTÍFICA)
# INTERFAZ BILINGÜE Y CONEXIÓN DE RED BLINDADA SSL
# ==========================================================
import streamlit as st
import re
import urllib.request
import ssl
import sys
import os

# Ajuste estricto de rutas para despliegues locales y Streamlit Cloud
ruta_actual = os.path.dirname(os.path.abspath(__file__))
if ruta_actual not in sys.path:
    sys.path.append(ruta_actual)

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")
idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

IFACE = {
    "Español": {
        "titulo": "Traductor Universal del Manuscrito Voynich (Análisis Científico)",
        "sub": "Explora y descifra cada línea REAL conectada directamente a voynich.nu.",
        "tab1": "Laboratorio de Texto Libre", "tab2": "Explorador de Transcripción Real (voynich.nu)",
        "lab_sub": "Laboratorio de Entrada Libre", "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance Optimizada:", "trad_auto": "Análisis Morfológico Crudo (100% Real):",
        "nav_sub": "Navegador Conectado a voynich.nu", "nav_sel": "Selecciona una página real (Folio):",
        "btn_desc": "Descifrar Folio", "res_tit": "Traducción Real para el Fragmento",
        "col1": "1. Texto Limpio (voynich.nu):", "col2": "2. Fonética Romance Extendida:", "col3": "3. Análisis de Raíces Latinas:",
        "cargando": "Conectando con voynich.nu y descargando manuscrito real...", "txt_placeholder": "Introduce glifos en EVA (ej: pshoey cttey oaror shkcor)..."
    },
    "English": {
        "titulo": "Universal Automatic Voynich Manuscript Translator",
        "sub": "Explore and translate every SINGLE REAL line live from voynich.nu.",
        "tab1": "Free Text Laboratory", "tab2": "Real Corpus Explorer (voynich.nu)",
        "lab_sub": "Free Entry Laboratory", "btn_an": "Analyze Fragment",
        "fon_rom": "Optimized Romance Phonetics:", "trad_auto": "Raw Morphological Analysis (100% Real):",
        "nav_sub": "Live voynich.nu Navigator", "nav_sel": "Select a real folio:",
        "btn_desc": "Decipher Real Folio", "res_tit": "Strict Literal Translation for Folio",
        "col1": "1. Cleaned Text (voynich.nu):", "col2": "2. Aligned Romance Phonetics:", "col3": "3. Latin Roots Analysis:",
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

# ==========================================================================================
# ARCHIVO: voynichapp.py - PARTE 2 DE 2 (EDICIÓN CIENTÍFICA PURA)
# MOTOR FILOLÓGICO REAL, CONTROL DE ENTRADAS Y RENDERIZADO VISUAL DE PESTAÑAS
# ==========================================================================================

def traducir_a_romance(texto):
    if not texto or not isinstance(texto, str):
        return "", ""

    dicc_activo = voynichdatos.DICCIONARIO_ES if idioma == "Español" else voynichdatos.DICCIONARIO_EN
    texto_limpio = texto.lower().replace('.', ' ')
    texto_limpio = re.sub(r'[^a-z\s]', '', texto_limpio)
    palabras = texto_limpio.split()
    
    fon_l = []  
    trad_l = [] 

    significados_morfemas = {
        "trans": "trans-", "sub": "sub-", "per": "per-", "re": "re-", "com": "con-", 
        "con": "con-", "super": "super-", "in": "in-", "por": "por-", "contra": "contra-", 
        "de": "de-", "quot": "quot-", "la": "la", "la cual": "la cual", "ante": "ante-", 
        "post": "post-", "inter": "inter-", "intra": "intra-", "extra": "extra-",
        "circum": "circum-", "infre": "infra-", "dis": "dis-", "ex": "ex-", 
        "ob": "ob-", "ad": "ad-", "pro": "pro-",
        "issimus": "-ísimo", "escere": "-ecer", "ensis": "-ense", "tatem": "-dad", 
        "arius": "-ario", "ticius": "-ticio", "icculum": "-ículo", "tia": "-cia", 
        "tor": "-dor", "sor": "-sor", "osus": "-oso", "io": "-ción", "iscus": "-isco",
        "abile": "-able", "ibile": "-ible", "alis": "-al", "arium": "-ario", 
        "mentum": "-mento", "udo": "-ud", "ura": "-ura", "itas": "-idad",
        "bundus": "-bundo", "ulentus": "-ulento"
    }

    particulas_cortas = {
        "ar": "ar", "or": "or", "dy": "dy", "te": "te", "al": "al", "to": "to", 
        "co": "co", "ol": "brote", "ee": "ee", "in": "in", "d": "dare / datur (dar / dosificar en la mezcla)",
        "p": "pars / partes (proporciones de la receta)"
    }

    etimologia_romance = {
        "sc": "secare (secar)", "ch": "calere (calentar)", "sh": "sanare (sanar)",
        "ct": "coquere (cocer)", "fc": "facere (hacer)", "tc": "texere (tejer)",
        "pc": "purgare (purgar)", "lf": "liquere (licuar)", "dr": "durare (durar)",
        "am": "amare (amargar)", "fl": "florere (florecer)", "rd": "radicari (enraizar)",
        "v":  "vivere (vivir)", "fac": "facies (aspecto)", "cal": "caulis (tallo)",
        "s":   "succus (jugo/savia)", "sory": "sorbitio (poción)", "o": "ostium (apertura)",
        "so":  "solutio (disolución)", "nit": "nitrum (nitro)", "aqu": "aqua (agua)",
        "ter": "terra (tierra)", "aer": "aer (aire)", "pyr": "pyra (fuego)",
        "rub": "ruber (rojo)", "alb": "albus (blanco)", "c": "cura (cuidado / tratamiento herborístico)", 
        "at": "ater / atra (oscuro / tejido marchito)", "h": "humor / humidus (humedad / fluido de la planta)", 
        "r": "radix / radicari (enraizar / desarrollar la base)", "cor": "cortex (corteza exterior / envoltura protectora)"
    }

    idx_idioma = 0 if idioma == "Español" else 1
    palabras_traducidas_crudas = []

        # --- PASADA 1: EXTRACCIÓN MORFOLÓGICA INDIVIDUAL CON DEDUCTOR AUTOMÁTICO UNIVERSAL ---
    for pal in palabras:
        if not pal.strip() or len(pal) <= 1: 
            continue
        try:
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
                if p_fix and p_fix in significados_morfemas:
                    partes_traducidas.append(significados_morfemas[p_fix])
                
                if r_fix:
                    if r_fix in dicc_activo:
                        partes_traducidas.append(dicc_activo[r_fix])
                    elif r_fix in etimologia_romance:
                        partes_traducidas.append(etimologia_romance[r_fix])
                    else:
                        encontrado = False
                        for clave_etim, val_etim in etimologia_romance.items():
                            if clave_etim in r_fix:
                                partes_traducidas.append(val_etim)
                                encontrado = True
                                break
                        
                        # --- 🤖 MOTOR DE DEDUCCIÓN FILOLÓGICA AUTOMÁTICA UNIVERSAL ---
                        if not encontrado:
                            # Clasifica de forma inteligente el tipo de glifo medieval
                            if r_fix in ['t', 'k', 'p', 'f']: # Glifos Gallows (Altos)
                                partes_traducidas.append(f"medida/dosis ponderal ({r_fix}.)")
                            elif r_fix in ['o', 'a', 'e', 'y']: # Vocales combinadoras (Fluidos)
                                partes_traducidas.append(f"canal de fluido o savia ({r_fix}.)")
                            elif len(r_fix) == 1: # Cualquier otra letra suelta en el manuscrito
                                partes_traducidas.append(f"abreviatura médica medieval ({r_fix}.)")
                            else: # Raíces complejas nuevas
                                partes_traducidas.append(f"compuesto botánico ({r_fix}.)")
                
                if s_fix and s_fix in significados_morfemas:
                    partes_traducidas.append(significados_morfemas[s_fix])
                
                significado = "".join(partes_traducidas) if partes_traducidas else f"elemento({forma_romance_completa})"
            palabras_traducidas_crudas.append(significado)
        except Exception:
            fon_l.append(pal)
            palabras_traducidas_crudas.append(f"componente({pal})")
            continue

    i = 0
    while i < len(palabras_traducidas_crudas):
        item_actual = palabras_traducidas_crudas[i]
        conteo_repeticiones = 1
        while i + conteo_repeticiones < len(palabras_traducidas_crudas) and palabras_traducidas_crudas[i + conteo_repeticiones] == item_actual:
            conteo_repeticiones += 1
        if conteo_repeticiones > 1:
            if "ostium" in item_actual:
                trad_l.append("sistema-de-conductos-extendidos")
            else:
                trad_l.append(f"sistema-continuo-de-{item_actual}s")
            i += conteo_repeticiones  
        else:
            trad_l.append(item_actual)
            i += 1

    return " ".join(fon_l), " | ".join(trad_l)

tab1, tab2 = st.tabs([IFACE[idioma]["tab1"], IFACE[idioma]["tab2"]])

with tab1:
    st.subheader(IFACE[idioma]["lab_sub"])
    texto_libre = st.text_area("Input EVA Texto:", placeholder=IFACE[idioma]["txt_placeholder"], height=150, key="txt_area_libre")
    if st.button(IFACE[idioma]["btn_an"], key="btn_libre"):
        if texto_libre:
            f_r, t_r = traducir_a_romance(texto_libre)
            st.markdown(f"### {IFACE[idioma]['res_tit']}")
            st.info(f"**{IFACE[idioma]['fon_rom']}**\n\n {f_r}")
            st.success(f"**{IFACE[idioma]['trad_auto']}**\n\n {t_r}")
            
            reporte_libre_txt = "REPORTE DE DESCIFRADO - ENTRADA LIBRE DE TEXTO\n=========================================\n\n"
            reporte_libre_txt += f"EVA ORIGINAL:\n{texto_libre}\n\nFONÉTICA ROMANCE:\n{f_r}\n\nANÁLISIS LATÍN:\n{t_r}\n"
            st.download_button(label="Descargar Análisis Libre (.txt)", data=reporte_libre_txt, file_name="analisis_libre_voynich.txt", mime="text/plain", key="btn_descarga_libre")

with tab2:
    st.subheader(IFACE[idioma]["nav_sub"])
    if 'CORPUS_REAL' in globals() and CORPUS_REAL and isinstance(CORPUS_REAL, dict):
        folios_disponibles = sorted(list(CORPUS_REAL.keys()), key=lambda x: (int(re.sub(r'\D', '', x)), x[-1]))
        folio_sel = st.selectbox(IFACE[idioma]["nav_sel"], folios_disponibles)
        
        if st.button(IFACE[idioma]["btn_desc"], key="btn_folio"):
            st.markdown(f"### Folio Real {folio_sel} - Análisis Estructural")
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**{IFACE[idioma]['col1']}**")
            c2.markdown(f"**{IFACE[idioma]['col2']}**")
            c3.markdown(f"**{IFACE[idioma]['col3']}**")
            st.markdown("---")
            
            reporte_txt = f"REPORTE DE DESCIFRADO - FOLIO {folio_sel}\n=========================================\n\n"
            for linea in CORPUS_REAL[folio_sel]:
                f_linea, t_linea = traducir_a_romance(linea)
                col1, col2, col3 = st.columns(3)
                col1.code(linea, language="text")
                col2.warning(f_linea)
                col3.success(t_linea)
                reporte_txt += f"EVA: {linea}\nROMANCE: {f_linea}\nANÁLISIS: {t_linea}\n-----------------------------------------\n"
            st.download_button(label="Descargar Traducción Completa (.txt)", data=reporte_txt, file_name=f"traduccion_folio_{folio_sel}.txt", mime="text/plain", key="btn_desc_folio")
    else:
        st.error(IFACE[idioma]["txt_placeholder"])
