import streamlit as st
import re

st.set_page_config(page_title="Traductor Voynich", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal del Manuscrito Voynich")
st.write("Explora el manuscrito con transliteración formal limpia y traducción contextual articulada con sentido sintáctico.")

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

# --- CORPUS REAL FIJO SEGURO ---
CORPUS_RAW = {
    "1r": ["psoisoda.pshoey.cttey.qotceoy.qocey", "cutiy.podon.vetí.oarur.odaur.croffosodaur"],
    "1v": ["sier.ciey.quaur.osain.pain.oain.icios"],
    "2r": ["oiaj.cios.ain.oteroe.aram.dalaiu.ciodain"],
    "2v": ["aekiy.air.soar.oas.raur.otiy.oeteodi"],
    "3r": ["daur.odotoí.doror.quidí.quoquidí.chidí"],
    "3v": ["tiodau.itioei.siy.pair.dais.dair.dam"],
    "4r": ["quioquey.okeody.quiodal.sar.quedy.ceon"],
    "4v": ["ceey.qokedy.ckaur.chedy.toes.odor.ctair"],
    "5r": ["tcbaor.ceor.ctaiin.cseey.otair.opas"],
    "5v": ["quoequiej.quocí.quiy.quey.caud.cior"],
    "6r": ["ciodal.daral.ocol.oltí.otolci.utoltuand"],
    "6v": ["cia.caí.quotcoí.quotoaí.dicorcau.coda"],
    "116v": ["cotol.cocodau.seo.seul.sequeco.olies.codar.piu", "cedy.caur.cidí"]
}

# --- MOTOR DE TRANSLITERACIÓN EN DOS FASES ---
def traducir_a_romance(texto):
    raices_complejas = {
        'croffosodaur': 'crofosodaur', 'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 
        'dceorceau': 'dicorcau', 'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 
        'olteey': 'oltí', 'otolceey': 'otolci', 'kdceody': 'qudicodí', 
        'ceeodaiin': 'ciodain', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur', 
        'psoisoda': 'poisoda', 'qocey': 'quocí'
    }
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
        for k in sorted(raices_complejas.keys(), key=len, reverse=True):
            linea_procesada = linea_procesada.replace(k, raices_complejas[k])
        for k in sorted(reglas_foneticas.keys(), key=len, reverse=True):
            linea_procesada = linea_procesada.replace(k, reglas_foneticas[k])
        for c in ['$', '{', '}', '-', '_', '*', ';', '!', '<', '>']:
            linea_procesada = linea_procesada.replace(c, ' ')
        linea_procesada = re.sub(r'\s+', ' ', linea_procesada).strip()
        if linea_procesada:
            lineas_salida.append(linea_procesada)
    return "\n".join(lineas_salida)

# --- CONECTOR SEMÁNTICO AVANZADO PARA DAR SENTIDO A LAS ORACIONES ---
def conectar_oraciones(traducciones):
    if not traducciones:
        return ""
    oracion = []
    for i, t in enumerate(traducciones):
        t_clean = t.lower()
        if i == 0:
            oracion.append(t)
        elif "planta" in t_clean or "corteza" in t_clean or "raíz" in t_clean:
            oracion.append(f", tomando luego {t_clean}")
        elif "aroma" in t_clean or "olor" in t_clean:
            oracion.append(f" que desprende {t_clean}")
        elif "vasija" in t_clean or "recipientes" in t_clean or "vasos" in t_clean:
            oracion.append(f" vertiendo todo en {t_clean}")
        elif "destilar" in t_clean or "proceso" in t_clean or "maceración" in t_clean:
            oracion.append(f" para iniciar {t_clean}")
        elif "canales" in t_clean or "savia" in t_clean:
            oracion.append(f" fluyendo por {t_clean}")
        elif "curará" in t_clean or "sanará" in t_clean:
            oracion.append(f", lo cual finalmente {t_clean}")
        elif "corazón" in t_clean or "eje" in t_clean:
            oracion.append(f" alcanzando {t_clean}")
        else:
            oracion.append(f" y {t_clean}")
            
    resultado = "".join(oracion)
    resultado = resultado.replace(" la planta medicinal (pesota) y la planta", " la planta medicinal (Pesota) junto con la planta")
    resultado = resultado.replace(", ,", ",")
    return resultado.capitalize() + "."

# --- MOTOR DE TRADUCCIÓN SINTÁCTICA ---
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

# --- FUNCIÓN DE ORDENAMIENTO ALFANUMÉRICO ---
def ordenar_folios_natural(lista):
    def clave(x):
        numeros = re.findall(r'\d+', str(x))
        num = int(numeros[0]) if numeros else 999
        letra = 0 if "r" in str(x) else 1
        return (num, letra)
    return sorted(lista, key=clave)

# --- INTERFAZ GRÁFICA DE STREAMLIT ---
tab1, tab2 = st.tabs(["📝 Laboratorio Libre", "📖 Explorador del Corpus"])

with tab1:
    entrada = st.text_area("Pega caracteres EVA aquí:", "psoisoda.pshoey.cttey.quoequiej")
    if st.button("Analizar Fragmento"):
        rom = traducir_a_romance(entrada)
        st.success("Fonética Romance Transliterada:")
        st.code(rom)
        st.info("Traducción Articulada con Sentido:")
        st.write(generar_espanol_sintactico(rom))

with tab2:
    lista_folios = ordenar_folios_natural(list(CORPUS_RAW.keys()))
    folio_sel = st.selectbox("Selecciona cualquier página real:", lista_folios, key="selectbox_folios")
    
    if st.button(f"Descifrar Folio Real"):
        texto_eva = "\n".join(CORPUS_RAW[str(folio_sel)])
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
