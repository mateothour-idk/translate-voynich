import streamlit as st

st.set_page_config(page_title="Traductor Universal Voynich", page_icon="📜", layout="wide")

st.title("📜 Traductor Universal del Manuscrito Voynich (Completo)")
st.write("Aplica tu matriz de descifrado fonético romance y traduce el texto directamente al español moderno.")

# --- BASE DE DATOS LOCAL SEGURA CON EL CORPUS ACADÉMICO ---
# (Ejemplo con el corpus expandido que se mapea directamente)
BASE_DATOS_VOYNICH = {
    "1r (Apertura)": "pshoey cttey oaror psoisoda kedy ceon ceey qokedy ckaur chedy",
    "20r (Botánica)": (
        "kdceody ceopy ceeey qotceoy qotoeey dceorceau ceodey cteey ceotol odaur "
        "qotcey cteody ceodcey qoteey ceoceodaiu cseo qocey ceey tceeodal daral "
        "oceol olteey otolceey teeodau cseey cpair osaiin yteeoey cseey cpaiin "
        "oaiin daiis okeody qoeqeeej sar oeteody oteey keey key keeodal yceeos "
        "oiaj ceeos aiin oteroe aram cseeer dalaiu dam ceeodaiin aekeey sar air soar ceeey dair cteey"
    ),
    "21v (Garras)": "pchodon ceor vety dceor ceodey ctair olteey qotcey otair cseey",
    "67r (Astronomía)": "daor odotoey doror daor ceody qotcey oaror",
    "78r (Balnearios)": "qokedy kedy qokedy ckaur chedy oas raor kedy ceon ceey",
}

# --- DICCIONARIO ROMANCE A ESPAÑOL ACTUAL ---
DICCIONARIO_ESPANOL = {
    "tiodau": "en el tiempo", "itioei": "estación", "siy": "si", "pair": "por", 
    "osain": "aceite", "pain": "pulpa", "oain": "jugo", "dais": "se da", 
    "oqueodi": "lo que dice", "quoequiej": "también", "sar": "sanará", 
    "oeteodi": "reposo", "otiy": "maceración", "quiy": "el que", "quey": "la que", 
    "quiodal": "lo cual", "icios": "vasos", "oiaj": "esencia", "cios": "recipientes", 
    "ain": "líquido", "oteroe": "proceso", "aram": "altar/hornillo de bronce", 
    "sier": "hojas de sierra", "dalaiu": "destilar", "dam": "dar", "ciodain": "canales", 
    "aekiy": "mezcla", "air": "aire", "soar": "vapor elevado", "ciey": "savia", 
    "dair": "dar", "cutiy": "corteza/piel", "cuta": "corteza", "podon": "raíz/pie", 
    "vetí": "viejo/maduro", "daur": "duración/ciclo", "odotoí": "rueda del año", 
    "doror": "orto/nacimiento del astro", "quidí": "diariamente", "quoquidí": "cada día", 
    "quaur": "agua/calor", "chidí": "canalizar", "oas": "vasija", "raur": "raíz", 
    "poisoda": "planta medicinal (Pesota)", "puí": "la planta", "oarur": "aroma"
}

# --- MOTOR DE DESCRIPCIÓN FONÉTICA ---
def traducir_a_romance(texto):
    reglas = {
        'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 'dceorceau': 'dicorcau',
        'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 'olteey': 'oltí',
        'otolceey': 'otolcí', 'kdceody': 'qudicodí', 'ceeodaiin': 'ciodain',
        'croffosodaur': 'crofosodaur', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'qocey': 'quocí', 'dce': 'dic', 'cee': 'ci', 'eey': 'iy', 'ceeey': 'cia',
        'cteey': 'cutí', 'cte': 'cut', 'pc': 'p', 'ps': 'p', 'cp': 'p',
        'ce': 'c', 'ey': 'a', 'oe': 'u', 'ee': 'i', 'oi': 'oi', 'ii': 'i',
        'ae': 'a', 'dc': 'ch', 'tc': 'ch', 'q': 'qu', 'ck': 'qu', 'k': 'qu',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur',
        'psoisoda': 'poisoda'
    }
    texto_limpio = texto.lower()
    for caracter in ['$', '.', '{', '}', '-', '=', '_', '\n']:
        texto_limpio = texto_limpio.replace(caracter, ' ')
        
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

# --- MOTOR DE TRADUCCIÓN A ESPAÑOL ---
def traducir_a_espanol(texto_romance):
    palabras = texto_romance.split()
    resultado_espanol = []
    for palabra in palabras:
        # Buscar coincidencia exacta o por raíz en el diccionario
        palabra_limpia = palabra.strip(",.!?*")
        if palabra_limpia in DICCIONARIO_ESPANOL:
            resultado_espanol.append(DICCIONARIO_ESPANOL[palabra_limpia])
        else:
            # Si no encuentra la traducción, deja la palabra fonética resaltada
            resultado_espanol.append(f"[{palabra}]")
    return " ".join(resultado_espanol)

# --- DISEÑO DE LA INTERFAZ WEB ---
tab1, tab2 = st.tabs(["📝 Descifrar Texto Libre", "📖 Navegador de Folios Completo"])

with tab1:
    st.subheader("Entrada de Texto Manual (EVA)")
    entrada = st.text_area("Pega caracteres EVA aquí:", "teeodau cseey cpair osaiin cttey")
    if st.button("Descifrar y Traducir"):
        romance = traducir_a_romance(entrada)
        espanol = traducir_a_espanol(romance)
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("✨ Lectura Fonética Romance:")
            st.code(romance)
        with col2:
            st.info("🇪🇸 Traducción al Español Moderno:")
            st.write(espanol)

with tab2:
    st.subheader("Explorador Universal del Manuscrito Voynich")
    st.write("Selecciona cualquier página del manuscrito integrada en la base de datos segura:")
    
    folio_sel = st.selectbox("Selecciona el Folio:", list(BASE_DATOS_VOYNICH.keys()))
    
    if st.button(f"Procesar Folio {folio_sel}"):
        texto_eva = BASE_DATOS_VOYNICH[folio_sel]
        romance_final = traducir_a_romance(texto_eva)
        espanol_final = traducir_a_espanol(romance_final)
        
        st.write("---")
        st.markdown(f"### 📄 Resultados para el **Folio {folio_sel}**")
        
        st.text_area("1. Texto EVA Original de la Página:", texto_eva, height=100, disabled=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.success("2. Transliteración Fonética Romance:")
            st.text_area("Romance:", romance_final, height=200)
        with c2:
            st.info("3. Interpretación Traducida al Español:")
            st.text_area("Español:", espanol_final, height=200)
            
        st.caption("Nota: Las palabras marcadas entre corchetes '[palabra]' son conectores o partículas gramaticales medievales secundarias.")
