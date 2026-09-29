import streamlit as st
import re
from voynichdata import DICCIONARIO_ES, DICCIONARIO_EN, CORPUS_MANUSCRITO

st.set_page_config(page_title="Universal Voynich Translator", page_icon="📜", layout="wide")

# Selector de idioma global en la barra lateral
idioma = st.sidebar.selectbox("🌐 Select Language / Selecciona Idioma", ["Español", "English"])

IFACE = {
    "Español": {
        "titulo": "Traductor Universal del Manuscrito Voynich (Matriz Definitiva)",
        "sub": "Explora y descifra cada línea real del manuscrito aplicando tu matriz expandida de doble procesamiento estricto.",
        "tab1": "Laboratorio de Texto Libre",
        "tab2": "Explorador del Corpus Real del Manuscrito (1r a 116v)",
        "lab_sub": "Laboratorio de Entrada Libre",
        "btn_an": "Analizar Fragmento",
        "fon_rom": "Fonética Romance Optimizada (Matriz Actualizada):",
        "trad_auto": "Traducción Literal Palabra por Palabra:",
        "nav_sub": "Traductor de Folios Continuo",
        "nav_sel": "Selecciona un folio del manuscrito entero:",
        "btn_desc": "Descifrar Folio",
        "res_tit": "Traducción Literal Estricta para el Folio",
        "col1": "1. Texto EVA Real del Manuscrito:",
        "col2": "2. Fonética Romance Sincronizada:",
        "col3": "3. Traducción Real (Orden Medieval Estricto):"
    },
    "English": {
        "titulo": "Universal Automatic Voynich Manuscript Translator (Final Matrix)",
        "sub": "Explore and translate every single line using your updated double-processing matrix with maximum rigor.",
        "tab1": "Free Text Laboratory",
        "tab2": "Real Manuscript Corpus Explorer (1r to 116v)",
        "lab_sub": "Free Entry Laboratory",
        "btn_an": "Analyze Fragment",
        "fon_rom": "Optimized Romance Phonetics (Updated Matrix):",
        "trad_auto": "Literal Word-by-Word Translation:",
        "nav_sub": "Automatic Folios Navigator (All Pages)",
        "nav_sel": "Select a folio from the entire manuscript:",
        "btn_desc": "Decipher Real Folio",
        "res_tit": "Strict Literal Translation for Folio",
        "col1": "1. Real EVA Text from Manuscript:",
        "col2": "2. Aligned Romance Phonetics:",
        "col3": "3. Real Translation (Strict Medieval Word Order):"
    }
}

st.title(IFACE[idioma]["titulo"])
st.write(IFACE[idioma]["sub"])

def distancia_levenshtein(s1, s2):
    if len(s1) < len(s2):
        return distancia_levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    fila_previa = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        fila_actual = [i + 1]
        for j, c2 in enumerate(s2):
            inserciones = fila_previa[j + 1] + 1
            eliminaciones = fila_actual[j] + 1
            sustituciones = fila_previa[j] + (c1 != c2)
            fila_actual.append(min(inserciones, eliminaciones, sustituciones))
        fila_previa = fila_actual
    return fila_previa[-1]

# --- TRANSLITERADOR EXPANDIDO CON TU MATRIZ DE REGLAS ACTUALIZADA ---
def traducir_a_romance(texto):
    dicc_activo = DICCIONARIO_ES if idioma == "Español" else DICCIONARIO_EN
    
    # 1. Pipeline de Limpieza Física y Normalización EVA
    texto_limpio = texto.lower()
    texto_limpio = re.sub(r'[^a-z0-9\s]', '', texto_limpio)
    palabras = texto_limpio.split()
    
    fonetica_lista = []
    traduccion_lista = []
    
    for pal in palabras:
        # 2. Matriz Estricta de Transliteración Fonética Romance
        fon = pal
        fon = re.sub(r'^qok', 'qu', fon)
        fon = re.sub(r'^eeey', 'ey', fon)
        fon = re.sub(r'ii', 'i', fon)
        fon = re.sub(r'ck', 'c', fon)
        fon = re.sub(r'^k', 'qu', fon)
        fon = re.sub(r'([a-z])\1+', r'\1', fon) # Remueve caracteres duplicados de baja entropía
        fonetica_lista.append(fon)
        
        # 3. Mapeo por Distancia de Levenshtein contra el Diccionario Activo
        if fon in dicc_activo:
            traduccion_lista.append(dicc_activo[fon])
        else:
            mejor_coincidencia = None
            distancia_minima = float('inf')
            
            for clave in dicc_activo.keys():
                dist = distancia_levenshtein(fon, clave)
                if dist < distancia_minima:
                    distancia_minima = dist
                    mejor_coincidencia = clave
            
            # Umbral de tolerancia de mutación de baja entropía
            if distancia_minima <= 2 and mejor_coincidencia:
                traduccion_lista.append(dicc_activo[mejor_coincidencia] + "*")
            else:
                traduccion_lista.append(f"[{pal}]") # Mantiene el token original si está fuera de rango
                
    return " ".join(fonetica_lista), " ".join(traduccion_lista)

# --- INTERFAZ DE USUARIO (TABS) ---
tab1, tab2 = st.tabs([IFACE[idioma]["tab1"], IFACE[idioma]["tab2"]])

with tab1:
    st.subheader(IFACE[idioma]["lab_sub"])
    area_texto = st.text_area("Input EVA Text / Introduce Texto EVA:", value="pshoey cttey oaror psoisoda")
    if st.button(IFACE[idioma]["btn_an"]):
        fon, trad = traducir_a_romance(area_texto)
        st.markdown(f"**{IFACE[idioma]['fon_rom']}** `{fon}`")
        st.success(f"**{IFACE[idioma]['trad_auto']}** {trad}")

with tab2:
    st.subheader(IFACE[idioma]["nav_sub"])
    
    # Ordenación natural de los folios (1r, 1v, 2r, 2v...)
    folios_ordenados = sorted(list(CORPUS_MANUSCRITO.keys()), key=lambda x: (int(re.sub(r'\D', '', x)), x[-1]))
    folio_sel = st.selectbox(IFACE[idioma]["nav_sel"], folios_ordenados)
    
    if st.button(IFACE[idioma]["btn_desc"]):
        st.markdown(f"### {IFACE[idioma]['res_tit']} {folio_sel}")
        lineas = CORPUS_MANUSCRITO[folio_sel]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**{IFACE[idioma]['col1']}**")
            for l in lineas:
                st.write(l)
                
        with col2:
            st.markdown(f"**{IFACE[idioma]['col2']}**")
            for l in lineas:
                fon, _ = traducir_a_romance(l)
                st.write(fon)
                
        with col3:
            st.markdown(f"**{IFACE[idioma]['col3']}**")
            for l in lineas:
                _, trad = traducir_a_romance(l)
                st.write(trad)
