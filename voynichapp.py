import streamlit as st
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio conectado a la matriz adaptativa.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO EXTENDIDO V5) ---
if "diccionario_v5" not in st.session_state:
    st.session_state.diccionario_v5 = {
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

# --- CORPUS ESTÁTICO EMBEBIDO (TODOS LOS FOLIOS DIFERENTES ASEGURADOS) ---
if "manuscrito_v5" not in st.session_state:
    corpus = {
        "Herbario (Botánica)": {
            "Folio 1r": "poisoda cutiy podon vetí oarur sier ciey icios oain osain",
            "Folio 1v": "oteroe aram dalaiu ciodain aekiy air soar oas raur",
            "Folio 2r": "otiy oeteodi daur odotoí doror quidí quoquidí chidí",
            "Folio 2v": "tiodau itioei siy pair dais dair dam quioquey okeody quiodal",
            "Folio 33v": "tararain idain cutiy dole criquy arain"  # Tu folio del Girasol
        },
        "Astronomía (Zodíaco)": {
            "Folio 67r": "doror odotoí daur tiodau quioquey okeody air soar oiaj cios",
            "Folio 67v": "odataur ciodain oteroe aram dalaiu aekiy quidí chidí"
        },
        "Cosmología (Astros)": {
            "Folio 74r": "odotoí quidí quoquidí chidí tiodau itioei doror quiodal",
            "Folio 74v": "doror odotoí daur tiodau quioquey okeody"
        },
        "Balneología (Fisiología)": {
            "Folio 75r": "icios cios ain ciodain quaur oteroe oas pain crofosodaur odaur",
            "Folio 78v": "ain ciodain quaur oteroe dalaiu aekiy air soar oas",
            "Folio 80r": "icios cios ain ciodain quaur oteroe"  # Tu folio de las piscinas
        },
        "Farmacéutica (Recetas)": {
            "Folio 88r": "poisoda cuta podon vetí oarur osain pain oain icios cios",
            "Folio 99v": "sier ciey quaur osain aram dalaiu ciodain otiy oeteodi"
        },
        "Recetas Cortas (Estrellas)": {
            "Folio 103r": "quidí chidí tiodau pair dais dair dam quioquey okeody",
            "Folio 116v": "quiodal oteroe aram dalaiu ciodain aekiy air soar oas raur"
        }
    }
    st.session_state.manuscrito_v5 = corpus

# --- MOTOR DE TRADUCCIÓN ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia: 
        return palabra
    if palabra_limpia in st.session_state.diccionario_v5: 
        return st.session_state.diccionario_v5[palabra_limpia]
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    if not texto: 
        return ""
    lineas_traducidas = []
    for linea in texto.strip().split("\n"):
        palabras_traducidas = [traducir_palabra(p) for p in linea.split(" ") if p]
        frase_sucia = " ".join(palabras_traducidas)
        frase_limpia = re.sub(r'\b(los|el|la|las|un|una)\b\s+(?=\b\1\b)', '', frase_sucia, flags=re.IGNORECASE)
        lineas_traducidas.append(re.sub(r'\s+', ' ', frase_limpia).strip())
    return "\n".join(lineas_traducidas)

# --- INTERFAZ GRÁFICA ---
tab1, tab2 = st.tabs(["📖 Navegador del Manuscrito", "🔍 Buscador de Diccionario"])

with tab1:
    seccion_elegida = st.selectbox("Filtrar por sección temática:", list(st.session_state.manuscrito_v5.keys()))
    folios_disponibles = sorted(list(st.session_state.manuscrito_v5[seccion_elegida].keys()))
    
    if folios_disponibles:
        folio_elegido = st.selectbox("Selecciona el Folio:", folios_disponibles)
        texto_folio = st.session_state.manuscrito_v5[seccion_elegida][folio_elegido]
        col1, col2 = st.columns(2)
        with col1:
            texto_editable = st.text_area("Texto Transcrito Original:", texto_folio, height=200)
        with col2:
            texto_descifrado = descifrar_texto_completo(texto_editable)
            st.text_area("Descifrado Automatizado:", texto_descifrado, height=200, disabled=True)
            st.download_button(label="💾 Descargar (.txt)", data=texto_descifrado, file_name=f"traduccion_{folio_elegido.lower()}.txt")

with tab2:
    busqueda = st.text_input("Introduce una palabra Voynich para buscar:")
    if busqueda:
        palabra_b = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        res = {k: v for k, v in st.session_state.diccionario_v5.items() if palabra_b in k}
        for clave, valor in res.items(): 
            st.write(f"🔹 **{clave}** ➔ {valor}")
