import streamlit as st
from voynichdata import aplicar_matriz_sustitucion, motor_prosa_fluida

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Traductor del Manuscrito Voynich",
    page_icon="📜",
    layout="centered"
)

# Título y descripción de tu aplicación
st.title("📜 Traductor Adaptativo del Manuscrito Voynich")
st.write(
    "Esta aplicación procesa texto transliterado en formato **EVA (Extensible Voynich Alphabet)**, "
    "aplica una matriz de reducción paleográfica y busca correspondencias en raíces de Latín Vulgar y Romance."
)

st.markdown("---")

# Área de entrada para el usuario
texto_usuario = st.text_area(
    "Introduce el texto en EVA aquí:",
    placeholder="Ejemplo: qokched dcectth shol...",
    help="Escribe o pega los caracteres correspondientes a la transcripción oficial de los folios."
)

# Botón de acción principal
if st.button("Procesar y Traducir", type="primary"):
    if texto_usuario.strip() == "":
        st.warning("Por favor, introduce algún fragmento de texto en EVA para comenzar.")
    else:
        with st.spinner("Aplicando matriz de sustitución y limpiando haches huérfanas..."):
            
            # 1. PASO CRÍTICO: Aplicamos tu nueva matriz de sustituciones ordenada
            texto_filtrado = aplicar_matriz_sustitucion(texto_usuario)
            
            # 2. SEGUNDO PASO: Procesamos el resultado con el diccionario adaptativo
            traduccion_final = motor_prosa_fluida(texto_filtrado)
            
        # Despliegue de resultados en contenedores visuales de Streamlit
        st.success("¡Procesamiento completado con éxito!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🧪 Texto Filtrado (Matriz)")
            st.info(f"`{texto_filtrado}`" if texto_filtrado else "*El texto quedó vacío tras los filtros*")
            
        with col2:
            st.markdown("### 🏛️ Prosa Romance Estimada")
            st.write(traduccion_final)

st.markdown("---")
st.caption("Proyecto Beta Experimental independiente desarrollado por Mateo Thour-idk. Todos los derechos reservados.")
