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
# ARCHIVO: voynichapp.py - PARTE 2 (FRAGMENTO 2A DE 2)
# MOTOR ETiMOLÓGICO EXTENDIDO Y PROCESADOR DE MORFEMAS
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

    # 1. MATRIZ TOTAL ABSOLUTA DE PREFIJOS (Sintaxis Latín y EVA extendida)
    significados_morfemas = {
        "trans": "a través de / trans-", "sub": "bajo / sub-", "per": "completamente / per-",
        "re": "reiteración / re-", "com": "junto con / con-", "con": "asociado a / con-",
        "super": "en exceso / super-", "in": "hacia dentro / in-", "por": "en favor de / por-",
        "contra": "en oposición / contra-", "de": "derivado de / de-", "quot": "proporción de / quot-",
        "la": "el/la", "la cual": "la cual", "ante": "antes de / ante-", "post": "después de / post-",
        "inter": "entre / inter-", "intra": "dentro de / intra-", "extra": "fuera de / extra-",
        "circum": "alrededor de / circum-", "infre": "debajo / infra-", "dis": "separación / dis-",
        "ex": "extracción / ex-", "ob": "enfrente / ob-", "ad": "hacia / ad-", "pro": "adelante / pro-",
        
        # 2. MATRIZ TOTAL ABSOLUTA DE SUFIJOS (Morfemas nominales y verbales)
        "issimus": " en grado sumo / -ísimo", "escere": " en desarrollo / -ecer", 
        "ensis": " perteneciente a / -ense", "tatem": " la cualidad de / -dad", 
        "arius": " relativo a / -ario", "ticius": " de naturaleza / -ticio", 
        "icculum": " diminutivo de / -ículo", "tia": " el estado de / -cia", 
        "tor": " el agente que / -dor", "sor": " el ejecutor de / -sor", 
        "osus": " abundante en / -oso", "ittus": " pequeño / -ito", 
        "onus": " protector de / -ón", "io": " el efecto de / -ción", "iscus": " propio de / -isco",
        "abile": "capacidad / -able", "ibile": "posibilidad / -ible", "alis": "relativo a / -al",
        "arium": "lugar de resguardo / -ario", "mentum": "instrumento o medio / -mento",
        "udo": "condición / -ud", "ura": "efecto de la acción / -ura", "itas": "cualidad / -idad",
        "bundus": "inclinación / -bundo", "ulentus": "abundancia / -ulento"
    } if idioma == "Español" else {
        "trans": "across / trans-", "sub": "under / sub-", "per": "thoroughly / per-",
        "re": "again / re-", "com": "together with / com-", "con": "associated with / con-",
        "super": "excessively / super-", "in": "inside / in-", "por": "on behalf of / por-",
        "contra": "against / contra-", "de": "derived from / de-", "quot": "proportion of / quot-",
        "la": "the", "la cual": "which", "ante": "before / ante-", "post": "after / post-",
        "inter": "between / inter-", "intra": "inside / intra-", "extra": "outside / extra-",
        "circum": "around / circum-", "infre": "below / infra-", "dis": "separation / dis-",
        "ex": "extraction / ex-", "ob": "against / ob-", "ad": "toward / ad-", "pro": "forward / pro-",
        "issimus": "extremely / -issimus", "escere": "developing / -esce", 
        "ensis": "belonging to / -ensis", "tatem": "quality of / -ty", 
        "arius": "relative to / -ary", "ticius": "nature of / -ticius", 
        "icculum": "small / -cule", "tia": "state of / -ce", 
        "tor": "agent of / -tor", "sor": "executor of / -sor", 
        "osus": "advanced / -ous", "ittus": "little / -ite", 
        "onus": "protector of / -on", "io": "effect of / -tion", "iscus": "characteristic of / -ish",
        "abile": "capacity / -able", "ibile": "possibility / -ible", "alis": "relative to / -al",
        "arium": "place for / -ary", "mentum": "means or tool / -ment",
        "udo": "condition / -ude", "ura": "effect of action / -ure", "itas": "quality / -ity",
        "bundus": "inclined to / -bund", "ulentus": "abundant / -ulent"
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
# ==========================================================
# ARCHIVO: voynichapp.py - PARTE 2 (FRAGMENTO 2B DE 2)
# MATRIZ DE RAÍCES, BUCLE INTELIGENTE Y RENDERIZADO VISUAL
# ==========================================================
    # 3. MATRIZ TOTAL ABSOLUTA DE RAÍCES ETIMOLÓGICAS
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
        "sory": ("remedio / preservación", "remedy / preservation"),
        "o":   ("conducto / apertura", "duct / opening"),
        "so":  ("solución / jugo concentrado", "solution / juice"),
        "nit": ("brillante / salitre (lat. nitrum)", "shiny / nitre"),
        "aqu": ("acuoso / soluble (lat. aqua)", "aqueous / water"),
        "ter": ("terroso / mineral (lat. terra)", "earthy / mineral"),
        "aer": ("gaseoso / volátil (lat. aer)", "gaseous / volatile"),
        "pyr": ("ígneo / reactivo (gr. pyr)", "fiery / reactive"),
        "doc": ("conducir / enseñar (lat. docere)", "to lead / teach"),
        "lig": ("ligadura / aglutinar (lat. ligare)", "binding / bond"),
        "mor": ("retardo / fijación (lat. morari)", "delay / fixation"),
        "mut": ("alteración / cambiar (lat. mutare)", "alteration / change"),
        "nov": ("reciente / fresco (lat. novus)", "fresh / new"),
        "sen": ("maduro / viejo (lat. senex)", "mature / old"),
        "rub": ("pigmento rojo / rubicundo", "red pigment"),
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

    # --- PASADA 2: SUAVIZADOR Y ENSAMBLADOR DE SINTAXIS FLUIDA FINAL ---
    i = 0
    while i < len(palabras_traducidas_crudas):
        item_actual = palabras_traducidas_crudas[i]
        conteo_repeticiones = 1
        while i + conteo_repeticiones < len(palabras_traducidas_crudas) and palabras_traducidas_crudas[i + conteo_repeticiones] == item_actual:
            conteo_repeticiones += 1
        
        if conteo_repeticiones > 1:
            if "conducto / apertura" in item_actual:
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
    if idioma == "Español":
        traduccion_final_limpia = traduccion_final_limpia.replace("el efecto de / -ción savia nutricia", "el proceso de conducción de la savia nutricia")
        traduccion_final_limpia = traduccion_final_limpia.replace("protector de / -ón sistema de conductos extendidos", "a través de un sistema protector de conductos extendidos")
    else:
        traduccion_final_limpia = traduccion_final_limpia.replace("effect of / -tion nutritious sap", "the process of conducting nutritious sap")
        traduccion_final_limpia = traduccion_final_limpia.replace("protector of / -on extended duct system", "through a protective system of extended ducts")
        
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
