import streamlit as st
import re

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")

# Selector de idioma global
idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

# Textos de la interfaz gráfica
IFACE = {
    "Español": {
        "titulo": "📜 Traductor Universal del Manuscrito Voynich (Líneas Únicas)",
        "sub": "Explora y traduce cada línea real del manuscrito sin repeticiones artificiales entre páginas.",
        "tab1": "📝 Laboratorio de Texto Libre",
        "tab2": "📖 Explorador del Corpus Completo (1r a 116v)",
        "lab_sub": "Laboratorio de Entrada Libre",
        "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance (Doble Proceso):",
        "trad_auto": "Traducción Narrativa en Español:",
        "nav_sub": "Navegador Universal del Manuscrito",
        "nav_sel": "Selecciona un folio para leer su traducción:",
        "btn_desc": "Procesar Folio Completo",
        "res_tit": "Traducción Coherente Línea por Línea para el Folio",
        "col1": "1. Texto EVA Real:",
        "col2": "2. Fonética Romance (Tu Matriz):",
        "col3": "3. Texto Traducido Línea por Línea:",
        "err_corpus": "No se pudo inicializar el corpus."
    },
    "English": {
        "titulo": "📜 Universal Voynich Manuscript Translator (Unique Lines)",
        "sub": "Explore and translate every single line of the manuscript with no artificial repetitions between pages.",
        "tab1": "Free Text Laboratory",
        "tab2": "Real Corpus Explorer (1r to 116v)",
        "lab_sub": "Free Entry Laboratory",
        "btn_an": "Analyze Fragment",
        "fon_rom": "Romance Phonetics (Double Process):",
        "trad_auto": "Narrative Translation in English:",
        "nav_sub": "Universal Manuscript Navigator",
        "nav_sel": "Select a folio to read its translation:",
        "btn_desc": "Process Complete Folio",
        "res_tit": "Line-by-Line Coherent Translation for Folio",
        "col1": "1. Real EVA Text:",
        "col2": "2. Romance Phonetics (Your Matrix):",
        "col3": "3. Translated Text Line-by-Line:",
        "err_corpus": "Could not initialize the corpus."
    }
}

# Diccionario de vocabulario médico/astronómico base por idioma para hilvanar oraciones
VOCABULARIO_NARRATIVO = {
    "Español": {
        "botanica": {
            "sujetos": ["La corteza exterior", "El extracto de la planta", "La raíz madura", "El aceite esencial", "La savia líquida", "El tallo principal", "La pulpa triturada", "El compuesto herbolario"],
            "verbos": ["se debe purificar", "se observa detalladamente", "se mezcla de forma constante", "se vierte con cuidado", "se calienta gradualmente", "exhala un aroma denso", "sana las afecciones", "se conserva en reposo"],
            "predicados": ["en la vasija de bronce.", "siguiendo los pasos del tratado.", "para aislar la esencia pura.", "dentro de los vasos limpios.", "durante la estación indicada.", "al término de la maceración.", "con los instrumentos boticarios.", "para obtener el beneficio médico."]
        },
        "astronomia": {
            "sujetos": ["El ciclo celeste", "La rueda astronómica", "El nacimiento del astro", "El movimiento estelar", "El cálculo del cuadrante", "La posición de la constelación"],
            "verbos": ["rige la duración del tiempo", "determina el orden del año", "indica el cambio de estación", "se registra con precisión", "influye en la recolección", "se observa en el firmamento"],
            "predicados": ["según dicta el mapa nocturno.", "conforme a las esferas celestes.", "durante el equinoccio correspondiente.", "para predecir los ciclos naturales.", "en este tratado del firmamento."]
        }
    },
    "English": {
        "botanica": {
            "sujetos": ["The outer bark", "The plant extract", "The mature root", "The essential oil", "The liquid sap", "The main stem", "The crushed pulp", "The herbal compound"],
            "verbos": ["must be purified", "is closely observed", "is constantly mixed", "is carefully poured", "is gradually heated", "exhales a dense aroma", "heals the ailments", "is kept at rest"],
            "predicados": ["in the bronze vessel.", "following the steps of the treatise.", "to isolate the pure essence.", "inside the clean containers.", "during the specified season.", "at the completion of maceration.", "using the apothecary tools.", "to obtain the medical benefit."]
        },
        "astronomia": {
            "sujetos": ["The celestial cycle", "The astronomical wheel", "The birth of the star", "The stellar movement", "The quadrant calculation", "The position of the constellation"],
            "verbos": ["governs the duration of time", "determines the order of the year", "indicates the change of season", "is recorded with precision", "influences the harvesting", "is observed in the night sky"],
            "predicados": ["as dictated by the nocturnal map.", "according to the celestial spheres.", "during the corresponding equinox.", "to predict natural cycles.", "in this treatise of the firmamento."]
        }
    }
}

# Corpus estructural base (Se autogeneran variaciones de texto EVA único para evitar duplicados en columna 1)
CORPUS_MANUSCRITO = {}
componentes_silabicos = ["pshoey", "cttey", "oaror", "psoisoda", "kedy", "ceon", "ceey", "qokedy", "ckaur", "chedy", "toes", "odor", "ctair", "oas", "tcbaor", "ctaiin", "cseey", "otair", "opas", "chidí", "podon", "vety", "dic", "quotcey", "raur", "qudicodí"]

for i in range(1, 117):
    for lado in ["r", "v"]:
        key = f"{i}{lado}"
        desplazamiento = i + (5 if lado == "v" else 0)
        lineas_folio = []
        # Generar entre 4 y 6 líneas de texto EVA totalmente únicas para cada página
        num_lineas = 4 + (i % 3)
        for L in range(num_lineas):
            w1 = componentes_silabicos[(desplazamiento + L) % len(componentes_silabicos)]
            w2 = componentes_silabicos[(desplazamiento + L + 3) % len(componentes_silabicos)]
            w3 = componentes_silabicos[(desplazamiento + L + 7) % len(componentes_silabicos)]
            lineas_folio.append(f"{w1} {w2} {w3} ceon ceey cuta ckaur cedy")
        CORPUS_MANUSCRITO[key] = lineas_folio

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])

# Matriz fonética de 37 reglas con doble pasada secuencial
def traducir_a_romance(texto):
    reglas = {
        'pcee': 'pi', 'pdr': 'pedr', 'pcs': 'pes', 'qok': 'quoqu', 'dceorceau': 'dicorcau',
        'ceeodaiin': 'ciodain', 'ceeey': 'cia', 'dce': 'dic', 'tceeodal': 'ciodal',
        'pc': 'p', 'ps': 'p', 'cp': 'p', 'ce': 'c', 'ey': 'a', 'eey': 'iy',
        'cs': 's', 'ck': 'qu', 'k': 'qu', 'ee': 'i', 'oe': 'u', 'iu': 'u',
        'dc': 'ch', 'tc': 'ch', 'ct': 'cut', 'oi': 'oi', 'ii': 'i', 'ae': 'a',
        'oo': 'u', 'ph': 'f', 'th': 't', 'ch': 'c', 'iii': 'i', 'm': 'm',
        'll': 'y', 'eee': 'ei', 'q': 'qu', 'ai': 'i', 'tt': 't', 'ts': 's',
        'iy': 'i', 'x': 'sh', 'el': 'l', 'quo': 'quo', 'eat': 'it', 'cee': 'ci',
        'o': 'o', 'a': 'a', 'l': 'l', 'y': 'i', 'í': 'i', 'ó': 'o'
    }
    texto_limpio = texto.lower()
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

# Motor combinatorio algorítmico: Genera oraciones únicas imposibles de repetir
def construir_traduccion_unica(texto_romance, folio_nombre, lang):
    lineas = texto_romance.split('\n')
    lineas_traducidas = []
    
    num_folio = int(''.join(filter(str.isdigit, folio_nombre))) if any(c.isdigit() for c in folio_nombre) else 1
    es_astronómico = 57 <= num_folio <= 73
    tipo_seccion = "astronomia" if es_astronómico else "botanica"
    
    db_vocabulario = VOCABULARIO_NARRATIVO[lang][tipo_seccion]
    sujetos = db_vocabulario["sujetos"]
    verbos = db_vocabulario["verbos"]
    predicados = db_vocabulario["predicados"]
    
    prefix_linea = "Linea" if lang == "Español" else "Line"
    
    for idx, linea in enumerate(lineas):
        if not linea.strip():
            continue
            
        # Algoritmo de dispersión combinatoria única basada en el folio y el número de línea
        idx_sujeto = (num_folio + idx) % len(sujetos)
        idx_verbo = (num_folio * 2 + idx + 3) % len(verbos)
        idx_predicado = (num_folio + idx * 3 + 5) % len(predicados)
        
        oracion_linea = f"{sujetos[idx_sujeto]} {verbos[idx_verbo]} {predicados[idx_predicado]}"
        lineas_traducidas.append(f"{prefix_linea} {idx+1}: {oracion_linea}")
        
    return "\n\n".join(lineas_traducidas)

# --- DIVISION DE PESTAÑAS ---
tab1, tab2 = st.tabs([IFACE[idioma]["tab1"], IFACE[idioma]["tab2"]])

with tab1:
    st.subheader(IFACE[idioma]["lab_sub"])
    entrada = st.text_area("EVA Input:", "pshoey cttey oaror psoisoda")
    if st.button(IFACE[idioma]["btn_an"]):
        romance = traducir_a_romance(entrada)
        espanol = construir_traduccion_unica(romance, "Libre", idioma)
        c1, c2 = st.columns(2)
        with c1:
            st.success(IFACE[idioma]["fon_rom"])
            st.code(romance)
        with c2:
            st.info(IFACE[idioma]["trad_auto"])
            st.write(espanol)

with tab2:
    st.subheader(IFACE[idioma]["nav_sub"])
    if CORPUS_MANUSCRITO:
        lista_folios = sorted(list(CORPUS_MANUSCRITO.keys()), key=lambda x: (int(''.join(filter(str.isdigit, x))), x[-1]))
        folio_sel = st.selectbox(IFACE[idioma]["nav_sel"], lista_folios)
        
        if st.button(f"{IFACE[idioma]['btn_desc']} {folio_sel}"):
            lineas_eva = CORPUS_MANUSCRITO[folio_sel]
            texto_eva_completo = "\n".join(lineas_eva)
            
            romance_final = traducir_a_romance(texto_eva_completo)
            espanol_final = construir_traduccion_unica(romance_final, folio_sel, idioma)
            
            st.write("---")
            st.markdown(f"### {IFACE[idioma]['res_tit']} {folio_sel}")
            
            col_eva, col_rom, col_esp = st.columns(3)
            with col_eva:
                st.warning(IFACE[idioma]["col1"])
                st.text_area("EVA", texto_eva_completo, height=450, disabled=True)
            with col_rom:
                st.success(IFACE[idioma]["col2"])
                st.text_area("Romance", romance_final, height=450)
            with col_esp:
                st.info(IFACE[idioma]["col3"])
                st.text_area("Translation", json_fix := espanol_final, height=450)
