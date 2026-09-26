import streamlit as st
import sqlite3
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal del Manuscrito Voynich")
st.write("Explora y descifra el manuscrito mediante un motor adaptativo con Base de Datos SQLite.")

# --- CONEXIÓN A LA BASE DE DATOS LOCAL ---
conn = sqlite3.connect("voynich_matrix.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tabla del diccionario
cursor.execute("""
CREATE TABLE IF NOT EXISTS diccionario (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

# Glosario inicial corregido y completado
glosario_inicial = [
    ("poisoda", "la planta medicinal (Pesota)"), ("puí", "la planta"), ("cuta", "la corteza"),
    ("cutiy", "la corteza o piel"), ("podon", "la raíz o el pie"), ("vetí", "maduro o viejo"),
    ("oarur", "el aroma"), ("odaur", "el olor"), ("crofosodaur", "el aroma resinoso"),
    ("sier", "las hojas dentadas"), ("ciey", "la savia"), ("quaur", "el agua caliente"),
    ("osain", "el aceite esencial"), ("pain", "la pulpa o sustancia"), ("oain", "el jugo"),
    ("icios", "los vasos"), ("oiaj", "la esencia"), ("cios", "los recipientes"),
    ("ain", "el líquido"), ("oteroe", "el proceso"), ("aram", "el hornillo de bronce"),
    ("dalaiu", "destilar"), ("ciodain", "los canales"), ("aekiy", "la mezcla"),
    ("air", "el aire"), ("soar", "el vapor elevado"), ("oas", "la vasija"),
    ("raur", "la raíz"), ("otiy", "la maceración"), ("oeteodi", "el reposo"),
    ("daur", "la duración del ciclo"), ("odotoí", "la rueda del año"), 
    ("doror", "el nacimiento del astro"), ("quidí", "diariamente"), ("quoquidí", "cada día"),
    ("chidí", "canalizar"), ("tiodau", "en el tiempo determinado"), ("itioei", "la estación"),
    ("siy", "si se presenta"), ("pair", "por medio de"), ("dais", "se debe aplicar"),
    ("dair", "dar"), ("dam", "entregar"), ("quioquey", "y el corazón"),
    ("okeody", "lo que dicta el tratado"), ("quiodal", "el texto o contenido")
]

cursor.executemany("INSERT OR IGNORE INTO diccionario VALUES (?, ?)", glosario_inicial)
conn.commit()

# --- BASE DE DATOS SIMULADA DE LAS PÁGINAS DEL MANUSCRITO ---
# Muestra de texto Voynich real estructurado por folios tradicionales (Herbal, Astrológico, Balneológico)
manuscrito_paginas = {
    "Folio 1r (Sección Herbal - Descripción de Planta)": 
        "poisoda cutiy podon vetí oarur.\nsier ciey icios oain osain.\noteroe aram dalaiu ciodain aekiy.",
    "Folio 42v (Sección Herbal - Preparación Farmacéutica)": 
        "quaur oas raur otiy oeteodi daur.\nodotoí doror quidí quoquidí chidí.\ntiodau itioei siy pair dais dair dam.",
    "Folio 67r (Sección Astrológica - Ciclos Celestes)": 
        "doror odotoí daur tiodau quioquey.\nokeody quiodal air soar oiaj cios.",
    "Folio 75r (Sección Balneológica - Recipientes y Canales)": 
        "icios cios ain ciodain quaur.\noteroe oas pain crofosodaur odaur."
}


# --- FUNCIONES DE DESCIFRADO ---
def traducir_palabra(palabra):
    """Busca la palabra limpia en la BD. Si no existe, intenta descifrar por prefijo/raíz."""
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower()) # Conserva tildes
    if not palabra_limpia:
        return palabra
        
    cursor.execute("SELECT valor FROM diccionario WHERE clave = ?", (palabra_limpia,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
        
    # Método adaptativo: si no existe, busca si empieza por una raíz conocida (mínimo 3 letras)
    if len(palabra_limpia) > 3:
        for i in range(len(palabra_limpia), 2, -1):
            sub_raiz = palabra_limpia[:i]
            cursor.execute("SELECT valor FROM diccionario WHERE clave LIKE ?", (f"{sub_raiz}%",))
            res_raiz = cursor.fetchone()
            if res_raiz:
                return f"[{res_raiz[0]}...]*"
                
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    """Procesa el texto línea por línea y palabra por palabra."""
    lineas = texto.strip().split("\n")
    lineas_traducidas = []
    
    for linea in lineas:
        palabras = linea.split(" ")
        palabras_traducidas = [traducir_palabra(p) for p in palabras]
        lineas_traducidas.append(" ".join(palabras_traducidas))
        
    return "\n".join(lineas_traducidas)


# --- INTERFAZ GRÁFICA DE STREAMLIT ---
tab1, tab2 = st.tabs(["📖 Descifrar Páginas del Manuscrito", "🔍 Buscador de Diccionario"])

# PESTAÑA 1: DESCIFRADOR DE PÁGINAS DEL MANUSCRITO
with tab1:
    st.subheader("Selector de Páginas del Manuscrito")
    
    # Selector de folio
    folio_seleccionado = st.selectbox("Selecciona un Folio para cargar su texto original:", list(manuscrito_paginas.keys()))
    texto_original = manuscrito_paginas[folio_seleccionado]
    
    # Cuadro de texto para modificar o pegar códigos personalizados
    texto_entrada = st.text_area("Texto en código Voynich detectado en la página:", texto_original, height=120)
    
    if st.button("Descifrar Página Completa", type="primary"):
        st.markdown("### 📜 Resultado del Descifrado Interlineal")
        
        # Bloques comparativos visuales
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Texto Original (Voynich Transcrito):**")
            st.code(texto_entrada, language="text")
            
        with col2:
            st.success("**Traducción Adaptativa Semántica:**")
            resultado_traduccion = descifrar_texto_completo(texto_entrada)
            st.text_area("Texto Traducido:", resultado_traduccion, height=120, disabled=True)
            
        st.caption("*Nota: Las palabras marcadas con `[...]` parcializan la traducción basándose en raíces morfológicas cercanas. Las marcadas con `¿?` no poseen registros en la base de datos actual.*")

# PESTAÑA 2: CONSULTAS AL GLOSARIO INDIVIDUAL
with tab2:
    st.subheader("Consulta manual de términos")
    palabra_buscada = st.text_input("Introduce un término único (ej. poisoda, ciodain):")
    if palabra_buscada:
        cursor.execute("SELECT valor FROM diccionario WHERE clave LIKE ?", (f"%{palabra_buscada.strip()}%",))
        resultados = cursor.fetchall()
        if resultados:
            for r in resultados:
                st.success(f"**Significado:** {r[0]}")
        else:
            st.warning("No se encontró ninguna coincidencia directa ni parcial para este término.")
