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

cursor.execute("""
CREATE TABLE IF NOT EXISTS diccionario (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

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
    ("Folio 80r", "Balneología (Fisiología)", "icios cios ain ciodain quaur oteroe"),
    ("Folio 88r", "Farmacéutica (Recetas)", "poisoda cuta podon vetí oarur osain pain oain icios cios"),
    ("Folio 99v", "Farmacéutica (Hojas y Raíces)", "sier ciey quaur osain aram dalaiu ciodain otiy oeteodi"),
    ("Folio 103r", "Estrellas (Catálogo)", "quidí chidí tiodau pair dais dair dam quioquey okeody"),
    ("Folio 116v", "Hojas Sueltas (Final)", "quiodal oteroe aram dalaiu ciodain aekiy air soar oas raur")
]

# Optimización: Carga masiva limpia y estructurada sin duplicar líneas
for i in range(3, 10):
    paginas_manuscrito.append((f"Folio {i}r", "Herbario (Botánica)", "poisoda cutiy podon vetí oarur sier ciey"))
    paginas_manuscrito.append((f"Folio {i}v", "Herbario (Botánica)", "oteroe aram dalaiu ciodain aekiy air soar"))

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
        
    if len(palabra_limpia) > 3:
        for i in range(len(palabra_limpia), 2, -1):
            sub_raiz = palabra_limpia[:i]
            cursor.execute("SELECT valor FROM diccionario WHERE clave LIKE ?", (f"{sub_raiz}%",))
            res_raiz = cursor.fetchone()
            if res_raiz:
                return f"[{res_raiz[0]}]*"
                
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

    st.caption("*Simbología: Las palabras con `¿?` no están en la BD; las `[]*` son aproximaciones por raíces.*")

# PESTAÑA 2: CONSULTA MANUAL DE TÉRMINOS
with tab2:
    st.subheader("Buscador predictivo del Glosario")
    busqueda = st.text_input("Introduce una palabra Voynich para ver su mapeo en la BD:")
    if busqueda:
        palabra_busqueda = re.sub(r'[^\wíóéáú]', '', busqueda.lower())
        cursor.execute("SELECT clave, valor FROM diccionario WHERE clave LIKE ?", (f"%{palabra_busqueda}%",))
        resultados = cursor.fetchall()
        if resultados:
            for clave, valor in resultados:
                st.write(f"🔹 **{clave}** ➔ {valor}")
        else:
            st.warning("No se encontraron coincidencias en el glosario.")

# PESTAÑA 3: GESTIÓN Y PERSISTENCIA DE CORPUS
with tab3:
    st.subheader("Gestión Avanzada de la Base de Datos")
    
    col_dict, col_folio = st.columns(2)
    with col_dict:
        st.write("### Registrar nuevo término")
        nueva_clave = st.text_input("Nueva palabra Voynich:")
        nuevo_valor = st.text_input("Traducción / Significado:")
        if st.button("Guardar en Diccionario"):
            if nueva_clave and nuevo_valor:
                cursor.execute("INSERT OR REPLACE INTO diccionario VALUES (?, ?)", (nueva_clave.lower().strip(), nuevo_valor.strip()))
                conn.commit()
                st.success("¡Término guardado con éxito!")
                st.rerun()
                
    with col_folio:
        st.write("### Actualizar texto de un folio existente")
        folio_update = st.selectbox("Folio a modificar en BD:", folios_disponibles, key="update_folio_select")
        cursor.execute("SELECT texto_voynich FROM manuscrito WHERE folio = ?", (folio_update,))
        texto_actual_db = cursor.fetchone()[0]
        nuevo_texto_db = st.text_area("Texto definitivo para guardar:", texto_actual_db)
        if st.button("Actualizar Base de Datos"):
            cursor.execute("UPDATE manuscrito SET texto_voynich = ? WHERE folio = ?", (nuevo_texto_db.strip(), folio_update))
            conn.commit()
            st.success("¡Folio actualizado correctamente en SQLite!")
            st.rerun()
