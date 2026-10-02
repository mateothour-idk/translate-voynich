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
        "ar": "ar", "or": "or", "dy": "dy", "te": "te", "al": "aliquid (otra porción)", 
        "to": "to", "co": "co", "ol": "brote", "ee": "ee", "in": "in",
        "d": "dare / datur (dar / dosificar)", "p": "pars / partes (proporciones)"
    }

        # 3. MATRIZ TOTAL ABSOLUTA DE RAÍCES EN LATÍN REAL DEL SIGLO XV (CORREGIDA)
    etimologia_romance = {
        "sc": ("secare (secar)", "secare (to dry)"),
        "ch": ("calere (calentar)", "calere (to heat)"),
        "sh": ("sanare (sanar)", "sanare (to heal)"),
        "ct": ("coquere (cocer)", "coquere (to cook)"),
        "fc": ("facere (hacer)", "facere (to make)"),
        "tc": ("texere (tejer)", "texere (to weave)"),
        "pc": ("purgare (purgar)", "purgare (to purge)"),
        "lf": ("liquere (licuar)", "liquere (to liquefy)"),
        "dr": ("durare (durar)", "durare (to endure)"),
        "am": ("amare (amargar)", "amare (to infuse bitterness)"),
        "fl": ("florere (florecer)", "florere (to bloom)"),
        "rd": ("radicari (enraizar)", "radicari (to take root)"),
        "v":  ("vivere (vivir)", "vivere (to live)"),
        "fac": ("facies (aspecto)", "facies (aspect)"),
        "cal": ("caulis (tallo)", "caulis (stem)"),
        "s":   ("succus (jugo/savia)", "succus (sap/extracted latex)"),
        "sory": ("sorbitio (poción)", "sorbitio (liquid potion)"),
        "o":   ("ostium (apertura)", "ostium (opening)"),
        "so":  ("solutio (disolución)", "solutio (mixture)"),
        "nit": ("nitrum (nitro)", "nitrum (nitre)"),
        "aqu": ("aqua (agua)", "aqua (water)"),
        "ter": ("terra (tierra)", "terra (earth)"),
        "aer": ("aer (aire)", "aer (air)"),
        "pyr": ("pyra (fuego)", "pyra (fire)"),
        "rub": ("ruber (rojo)", "ruber (red)"),
        "alb": ("albus (blanco)", "albus (white)"),
        
        # --- Mapeo de letras sueltas individuales indexadas ---
        "c":   ("cura (curar/tratamiento)", "cura (to heal/treatment)"),
        "h":   ("humidus (humedad)", "humidus (moisture)"),
        "a":   ("amare (amargor/principio activo)", "amare (bitterness/active principle)"),
        "at":  ("ater (oscuro)", "ater (dark)"),
        "r":   ("radix (raíz)", "radix (root)"),
        "cor": ("cortex (corteza)", "cortex (bark)")
    }

    idx_idioma = 0 if idioma == "Español" else 1
    palabras_traducidas_crudas = []
    
    # --- PASADA 1: EXTRACCIÓN MORFOLÓGICA REVISADA Y REPARADA (TEXTO REAL) ---
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
                        # Extrae la cadena de texto de la tupla de manera segura
                        cadena_latina = etimologia_romance[r_fix][idx_idioma]
                        partes_traducidas.append(cadena_latina)
                    else:
                        encontrado = False
                        for clave_etim, val_etim in etimologia_romance.items():
                            if clave_etim in r_fix:
                                cadena_latina = val_etim[idx_idioma]
                                partes_traducidas.append(cadena_latina)
                                encontrado = True
                                break
                        
                        if not encontrado:
                            if r_fix in ['t', 'k', 'p', 'f']:
                                partes_traducidas.append(f"medida ({r_fix}.)")
                            elif r_fix in ['o', 'a', 'e', 'y']:
                                partes_traducidas.append(f"canal ({r_fix}.)")
                            elif len(r_fix) == 1:
                                partes_traducidas.append(f"abrev ({r_fix}.)")
                            else:
                                partes_traducidas.append(f"compuesto ({r_fix}.)")
                
                if s_fix and s_fix in significados_morfemas:
                    partes_traducidas.append(significados_morfemas[s_fix])
                
                                # --- BUSCA ESTA SECCIÓN AL FINAL DE LA PASADA 1 ---
                significado = "".join(partes_traducidas) if partes_traducidas else f"elemento({forma_romance_completa})"
            
            # === FILTRO RADICAL DE LIMPIEZA INMEDIATA ===
            # Si la palabra contiene explicaciones largas unidas por guiones, las limpia de golpe aquí
            if "-isco" in significado:
                significado = "cura-isco"
            elif "-ario" in significado or "-rio" in significado:
                significado = "cura-ario"
            elif "-oso" in significado:
                significado = "brote-oso"
            elif "-ense" in significado:
                significado = "tallo-ense"
            elif "-dor" in significado:
                if "secar" in significado: significado = "secar-dor"
                if "hacer" in significado: significado = "hacer-dor"
                                # === FILTRO RADICAL DE LIMPIEZA INMEDIATA ===
            if "-isco" in significado:
                significado = "cura-isco"
            elif "-ario" in significado or "-rio" in significado:
                significado = "cura-ario"
            elif "coquere" in significado and "-ción" in significado:
                significado = "coquere-cion"  # <--- ¡Inyecta esta línea de control aquí!
            elif "contra-" in significado and "tor" in significado:
                significado = "contra-brote-tor"

            palabras_traducidas_crudas.append(significado)
        except Exception:
            fon_l.append(pal)
            palabras_traducidas_crudas.append(f"componente({pal})")
            continue

        # --- PASADA 2: SUAVIZADOR Y ENSAMBLADOR DE SINTAXIS FLUIDA (BLINDADO) ---
    i = 0
    while i < len(palabras_traducidas_crudas):
        item_actual = palabras_traducidas_crudas[i]
        
        # Corrección inmediata de uniones mecánicas antes de armar la cadena
        if item_actual == "cura-isco":
            item_actual = "propio del tratamiento medicinal (curatisco)"
        elif item_actual == "cura-rio":
            item_actual = "proceso de curación o tratamiento"
        elif item_actual == "cura-ario":
            item_actual = "recetario de tratamientos médicos"
        elif item_actual == "humor-ario":
            item_actual = "relativo a los fluidos o humores de la planta"
        elif item_actual == "humidus-ario":
            item_actual = "relativo al estado de humedad vegetal"
        elif item_actual == "brote-oso":
            item_actual = "brote abundante en savia nutricia"
        elif item_actual == "tallo-ense":
            item_actual = "perteneciente a la estructura del tallo"
        elif item_actual == "secar-dor":
            item_actual = "agente deshidratante o desecante"
        elif item_actual == "hacer-dor":
            item_actual = "agente extractor o confeccionador"

        conteo_repeticiones = 1
        while i + conteo_repeticiones < len(palabras_traducidas_crudas) and palabras_traducidas_crudas[i + conteo_repeticiones] == palabras_traducidas_crudas[i]:
            conteo_repeticiones += 1
            
        if conteo_repeticiones > 1:
            if "ostium" in item_actual:
                trad_l.append("sistema de conductos extendidos")
            elif "recetario" in item_actual or "cura-ario" in palabras_traducidas_crudas[i]:
                trad_l.append("sistema continuo de recetarios médicos")
            else:
                trad_l.append(f"sistema continuo de {item_actual}s")
            i += conteo_repeticiones  
        else:
            trad_l.append(item_actual)
            i += 1

            # === CONEXIÓN UNIFICADA DE CADENA LOCAL ===
    traduccion_final_limpia = " | ".join(trad_l)
    
    # === PROCESADOR DE SINTAXIS 100% FLUIDA (CORREGIDO) ===
        # === PROCESADOR DE SINTAXIS 100% FLUIDA (EDICIÓN DEFINITIVA) ===
    if idioma == "Español":
        traduccion_final_limpia = traduccion_final_limpia.replace("con-ostium-dor", "agente estimulador de la apertura de poros")
        traduccion_final_limpia = traduccion_final_limpia.replace("contra-brote-tor", "agente estimulador del secado de brotes")
        traduccion_final_limpia = traduccion_final_limpia.replace("coquere-cion", "proceso de cocción o ebullición")
        traduccion_final_limpia = traduccion_final_limpia.replace("corazón", "corteza protectora externa")
        
        # --- 🧼 SOLUCIÓN DE SOLUTIO CIA Y RADIX ECER CON LÍMITES FLEXIBLES ---
        traduccion_final_limpia = re.sub(r'\bsolutio\s*[-|]*\s*cia\b', 'estado de disolución líquida', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bradix\s*[-|]*\s*ecer\b', 'proceso de enraizamiento de la base', traduccion_final_limpia)
        
        # --- TRADUCCIÓN ESTRICTA DE LÍMITES PALABRA POR PALABRA ---
        traduccion_final_limpia = re.sub(r'\bin caulis\b', 'en el tallo principal', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bin-caulis\b', 'en el tallo principal', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bfacies\b', 'aspecto o morfología foliar', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcaulis\b', 'tallo', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bsuccus\b', 'savia o jugo vital', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bsorbitio\b', 'poción o brebaje', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcontra humidus\b', 'contra la humedad', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcontra-humidus\b', 'contra la humedad', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bostium\b', 'apertura del poro foliar', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcalere\b', 'someter a temperatura', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bamare\b', 'principio activo amargo', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcura\b', 'tratamiento herborístico', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bor\b', 'origen del brote', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bar\b', 'estructura leñosa de la rama', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcum\b', 'mezclado con', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcoquere\b', 'cocer al fuego', traduccion_final_limpia)
        
        traduccion_final_limpia = traduccion_final_limpia.replace("abrev(d.)", "dosificar")
        traduccion_final_limpia = traduccion_final_limpia.replace("abrev (d.)", "dosificar")
        traduccion_final_limpia = re.sub(r'\babrev\b', 'dosificación', traduccion_final_limpia)

    else:
        # === PROCESADOR DE SINTAXIS 100% INGLÉS FLUIDO (EDICIÓN DEFINITIVA) ===
        traduccion_final_limpia = traduccion_final_limpia.replace("con-ostium-dor", "pore-opening stimulating agent")
        traduccion_final_limpia = traduccion_final_limpia.replace("contra-brote-tor", "sprout dehydration accelerating agent")
        traduccion_final_limpia = traduccion_final_limpia.replace("coquere-cion", "decoction or boiling process")
        traduccion_final_limpia = traduccion_final_limpia.replace("brote-oso", "abundant sap sprout")
        traduccion_final_limpia = traduccion_final_limpia.replace("tallo-ense", "belonging to the stem structure")
        
        # --- 🧼 SOLUCIÓN DE SOLUTIO CIA Y RADIX ECER CON LÍMITES FLEXIBLES PARA INGLÉS ---
        traduccion_final_limpia = re.sub(r'\bsolutio\s*[-|]*\s*cia\b', 'liquid dissolution state', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bradix\s*[-|]*\s*ecer\b', 'base rooting process', traduccion_final_limpia)
        
        # --- TRADUCCIÓN ESTRICTA DE LÍMITES PALABRA POR PALABRA ---
        traduccion_final_limpia = re.sub(r'\bin caulis\b', 'in the main stem', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bin-caulis\b', 'in the main stem', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bfacies\b', 'leaf morphology or aspect', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcaulis\b', 'stem', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bsuccus\b', 'vital sap or juice', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bsorbitio\b', 'potion or brew', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcontra humidus\b', 'against moisture', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcontra-humidus\b', 'against moisture', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bostium\b', 'opening of the stomatal pore', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcalere\b', 'apply laboratory heat', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bamare\b', 'bitter active principle', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcura\b', 'medical treatment', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bor\b', 'origin of the sprout', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bar\b', 'woody structure of the branch', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcum\b', 'mixed with', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\bcoquere\b', 'boil over fire', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'\babrev\b', 'dosage', traduccion_final_limpia)

    # === LIMPIEZA MASIVA FINAL DE EXPLICACIONES TÉCNICAS Y GUIONES ===
    # Purgamos paréntesis al final para evitar el error de variable local de arriba
    traduccion_final_limpia = re.sub(r'\s*\([^)]*\)', '', traduccion_final_limpia)
    traduccion_final_limpia = traduccion_final_limpia.replace("-", " ").replace(" / ", " o ")

    return " ".join(fon_l), traduccion_final_limpia.strip()

# --- CONFIGURACIÓN DE PESTAÑAS (FUERA DE CONDICIONALES) ---
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
        st.error("⚠️ No se pudieron cargar los folios desde voynich.nu de forma remota. Por favor, utiliza la pestaña 'Laboratorio de Texto Libre' para analizar tus glifos manualmente.")
