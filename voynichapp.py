import streamlit as st

st.set_page_config(page_title="Traductor Completo del Manuscrito Voynich", page_icon="📜", layout="wide")

st.title("📜 Traductor Universal del Manuscrito Voynich")
st.write("Esta herramienta aplica tu matriz de descifrado fonético romance y latín medieval sobre las páginas del manuscrito.")

# Base de datos local integrada con tus folios clave para evitar errores de conexión
BASE_DATOS_VOYNICH = {
    "20r": (
        "kdceody ceopy ceeey qotceoy qotoeey dceorceau ceodey cteey ceotol odaur\n"
        "qotcey cteody ceodcey qoteey ceoceodaiu cseo qocey ceey tceeodal daral\n"
        "oceol olteey otolceey\n"
        "teeodau cseey cpair osaiin yteeoey cseey cpaiin oaiin daiis okeody\n"
        "qoeqeeej sar oeteody oteey keey key keeodal yceeos oiaj ceeos aiin\n"
        "oteroe aram cseeer dalaiu dam ceeodaiin aekeey sar air soar ceeey dair cteey"
    ),
    "21v": "pchodon ceor vety dceor ceodey ctair olteey qotcey otair",
    "67r": "daor odotoey doror daor ceody qotcey oaror",
    "78r": "qokedy kedy qokedy ckaur chedy oas raor kedy ceon ceey"
}

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
    texto_limpio = texto.lower()
    for caracter in ['$', '.', '{', '}', '-', '=', '_']:
        texto_limpio = texto_limpio.replace(caracter, ' ')
        
    for k in sorted(reglas.keys(), key=len, reverse=True):
        texto_limpio = texto_limpio.replace(k, reglas[k])
    return texto_limpio

tab1, tab2 = st.tabs(["📝 Traducir Texto Libre", "📖 Seleccionar Folio Completo"])

with tab1:
    st.subheader("Traducción manual de fragmentos")
    entrada = st.text_area("Pega aquí tus palabras en formato EVA:", "teeodau cseey cpair osaiin")
    if st.button("Descifrar Fragmento"):
        st.success("Resultado Fonético:")
        st.write(traducir_texto(entrada))

with tab2:
    st.subheader("Descifrador Automático por Folio (Modo Local Seguro)")
    st.write("Selecciona uno de los folios clave cargados directamente en el sistema.")
    
    folio_seleccionado = st.selectbox("Elige el Folio que deseas leer:", list(BASE_DATOS_VOYNICH.keys()))
    
    if st.button(f"Descifrar Folio {folio_seleccionado}"):
        texto_completo_eva = BASE_DATOS_VOYNICH[folio_seleccionado]
        resultado_final = traducir_texto(texto_completo_eva)
        
        st.info(f"📄 Procesando el texto original EVA del Folio {folio_seleccionado}...")
        st.success(f"✨ Transliteración fonética romance completa:")
        st.text_area("Resultado:", resultado_final, height=250)
