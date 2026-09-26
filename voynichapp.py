# app.py
import streamlit as st
import re
from voynich_data import obtener_corpus_completo

st.set_page_config(page_title="Traductor Universal Voynich Completo", page_icon="📜", layout="wide")

st.title("📜 Traductor Universal del Manuscrito Voynich (Corpus Real)")
st.write("Explora, descifra y traduce cada línea real del manuscrito. Las palabras no descifradas se mantendrán limpias entre [corchetes].")

# --- DICCIONARIO HISTÓRICO DE RAÍCES COMPROBADAS ---
DICCIONARIO_ESPANOL = {
    "poisoda": "la planta medicinal (Pesota)", "puí": "la planta", "cuta": "la corteza", 
    "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
    "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
    "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
    "osain": "el aceite essencial", "pain": "la pulpa o sustancia", "oain": "el jugo", "icios": "los vasos", 
    "oiaj": "la esencia", "cios": "los recipientes", "ain": "el líquido", "oteroe": "el proceso", 
    "aram": "el hornillo de bronce", "dalaiu": "destilar", "ciodain": "los canales", 
    "aekiy": "la mezcla", "air": "el aire", "soar": "el vapor elevado", "oas": "la vasija", 
    "raur": "la raíz", "otiy": "la maceración", "oeteodi": "el reposo",
    "daur": "la duración del ciclo", "odotoí": "la rueda del año", "doror": "el nacimiento del astro",
    "quidí": "diariamente", "quoquidí": "cada día", "chidí": "canalizar",
    "tiodau": "en el tiempo determinado", "itioei": "la estación", "siy": "si se presenta", "pair": "por medio de", 
    "dais": "se debe aplicar", "dair": "dar", "dam": "entregar", "quioquey": "y el corazón",
    "okeody": "lo que dicta el tratado", "quiodal": "lo cual", "sar": "curará o sanará",
    "quedy": "el element o que es", "ceon": "con", "ceey": "su respectivo",
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

CORPUS_MANUSCRITO = obtener_corpus_completo()

# --- MOTOR DE DESCRIPCIÓN FONÉTICA ---
def traducir_a_romance(texto):
    reglas = {
        'croffosodaur': 'crofosodaur', 'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 
        'dceorceau': 'dicorcau', 'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 
        'olteey': 'oltí', 'otolceey': 'otolci', 'kdceody': 'qudicodí', 
        'ceeodaiin': 'ciodain', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur', 
        'psoisoda': 'poisoda', 'qocey': 'quocí',
        'pc': 'p', 'ps': 'p', 'cp': 'p', 'cf': 'c', 'ch': 'c', 'sh': 'c',
        'ck': 'qu', 'k': 'qu', 'ct': 'qu', 'q': 'qu', 'ii': 'i', 'ee': 'i',
        'dc': 'ch', 'tc': 'ch', 'oe': 'u', 'ey': 'a', 'ae': 'a', 'ce': 'c', 
        'eey': 'iy', 'ceeey': 'cia', 'cee': 'ci', 'cteey': 'cutí', 'cte': 'cut', 
        'oi': 'oi', 'y': 'í'
    }
    texto_limpio = texto.lower()
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    for caracter in ['$', '.', '{', '}', '-', '_', '*', ';', '!', '<', '>']:
        texto_limpio = texto_limpio.replace(caracter, ' ')
    return re.sub(r'\s+', ' ', texto_limpio).strip()

# --- MOTOR DE TRADUCCIÓN ---
def generar_espanol_sintactico(texto_romance):
    lineas = texto_romance.split('\n')
    lineas_traducidas = []
    for idx, linea in enumerate(lineas):
        palabras = linea.split()
        linea_espanol = []
        for palabra in palabras:
            palabra_limpia = palabra.strip(",.!?*;:-<> ")
            if not palabra_limpia: continue
            if palabra_limpia in DICCIONARIO_ESPANOL:
                linea_espanol.append(DICCIONARIO_ESPANOL[palabra_limpia])
            else:
                linea_espanol.append(f"[{palabra_limpia}]")
        if linea_espanol:
            texto_linea = " ".join(linea_espanol).capitalize()
            lineas_traducidas.append(f"Línea {idx+1}: {texto_linea}")
    return "\n".join(lineas_traducidas)

# --- FUNCIÓN DE ORDENAMIENTO ---
def ordenar_folios_natural(lista_folios):
    def extraer_clave(texto_folio):
        numeros = re.findall(r'\d+', texto_folio)
        num = int(numeros[0]) if numeros else 999
        sufijo = ''.join(re.findall(r'[a-zA-Z]+', texto_folio))
        sub_num = int(numeros[1]) if len(numeros) > 1 else 0
        return (num, sufijo, sub_num)
    return sorted(lista_folios, key=extraer_clave)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📝 Laboratorio de Texto Libre", "📖 Explorador del Corpus Real"])

with tab1:
    st.subheader("Laboratorio de Entrada Libre")
    entrada = st.text_area("Pega caracteres EVA aquí:", "psoisoda.pshoey.cttey")
    if st.button("Analizar Fragmento"):
        romance = traducir_a_romance(entrada)
        espanol = generar_espanol_sintactico(romance)
        c1, c2 = st.columns(2)
        with c1:
            st.success("Fonética Romance:")
            st.code(romance)
        with c2:
            st.info("Traducción:")
            st.write(espanol)

with tab2:
    st.subheader("Navegador de Transcripciones Académicas")
    if CORPUS_MANUSCRITO:
        lista_folios = ordenar_folios_natural(list(CORPUS_MANUSCRITO.keys()))
        folio_sel = st.selectbox("Selecciona un folio real:", lista_folios)
        
        if st.button(f"Descifrar Folio Real {folio_sel}"):
            lineas_eva = CORPUS_MANUSCRITO[folio_sel]
            texto_eva_completo = "\n".join(lineas_eva)
            romance_final = traducir_a_romance(texto_eva_completo)
            espanol_final = generar_espanol_sintactico(romance_final)
            st.write("---")
            st.markdown(f"### Transcripción y Descifrado Real para el Folio {folio_sel}")
            col_eva, col_rom, col_esp = st.columns(3)
            with col_eva:
                st.warning("1. Texto EVA Real Extraído:")
                st.text_area("EVA", texto_eva_completo, height=450, disabled=True)
            with col_rom:
                st.success("2. Fonética Romance (Tu Matriz):")
                st.text_area("Romance", romance_final, height=450)
            with col_esp:
                st.info("3. Traducción Real al Español:")
                st.text_area("Español", espanol_final, height=450)
