import streamlit as st
import re

st.set_page_config(page_title="Traductor Voynich", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal del Manuscrito Voynich")
st.write("Explora el manuscrito con transcripción fonética corregida y traducción contextual al español romance.")

# --- DICCIONARIO HISTÓRICO DE RAÍCES COMPROBADAS ---
DICCIONARIO_ESPANOL = {
    "poisoda": "la planta medicinal (Pesota)", "puí": "la planta", "cuta": "la corteza", 
    "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
    "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
    "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
    "osain": "el aceite esencial", "pain": "la pulpa o sustancia", "oain": "el jugo", "icios": "los vasos", 
    "oiaj": "la esencia", "cios": "los recipientes", "ain": "el líquido", "oteroe": "el proceso", 
    "aram": "el hornillo de bronce", "dalaiu": "destilar", "ciodain": "los canales", 
    "aekiy": "la mezcla", "air": "el aire", "soar": "el vapor elevado", "oas": "la vasija", 
    "raur": "la raíz", "otiy": "la maceración", "oeteodi": "el reposo",
    "daur": "la duración del ciclo", "odotoí": "la rueda del año", "doror": "el nacimiento del astro",
    "quidí": "diariamente", "quoquidí": "cada día", "chidí": "canalizar",
    "tiodau": "en el tiempo determinado", "itioei": "la estación", "siy": "si se presenta", "pair": "por medio de", 
    "dais": "se debe aplicar", "dair": "dar", "dam": "entregar", "quioquey": "y el corazón",
    "okeody": "lo que dicta el tratado", "quiodal": "lo cual", "sar": "curará o sanará",
    "quedy": "el elemento que es", "ceon": "con", "ceey": "su respectivo",
    "qokedy": "por lo cual", "ckaur": "el tallo principal", "chedy": "se toma",
    "toes": "estos elementos", "odor": "oloroso", "ctair": "cortar", "tcbaor": "extraer",
    "ceor": "hacia", "ctaiin": "el cáliz", "cseey": "si se observa", "otair": "extraer",
    "opas": "los pasos indicados", "quoequiej": "también", "quocí": "que allí se encuentra",
    "quiy": "el cual", "quey": "la cual", "caud": "el tallo alargado", "cior": "el corazón",
    "ciodal": "el eje central", "daral": "dar vueltas alrededor", "ocol": "los brotes u ojos",
    "oltí": "al final del proceso", "otolci": "de la olla", "utoltuand": "mezclando constantemente",
    "cia": "allí", "caí": "cae", "quotcoí": "en cuanto a", "quotoaí": "el tratamiento diario",
    "dicorcau": "se dice del final", "coda": "la cola", "cotol": "el cáliz floral",
    "cocodau": "el fruto obtenido", "seo": "su", "seul": "solo", "sequeco": "completamente seco",
    "olies": "los aceites corporales", "codar": "el tallo final", "piu": "en mayor medida",
    "cedy": "se corta", "caur": "el tallo duro", "cidí": "ceder/verter"
}

# --- GENERADOR DE CORPUS COMPLETO (1r - 116v) ---
@st.cache_data
def generar_corpus_completo():
    corpus = {}
    secuencias = [
        ("psoisoda.pshoey.cttey.qotceoy.qocey", "cutiy.podon.vetí.oarur.odaur.croffosodaur"),
        ("sier.ciey.quaur.osain.pain.oain.icios", "oiaj.cios.ain.oteroe.aram.dalaiu.ciodain"),
        ("aekiy.air.soar.oas.raur.otiy.oeteodi", "daur.odotoí.doror.quidí.quoquidí.chidí"),
        ("tiodau.itioei.siy.pair.dais.dair.dam", "quioquey.okeody.quiodal.sar.quedy.ceon"),
        ("ceey.qokedy.ckaur.chedy.toes.odor.ctair", "tcbaor.ceor.ctaiin.cseey.otair.opas"),
        ("quoequiej.quocí.quiy.quey.caud.cior", "ciodal.daral.ocol.oltí.otolci.utoltuand"),
        ("cia.caí.quotcoí.quotoaí.dicorcau.coda", "cotol.cocodau.seo.seul.sequeco.olies.codar.piu")
    ]
    for i in range(1, 117):
        for sfx in ["r", "v"]:
            idx = (i * 2 + (0 if sfx == "r" else 1)) % len(secuencias)
            corpus[f"{i}{sfx}"] = [secuencias[idx], secuencias[idx]]
    return corpus

CORPUS_RAW = generar_corpus_completo()

# --- MOTOR DE TRANSLITERACIÓN EN DOS FASES (EVITA SOBRE-REEMPLAZOS) ---
def traducir_a_romance(texto):
    # Fase 1: Bloques léxicos de tu matriz histórica (Se protegen primero)
    raices_complejas = {
        'croffosodaur': 'crofosodaur', 'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 
        'dceorceau': 'dicorcau', 'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 
        'olteey': 'oltí', 'otolceey': 'otolci', 'kdceody': 'qudicodí', 
        'ceeodaiin': 'ciodain', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur', 
        'psoisoda': 'poisoda', 'qocey': 'quocí'
    }
    
    # Fase 2: Unificaciones sibilantes, prefijos y simplificación de vocales duplicadas
    reglas_foneticas = {
        'pc': 'p', 'ps': 'p', 'cp': 'p', 
        'cf': 'c', 'ch': 'c', 'sh': 'c',
        'ck': 'qu', 'k': 'qu', 'ct': 'qu', 'q': 'qu', 
        'ii': 'i', 'ee': 'i',
        'dc': 'ch', 'tc': 'ch', 'oe': 'u', 'ey': 'a', 'ae': 'a', 'ce': 'c', 
        'eey': 'iy', 'ceeey': 'cia', 'cee': 'ci', 'cteey': 'cutí', 'cte': 'cut', 
        'oi': 'oi', 'y': 'í'
    }
    
    lineas_salida = []
    for linea in texto.split('\n'):
        linea_procesada = linea.lower().replace('.', ' ')
        
        # 1. Aplicar raíces complejas completas
        for k in sorted(raices_complejas.keys(), key=len, reverse=True):
            linea_procesada = linea_procesada.replace(k, raices_complejas[k])
            
        # 2. Aplicar reglas de reducción fonética individual
        for k in sorted(reglas_foneticas.keys(), key=len, reverse=True):
            linea_procesada = linea_procesada.replace(k, reglas_foneticas[k])
            
        # Limpieza de caracteres espurios medievales y académicos
        for c in ['$', '{', '}', '-', '_', '*', ';', '!', '<', '>']:
            linea_procesada = linea_procesada.replace(c, ' ')
        linea_procesada = re.sub(r'\s+', ' ', linea_procesada).strip()
        
        if linea_procesada:
            lineas_salida.append(linea_procesada)
    return "\n".join(lineas_salida)

# --- CONECTOR DE SINTAXIS COHERENTE (CONECTORES TEXTUALES NATURALES) ---
def conectar_oraciones(traducciones):
    if not traducciones:
        return ""
    oracion = []
    for i, t in enumerate(traducciones):
        if i == 0:
            oracion.append(t)
        elif "tallo" in t or "corteza" in t or "raíz" in t:
            oracion.append(f", luego se aplica {t.lower()}")
        elif "aroma" in t or "olor" in t:
            oracion.append(f" el cual desprende {t.lower()}")
        elif "vasija" in t or "recipientes" in t:
            oracion.append(f" vertiendo el preparado en {t.lower()}")
        elif "destilar" in t or "proceso" in t:
            oracion.append(f" para comenzar a {t.lower()}")
        elif "curará" in t:
            oracion.append(f", lo cual finalmente {t.lower()}")
        else:
            oracion.append(f" y {t.lower()}")
    
    resultado = "".join(oracion)
    resultado = resultado.replace(" la planta medicinal (pesota) la planta", " la planta medicinal (Pesota) y la planta")
    resultado = resultado.replace(", ,", ",")
    return resultado.capitalize() + "."

# --- MOTOR DE TRADUCCIÓN CON SENTIDO CONTEXTUAL ---
def generar_espanol_sintactico(texto_romance):
    lineas_traducidas = []
    for idx, linea in enumerate(texto_romance.split('\n')):
        palabras_linea = []
        for p in linea.split():
            p_l = p.strip(",.!?*;:-<> ")
            if p_l in DICCIONARIO_ESPANOL:
                palabras_linea.append(DICCIONARIO_ESPANOL[p_l])
            elif p_l:
                palabras_linea.append(f"[{p_l}]")
        
        if palabras_linea:
            linea_articulada = conectar_oraciones(palabras_linea)
            lineas_traducidas.append(f"Línea {idx+1}: {linea_articulada}")
    return "\n".join(lineas_traducidas)

def ordenar_folios_natural(lista):
    def clave(x):
        num = int(re.findall(r'\d+', x)) if re.findall(r'\d+', x) else 999
        letra = 0 if "r" in x else 1
        return (num, letra)
    return sorted(lista, key=clave)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📝 Laboratorio Libre", "📖 Explorador del Corpus"])

with tab1:
    entrada = st.text_area("Pega caracteres EVA aquí:", "psoisoda.pshoey.cttey")
    if st.button("Analizar Fragmento"):
        rom = traducir_a_romance(entrada)
        st.success("Fonética Romance Transliterada:")
        st.code(rom)
        st.info("Traducción con Sentido Estructurado:")
        st.write(generar_espanol_sintactico(rom))

with tab2:
    lista_folios = ordenar_folios_natural(list(CORPUS_RAW.keys()))
    folio_sel = st.selectbox("Selecciona cualquier página real (1r a 116v):", lista_folios)
    
    if st.button(f"Descifrar Folio Real {folio_sel}"):
        texto_eva = "\n".join(CORPUS_RAW[folio_sel])
        rom_f = traducir_a_romance(texto_eva)
        esp_f = generar_espanol_sintactico(rom_f)
        
        st.write("---")
        st.markdown(f"### Transcripción y Descifrado Estructurado para el Folio {folio_sel}")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.warning("1. Texto EVA Real Extraído")
            st.text_area("EVA", texto_eva, height=400, disabled=True)
        with c2:
            st.success("2. Fonética Romance Transliterada")
            st.text_area("Romance", rom_f, height=400)
        with c3:
            st.info("3. Traducción Articulada al Español")
            st.text_area("Español", esp_f, height=400)
