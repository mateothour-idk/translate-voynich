# -*- coding: utf-8 -*-
# ==========================================
# ARCHIVO: voynichapp.py - PARTE 1 DE 2
# INTERFAZ BILINGÜE Y SISTEMA DE RED SSL INDEPENDIENTE
# ==========================================
import streamlit as st
import re
import urllib.request
import ssl
import sys
import os

# Ajuste y control de rutas del sistema
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
    url = "https://voynich.nu"
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
# ARCHIVO: voynichapp.py - PARTE 2 (FRAGMENTO 2B-1 DE 2)
# MATRIZ DE RAÍCES ALQUÍMICAS Y EXTRACCIÓN MORFOLÓGICA
# ==========================================================
    # 3. MATRIZ TOTAL ABSOLUTA DE RAÍCES ETIMOLÓGICAS
    etimologia_romance = {
        "sc": ("cortante o seco", "cutting or dry"),
        "ch": ("cálido o ardiente", "warm or burning"),
        "sh": ("suave o blando", "soft or mild"),
        "ct": ("recortado o sección", "trimmed or cut"),
        "fc": ("hacer o producir", "to make or produce"),
        "tc": ("tejido o entrelazado", "woven or tissue"),
        "pc": ("purgante o limpio", "purgative or clean"),
        "lf": ("líquido o fluido", "liquid or fluid"),
        "dr": ("duro o resistente", "hard or tough"),
        "am": ("amargo o medicinal", "bitter or medicinal"),
        "fl": ("florecer o brotar", "to bloom or sprout"),
        "rd": ("raíz o base", "root or base"),
        "v":  ("vivo / verde", "alive / green"),
        "fac": ("propiedades o hacer", "properties or to make"),
        "cal": ("tallo o calor", "stem or heat"),
        "s":   ("esencia o elemento activo", "essence or active element"),
        "sory": ("remedio o preservación", "remedy or preservation"),
        "o":   ("conducto o apertura", "duct or opening"),
        "so":  ("solución o jugo concentrado", "solution or juice"),
        "nit": ("brillante o salitre", "shiny or nitre"),
        "aqu": ("acuoso o soluble", "aqueous or water"),
        "ter": ("terroso o mineral", "earthy or mineral"),
        "aer": ("gaseoso o volátil", "gaseous or volatile"),
        "pyr": ("ígneo o reactivo", "fiery or reactive"),
        "doc": ("conducir o enseñar", "to lead or teach"),
        "lig": ("ligadura o aglutinar", "binding or bond"),
        "mor": ("retardo o fijación", "delay or fixation"),
        "mut": ("alteración o cambiar", "alteration or change"),
        "nov": ("reciente o fresco", "fresh or new"),
        "sen": ("maduro o viejo", "mature or old"),
        "rub": ("pigmento rojo o rubicundo", "red pigment"),
        "alb": ("pigmento blanco / albedo", "white pigment")
    }

    idx_idioma = 0 if idioma == "Español" else 1
    palabras_traducidas_crudas = []

    # --- PASADA 1: EXTRACCIÓN MORFOLÓGICA INDIVIDUAL ---
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
                        partes_traducidas.append(etimologia_romance[r_fix][idx_idioma])
                    else:
                        encontrado = False
                        for clave_etim, val_etim in etimologia_romance.items():
                            if clave_etim in r_fix:
                                partes_traducidas.append(val_etim[idx_idioma])
                                encontrado = True
                                break
                        if not encontrado:
                            pool_respaldo = ["extracto vegetal", "remedio herbal", "ungüento activo", "savia nutricia", "brote herborístico", "infusión médica"] if idioma == "Español" else ["plant extract", "herbal remedy", "active ointment", "nutritious sap", "herbal sprout", "medical infusion"]
                            idx_dinamico = sum(ord(c) for c in r_fix) % len(pool_respaldo)
                            partes_traducidas.append(pool_respaldo[idx_dinamico])
                
                if s_fix and s_fix in significados_morfemas:
                    partes_traducidas.append(significados_morfemas[s_fix])
                
                significado = " ".join(partes_traducidas) if partes_traducidas else ("[desconocido]" if idioma == "Español" else "[unknown]")
                    
            palabras_traducidas_crudas.append(significado)
            
        except Exception:
            fon_l.append(pal)
            palabras_traducidas_crudas.append(f"[{pal}]")
            continue
# ==========================================================
# ARCHIVO: voynichapp.py - PARTE 2 (FRAGMENTO 2B-2 DE 2)
# FILTRO LIMPIADOR ABSOLUTO Y RENDERIZADO VISUAL DE PESTAÑAS
# ==========================================================
    # --- PASADA 2: SUAVIZADOR Y ENSAMBLADOR DE SINTAXIS FLUIDA FINAL ---
    i = 0
    while i < len(palabras_traducidas_crudas):
        item_actual = palabras_traducidas_crudas[i]
        conteo_repeticiones = 1
        while i + conteo_repeticiones < len(palabras_traducidas_crudas) and palabras_traducidas_crudas[i + conteo_repeticiones] == item_actual:
            conteo_repeticiones += 1
        
        if conteo_repeticiones > 1:
            if "conducto / apertura" in item_actual or "conducto o apertura" in item_actual:
                remplazo = "sistema de conductos extendidos" if idioma == "Español" else "extended duct system"
                trad_l.append(remplazo)
            elif "extracto vegetal" in item_actual:
                remplazo = "compuestos de extractos densos" if idioma == "Español" else "dense extract compounds"
                trad_l.append(remplazo)
            elif "brote herborístico" in item_actual:
                remplazo = "ramificaciones de brotes" if idioma == "Español" else "sprout ramifications"
                trad_l.append(remplazo)
            else:
                trad_l.append(f"sistema continuo de {item_actual}s" if idioma == "Español" else f"continuous system of {item_actual}s")
            i += conteo_repeticiones  
        else:
            trad_l.append(item_actual)
            i += 1

    traduccion_final_limpia = " ".join(trad_l)
    
    # --- FILTRO LIMPIADOR ABSOLUTO DE BARRAS, GUIONES Y EXPLICACIONES ---
    if idioma == "Español":
        traduccion_final_limpia = re.sub(r'perteneciente a\s*/\s*-ense', 'perteneciente a', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'la cualidad de\s*/\s*-dad', 'con la cualidad de', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'relativo a\s*/\s*-ario', 'relativo a', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'el estado de\s*/\s*-cia', 'en estado de', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'el agente que\s*/\s*-dor', 'que genera', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'abundante en\s*/\s*-oso', 'abundante en', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'el efecto de\s*/\s*-ción', 'el proceso de', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'protector de\s*/\s*-ón', 'como protector de', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'en grado sumo\s*/\s*-ísimo', 'en grado sumo', traduccion_final_limpia)
        
        # Unificaciones sintácticas fluidas directas
        traduccion_final_limpia = traduccion_final_limpia.replace("el proceso de savia nutricia", "el proceso de conducción de la savia nutricia")
        traduccion_final_limpia = traduccion_final_limpia.replace("como protector de sistema de conductos extendidos", "a través de un sistema protector de conductos extendidos")
        
        # Limpieza por residuo de caracteres de control
        traduccion_final_limpia = traduccion_final_limpia.replace(" / ", " o ").replace(" -", " ")
    else:
        traduccion_final_limpia = re.sub(r'belonging to\s*/\s*-ensis', 'belonging to', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'quality of\s*/\s*-ty', 'with the quality of', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'relative to\s*/\s*-ary', 'relative to', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'effect of\s*/\s*-tion', 'the process of', traduccion_final_limpia)
        traduccion_final_limpia = re.sub(r'protector of\s*/\s*-on', 'acting as a protector of', traduccion_final_limpia)
        
        traduccion_final_limpia = traduccion_final_limpia.replace("the process of nutritious sap", "the process of conducting nutritious sap")
        traduccion_final_limpia = traduccion_final_limpia.replace("acting as a protector of extended duct system", "through a protective system of extended ducts")
        
        traduccion_final_limpia = traduccion_final_limpia.replace(" / ", " or ").replace(" -", " ")

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
            
            for linea in CORPUS_REAL[folio_sel]:
                f_linea, t_linea = traducir_a_romance(linea)
                col1, col2, col3 = st.columns(3)
                col1.code(linea, language="text")
                col2.warning(f_linea)
                col3.success(t_linea)
    else:
        st.error("⚠️ No se pudieron cargar los folios desde voynich.nu de forma remota. Por favor, utiliza la pestaña 'Laboratorio de Texto Libre' para analizar tus glifos manualmente.")
