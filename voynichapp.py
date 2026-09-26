import streamlit as st
import urllib.request

st.set_page_config(page_title="Traductor Completo del Manuscrito Voynich", page_icon="📜", layout="wide")

st.title("📜 Traductor Universal del Manuscrito Voynich")
st.write("Esta herramienta aplica tu matriz de descifrado fonético romance a **cualquiera de las páginas** del manuscrito.")

# Matriz de traducción unificada y optimizada
def traducir_texto(texto):
    reglas = {
        'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 'dceorceau': 'dicorcau',
        'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 'olteey': 'oltí',
        'otolceey': 'otolcí', 'kdceody': 'qudicodí', 'ceeodaiin': 'ciodain',
        'croffosodaur': 'crofosodaur', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'qocey': 'quocí', 'dce': 'dic', 'cee': 'ci', 'eey': 'iy', 'ceeey': 'cia',
        'cteey': 'cutí', 'cte': 'cut', 'pc': 'p', 'ps': 'p', 'cp': 'p',
        'ce': 'c', 'ey': 'a', 'oe': 'u', 'ee': 'i', 'oi': 'oi', 'ii': 'i',
        'ae': 'a', 'dc': 'ch', 'tc': 'ch', 'q': 'qu', 'ck': 'qu', 'k': 'qu'
    }
    # Convertir a minúsculas y limpiar caracteres extraños de transcripción
    texto_limpio = texto.lower()
    for caracter in ['$', '.', '{', '}', '-', '=', '_']:
        texto_limpio = texto_limpio.replace(caracter, ' ')
        
    # Aplicar reemplazos por longitud decreciente para evitar colisiones
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

# Crear pestañas para facilitar la experiencia del usuario
tab1, tab2 = st.tabs(["📝 Traducir Texto Libre", "📖 Seleccionar Folio Completo"])

with tab1:
    st.subheader("Traducción manual de fragmentos")
    entrada = st.text_area("Pega aquí tus palabras en formato EVA:", "teeodau cseey cpair osaiin")
    if st.button("Descifrar Fragmento"):
        st.success("Resultado Fonético:")
        st.write(traducir_texto(entrada))

with tab2:
    st.subheader("Descifrador Automático por Folio")
    st.write("El sistema se conectará a los servidores académicos para extraer el texto EVA original de la página elegida.")
    
    # Generar lista de folios típicos (1r a 116v)
    folios_disponibles = [f"{i}r" for i in range(1, 117)] + [f"{i}v" for i in range(1, 117)]
    folios_disponibles.sort(key=lambda x: (int(''.join(filter(str.isdigit, x))), x[-1]))
    
    folio_seleccionado = st.selectbox("Elige el Folio que deseas leer:", folios_disponibles)
    
    if st.button(f"Descargar y Descifrar Folio {folio_seleccionado}"):
        try:
            # Enlace al repositorio público con la transcripción completa del Voynich
            url_archivo = "https://githubusercontent.com"
            
            with urllib.request.urlopen(url_archivo) as response:
                lineas = response.read().decode('utf-8').splitlines()
            
            texto_folio = []
            for linea in lineas:
                # Filtrar las líneas que pertenecen exclusivamente al folio elegido
                if linea.startswith(f"<{folio_seleccionado}."):
                    # Extraer solo el contenido de texto EVA quitando la etiqueta del folio
                    partes = linea.split(">")
                    if len(partes) > 1:
                        texto_folio.append(partes[1].strip())
            
            if texto_folio:
                texto_completo_eva = "\n".join(texto_folio)
                st.info(f"📄 Texto original en formato EVA detectado ({len(texto_folio)} líneas). Procesando descifrado...")
                
                resultado_final = traducir_texto(texto_completo_eva)
                
                st.success(f"✨ Transliteración fonética romance completa del Folio {folio_seleccionado}:")
                st.text_area("Resultado:", resultado_final, height=400)
            else:
                st.warning(f"No se encontraron líneas transcritas para el Folio {folio_seleccionado} en este archivo.")
                
        except Exception as e:
            st.error(f"Error al conectar con la base de datos de transcripción: {e}")
