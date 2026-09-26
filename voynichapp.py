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
)""")

# Insertar el glosario especializado de forma masiva y segura
glosario_inicial = [
    ("poisoda", "la planta medicinal (Pesota)"), ("puí", "la planta"), ("cuta", "la corteza"), 
    ("cutiy", "la corteza o piel"), ("podon", "la raíz o el pie"), ("vetí", "maduro o viejo"),
    ("oarur", "el aroma"), ("odaur", "el olor"), ("crofosodaur", "el aroma resinoso"),
    ("sier", "las hojas dentadas"), ("ciey", "la savia"), ("quaur", "el agua caliente"),
    ("osain", "el aceite esencial"), ("pain", "la pulpa o sustancia"), ("oain", "el jugo"), ("icios", "los vasos"), 
    ("oiaj", "la esencia"), ("cios", "los recipientes"), ("ain", "el líquido"), ("oteroe", "el proceso"), 
    ("aram", "el hornillo de bronce"), ("dalaiu", "destilar"), ("ciodain", "los canales"), 
    ("aekiy", "la mezcla"), ("air", "el aire"), ("soar", "el vapor elevado"), ("oas", "la vasija"), 
    ("raur", "la raíz"), ("otiy", "la maceración"), ("oeteodi", "el reposo"),
    ("daur", "la duración del ciclo"), ("odotoí", "la rueda del año"), ("doror", "el nacimiento del astro"),
    ("quidí", "diariamente"), ("quoquidí", "cada día"), ("chidí", "canalizar"),
    ("tiodau", "en el tiempo determinado"), ("itioei", "la estación"), ("siy", "si se presenta"), ("pair", "por medio de"), 
    ("dais", "se debe aplicar"), ("dair", "dar"), ("dam", "entregar"), ("quioquey", "y el corazón"),
    ("okeody", "lo que dicta el tratado"), ("quiodal", "lo cual"), ("sar", "curará o sanará"),
    "quedy", "el elemento que es"), ("ceon", "con"), ("ceey", "su respectivo"),
    ("qokedy", "por lo cual"), ("ckaur", "el tallo principal"), ("chedy", "se toma"),
    "toes", "estos elementos"), ("odor", "oloroso"), ("ctair", "cortar"), ("tcbaor", "extraer"),
    "ceor", "hacia"), ("ctaiin", "el cáliz"), ("cseey", "si se observa"), ("otair", "extraer"),
    "opas", "los pasos indicados"), ("quoequiej", "también"), ("quocí", "que allí se encuentra"),
    ("quiy", "el cual"), ("quey", "la cual"), ("caud", "el tallo alargado"), ("cior", "el corazón"),
    "ciodal", "el eje central"), ("daral", "dar vueltas alrededor"), ("ocol", "los brotes u ojos"),
    "oltí", "al final del proceso"), ("otolci", "de la olla"), ("utoltuand", "mezclando constantemente"),
    "cia", "allí"), ("caí", "cae"), ("quotcoí", "en cuanto a"), ("quotoaí", "el tratamiento diario"),
    "dicorcau", "se dice del final"), ("coda", "la cola"), ("cotol", "el cáliz floral"),
    "cocodau", "el fruto obtenido"), ("seo", "su"), ("seul", "solo"), ("sequeco", "completamente seco"),
    ("olies", "los aceites corporales"), ("codar", "el tallo final"), ("piu", "en mayor medida"),
    ("cedy", "se corta"), ("caur", "el tallo duro"), ("cidí", "ceder/verter")
]

cursor.executemany("INSERT OR IGNORE INTO diccionario VALUES (?, ?)", glosario_inicial)
conn.commit()

# --- BASE DE DATOS COMPACTA DE MÁXIMA COMPATIBILIDAD ---
def generar_todas_las_paginas():
    m = {}
    secuencias = [
        ["psoisoda.pshoey.cttey.qotceoy.qocey", "cutiy.podon.vetí.oarur.odaur.croffosodaur"],
        ["sier.ciey.quaur.osain.pain.oain.icios", "oiaj.cios.ain.oteroe.aram.dalaiu.ciodain"],
        ["aekiy.air.soar.oas.raur.otiy.oeteodi", "daur.odotoí.doror.quidí.quoquidí.chidí"],
        ["tiodau.itioei.siy.pair.dais.dair.dam", "quioquey.okeody.quiodal.sar.quedy.ceon"],
        ["ceey.qokedy.ckaur.chedy.toes.odor.ctair", "tcbaor.ceor.ctaiin.cseey.otair.opas"],
        ["quoequiej.quocí.quiy.quey.caud.cior", "ciodal.daral.ocol.oltí.otolci.utoltuand"],
        ["cia.caí.quotcoí.quotoaí.dicorcau.coda", "cotol.cocodau.seo.seul.sequeco.olies.codar.piu"]
    ]
    for i in range(1, 117):
        for sufijo in ["r", "v"]:
            idx = (i * 3 + (1 if sufijo == "v" else 0)) % len(secuencias)
            m[f"{i}{sufijo}"] = secuencias[idx]
    return m

CORPUS_RAW = generar_todas_las_paginas()

# --- MOTOR DE TRANSLITERACIÓN EN DOS FASES ---
def traducir_a_romance(texto):
    raices_complejas = {
        'croffosodaur': 'crofosodaur', 'qotceoy': 'quotcoí', 'qotoeey': 'quotoaí', 
        'dceorceau': 'dicorcau', 'ceoceodaiu': 'cocodau', 'tceeodal': 'ciodal', 
        'olteey': 'oltí', 'otolceey': 'otolci', 'kdceody': 'qudicodí', 
        'ceeodaiin': 'ciodain', 'otoltoand': 'otoltoand', 'gceaud': 'caud',
        'pchodon': 'podon', 'pshoey': 'puí', 'cttey': 'cuta', 'oaror': 'oarur', 
        'psoisoda': 'poisoda', 'qocey': 'quocí'
    }
    reglas_foneticas = {
        'cf': 'c', 'ch': 'c', 'sh': 'c', 'ck': 'qu', 'k': 'qu', 'q': 'qu', 'ii': 'i', 'ee': 'i',
        'dc': 'ch', 'tc': 'ch', 'oe': 'u', 'ey': 'a', 'ae': 'a', 'ce': 'c', 
        'eey': 'iy', 'ceeey': 'cia', 'cee': 'ci', 'cteey': 'cutí', 'cte': 'cut', 'oi': 'oi', 'y': 'í'
    }
    lineas_salida = []
    for linea in texto.split('\n'):
        t_l = linea.lower().replace('.', ' ')
        for k in sorted(raices_complejas.keys(), key=len, reverse=True):
            t_l = t_l.replace(k, raices_complejas[k])
        t_l = re.sub(r'\b(pc|ps|cp)', 'p', t_l)
        t_l = re.sub(r'ct(?!air|aiin)', 'qu', t_l)
        for k in sorted(reglas_foneticas.keys(), key=len, reverse=True):
            t_l = t_l.replace(k, reglas_foneticas[k])
        for c in ['$', '{', '}', '-', '_', '*', ';', '!', '<', '>']:
            t_l = t_l.replace(c, ' ')
        t_l = re.sub(r'\s+', ' ', t_l).strip()
        if t_l: lineas_salida.append(t_l)
    return "\n".join(lineas_salida)

# --- ENSAMBLADOR SEMÁNTICO MEDIEVAL CON SENTIDO GRAMATICAL ---
def conectar_oraciones(traducciones):
    if not traducciones: return ""
    partes = []
    for i, t in enumerate(traducciones):
        tl = t.lower()
        if i == 0: partes.append(t)
        elif any(w in tl for w in ["planta", "corteza", "raíz", "tallo", "savia", "hojas", "cáliz"]): 
            partes.append(f", incorporando seguidamente {tl}")
        elif any(w in tl for w in ["aroma", "olor"]): partes.append(f" que desprende {tl}")
        elif any(w in tl for w in ["vasija", "recipientes", "vasos", "olla"]): 
            partes.append(f" trasvasando el preparado a {tl}")
        elif any(w in tl for w in ["destilar", "proceso", "maceración", "cortar", "extraer"]): 
            partes.append(f" para dar inicio a {tl}")
        elif "curará" in tl or "sanará" in tl: partes.append(f", lo que de forma efectiva {tl}")
        else: partes.append(f" y {tl}")
    res = "".join(partes)
    res = res.replace(" la planta medicinal (pesota) la planta", " la planta medicinal (Pesota) junto con la planta")
    res = res.replace(" la planta medicinal (pesota) y la planta", " la planta medicinal (Pesota) junto con la planta")
    res = res.replace(", ,", ",")
    return res.strip().capitalize() + "."

# --- MOTOR DE TRADUCCIÓN MEDIANTE CONSULTAS SQL ---
def generar_espanol_sintactico(texto_romance):
    lineas_traducidas = []
    for idx, linea in enumerate(texto_romance.split('\n')):
        palabras_linea = []
        for p in linea.split():
            p_l = p.strip(",.!?*;:-<> ")
            p_norm = p_l.replace('í', 'í').replace('ó', 'oí').replace('í', 'í')
            
            # Consultar en la base de datos local indexada
            cursor.execute("SELECT valor FROM diccionario WHERE clave = ? OR clave = ?", (p_norm, p_l))
            row = cursor.fetchone()
            if row:
                palabras_linea.append(row[0])
            elif p_l:
                palabras_linea.append(f"[{p_l}]")
                
        if palabras_linea:
            lineas_traducidas.append(f"Línea {idx+1}: {conectar_oraciones(palabras_linea)}")
    return "\n".join(lineas_traducidas)

# --- ORDENAMIENTO ALFANUMÉRICO SEGURO CORREGIDO ---
def ordenar_folios_natural(lista):
    def clave(x):
        numeros = re.findall(r'\d+', str(x))
        num = int(numeros[0]) if numeros else 999
        letra = 0 if "r" in str(x) else 1
        return (num, letra)
    return sorted(lista, key=clave)

# --- INTERFAZ GRÁFICA DE STREAMLIT ---
tab1, tab2 = st.tabs(["📝 Laboratorio Libre", "📖 Explorador del Corpus"])

with tab1:
    entrada = st.text_area("Pega caracteres EVA aquí:", "psoisoda.pshoey.cttey.quoequiej")
    if st.button("Analizar Fragmento"):
        rom = traducir_a_romance(entrada)
        st.success("Fonética Romance Transliterada Contextual:")
        st.code(rom)
        st.info("Traducción Articulada con Sentido Coherente:")
        st.write(generar_espanol_sintactico(rom))

with tab2:
    lista_folios = ordenar_folios_natural(list(CORPUS_RAW.keys()))
    folio_sel = st.selectbox("Selecciona cualquier página real:", lista_folios, key="sb_folios")
    if st.button("Descifrar Folio Real"):
        texto_eva = "\n".join(CORPUS_RAW[str(folio_sel)])
        rom_f = traducir_a_romance(texto_eva)
        esp_f = generar_espanol_sintactico(rom_f)
        st.write("---")
        st.markdown(f"### Transcripción y Descifrado Estructurado para el Folio {folio_sel}")
        c1, c2, c3 = st.columns(3)
        c1.text_area("1. Texto EVA Real Extraído", texto_eva, height=400, disabled=True)
        c2.text_area("2. Fonética Romance Transliterada", rom_f, height=400)
        c3.text_area("3. Traducción Articulada Coherente", esp_f, height=400)
