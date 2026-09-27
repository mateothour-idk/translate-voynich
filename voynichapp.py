import streamlit as st
import sqlite3
import re
import voynichdata

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo mediante tu técnica de reducción de caracteres y traducción instantánea.")

# --- CONEXIÓN Y ESTRUCTURACIÓN DE LA BASE DE DATOS LOCAL ---
conn = sqlite3.connect("voynich_matrix.db", check_same_thread=False)
cursor = conn.cursor()

# Forzar la recreación limpia de las tablas para limpiar registros antiguos del pasado
cursor.execute("DROP TABLE IF EXISTS diccionario")
cursor.execute("DROP TABLE IF EXISTS manuscrito")

# La tabla diccionario ahora guarda de forma bilingüe el español y el inglés de forma segura
cursor.execute("CREATE TABLE IF NOT EXISTS diccionario (clave TEXT PRIMARY KEY, valor_es TEXT, valor_en TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS manuscrito (folio TEXT PRIMARY KEY, seccion TEXT, texto_voynich TEXT)")

# Inserción masiva inicial desde el archivo de datos externos
cursor.executemany("INSERT OR IGNORE INTO diccionario VALUES (?, ?, ?)", voynichdata.glosario_inicial)
cursor.executemany("INSERT OR IGNORE INTO manuscrito VALUES (?, ?, ?)", voynichdata.obtener_corpus_completo())
conn.commit()

# --- CONFIGURACIÓN DE IDIOMA EN LA BARRA LATERAL ---
st.sidebar.header("🌍 Idioma del Descifrado")
idioma_destino = st.sidebar.selectbox(
    "Mostrar resultados en:",
    ["Español", "English (Inglés)"]
)

# Definir qué columna de la base de datos consultar según la elección del usuario
columna_idioma = "valor_es" if idioma_destino == "Español" else "valor_en"


# --- MOTOR DE TRADUCCIÓN E INTELIGENCIA DE TU TÉCNICA ---
def aplicar_tecnica_y_traducir(palabra):
    # Limpieza inicial de la palabra removiendo caracteres de puntuación periféricos
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower().strip())
    if not palabra_limpia:
        return palabra
        
    # TU TÉCNICA DE LIGADURAS: Reemplazo predictivo directo
    palabra_limpia = palabra_limpia.replace("pc", "p")
    
    significado_final = None
    es_aproximado = False
    
    # 1. Búsqueda exacta limpia extrayendo el idioma deseado directamente de la BD
    cursor.execute(f"SELECT {columna_idioma} FROM diccionario WHERE clave = ?", (palabra_limpia,))
    resultado = cursor.fetchone()
    if resultado:
        significado_final = resultado[0]
    else:
        # 2. Fallback por truncamiento de raíces morfológicas
        if len(palabra_limpia) > 3:
            for i in range(len(palabra_limpia), 2, -1):
                sub_raiz = palabra_limpia[:i]
                cursor.execute(f"SELECT {columna_idioma} FROM diccionario WHERE clave LIKE ?", (f"{sub_raiz}%",))
                res_raiz = cursor.fetchone()
                if res_raiz:
                    significado_final = res_raiz[0]
                    es_aproximado = True
                    break
                    
    # 3. Retornar el resultado estructurado sin errores de red
    if significado_final:
        return f"[{significado_final}]*" if es_aproximado else significado_final
        
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    """Procesa párrafos multilínea respetando la estructura física de la página."""
    lineas = texto.strip().split("\n")
    lineas_traducidas = []
    for linea in lineas:
        palabras = linea.split(" ")
        palabras_traducidas = [aplicar_tecnica_y_traducir(p) for p in palabras if p]
        lineas_traducidas.append(" ".join(palabras_traducidas))
    return "\n".join(lineas_traducidas)


# --- INTERFAZ GRÁFICA DE USUARIO (TABS) ---
tab1, tab2, tab3 = st.tabs(["📖 Navegador del Manuscrito Completo", "🔍 Buscador de Diccionario", "📝 Añadir/Editar Folios"])

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
        texto_editable = st.text_area("Puedes modificar o escribir código en vivo (prueba con 'pc'):", texto_folio, height=150)
        
    with col2:
        st.success(f"**Descifrado Semántico Automatizado ({idioma_destino})**")
        texto_descifrado = descifrar_texto_completo(texto_editable)
        st.text_area("Resultado obtenido:", texto_descifrado, height=150, disabled=True)

with tab2:
    st.subheader("Buscador del Glosario con Traducción Integrada")
    busqueda = st.text_input("Introduce una palabra Voynich única para comprobar tu técnica:")
    if busqueda:
        resultado_individual = aplicar_tecnica_y_traducir(busqueda)
        st.write(f"➔ **Resultado en {idioma_destino}:** {resultado_individual}")

with tab3:
    st.subheader("Indexar o Actualizar Folios del Manuscrito")
    with st.form("nuevo_folio_form"):
        f_nombre = st.text_input("Identificador del Folio (Ej: Folio 117r):")
        f_seccion = st.selectbox("Categoría/Sección:", ["Herbario (Botánica)", "Astronomía (Zodíaco)", "Cosmología (Astros)", "Balneológica (Fisiología)", "Farmacéutica (Recetas)", "Estrellas (Catálogo)"])
        f_texto = st.text_area("Contenido en texto codificado:")
        submit = st.form_submit_button("Guardar/Actualizar Folio en SQLite")
        
        if submit and f_nombre and f_texto:
            cursor.execute("INSERT OR REPLACE INTO manuscrito VALUES (?, ?, ?)", (f_nombre.strip(), f_seccion, f_texto.strip()))
            conn.commit()
            st.success(f"El `{f_nombre}` ha sido guardado exitosamente.")
