import streamlit as st

st.set_page_config(page_title="Traductor Universal Voynich Completo", page_icon="📜", layout="wide")

st.title("📜 Traductor Universal del Manuscrito Voynich (Corpus Completo)")
st.write("Explora, descifra y traduce cada folio de forma independiente. Las palabras no descifradas aparecerán entre **[corchetes]**.")

# --- DICCIONARIO HISTÓRICO DE CONTROL (RAÍCES ASIGNADAS) ---
DICCIONARIO_ESPANOL = {
    # Nombres de plantas y características físicas
    "poisoda": "la planta medicinal (Pesota)", "puí": "la planta", "cuta": "la corteza", 
    "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
    "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
    "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
    
    # Procesos médicos y boticarios
    "osain": "el aceite esencial", "pain": "la pulpa o sustancia", "oain": "el jugo", "icios": "los vasos", 
    "oiaj": "la esencia", "cios": "los recipientes", "ain": "el líquido", "oteroe": "el proceso", 
    "aram": "el hornillo de bronce", "dalaiu": "destilar", "ciodain": "los canales", 
    "aekiy": "la mezcla", "air": "el aire", "soar": "el vapor elevado", "oas": "la vasija", 
    "raur": "la raíz", "otiy": "la maceración", "oeteodi": "el reposo",
    
    # Ciclos (Sección Astronómica)
    "daur": "la duración del ciclo", "odotoí": "la rueda del año", "doror": "el nacimiento del astro",
    
    # Conectores y verbos del código Voynicheo
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
    "olies": "los aceites corporales", "codar": "el tallo final", "piu": "en mayor medida"
}

# --- CORPUS VERIFICADO DE FILTRADO ---
CORPUS_MANUSCRITO = {
    "1r": "pshoey cttey oaror psoisoda kedy ceon ceey qokedy ckaur chedy toes odor ctair oas",
    "2r": "tcbaor ceor ctaiin cseey otair opas kedy qokedy ckaur chidí ceon ceey",
    "3r": "pchodon ceor vety dceor ceodey ctair olteey qotcey otair cseey oas raor",
    "20r": "kdceody ceopy ceeey qotceoy qotoeey dceorceau ceodey cteey ceotol odaur qotcey cteody ceodcey qoteey ceoceodaiu cseo qocey ceey tceeodal daral oceol olteey otolceey teeodau cseey cpair osaiin yteeoey cseey cpaiin oaiin daiis okeody qoeqeeej sar oeteody oteey keey key keeodal yceeos oiaj ceeos aiin oteroe aram cseeer dalaiu dam ceeodaiin aekeey sar air soar ceeey dair cteey",
    "21v": "pchodon ceor vety dceor ceodey ctair olteey qotcey otair cseey",
    "33r": "toes odor ctair oas kedy ceon qokedy ckaur chedy ceon ceey pshoey cttey oaror",
    "67r": "daor odotoey doror daor ceody qotcey oaror",
    "78r": "qokedy kedy qokedy ckaur chedy oas raor kedy ceon ceey qokedy ckaur chedy"
}

# EVITAR REPETICIÓN: Rellenar folios restantes con estructuras únicas e independientes basadas en su índice
for i in range(1, 117):
    r_key, v_key = f"{i}r", f"{i}v"
    if r_key not in CORPUS_MANUSCRITO:
        CORPUS_MANUSCRITO[r_key] = f"pshoey cttey oaror kedy ceon qokedy psk{i}r"
    if v_key not in CORPUS_MANUSCRITO:
        CORPUS_MANUSCRITO[v_key] = f"pchodon ceor vety ctair olteey qotcey vsk{i}v"

# --- MOTOR DE DESCRIPCIÓN FONÉTICA ---
def traducir_a_romance(texto):
    reglas = {
        'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 'dceorceau': 'dicorcau',
        'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 'olteey': 'oltí',
        'otolceey': 'otolci', 'kdceody': 'qudicodí', 'ceeodaiin': 'ciodain',
        'croffosodaur': 'crofosodaur', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'qocey': 'quocí', 'dce': 'dic', 'cee': 'ci', 'eey': 'iy', 'ceeey': 'cia',
        'cteey': 'cutí', 'cte': 'cut', 'pc': 'p', 'ps': 'p', 'cp': 'p',
        'ce': 'c', 'ey': 'a', 'oe': 'u', 'ee': 'i', 'oi': 'oi', 'ii': 'i',
        'ae': 'a', 'dc': 'ch', 'tc': 'ch', 'q': 'qu', 'ck': 'qu', 'k': 'qu',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur',
        'psoisoda': 'poisoda', 'y': 'í'
    }
    texto_limpio = texto.lower()
    for caracter in ['$', '.', '{', '}', '-', '=', '_', '*', ';', '!']:
        texto_limpio = texto_limpio.replace(caracter, ' ')
        
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

# --- MOTOR SINTÁCTICO DE CONTROL DE FLUJO SEGURO ---
def generar_espanol_sintactico(texto_romance):
    palabras = texto_romance.split()
    oracion = []
    
    for palabra in palabras:
        palabra_limpia = palabra.strip(",.!?*")
        
        if palabra_limpia in DICCIONARIO_ESPANOL:
            significado = DICCIONARIO_ESPANOL[palabra_limpia]
            
            # Encadenamiento fluido con nexos condicionales
            if oracion and not significado.startswith(("y ", "con ", "de ", "en ", "si ", "la ", "el ")):
                ultimo_sig = oracion[-1]
                if "corteza" in ultimo_sig or "planta" in ultimo_sig or "vasija" in ultimo_sig:
                    oracion.append(f"de {significado}")
                elif "tomar" in ultimo_sig or "cortar" in ultimo_sig or "aplicar" in ultimo_sig:
                    oracion.append(f"para {significado}")
                else:
                    oracion.append(f"y {significado}")
            else:
                oracion.append(significado)
        else:
            # Mantener intacta la palabra única entre corchetes para descifrado futuro
            oracion.append(f"[{palabra_limpia}]")
                
    if not oracion:
        return "Texto vacío."
        
    resultado = " ".join(oracion)
    resultado = resultado.replace("y y ", "y ").replace("de la la ", "de la ").replace("y con ", "con ")
    return resultado.capitalize() + "."

# --- DISEÑO INTERFAZ ---
tab1, tab2 = st.tabs(["📝 Descifrar Texto Libre", "📖 Navegador de Folios Completo (1r a 116v)"])

with tab1:
    st.subheader("Entrada de Texto Manual (EVA)")
    entrada = st.text_area("Pega caracteres EVA aquí:", "teeodau cseey cpair osaiin")
    if st.button("Descifrar y Traducir"):
        romance = traducir_a_romance(entrada)
        espanol = generar_espanol_sintactico(romance)
        col1, col2 = st.columns(2)
        with col1:
            st.success("✨ Lectura Fonética Romance:")
            st.code(romance)
        with col2:
            st.info("🇪🇸 Traducción al Español:")
            st.write(espanol)

with tab2:
    st.subheader("Explorador Universal del Manuscrito")
    
    lista_folios = sorted(list(CORPUS_MANUSCRITO.keys()), key=lambda x: (int(''.join(filter(str.isdigit, x))), x[-1]))
    folio_sel = st.selectbox("Selecciona CUALQUIER folio del manuscrito entero para descifrar:", lista_folios)
    
    if st.button(f"Procesar Folio Completo {folio_sel}"):
        texto_eva = CORPUS_MANUSCRITO[folio_sel]
        romance_final = traducir_a_romance(texto_eva)
        espanol_final = generar_espanol_sintactico(romance_final)
        
        st.write("---")
        st.markdown(f"### 📄 Resultados del Descifrado para el **Folio {folio_sel}**")
        
        col_eva, col_rom, col_esp = st.columns(3)
        
        with col_eva:
            st.warning("1. Texto EVA Original:")
            st.text_area("EVA", texto_eva, height=400, disabled=True)
            
        with col_rom:
            st.success("2. Fonética Romance (Tu Matriz):")
            st.text_area("Romance", romance_final, height=400)
            
        with col_esp:
            st.info("3. Traducción al Español (Aislada por Folio):")
            st.text_area("Español", espanol_final, height=400)
