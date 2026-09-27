import streamlit as st
import requests
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio conectado al corpus real de Voynich.nu.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO NATIVO EXTENDIDO V4) ---
if "diccionario_v4" not in st.session_state:
    st.session_state.diccionario_v4 = {
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

# --- DESCARGA Y PARSEO DEL CORPUS REAL DESDE VOYNICH.NU ---
@st.cache_data(show_spinner="Descargando corpus académico real...")
def cargar_corpus_real_voynich():
    url = "https://www.voynich.nu/data/ZL3b-n.txt"
    corpus_v4 = {
        "Herbario (Botánica)": {}, "Astronomía (Zodíaco)": {}, "Cosmología (Astros)": {},
        "Balneología (Fisiología)": {}, "Farmacéutica (Recetas)": {}, "Recetas Cortas (Estrellas)": {}
    }
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            for linea in response.text.split("\n"):
                match = re.match(r'<f(\d+[rv])\..*?>\s*(.*)', linea)
                if match:
                    folio_id = f"Folio {match.group(1)}"
                    texto_limpio = re.sub(r'[{}[\]!%=;@\$.,]', ' ', match.group(2).strip())
                    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()
                    if not texto_limpio or texto_limpio.startswith("#"): continue
                    
                    num_folio = int(re.search(r'\d+', folio_id).group())
                    if 1 <= num_folio <= 66: seccion = "Herbario (Botánica)"
                    elif 67 <= num_folio <= 73: seccion = "Astronomía (Zodíaco)"
                    elif num_folio == 74: seccion = "Cosmología (Astros)"
                    elif 75 <= num_folio <= 84: seccion = "Balneología (Fisiología)"
                    elif 85 <= num_folio <= 99: seccion = "Farmacéutica (Recetas)"
                    else: seccion = "Recetas Cortas (Estrellas)"
                    
                    if folio_id not in corpus_v4[seccion]: corpus_v4[seccion][folio_id] = texto_limpio
                    else: corpus_v4[seccion][folio_id] += "\n" + texto_limpio
    except Exception:
        corpus_v4["Herbario (Botánica)"]["Folio 33v"] = "tararain idain cutiy dole criquy arain"
    return corpus_v4

if "manuscrito_v4" not in st.session_state:
    st.session_state.manuscrito_v4 = cargar_corpus_real_voynich()

# --- MOTOR DE TRADUCCIÓN INTERLINEAL ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia: return palabra
    if palabra_limpia in st.session_state.diccionario_v4: return st.session_state.diccionario_v4[palabra_limpia]
    if len(palabra_limpia) > 3:
        for i in range(len(palabra_limpia), 2, -1):
            sub_raiz = palabra_limpia[:i]
            coincidencias = [v for k, v in st.session_state.diccionario_v4.items() if k.startswith(sub_raiz)]
            if coincidencias: return f"[{coincidencias[0]}]*"
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    if not texto: return ""
    lineas_traducidas = []
    for linea in texto.strip().split("\n"):
        palabras_traducidas = [traducir_palabra(p) for p in linea.split(" ")]
        frase_sucia = " ".join(palabras_traducidas)
        frase_limpia = re.sub(r'\b(los|el|la|las|un|una)\b\s+(?=\b\1\b)', '', frase_sucia, flags=re.IGNORECASE)
        lineas_traducidas.append(re.sub(r'\s+', ' ', frase_limpia).strip())
    return "\n".join(lineas_traducidas)

# --- INTERFAZ DE USUARIO ---
tab1, tab2, tab3 = st.tabs(["📖 Navegador del Manuscrito Completo", "🔍 Buscador de Diccionario", "📝 Añadir/Editar Datos"])

with tab1:
    st.subheader("Selector e Índice General de Folios")
    seccion_elegida = st.selectbox("Filtrar por sección temática:", list(st.session_state.manuscrito_v4.keys()))
    folios_disponibles = sorted(list(st.session_state.manuscrito_v4[seccion_elegida].keys()))
    
    if folios_disponibles:
        folio_elegido = st.selectbox("Selecciona el Folio de la página a descifrar:", folios_disponibles)
        texto_folio = st.session_state.manuscrito_v4[seccion_elegida][folio_elegido]
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Texto Transcrito Original del `{folio_elegido}`**")
            texto_editable = st.text_area("Puedes modificar el texto en vivo:", texto_folio, height=200)
        with col2:
            st.success(f"**Descifrado Semántico Automatizado**")
            texto_descifrado = descifrar_texto_completo(texto_editable)
            st.text_area("Resultado obtenido:", texto_descifrado, height=200, disabled=True)
            st.download_button(
                label="💾 Descargar Traducción (.txt)",
                data=f"--- TRADUCCIÓN DEL {folio_elegido.upper()} ---\n\nTexto Original:\n{texto_editable}\n\nTraducción:\n{texto_descifrado}",
                file_name=f"traduccion_voynich_{folio_elegido.lower().replace(' ', '_')}.txt", mime="text/plain"
            )
    else: st.warning("No hay folios disponibles para esta sección.")

with tab2:
    st.subheader("Buscador predictivo del Glosario")
    busqueda = st.text_input("Introduce una palabra Voynich para ver su mapeo:")
    if busqueda:
        palabra_b = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        res = {k: v for k, v in st.session_state.diccionario_v4.items() if palabra_b in k}
        for clave, valor in res.items(): st.write(f"🔹 **{clave}** ➔ {valor}")

with tab3:
    st.subheader("Gestión Avanzada de Datos (En memoria de Sesión)")
    col_dict, col_folio = st.columns(2)
    with col_dict:
        st.write("### Registrar nuevo término")
        n_clave = st.text_input("Nueva palabra Voynich:")
        n_valor = st.text_input("Traducción / Significado:")
        if st.button("Guardar en Diccionario") and n_clave and n_valor:
            st.session_state.diccionario_v4[n_clave.lower().strip()] = n_valor.strip()
            st.success("¡Término guardado!")
            st.rerun()
    with col_folio:
        st.write("### Actualizar texto de un folio existente")
        todos = [f"{s} - {f}" for s, d in st.session_state.manuscrito_v4.items() for f in d.keys()]
        if todos:
            f_update = st.selectbox("Folio a modificar:", sorted(todos))
            sec_up, fol_up = f_update.split(" - ")
            n_txt = st.text_area("Texto definitivo:", st.session_state.manuscrito_v4[sec_up][fol_up], key="area_up")
            if st.button("Actualizar Memoria"):
                st.session_state.manuscrito_v4[sec_up][fol_up] = n_txt.strip()
                st.success("¡Folio modificado!")
                st.rerun()
