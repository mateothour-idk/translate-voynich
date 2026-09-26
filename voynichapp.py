import streamlit as st
import sqlite3
import re

st.set_page_config(page_title="Traductor Voynich DB", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal del Manuscrito Voynich")
st.write("Explora el manuscrito mediante un motor adaptativo con Base de Datos SQLite integrada.")

# --- APERTURA Y CONFIGURACIÓN AUTOMÁTICA DE LA BASE DE DATOS LOCAL ---
conn = sqlite3.connect("voynich_matrix.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tablas estructurales si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS diccionario (
    clave TEXT PRIMARY KEY,
    valor TEXT
)
""")

# Insertar el glosario especializado de forma masiva y segura
glosario_inicial = [
    ("poisoda", "la planta medicinal (Pesota)"),
    ("puí", "la planta"),
    ("cuta", "la corteza"),
    ("cutiy", "la corteza o piel"),
    ("podon", "la raíz o el pie"),
    ("vetí", "maduro o viejo"),
    ("oarur", "el aroma"),
    ("odaur", "el olor"),
    ("crofosodaur", "el aroma resinoso"),
    ("sier", "las hojas dentadas"),
    ("ciey", "la savia"),
    ("quaur", "el agua caliente"),
    ("osain", "el aceite esencial"),
    ("pain", "la pulpa o sustancia"),
    ("oain", "el jugo"),
    ("icios", "los vasos"),
    ("oiaj", "la esencia"),
    ("cios", "los recipientes"),
    ("ain", "el líquido"),
    ("oteroe", "el proceso"),
    ("aram", "el hornillo de bronce"),
    ("dalaiu", "destilar"),
    ("ciodain", "los canales"),
    ("aekiy", "la mezcla"),
    ("air", "el aire"),
    ("soar", "el vapor elevado"),
    ("oas", "la vasija"),
    ("raur", "la raíz"),
    ("otiy", "la maceración"),
    ("oeteodi", "el reposo"),
    ("daur", "la duración del ciclo"),
    ("odotoí", "la rueda del año"),
    ("doror", "el nacimiento del astro"),
    ("quidí", "diariamente"),
    ("quoquidí", "cada día"),
    ("chidí", "canalizar"),
    ("tiodau", "en el tiempo determinado"),
    ("itioei", "la estación"),
    ("siy", "si se presenta"),
    ("pair", "por medio de"),
    ("dais", "se debe aplicar"),
    ("dair", "dar"),
    ("dam", "entregar"),
    ("quioquey", "y el corazón"),
    ("okeody", "lo que dicta el tratado"),
    ("quiodal", "el texto o contenido")  # Elemento final cerrado correctamente
]

# Ejecutar inserción masiva en SQLite
cursor.executemany("INSERT OR IGNORE INTO diccionario VALUES (?, ?)", glosario_inicial)
conn.commit()

# Interfaz de búsqueda interactiva
st.subheader("Motor de Búsqueda de Glosario")
palabra_buscada = st.text_input("Introduce una palabra en código Voynich:")

if palabra_buscada:
    cursor.execute("SELECT valor FROM diccionario WHERE clave LIKE ?", (f"%{palabra_buscada.strip()}%",))
    resultados = cursor.fetchall()
    if resultados:
        for r in resultados:
            st.success(f"**Traducción:** {r[0]}")
    else:
        st.warning("No se encontró ninguna coincidencia en la base de datos.")
