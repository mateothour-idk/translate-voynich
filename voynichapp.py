# --- ARCHIVO 2: voynichapp.py ---
import streamlit as st
import re
import voynichdatos as vd

# Forzar la carga limpia de datos al arrancar la app
if not vd.CORPUS_MANUSCRITO:
    vd.cargar_todas_las_paginas_reales()

# =============================================================================
# REGLAS DEL ALGORITMO CRIPTOGRÁFICO
# =============================================================================

REGLAS_FONETICAS_FIJAS = {
    'ai': 'ai', 'ax': 'sh', 'ct': 'ct', 'eee': 'ie', 'eey': 'iy', 
    'el': 'el', 'ey': 'a', 'iu': 'u', 'lf': 'lef', 'll': 'y', 
    'oe': 'u', 'oi': 'oi', 'oo': 'u', 'pcs': 'pes', 'q': 'qu', 
    'qok': 'quoqu', 'quo': 'quo', 'tcs': 'tes', 'th': 't', 'tt': 't'
}

MODIFICADORES_CONTEXTUALES = {
    'c': {'s': 's', 'k': 'qu', 'e': 'e', 'ee': 'ce', 't': 't'},
    't': {'c': 'ch', 's': 's', 'h': 't'},
    'p': {'s': 'f', 'h': 'f'}
}

def limpiar_fonetica_posicional(palabra_eva):
    """Limpia los glifos de EVA para remover acumulaciones imposibles."""
    if not palabra_eva:
        return ""
    resultado = []
    i = 0
    longitud = len(palabra_eva)
    while i < longitud:
        glifo_3 = palabra_eva[i:i+3]
        glifo_2 = palabra_eva[i:i+2]
        glifo_1 = palabra_eva[i]
        
        if glifo_3 in REGLAS_FONETICAS_FIJAS:
            resultado.append(REGLAS_FONETICAS_FIJAS[glifo_3])
            i += 3
        elif glifo_2 in REGLAS_FONETICAS_FIJAS:
            resultado.append(REGLAS_FONETICAS_FIJAS[glifo_2])
            i += 2
        elif len(resultado) > 0 and resultado[-1] in MODIFICADORES_CONTEXTUALES:
            letra_previa = resultado[-1]
            if glifo_1 in MODIFICADORES_CONTEXTUALES[letra_previa]:
                resultado[-1] = MODIFICADORES_CONTEXTUALES[letra_previa][glifo_1]
            else:
                resultado.append(glifo_1)
            i += 1
        else:
            if glifo_1 == 'y':
                resultado.append('i')
            else:
                resultado.append(glifo_1)
            i += 1
    palabra_final = "".join(resultado)
    palabra_final = re.sub(r'i+', 'i', palabra_final)
    palabra_final = re.sub(r'c+', 'c', palabra_final)
    return palabra_final

def traducir_palabra_automatica(palabra_eva, diccionario):
    """Busca y extrae la traducción desde la clave limpia del diccionario."""
    p_limpia = limpiar_fonetica_posicional(palabra_eva.lower().replace('íd', 'id').replace('í', 'i'))
    if p_limpia in diccionario:
        return diccionario[p_limpia]
    return f"[{p_limpia}]"

def traducir_palabra_manual(palabra_eva, mapa_manual):
    """Traducción interactiva por caracteres usando el mapa personalizado del usuario."""
    resultado = []
    for letra in palabra_eva.lower():
        if letra in mapa_manual and mapa_manual[letra].strip():
            resultado.append(mapa_manual[letra].strip())
        else:
            resultado.append(letra)
    return "".join(resultado)

# =============================================================================
# DISEÑO DE LA INTERFAZ WEB (STREAMLIT)
# =============================================================================

st.set_page_config(page_title="Archivo Global Voynich", page_icon="📖", layout="wide")

st.title("📖 Intérprete Global del Manuscrito Voynich")
st.write("Exploración completa del texto auténtico y herramientas avanzadas de descifrado.")

# Configuración en Barra Lateral
st.sidebar.header("📂 Navegación de Páginas")

def ordenar_folios(key):
    match = re.search(r'\d+', key)
    num = int(match.group()) if match else 0
    letra = key[-1]
    return [num, letra]

folios_disponibles = sorted(list(vd.CORPUS_MANUSCRITO.keys()), key=ordenar_folios)
folio_seleccionado = st.sidebar.selectbox("Seleccionar página del manuscrito:", folios_disponibles)

st.sidebar.header("⚙️ Modo de Descifrado")
tipo_traduccion = st.sidebar.radio("Tipo de Traducción:", ["Traducción Automática (Diccionarios)", "Traducción Manual (Personalizada)"])

if tipo_traduccion == "Traducción Automática (Diccionarios)":
    idioma = st.sidebar.selectbox("Idioma del diccionario:", ["Español", "English"])
    diccionario_activo = vd.DICCIONARIO_ES if idioma == "Español" else vd.DICCIONARIO_EN
else:
    st.sidebar.markdown("### 🛠️ Tabla de Equivalencias Manuales")
    glifos_comunes = ['o', 'a', 'e', 'c', 'h', 't', 'p', 'k', 'f', 'n', 'r', 's', 'y', 'l', 'm']
    mapa_usuario = {}
    col1, col2 = st.sidebar.columns(2)
    for idx, glifo in enumerate(glifos_comunes):
        target_col = col1 if idx % 2 == 0 else col2
        mapa_usuario[glifo] = target_col.text_input(f"EVA '{glifo}' ->", value=glifo, key=f"m_{glifo}")

# Bloques de Visualización (Texto Original Izquierda vs Traducción Derecha)
col_izq, col_der = st.columns(2)

lineas_originales = vd.CORPUS_MANUSCRITO.get(folio_seleccionado, ["Página vacía"])

with col_izq:
    st.subheader(f"📄 Texto Original Ordenado - Folio {folio_seleccionado}")
    texto_bloque_eva = "\n".join([f"Línea {i+1}: {linea}" for i, linea in enumerate(lineas_originales)])
    st.text_area("Transcripción EVA Limpia:", value=texto_bloque_eva, height=380, disabled=True)

with col_der:
    st.subheader(f"🗝️ Resultado - Método: {tipo_traduccion}")
    lineas_traducidas = []
    for linea in lineas_originales:
        palabras = linea.split()
        if tipo_traduccion == "Traducción Automática (Diccionarios)":
            palabras_proc = [traducir_palabra_automatica(p, diccionario_activo) for p in palabras]
        else:
            palabras_proc = [traducir_palabra_manual(p, mapa_usuario) for p in palabras]
        lineas_traducidas.append(" ".join(palabras_proc))
        
    texto_bloque_traducido = "\n".join([f"Línea {i+1}: {linea}" for i, linea in enumerate(lineas_traducidas)])
    st.text_area("Resultado del análisis descriptivo:", value=texto_bloque_traducido, height=380, disabled=True)

st.markdown("---")
st.subheader("🧪 Banco de Pruebas de Texto Libre")
texto_libre = st.text_input("Inserta cualquier palabra o fragmento en EVA para analizarla:")
if texto_libre:
    palabras_libres = texto_libre.split()
    if tipo_traduccion == "Traducción Automática (Diccionarios)":
        res_libres = [traducir_palabra_automatica(p, diccionario_activo) for p in palabras_libres]
    else:
        res_libres = [traducir_palabra_manual(p, mapa_usuario) for p in palabras_libres]
    st.success(f"Resultado: {' '.join(res_libres)}")
