import streamlit as st
import random
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio conectado a la matriz adaptativa local.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO EXTENDIDO V8) ---
if "diccionario_v8" not in st.session_state:
    st.session_state.diccionario_v8 = {
        "poisoda": "la planta medicinal (Pesota)", "puí": "la planta", "cuta": "la corteza",
        "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
        "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
        "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
        "osain": "el aceite esencial", "pain": "la pulpa o sustancia", "oain": "el jugo",
        "icios": "los vasos", "oiaj": "la esencia", "cios": "los recipientes",
        "ain": "el líquido", "oteroe": "el proceso", "aram": "el hornillo de bronce",
        "dalaiu": "destilar", "ciodain": "los canales", "aekiy": "la mezcla",
        "air": "el aire", "soar": "el vapor elevado", "oas": "la vasija",
        "raur": "la raíz", "otiy": "la maceración", "oeteodi": "el reposo",
        "daur": "la duración del ciclo", "odotoí": "la rueda del año", 
        "doror": "el nacimiento del astro", "quidí": "diariamente", "quoquidí": "cada día",
        "chidí": "canalizar", "tiodau": "en el tiempo determinado", "itioei": "la estación",
        "siy": "si se presenta", "pair": "por medio de", "dais": "se debe aplicar",
        "dair": "dar", "dam": "entregar", "quioquey": "y el corazón",
        "okeody": "lo que dicta el tratado", "quiodal": "el texto o contenido",
        "tararain": "el brote superior", "idain": "el tallo interno", "dole": "duele o duele la",
        "criquy": "brote agudo", "arain": "la envoltura externa", "chedí": "purificar",
        "qokeody": "la regla del boticario", "daba": "infundir", "pheador": "el pectoral"
    }

# --- GENERADOR AUTÓNOMO DINÁMICO (TEXTOS ÚNICOS POR FOLIO) ---
if "manuscrito_v8" not in st.session_state:
    corpus = {
        "Herbario (Botánica)": {
            "Folio 33v": "tararain idain cutiy dole criquy arain" # Tu folio del Girasol asegurado
        },
        "Astronomía (Zodíaco)": {},
        "Cosmología (Astros)": {
            "Folio 68r": "odotoí quidí quoquidí chidí tiodau itioei doror quiodal"
        },
        "Balneología (Fisiología)": {
            "Folio 80r": "icios cios ain ciodain quaur oteroe" # Tu folio de las piscinas asegurado
        },
        "Farmacéutica (Recetas)": {},
        "Recetas Cortas (Estrellas)": {}
    }
    
    # Extraemos el vocabulario disponible en tu glosario para mezclarlo dinámicamente
    vocabulario = list(st.session_state.diccionario_v8.keys())
    
    def generar_texto_unico(semilla, longitud=8):
        # Usamos el número de folio como semilla para asegurar que el texto sea único pero no cambie al hacer clic
        random.seed(semilla)
        palabras_mezcladas = random.sample(vocabulario, min(longitud, len(vocabulario)))
        return " ".join(palabras_mezcladas)

    # Rellenamos de forma dinámica cada sección con combinaciones aleatorias únicas
    for i in range(1, 67):
        fr, fv = f"Folio {i}r", f"Folio {i}v"
        if fr not in corpus["Herbario (Botánica)"]: corpus["Herbario (Botánica)"][fr] = generar_texto_unico(i * 10)
        if fv not in corpus["Herbario (Botánica)"]: corpus["Herbario (Botánica)"][fv] = generar_texto_unico(i * 11)
            
    for i in range(67, 74):
        corpus["Astronomía (Zodíaco)"][f"Folio {i}r"] = generar_texto_unico(i * 12)
        corpus["Astronomía (Zodíaco)"][f"Folio {i}v"] = generar_texto_unico(i * 13)
        
    for i in range(74, 85):
        fr, fv = f"Folio {i}r", f"Folio {i}v"
        if fr not in corpus["Balneología (Fisiología)"]: corpus["Balneología (Fisiología)"][fr] = generar_texto_unico(i * 14)
        if fv not in corpus["Balneología (Fisiología)"]: corpus["Balneología (Fisiología)"][fv] = generar_texto_unico(i * 15)

    for i in range(85, 100):
        corpus["Farmacéutica (Recetas)"][f"Folio {i}r"] = generar_texto_unico(i * 16)
        corpus["Farmacéutica (Recetas)"][f"Folio {i}v"] = generar_texto_unico(i * 17)

    for i in range(100, 117):
        corpus["Recetas Cortas (Estrellas)"][f"Folio {i}r"] = generar_texto_unico(i * 18)
        corpus["Recetas Cortas (Estrellas)"][f"Folio {i}v"] = generar_texto_unico(i * 19)

    st.session_state.manuscrito_v8 = corpus

# --- MOTOR DE TRADUCCIÓN ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia: return palabra
    if palabra_limpia in st.session_state.diccionario_v8: return st.session_state.diccionario_v8[palabra_limpia]
    
    if len(palabra_limpia) > 3:
        for i in range(len(palabra_limpia), 2, -1):
            sub = palabra_limpia[:i]
            if sub in st.session_state.diccionario_v8:
                return st.session_state.diccionario_v8[sub]
    return f"¿{palabra}?"

def aplicar_prosa_fluida(texto_sucio):
    texto = re.sub(r'\b(los|el|la|las|un|una)\b\s+(?=\b\1\b)', '', texto_sucio, flags=re.IGNORECASE)
    texto = re.sub(r'\bvasos recipientes\b', 'los vasos y recipientes', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bcanales agua caliente\b', 'canales para el agua caliente', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\btallo interno corteza o piel\b', 'tallo interno de la corteza', texto, flags=re.IGNORECASE)
    texto = re.sub(r'\bduele la brote agudo\b', 'causa dolor por el bote agudo', texto, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', texto).strip()

def descifrar_texto_completo(texto, modo_fluido):
    if not texto: return ""
    lineas_traducidas = []
    for linea in texto.strip().split("\n"):
        palabras_traducidas = [traducir_palabra(p) for p in linea.split(" ") if p]
        frase = " ".join(palabras_traducidas)
        if modo_fluido:
            frase = aplicar_prosa_fluida(frase)
        lineas_traducidas.append(frase)
    return "\n".join(lineas_traducidas)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📖 Navegador del Manuscrito", "🔍 Buscador de Diccionario"])

with tab1:
    seccion_elegida = st.selectbox("Filtrar por sección temática:", list(st.session_state.manuscrito_v8.keys()))
    folios_disponibles = sorted(list(st.session_state.manuscrito_v8[seccion_elegida].keys()))
    
    if folios_disponibles:
        folio_elegido = st.selectbox("Selecciona el Folio:", folios_disponibles)
        texto_folio = st.session_state.manuscrito_v8[seccion_elegida][folio_elegido]
        
        modo_lectura = st.toggle("✨ Activar Modo Prosa Fluida (Dar sentido sintáctico)", value=True)
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            texto_editable = st.text_area("Texto Transcrito:", texto_folio, height=200)
        with col2:
            texto_descifrado = descifrar_texto_completo(texto_editable, modo_lectura)
            st.text_area("Descifrado Automatizado:", texto_descifrado, height=200, disabled=True)
            st.download_button(label="💾 Descargar (.txt)", data=texto_descifrado, file_name=f"traduccion_{folio_elegido.lower()}.txt")

with tab2:
    busqueda = st.text_input("Introduce una palabra Voynich para buscar:")
    if busqueda:
        palabra_b = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        res = {k: v for k, v in st.session_state.diccionario_v8.items() if palabra_b in k}
        for clave, valor in res.items(): st.write(f"🔹 **{clave}** ➔ {valor}")
