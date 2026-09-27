import streamlit as st
import sqlite3
import re
from deep_translator import GoogleTranslator
import voynichdata

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito mediante tu técnica de reducción de caracteres y traducción multiidioma.")

# --- CONEXIÓN Y ESTRUCTURACIÓN DE LA BASE DE DATOS LOCAL ---
conn = sqlite3.connect("voynich_matrix.db", check_same_thread=False)
cursor = conn.cursor()

# IMPORTANTE: Forzamos la recreación de tablas para limpiar registros corruptos anteriores
cursor.execute("DROP TABLE IF EXISTS diccionario")
cursor.execute("DROP TABLE IF EXISTS manuscrito")

cursor.execute("CREATE TABLE IF NOT EXISTS diccionario (clave TEXT PRIMARY KEY, valor TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS manuscrito (folio TEXT PRIMARY KEY, seccion TEXT, texto_voynich TEXT)")

# Inserción masiva limpia
cursor.executemany("INSERT OR IGNORE INTO diccionario VALUES (?, ?)", voynichdata.glosario_inicial)
cursor.executemany("INSERT OR IGNORE INTO manuscrito VALUES (?, ?, ?)", voynichdata.obtener_corpus_completo())
conn.commit()

# --- CONFIGURACIÓN DE IDIOMA EN LA BARRA LATERAL ---
st.sidebar.header("🌍 Traducción Global")
idioma_destino = st.sidebar.selectbox(
    "Traducir resultados al idioma:",
    ["Español", "English (Inglés)", "Latín", "Italiano", "Français (Francés)", "Deutsch (Alemán)", "Português"]
)

codigos_idiomas = {
    "Español": "es", "English (Inglés)": "en", "Latín": "la", 
    "Italiano": "it", "Français (Francés)": "fr", "Deutsch (Alemán)": "de", "Português": "pt"
}

# --- MOTOR DE TRADUCCIÓN E INTELIGENCIA DE TU TÉCNICA ---
def aplicar_tecnica_y_traducir(palabra):
    palabra_limpia = re.sub(r'[^\wíóéáú]', '', palabra.lower())
    if not palabra_limpia:
        return palabra
        
    # TU TÉCNICA DE LIGADURAS
    palabra_limpia = palabra_limpia.replace("pc", "p")
    
    significado_final = None
    
    # 1. Búsqueda exacta (Corregido con [0] para extraer la cadena de texto pura)
    cursor.execute("SELECT valor FROM diccionario WHERE clave = ?", (palabra_limpia,))
    resultado = cursor.fetchone()
    if resultado:
        significado_final = str(resultado[0])  
    else:
        # 2. Fallback adaptativo por raíces morfológicas
        if len(palabra_limpia) > 3:
            for i in range(len(palabra_limpia), 2, -1):
                sub_raiz = palabra_limpia[:i]
                cursor.execute("SELECT valor FROM diccionario WHERE clave LIKE ?", (f"{sub_raiz}%",))
                res_raiz = cursor.fetchone()
                if res_raiz:
                    significado_final = f"[{str(res_raiz[0])}]*"
                    break
                    
    # 3. Procesamiento y ejecución de la traducción a la API
    if significado_final:
        if idioma_destino != "Español":
            try:
                # Comprobar si proviene del fallback de raíces
                es_aproximado = significado_final.startswith("[")
                texto_a_traducir = significado_final.replace("[", "").replace("]*", "") if es_aproximado else significado_final
                
                # Traducción del string limpio
                traduccion = GoogleTranslator(source='es', target=codigos_idiomas[idioma_destino]).translate(texto_a_traducir)
                
                return f"[{traduccion}]*" if es_aproximado else traduccion
            except Exception:
                return significado_final
        return significado_final
        
    return f"¿{palabra}?"

def descifrar_texto_completo(texto):
    lineas = texto.strip().split("\n")
    lineas_traducidas = []
    for linea in lineas:
        palabras = linea.split(" ")
        palabras_traducidas = [aplicar_tecnica_y_traducir(p) for p in palabras]
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
