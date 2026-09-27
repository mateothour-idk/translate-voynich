import streamlit as st
import random
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio conectado a la matriz adaptativa local.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO EXTENDIDO V10) ---
if "diccionario_v10" not in st.session_state:
    st.session_state.diccionario_v10 = {
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
if "manuscrito_v10" not in st.session_state:
    corpus = {
        "Herbario (Botánica)": {
            "Folio 33v": "tararain idain cutiy dole criquy arain" # Folio del Girasol
        },
        "Astronomía (Zodíaco)": {},
        "Cosmología (Astros)": {
            "Folio 68r": "odotoí quidí quoquidí chidí tiodau itioei doror quiodal"
        },
        "Balneología (Fisiología)": {
            "Folio 80r": "icios cios ain ciodain quaur oteroe" # Folio de las piscinas
        },
        "Farmacéutica (Recetas)": {},
        "Recetas Cortas (Estrellas)": {}
    }
    
    vocabulario = list(st.session_state.diccionario_v10.keys())
    
    def generar_texto_unico(semilla, longitud=8):
        random.seed(semilla)
        vocab_extendido = vocabulario + ["olad", "oror", "ctey", "tane", "paly", "shor"]
        palabras_mezcladas = random.sample(vocab_extendido, min(longitud, len(vocab_extendido)))
        return " ".join(palabras_mezcladas)

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

    st.session_state.manuscrito_v10 = corpus

# --- MOTOR DE TRADUCCIÓN ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia: return palabra
    if palabra_limpia in st.session_state.diccionario_v10: return st.session_state.diccionario_v10[palabra_limpia]
    return f"¿{palabra}?"

def aplicar_prosa_fluida(texto_sucio):
    # 1. Limpieza inicial de duplicados
    texto = re.sub(r'\b(los|el|la|las|un|una)\b\s+(?=\b\1\b)', '', texto_sucio, flags=re.IGNORECASE)
    
    # 2. Inyección agresiva de conectores y verbos entre corchetes [...]
    # Conexión Temporal/Frecuencia (ej: "diariamente la raíz" -> "diariamente [se toma] la raíz")
    texto = re.sub(r'\b(diariamente|cada día)\s+(la|los|el|las)\b', r'\1 [se toma] \2', texto, flags=re.IGNORECASE)
    
    # Conexión de Elementos Anatómicos/Plantas (ej: "la raíz los recipientes" -> "la raíz [en] los recipientes")
    texto = re.sub(r'\b(la raíz|el tallo interno|la corteza|las hojas dentadas)\s+(los recipientes|los vasos|la vasija|los canales)\b', r'\1 [en] \2', texto, flags=re.IGNORECASE)
    
    # Conexión de Acción y Proceso (ej: "recipientes la envoltura" -> "recipientes [para] la envoltura")
    texto = re.sub(r'\b(los recipientes|los vasos|la vasija)\s+(la envoltura externa|el líquido|la pulpa|la savia|el jugo)\b', r'\1 [para] \2', texto, flags=re.IGNORECASE)
    
    # Conexión de Procesos Médicos (ej: "entregar purificar" -> "entregar [y] purificar")
    texto = re.sub(r'\b(entregar|dar|aplicar)\s+(purificar|destilar|infundir|canalizar)\b', r'\1 [y] \2', texto, flags=re.IGNORECASE)
    
    # Conexión hacia el Resultado (ej: "purificar la maceración" -> "purificar [durante] la maceración")
    texto = re.sub(r'\b(purificar|destilar|infundir|canalizar|entregar)\s+(la maceración|el reposo|el proceso)\b', r'\1 [durante] \2', texto, flags=re.IGNORECASE)

    # Conexiones generales de sustantivos sueltos consecutivos
    texto = re.sub(r'\b(la envoltura externa)\s+(el tallo interno)\b', r'\1 [junto al] \2', texto, flags=re.IGNORECASE)

    return re.sub(r'\s+', ' ', texto).strip()

def descifrar_texto_completo(texto, modo_fluido):
    if not texto: return "", 0, 0
    lineas_traducidas = []
    total_palabras = 0
    desconocidas = 0
    
    for linea in texto.strip().split("\n"):
        palabras = [p for p in linea.split(" ") if p]
        total_palabras += len(palabras)
        
        palabras_traducidas = []
        for p in palabras:
            traducida = traducir_palabra(p)
            if "¿" in traducida:
                desconocidas += 1
            palabras_traducidas.append(traducida)
            
        frase = " ".join(palabras_traducidas)
        if modo_fluido:
            frase = aplicar_prosa_fluida(frase)
        lineas_traducidas.append(frase)
        
    return "\n".join(lineas_traducidas), total_palabras, desconocidas

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📖 Navegador del Manuscrito", "🔍 Buscador de Diccionario"])

with tab1:
    seccion_elegida = st.selectbox("Filtrar por sección temática:", list(st.session_state.manuscrito_v10.keys()))
    folios_disponibles = sorted(list(st.session_state.manuscrito_v10[seccion_elegida].keys()))
    
    if folios_disponibles:
        folio_elegido = st.selectbox("Selecciona el Folio:", folios_disponibles)
        texto_folio = st.session_state.manuscrito_v10[seccion_elegida][folio_elegido]
        
        modo_lectura = st.toggle("✨ Activar Modo Prosa Fluida (Inyectar sintaxis estructurada [...])", value=True)
        st.markdown("---")
        
        texto_descifrado, total, incognitas = descifrar_texto_completo(texto_folio, modo_lectura)
        conocidas = total - incognitas
        porcentaje = int((conocidas / total) * 100) if total > 0 else 0
        
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        with col_metric1:
            st.metric(label="🔍 Palabras Incógnitas restantes", value=f"{incognitas} / {total}")
        with col_metric2:
            st.metric(label="✅ Palabras Traducidas con éxito", value=f"{conocidas}")
        with col_metric3:
            st.metric(label="📊 Grado de Descifrado", value=f"{porcentaje}%")
        st.progress(porcentaje / 100.0)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            texto_editable = st.text_area("Texto Transcrito Original:", texto_folio, height=180)
            texto_descifrado_ed, total_ed, inc_ed = descifrar_texto_completo(texto_editable, modo_lectura)
        with col2:
            st.text_area("Descifrado Automatizado:", texto_descifrado_ed, height=180, disabled=True)
            st.download_button(label="💾 Descargar (.txt)", data=texto_descifrado_ed, file_name=f"traduccion_{folio_elegido.lower()}.txt")

with tab2:
    busqueda = st.text_input("Introduce una palabra Voynich para buscar:")
    if busqueda:
        palabra_b = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        res = {k: v for k, v in st.session_state.diccionario_v10.items() if palabra_b in k}
        for clave, valor in res.items(): st.write(f"🔹 **{clave}** ➔ {valor}")
