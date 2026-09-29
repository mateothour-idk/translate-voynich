# --- ARCHIVO 2: voynichapp.py ---
import streamlit as st
import re
import voynichdatos as vd
from collections import Counter

if not vd.CORPUS_MANUSCRITO:
    vd.cargar_todas_las_paginas_reales()

# =============================================================================
# MOTOR CRIPTOGRÁFICO DE CONSISTENCIA ACADÉMICA (Sustitución y Abrev. Fijas)
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

# Mapeo fonético estricto que simula abreviaturas latinas del siglo XV
TRADUCCION_FONEMAS_DEFECTO = {
    'a': 'a', 'b': 'b', 'c': 'c', 'd': 'rum', 'e': 'e', 'f': 'f', 'g': 'g', 
    'h': 'h', 'i': 'i', 'k': 'qu', 'l': 'is', 'm': 'm', 'n': 'n', 'o': 'o', 
    'p': 'per', 'q': 'que', 'r': 'r', 's': 's', 't': 't', 'u': 'u', 'v': 'v', 
    'x': 'sh', 'y': 'i', 'z': 'z'
}

def limpiar_fonetica_posicional(palabra_eva):
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
    """Descifra el texto descomponiendo términos en raíces fijas y abreviaturas silábicas."""
    p_limpia = limpiar_fonetica_posicional(palabra_eva.lower().replace('íd', 'id').replace('í', 'i'))
    
    if not p_limpia:
        return ""
        
    if p_limpia in diccionario:
        return diccionario[p_limpia]
        
    traducciones_parciales = []
    llaves_ordenadas = sorted(diccionario.keys(), key=len, reverse=True)
    
    palabra_restante = p_limpia
    while len(palabra_restante) > 0:
        encontrado = False
        for llave in llaves_ordenadas:
            if palabra_restante.startswith(llave):
                traducciones_parciales.append(f" {diccionario[llave]} ")
                palabra_restante = palabra_restante[len(llave):]
                encontrado = True
                break
        
        if not encontrar_encontrado if 'encontrar_encontrado' in locals() else encontrado:
            pass
        if not encontrado:
            # Extraer rigurosamente el primer carácter y aplicar equivalencia de abreviatura latina
            letra_actual = palabra_restante[0]
            letra_traducida = TRADUCCION_FONEMAS_DEFECTO.get(letra_actual, letra_actual)
            traducciones_parciales.append(letra_traducida)
            palabra_restante = palabra_restante[1:]  # Reducción estricta de la cadena
            
    resultado_unido = "".join(traducciones_parciales)
    resultado_unido = " ".join(resultado_unido.split())
    return resultado_unido

def traducir_palabra_manual(palabra_eva, mapa_manual):
    resultado = []
    for letra in palabra_eva.lower():
        if letra in mapa_manual and mapa_manual[letra].strip():
            resultado.append(mapa_manual[letra].strip())
        else:
            resultado.append(letra)
    return "".join(resultado)

# =============================================================================
# INTERFAZ GRÁFICA (STREAMLIT)
# =============================================================================

st.set_page_config(page_title="Archivo Global Voynich", page_icon="📖", layout="wide")

st.title("📖 Intérprete Riguroso del Manuscrito Voynich")
st.write("Modelo de descifrado sistemático basado en abreviaturas medievales y morfología botánica.")

st.sidebar.header("📂 Navegación de Páginas")

def ordenar_folios(key):
    match = re.search(r'\d+', key)
    num = int(match.group()) if match else 0
    letra = key[-1]
    return [num, letra]

folios_disponibles = sorted(list(vd.CORPUS_MANUSCRITO.keys()), key=ordenar_folios)
folio_seleccionado = st.sidebar.selectbox("Seleccionar página del manuscrito:", folios_disponibles)

st.sidebar.header("⚙️ Modo de Descifrado")
tipo_traduccion = st.sidebar.radio("Tipo de Traducción:", ["Traducción Automática (Modelo Académico)", "Traducción Manual (Personalizada)"])

if tipo_traduccion == "Traducción Automática (Modelo Académico)":
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

col_izq, col_der = st.columns(2)
lineas_originales = vd.CORPUS_MANUSCRITO.get(folio_seleccionado, ["Página vacía"])

with col_izq:
    st.subheader(f"📄 Texto Original Ordenado - Folio {folio_seleccionado}")
    texto_bloque_eva = "\n".join([f"Línea {i+1}: {linea}" for i, linea in enumerate(lineas_originales)])
    st.text_area("Transcripción EVA Limpia:", value=texto_bloque_eva, height=380, disabled=True)

with col_der:
    st.subheader(f"🗝️ Traducción Estimada (Consistente)")
    lineas_traducidas = []
    for linea in lineas_originales:
        palabras = linea.split()
        if tipo_traduccion == "Traducción Automática (Modelo Académico)":
            palabras_proc = [traducir_palabra_automatica(p, diccionario_activo) for p in palabras]
        else:
            palabras_proc = [traducir_palabra_manual(p, mapa_usuario) for p in palabras]
        lineas_traducidas.append(" ".join(palabras_proc))
        
    texto_bloque_traducido = "\n".join([f"Línea {i+1}: {linea}" for i, linea in enumerate(lineas_traducidas)])
    st.text_area("Prosa resultante del análisis paleográfico:", value=texto_bloque_traducido, height=380, disabled=True)

# Módulo estadístico
st.markdown("---")
st.subheader(f"📊 Analizador Estadístico de Frecuencia — Folio {folio_seleccionado}")
texto_completo_folio = "".join(lineas_originales).lower().replace(" ", "")

if texto_completo_folio:
    conteo_letras = Counter(texto_completo_folio)
    total_letras = sum(conteo_letras.values())
    top_letras = conteo_letras.most_common(10)
    
    columnas_stats = st.columns(5)
    for index, (letra, cantidad) in enumerate(top_letras):
        col_target = columnas_stats[index % 5]
        porcentaje = (cantidad / total_letras) * 100
        with col_target:
            st.metric(label=f"Glifo EVA '{letra}'", value=f"{cantidad} veces", delta=f"{porcentaje:.1f}%")

st.markdown("---")
st.subheader("🧪 Banco de Pruebas de Texto Libre")
texto_libre = st.text_input("Inserta cualquier palabra o fragmento en EVA para analizarla:")
if texto_libre:
    palabras_libres = texto_libre.split()
    if tipo_traduccion == "Traducción Automática (Modelo Académico)":
        res_libres = [traducir_palabra_automatica(p, diccionario_activo) for p in palabras_libres]
    else:
        res_libres = [traducir_palabra_manual(p, mapa_usuario) for p in palabras_libres]
    st.success(f"Resultado: {' '.join(res_libres)}")
