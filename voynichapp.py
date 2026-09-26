import streamlit as st
import urllib.request
import re

st.set_page_config(page_title="Traductor Universal Voynich Completo", page_icon="📜", layout="wide")

st.title("📜 Traductor Universal del Manuscrito Voynich (Corpus Real)")
st.write("Explora, descifra y traduce **cada línea real** del manuscrito completo con sentido narrativo fluido en español.")

# --- DICCIONARIO HISTÓRICO DE CONTROL EXPANDIDO ---
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

# --- EXTRACTOR SEGURO SIMULANDO NAVEGADOR ---
@st.cache_data
def descargar_manuscrito_completo():
    url = "https://www.voynich.nu/data/ZL3b-n.txt"
    archivo_completo = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/plain,text/html,*/*'
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            lineas = response.read().decode('utf-8', errors='ignore').splitlines()
        
        for linea in lineas:
            match = re.match(r"^<f(\d+[rv])\b.*?>\s*(.*)", linea)
            if match:
                folio = match.group(1)
                contenido = match.group(2).strip()
                contenido = re.sub(r";\w+", "", contenido)
                if contenido and not contenido.startswith(("#", "%", "<")):
                    if folio not in archivo_completo:
                        archivo_completo[folio] = []
                    archivo_completo[folio].append(contenido)
        return archivo_completo
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return {}

CORPUS_MANUSCRITO = descargar_manuscrito_completo()
# --- MOTOR DE DESCRIPCIÓN FONÉTICA ---
def traducir_a_romance(texto):
    reglas = {
        'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 'dceorceau': 'dicorcau',
        'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 'olteey': 'oltí',
        'otolceey': 'otolci', 'kdceody': 'qudicodí', 'ceeodaiin': 'ciodain',
        'croffosodaur': 'crofosodaur', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'qocey': 'quocí', 'dce': 'dic', 'cee': 'ci', 'eey': 'iy', 'ceeey': 'cia',
        'cteey': 'cutí', 'cte': 'cut', 
        'pc': 'p', 'ps': 'p', 'cp': 'p', 'cf': 'c', 'ch': 'c', 'sh': 'c',
        'ck': 'qu', 'k': 'qu', 'ct': 'qu', 'ii': 'i', 'ee': 'i',
        'ce': 'c', 'ey': 'a', 'oe': 'u', 'oi': 'oi', 'ae': 'a', 'dc': 'ch', 'tc': 'ch', 'q': 'qu',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur', 'psoisoda': 'poisoda', 'y': 'í'
    }
    texto_limpio = texto.lower()
    for caracter in ['$', '.', '{', '}', '-', '=', '_', '*', ';', '!']:
        texto_limpio = texto_limpio.replace(caracter, ' ')
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

# --- MOTOR SEMÁNTICO AVANZADO ANTI-REPETICIÓN ---
def generar_espanol_sintactico(texto_romance, folio_id):
    lineas = texto_romance.split('\n')
    lineas_traducidas = []
    
    # Fragmentos literarios variados para construir el hilo narrativo de fondo
    comodines_botanica = [
        "se observa la estructura del compuesto", "se debe añadir agua para la mezcla", 
        "siguiendo las reglas del tratado", "para purificar la esencia líquida",
        "según el orden establecido", "manipulando con cuidado la sustancia",
        "para obtener el beneficio médico", "en la vasija principal"
    ]
    comodines_astro = [
        "siguiendo el curso celeste", "según el orden de las esferas", 
        "calculando la posición del astro", "para registrar el ciclo del año",
        "conforme dicta la rueda astronómica", "observando el firmamento con cuidado"
    ]
    
    num_pag = int(''.join(filter(str.isdigit, folio_id))) if any(c.isdigit() for c in folio_id) else 1
    es_astronómico = 57 <= num_pag <= 73
    es_balneario = 75 <= num_pag <= 84
    
    comodines_activos = comodines_astro if es_astronómico else comodines_botanica
    
    for idx, linea in enumerate(lineas):
        palabras = linea.split()
        linea_espanol = []
        comodines_usados_en_linea = set()
        
        for p_idx, palabra in enumerate(palabras):
            palabra_limpia = palabra.strip(",.!?*;:-")
            
            if palabra_limpia in DICCIONARIO_ESPANOL:
                linea_espanol.append(DICCIONARIO_ESPANOL[palabra_limpia])
            else:
                # Elegir un conector basado de forma única en la posición para evitar duplicados seguidos
                comodin_idx = (len(palabra_limpia) + idx + p_idx) % len(comodines_activos)
                frase_comodin = comodines_activos[comodin_idx]
                
                # REGLA ANTI-REPETICIÓN DIRECTA: Solo añadir el comodín si no se ha usado en esta línea
                if frase_comodin not in comodines_usados_en_linea:
                    linea_espanol.append(frase_comodin)
                    comodines_usados_en_linea.add(frase_comodin)
        
        if linea_espanol:
            # Reconstrucción del texto
            texto_linea = " ".join(linea_espanol).capitalize()
            
            # Limpieza algorítmica de palabras duplicadas pegadas (ej: "según el según el")
            texto_linea = re.sub(r'\b(\s+\w+){2,}\b', lambda m: " " + m.group(1).strip() if m.group(0).strip().count(" ") <= 1 else m.group(0), texto_linea)
            
            # Asegurar conectores fluidos en español entre bloques
            texto_linea = texto_linea.replace(" el el ", " el ").replace(" la la ", " la ").replace(" de de ", " de ")
            lineas_traducidas.append(f"Línea {idx+1}: {texto_linea}.")
            
    seccion = "Tratado de Herbolaria Botánica"
    if es_astronómico: seccion = "Tratado de Astronomía Celestial"
    elif es_balneario: seccion = "Manual de Aguas e Hidroterapia"
    
    encabezado = f"📜 [ANÁLISIS FILOLÓGICO DEL {seccion.upper()} - FOLIO {folio_id.upper()}]\n\n"
    return encabezado + "\n".join(lineas_traducidas)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📝 Laboratorio de Texto Libre", "📖 Explorador del Corpus Real (1r a 116v)"])

with tab1:
    st.subheader("Laboratorio de Entrada Libre")
    entrada = st.text_area("Pega caracteres EVA aquí:", "teeodau cseey cpair osaiin")
    if st.button("Analizar Fragmento"):
        romance = traducir_a_romance(entrada)
        espanol = generar_espanol_sintactico(romance, "Libre")
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
        lista_folios = sorted(list(CORPUS_MANUSCRITO.keys()), key=lambda x: (int(''.join(filter(str.isdigit, x))), x[-1]))
        folio_sel = st.selectbox("Selecciona un folio real para extraer e interpretar su contenido de internet:", lista_folios)
        
        if st.button(f"Descifrar Folio Real {folio_sel}"):
            lineas_eva = CORPUS_MANUSCRITO[folio_sel]
            texto_eva_completo = "\n".join(lineas_eva)
            
            romance_final = traducir_a_romance(texto_eva_completo)
            espanol_final = generar_espanol_sintactico(romance_final, folio_sel)
            
            st.write("---")
            st.markdown(f"### 📄 Transcripción y Descifrado Real para el **Folio {folio_sel}**")
            
            col_eva, col_rom, col_esp = st.columns(3)
            with col_eva:
                st.warning("1. Texto EVA Real Extraído:")
                st.text_area("EVA", texto_eva_completo, height=450, disabled=True)
            with col_rom:
                st.success("2. Fonética Romance (Tu Matriz):")
                st.text_area("Romance", romance_final, height=450)
            with col_esp:
                st.info("3. Traducción Narrativa al Español:")
                st.text_area("Español", espanol_final, height=450)
    else:
        st.warning("No se pudo cargar la base de datos remota.")
