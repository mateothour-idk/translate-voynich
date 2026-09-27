import streamlit as st
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio mediante un motor adaptativo en la nube.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO NATIVO) ---
# Inicializamos el diccionario en el estado de la sesión de Streamlit para permitir edición en vivo
if "diccionario" not in st.session_state:
    st.session_state.diccionario = {
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
        "okeody": "lo que dicta el tratado", "quiodal": "el texto o contenido"
    }

# --- CORPUS DEL MANUSCRITO ---
if "manuscrito" not in st.session_state:
    st.session_state.manuscrito = {
        "Herbario (Botánica)": {
            "Folio 1r": "poisoda cutiy podon vetí oarur sier ciey icios oain osain",
            "Folio 1v": "oteroe aram dalaiu ciodain aekiy air soar oas raur",
            "Folio 2r": "otiy oeteodi daur odotoí doror quidí quoquidí chidí",
            "Folio 2v": "tiodau itioei siy pair dais dair dam quioquey okeody quiodal",
            "Folio 3r": "poisoda cutiy podon vetí oarur sier ciey",
            "Folio 3v": "oteroe aram dalaiu ciodain aekiy air soar"
        },
        "Astronomía (Zodíaco)": {
            "Folio 67r": "doror odotoí daur tiodau quioquey okeody air soar oiaj cios",
            "Folio 69r": "doror odotoí daur tiodau quioquey okeody"
        },
        "Cosmología (Astros)": {
            "Folio 68r": "odotoí quidí quoquidí chidí tiodau itioei doror quiodal"
        },
        "Balneología (Fisiología)": {
            "Folio 75r": "icios cios ain ciodain quaur oteroe oas pain crofosodaur odaur",
            "Folio 78v": "ain ciodain quaur oteroe dalaiu aekiy air soar oas",
            "Folio 80r": "icios cios ain ciodain quaur oteroe"
        },
        "Farmacéutica (Recetas)": {
            "Folio 88r": "poisoda cuta podon vetí oarur osain pain oain icios cios",
            "Folio 99v": "sier ciey quaur osain aram dalaiu ciodain otiy oeteodi"
        },
        "Estrellas (Catálogo)": {
            "Folio 103r": "quidí chidí tiodau pair dais dair dam quioquey okeody"
        }
    }

# --- MOTOR DE TRADUCCIÓN INTERLINEAL ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia:
        return palabra
        
    # Búsqueda exacta en diccionario de sesión
    if palabra_limpia in st.session_state.diccionario:
        return st.session_state.diccionario[palabra_limpia]
        
    # Método adaptativo por raíces morfológicas
    if len(palabra_limpia) > 3:
        for i in range(len(palabra_limpia), 2, -1):
            sub_raiz = palabra_limpia[:i]
            # Buscar claves que empiecen con la sub-raíz
            coincidencias = [v for k, v in st.session_state.diccionario.items() if k.startswith(sub_raiz)]
            if coincidencias:
                return f"[{coincidencias[0]}]*"
                
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    if not texto:
        return ""
    lineas = texto.strip().split("\n")
    lineas_traducidas = []
    
    for linea in lineas:
        palabras = linea.split(" ")
        palabras_traducidas = [traducir_palabra(p) for p in palabras]
        frase_sucia = " ".join(palabras_traducidas)
        
        # Filtro de post-procesamiento sintáctico para limpiar artículos repetidos consecutivos
        frase_limpia = re.sub(r'\b(los|el|la|las|un|una)\b\s+(?=\b\1\b)', '', frase_sucia, flags=re.IGNORECASE)
        frase_limpia = re.sub(r'\s+', ' ', frase_limpia).strip()
        lineas_traducidas.append(frase_limpia)
        
    return "\n".join(lineas_traducidas)


# --- INTERFAZ DE USUARIO EN STREAMLIT ---
tab1, tab2, tab3 = st.tabs(["📖 Navegador del Manuscrito Completo", "🔍 Buscador de Diccionario", "📝 Añadir/Editar Datos"])

# PESTAÑA 1: EXPLORADOR DE TODAS LAS PÁGINAS
with tab1:
    st.subheader("Selector e Índice General de Folios")
    
    secciones = list(st.session_state.manuscrito.keys())
    seccion_elegida = st.selectbox("Filtrar por sección temática:", secciones)
    
    folios_disponibles = list(st.session_state.manuscrito[seccion_elegida].keys())
    folio_elegido = st.selectbox("Selecciona el Folio de la página a descifrar:", folios_disponibles)
    
    texto_folio = st.session_state.manuscrito[seccion_elegida][folio_elegido]
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Texto Transcrito Original del `{folio_elegido}`**")
        texto_editable = st.text_area("Puedes modificar el texto de la página en vivo:", texto_folio, height=150)
        
    with col2:
        st.success(f"**Descifrado Semántico Automatizado**")
        texto_descifrado = descifrar_texto_completo(texto_editable)
        st.text_area("Resultado obtenido:", texto_descifrado, height=150, disabled=True)

    st.caption("*Simbología: Las palabras con `¿?` no están en la BD; las `[]*` son aproximaciones por raíces.*")

# PESTAÑA 2: CONSULTA MANUAL DE TÉRMINOS
with tab2:
    st.subheader("Buscador predictivo del Glosario")
    busqueda = st.text_input("Introduce una palabra Voynich para ver su mapeo:")
    if busqueda:
        palabra_busqueda = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        resultados = {k: v for k, v in st.session_state.diccionario.items() if palabra_busqueda in k}
        if resultados:
            for clave, valor in resultados.items():
                st.write(f"🔹 **{clave}** ➔ {valor}")
        else:
            st.warning("No se encontraron coincidencias en el glosario.")

# PESTAÑA 3: GESTIÓN Y PERSISTENCIA DE CORPUS
with tab3:
    st.subheader("Gestión Avanzada de Datos (En memoria de Sesión)")
    
    col_dict, col_folio = st.columns(2)
    with col_dict:
        st.write("### Registrar nuevo término")
        nueva_clave = st.text_input("Nueva palabra Voynich:")
        nuevo_valor = st.text_input("Traducción / Significado:")
        if st.button("Guardar en Diccionario"):
            if nueva_clave and nuevo_valor:
                st.session_state.diccionario[nueva_clave.lower().strip()] = nuevo_valor.strip()
                st.success("¡Término guardado temporalmente con éxito!")
                st.rerun()
                
    with col_folio:
        st.write("### Actualizar texto de un folio existente")
        # Conseguimos una lista plana de todos los folios para facilitar la edición
        todos_los_folios = []
        for sec, f_dict in st.session_state.manuscrito.items():
            for f in f_dict.keys():
                todos_los_folios.append(f"{sec} - {f}")
                
        folio_update_full = st.selectbox("Folio a modificar:", todos_los_folios)
        sec_up, fol_up = folio_update_full.split(" - ")
        
        texto_actual_db = st.session_state.manuscrito[sec_up][fol_up]
        nuevo_texto_db = st.text_area("Texto definitivo para guardar:", texto_actual_db, key="area_up")
        
        if st.button("Actualizar Memoria"):
            st.session_state.manuscrito[sec_up][fol_up] = nuevo_texto_db.strip()
            st.success("¡Folio modificado con éxito en la sesión actual!")
            st.rerun()
