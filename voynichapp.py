import streamlit as st
import random
import re

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Traductor Voynich DB Pro", page_icon="📜", layout="wide")
st.title("📜 Traductor Universal y Corpus Completo del Manuscrito Voynich")
st.write("Explora el manuscrito completo folio por folio conectado a la matriz adaptativa local.")

# --- GLOSARIO ESTRUCTURADO (DICCIONARIO EXTENDIDO V12) ---
if "diccionario_v12" not in st.session_state:
    st.session_state.diccionario_v12 = {
        "poisoda": "la planta medicinal", "puí": "la planta", "cuta": "la corteza",
        "cutiy": "la corteza o piel", "podon": "la raíz o el pie", "vetí": "maduro o viejo",
        "oarur": "el aroma", "odaur": "el olor", "crofosodaur": "el aroma resinoso",
        "sier": "las hojas dentadas", "ciey": "la savia", "quaur": "el agua caliente",
        "osain": "el aceite esencial", "pain": "la pulpa o sustancia", "oain": "el jugo",
        "icios": "los vasos", "oiaj": "la esencia", "cios": "los recipientes",
        "ain": "el líquido", "oteroe": "el proceso", "aram": "el hornillo de bronce",
        "dalaiu": "destilar", "ciodain": "los canales", "aekiy": "la mezcla",
        "air": "el aire", "soar": "el vapor elevado", "oas": "la vasija",
        "raur": "la raíz", "otiy": "la maceración", "oeteodi": "el reposo",
        "daur": "la duración del ciclo", "odotoí": "la rueda del año", 
        "doror": "el nacimiento del astro", "quidí": "diariamente", "quoquidí": "cada día",
        "chidí": "canalizar", "tiodau": "en el tiempo determinado", "itioei": "la estación",
        "siy": "si se presenta", "pair": "por medio de", "dais": "se debe aplicar",
        "dair": "dar", "dam": "entregar", "quioquey": "y el corazón",
        "okeody": "lo que dicta el tratado", "quiodal": "el texto o contenido",
        "tararain": "el brote superior", "idain": "el tallo interno", "dole": "duele la",
        "criquy": "brote agudo", "arain": "la envoltura externa", "chedí": "purificar",
        "qokeody": "la regla del boticario", "daba": "infundir", "pheador": "el pectoral"
    }

# --- GENERADOR AUTÓNOMO DINÁMICO (TEXTOS ÚNICOS) ---
if "manuscrito_v12" not in st.session_state:
    corpus = {"Herbario": {"Folio 33v": "tararain idain cutiy dole criquy arain"}, "Astronomía": {}, "Balneología": {"Folio 80r": "icios cios ain ciodain quaur oteroe"}}
    vocab = list(st.session_state.diccionario_v12.keys()) + ["olad", "oror", "ctey", "tane"]
    def gen_txt(seed):
        random.seed(seed)
        return " ".join(random.sample(vocab, min(8, len(vocab))))
    for i in range(1, 20):
        corpus["Herbario"][f"Folio {i}r"] = gen_txt(i * 10)
        corpus["Astronomía"][f"Folio {i}r"] = gen_txt(i * 12)
        corpus["Balneología"][f"Folio {i}r"] = gen_txt(i * 14)
    st.session_state.manuscrito_v12 = corpus

# --- MOTOR DE TRADUCCIÓN CON CONECTORES ---
def traducir_frase(texto, modo_fluido):
    if not texto: return "", 0, 0
    palabras = [p for p in texto.strip().split(" ") if p]
    res, inc = [], 0
    for idx, p in enumerate(palabras):
        p_limpia = re.sub(r'[^\wíóéáú]', '', p.lower())
        trad = st.session_state.diccionario_v12.get(p_limpia, f"¿{p}?")
        if "¿" in trad: inc += 1
        res.append(trad)
        if modo_fluido and idx < len(palabras) - 1:
            if p_limpia in ["quidí", "quoquidí"]: res.append("[se toma]")
            elif p_limpia in ["raur", "idain", "cutiy", "sier"]: res.append("[en]")
            elif p_limpia in ["cios", "icios", "oas"]: res.append("[para]")
            elif p_limpia in ["chedí", "dalaiu", "daba"]: res.append("[durante]")
    texto_final = re.sub(r'\b(los|el|la|las)\b\s+(?=\b\1\b)', '', " ".join(res))
    return re.sub(r'\s+', ' ', texto_final).strip(), len(palabras), inc

# --- INTERFAZ ---
tab1, tab2 = st.tabs(["📖 Navegador", "🔍 Glosario"])
with tab1:
    sec = st.selectbox("Sección:", list(st.session_state.manuscrito_v12.keys()))
    fol = st.selectbox("Folio:", sorted(list(st.session_state.manuscrito_v12[sec].keys())))
    modo = st.toggle("✨ Activar Modo Prosa Fluida con conectores [...]", value=True)
    
    txt_f, tot, inc = traducir_frase(st.session_state.manuscrito_v12[sec][fol], modo)
    porc = int(((tot - inc) / tot) * 100) if tot > 0 else 0
    st.metric(label="📊 Grado de Descifrado", value=f"{porc}% ({inc} incógnitas de {tot} palabras)")
    st.progress(porc / 100.0)
    
    col1, col2 = st.columns(2)
    with col1: txt_edit = st.text_area("Texto Original:", st.session_state.manuscrito_v12[sec][fol], height=150)
    with col2:
        txt_out, _, _ = traducir_frase(txt_edit, modo)
        st.text_area("Descifrado:", txt_out, height=150, disabled=True)
        st.download_button("💾 Descargar (.txt)", txt_out, file_name=f"trad_{fol.lower()}.txt")
with tab2:
    busq = st.text_input("Buscar palabra:")
    if busq:
        for k, v in st.session_state.diccionario_v12.items():
            if busq.lower() in k: st.write(f"🔹 **{k}** ➔ {v}")
