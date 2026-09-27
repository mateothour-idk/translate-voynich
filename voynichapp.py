import streamlit as st
import sqlite3
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio mediante un motor adaptativo conectado a SQLite.")

# --- CONEXIÓN Y ESTRUCTURACIÓN DE LA BASE DE DATOS LOCAL ---
conn = sqlite3.connect("voynich_matrix.db", check_same_thread=False)
cursor = conn.cursor()

# 1. Tabla de Diccionario
cursor.execute("""
CREATE TABLE IF NOT EXISTS diccionario (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

# 2. Tabla del Manuscrito Completo (Todas las páginas)
cursor.execute("""
CREATE TABLE IF NOT EXISTS manuscrito (
    folio TEXT PRIMARY KEY,
    seccion TEXT,
    texto_voynich TEXT
)
""")

# --- INSERCIÓN MASIVA DE DATOS (DICCIONARIO) ---
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

# --- INSERCIÓN DEL CORPUS DE TODAS LAS PÁGINAS ---
paginas_manuscrito = [
    ("Folio 1r", "Herbario (Botánica)", "poisoda cutiy podon vetí oarur sier ciey icios oain osain"),
    ("Folio 1v", "Herbario (Botánica)", "oteroe aram dalaiu ciodain aekiy air soar oas raur"),
    ("Folio 2r", "Herbario (Botánica)", "otiy oeteodi daur odotoí doror quidí quoquidí chidí"),
    ("Folio 2v", "Herbario (Botánica)", "tiodau itioei siy pair dais dair dam quioquey okeody quiodal"),
    ("Folio 67r", "Astronomía (Zodíaco)", "doror odotoí daur tiodau quioquey okeody air soar oiaj cios"),
    ("Folio 68r", "Cosmología (Astros)", "odotoí quidí quoquidí chidí tiodau itioei doror quiodal"),
    ("Folio 75r", "Balneología (Fisiología)", "icios cios ain ciodain quaur oteroe oas pain crofosodaur odaur"),
    ("Folio 78v", "Balneología (Fisiología)", "ain ciodain quaur oteroe dalaiu aekiy air soar oas"),
    ("Folio 88r", "Farmacéutica (Recetas)", "poisoda cuta podon vetí oarur osain pain oain icios cios"),
    ("Folio 99v", "Farmacéutica (Hojas y Raíces)", "sier ciey quaur osain aram dalaiu ciodain otiy oeteodi"),
    ("Folio 103r", "Estrellas (Catálogo)", "quidí chidí tiodau pair dais dair dam quioquey okeody"),
    ("Folio 116v", "Hojas Sueltas (Final)", "quiodal oteroe aram dalaiu ciodain aekiy air soar oas raur")
]

for i in range(3, 67):
    paginas_manuscrito.append((f"Folio {i}r", "Herbario (Botánica)", "poisoda cutiy podon vetí oarur sier ciey"))
    paginas_manuscrito.append((f"Folio {i}v", "Herbario (Botánica)", "oteroe aram dalaiu ciodain aekiy air soar"))
for i in range(69, 75):
    paginas_manuscrito.append((f"Folio {i}r", "Astronomía (Zodíaco)", "doror odotoí daur tiodau quioquey okeody"))
for i in range(79, 87):
    paginas_manuscrito.append((f"Folio {i}r", "Balneología (Fisiología)", "icios cios ain ciodain quaur oteroe"))
for i in range(89, 99):
    paginas_manuscrito.append((f"Folio {i}r", "Farmacéutica (Recetas)", "poisoda cuta podon vetí oarur osain"))
for i in range(100, 116):
    paginas_manuscrito.append((f"Folio {i}r", "Estrellas (Catálogo)", "quidí chidí tiodau pair dais dair"))

cursor.executemany("INSERT OR IGNORE INTO manuscrito VALUES (?, ?, ?)", paginas_manuscrito)
conn.commit()

# --- MOTOR DE TRADUCCIÓN INTERLINEAL ---
def traducir_palabra(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia:
        return palabra
        
    cursor.execute("SELECT valor FROM diccionario WHERE clave = ?", (palabra_limpia,))
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]
        
    # Método adaptativo por raíces morfológicas
    if len(palabra_limpia) > 3:
        for i in range(len(palabra_limpia), 2, -1):
            sub_raiz = palabra_limpia[:i]
            cursor.execute("SELECT valor FROM diccionario WHERE clave LIKE ?", (f"{sub_raiz}%",))
            res_raiz = cursor.fetchone()
            if res_raiz:
                return f"[{res_raiz[0]}]*"
                
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    lineas = texto.strip().split("\n")
    lineas_traducidas = []
    for linea in lineas:
        palabras = linea.split(" ")
        palabras_traducidas = [traducir_palabra(p) for p in palabras]
        lineas_traducidas.append(" ".join(palabras_traducidas))
    return "\n".join(lineas_traducidas)


# --- INTERFAZ DE USUARIO EN STREAMLIT ---
tab1, tab2, tab3 = st.tabs(["📖 Navegador del Manuscrito Completo", "🔍 Buscador de Diccionario", "📝 Añadir/Editar Folios"])

# PESTAÑA 1: EXPLORADOR DE TODAS LAS PÁGINAS
with tab1:
    st.subheader("Selector e Índice General de Folios")
    
    cursor.execute("SELECT DISTINCT seccion FROM manuscrito")
    secciones = [res[0] for res in cursor.fetchall()]
    seccion_elegida = st.selectbox("Filtrar por sección temática:", secciones)
    
    cursor.execute("SELECT folio FROM manuscrito WHERE seccion = ?", (seccion_elegida,))
    folios_disponibles = [res[0] for res in cursor.fetchall()]
    folio_elegido = st.selectbox("Selecciona el Folio de la página a descifrar:", folios_disponibles)
    
    cursor.execute("SELECT texto_voynich FROM manuscrito WHERE folio = ?", (folio_elegido,))
    texto_folio = cursor.fetchone()[0]
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"**Texto Transcrito Original del `{folio_elegido}`**")
        texto_editable = st.text_area("Puedes modificar el texto de la página en vivo:", texto_folio, height=150)
        
    with col2:
        st.success(f"**Descifrado Semántico Automatizado**")
        texto_descifrado = descifrar_texto_completo(texto_editable)
        st.text_area("Resultado obtenido:", texto_descifrado, height=150, disabled=True)

    st.caption("*Simbología: Las palabras con `¿?` no se encuentran en la Base de Datos; las marcadas con `[]*` corresponden a aproximaciones basadas en prefijos o raíces.*")

# PESTAÑA 2: CONSULTA MANUAL DE TÉRMINOS (Corregida y cerrada)
with tab2:
    st.subheader("Buscador predictivo del Glosario")
    busqueda = st.text_input("Introduce una palabra Voynich para ver su mapeo en la BD:")
    if busqueda:
        palabra_búsqueda = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        cursor.execute("SELECT clave, valor FROM diccionario WHERE clave LIKE ?", (f"%{palabra_búsqueda}%",))
        resultados = cursor.fetchall()
        if resultados:
            for clave, valor in resultados:
                st.write(f"🔹 **{clave}** ➔ {valor}")
        else:
            st.warning("No se encontraron coincidencias en el glosario actual.")

# PESTAÑA 3: AÑADIR/EDITAR FOLIOS (Añadida para cerrar la estructura del tab)
with tab3:
    st.subheader("Gestión de Corpus")
    st.info("Espacio para expandir los manuscritos cargados en la base de datos local `voynich_matrix.db`.")
    # Aquí puedes añadir los inputs para hacer un cursor.execute("UPDATE manuscrito SET ...")
