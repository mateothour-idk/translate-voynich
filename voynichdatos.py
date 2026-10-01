# ==========================================
# PARTE 1: CONFIGURACIÓN Y DICCIONARIO ESPAÑOL
# ==========================================
import re

DICCIONARIO_ES = {
    "pui": "planta", "cuta": "corteza", "oarur": "aroma", "poisoda": "pocion (medicina)",
    "quedy": "elemento", "con": "cum (con)", "su": "su", "quoqu": "por lo tanto", 
    "caur": "caulis (tallo)", "chedy": "extracto", "toes": "estos", "odor": "oloroso", 
    "cutair": "cortar", "oas": "vasija", "tcbaor": "recolectar", "hacia": "hacia", 
    "ctaiin": "cáliz", "si": "si", "otair": "surgir", "opas": "pasos", 
    "chidi": "canalizar", "podon": "raíz", "vety": "maduro", "dic": "dice", 
    "olteey": "final", "quotcey": "limpio", "raur": "base", "qudicodi": "tratado", 
    "copi": "abundante", "cia": "allí", "quotcoi": "cuanto", "quotoai": "diario", 
    "dicorcau": "sustancia", "cuti": "piel", "cotol": "cáliz", "odaur": "olor", 
    "cocodau": "fruto", "seo": "su", "quoci": "allí", "ciodal": "eje", 
    "daral": "girar", "ocol": "brotes", "olti": "término", "otolci": "olla", 
    "tiodau": "tiempo", "pair": "por", "osain": "aceite", "pain": "pulpa", 
    "oain": "jugo", "dais": "aplicar", "okeody": "regula (regla)", "quoequiej": "también", 
    "sar": "sanará", "oeteody": "reposo", "otiy": "maceración", "quiy": "el cual", 
    "quey": "la cual", "icios": "los vasos", "oiaj": "esencia", "cios": "recipientes", 
    "ain": "líquido", "oteroe": "proceso", "aram": "hornillo", "sier": "hojas", 
    "dalaiu": "destilar", "dam": "dar", "ciodain": "conductos", "aekiy": "mezcla", 
    "air": "aire", "soar": "vapor", "ciey": "savia", "odotoi": "cycle", 
    "doror": "nacimiento", "quaur": "calor", "caud": "tallo largo", "cedy": "cortar", "cidí": "verter",
    "folia": "hoja", "ramus": "rama", "flos": "flor", "semen": "semilla", "capsa": "cápsula",
    "gemma": "yema", "nux": "nuez", "baca": "baya", "spina": "espina", "radix": "raíz profunda",
    "stolo": "estolón", "bulbus": "bulbo", "vimen": "mimbre", "cortex": "corteza externa",
    "medula": "médula interior", "pith": "núcleo", "nodo": "nudo del tallo", "internod": "entrenudo",
    "petalo": "pétalo", "sepalo": "sépalo", "pollen": "polen", "anthera": "antera",
    "humida": "húmedo", "sicca": "seco", "calida": "caliente", "frigida": "frío", "amara": "amargo",
    "dulcis": "dulce", "acris": "acre", "mitis": "suave", "veneno": "venenoso", "salutis": "curativo",
    "sanct": "sagrado", "oculta": "secreto/oculto", "cocta": "cocido", "cruda": "crudo",
    "pura": "puro", "mixta": "mezclado", "soluta": "disuelto", "spissa": "espeso", "tenuis": "delgado",
    "recens": "fresco", "vetus": "viejo", "marcida": "marchito", "viridis": "verde",
    "coctio": "cocción", "infuso": "infusión", "macer": "macerar", "filtr": "filtrar",
    "colat": "colar", "trit": "triturar", "conter": "moler", "coag": "coagular",
    "solv": "disolver", "evap": "evaporar", "sublim": "sublimar", "ferment": "fermentar",
    "expre": "exprimir", "lavat": "lavado", "purgat": "purga", "unctu": "ungüento",
    "gutta": "gotas", "pulvis": "polvo", "sirup": "jarabe", "elixir": "elixir",
    "herba": "hierba", "arbor": "árbol", "frutex": "arbusto", "muscus": "musgo", "fungus": "hongo",
    "filix": "helecho", "alga": "alga", "juncus": "junco", "gramen": "gramínea",
    "salvia": "salvia", "malva": "malva", "mentha": "menta", "rosa": "rosa", "lilium": "lirio",
    "papaver": "amapola", "solanum": "solano", "apis": "apio", "allium": "ajo",
    "sana": "sanar", "cura": "curar", "lenit": "aliviar", "purg": "purgar", "dorm": "hacer dormir",
    "vulner": "heridas", "febri": "fiebre", "dolor": "dolor", "stoma": "estómago", "capitis": "cabeza",
    "ocul": "ojos", "cutis": "afecciones de la piel", "pectus": "pecho/tos"
}
# ==========================================
# PARTE 2: DICCIONARIO INGLÉS Y MACRO-GLIFOS
# ==========================================
DICCIONARIO_EN = {
    "pui": "plant", "cuta": "bark", "oarur": "aroma", "poisoda": "medicinal potion",
    "quedy": "element", "con": "with", "su": "its", "quoqu": "whereby", 
    "caur": "caulis (stem)", "chedy": "extracted", "toes": "these", "odor": "scented", 
    "cutair": "to cut", "oas": "vessel", "tcbaor": "gather", "hacia": "towards", 
    "ctaiin": "calyx", "si": "if", "otair": "arise", "opas": "steps", 
    "chidi": "channel", "podon": "radix (root)", "vety": "mature", "dic": "says", 
    "olteey": "end", "quotcey": "cleansed", "raur": "base", "qudicodi": "treatise", 
    "copi": "abundant", "cia": "there", "quotcoi": "as for", "quotoai": "daily", 
    "dicorcau": "substance", "cuti": "skin", "cotol": "calyx", "odaur": "scent", 
    "cocodau": "fruit", "seo": "its", "quoci": "there", "ciodal": "axis", 
    "daral": "rotate", "ocol": "buds", "olti": "completion", "otolci": "pot", 
    "tiodau": "time", "pair": "by", "osain": "oil", "pain": "pulp", 
    "oain": "juice", "dais": "applied", "okeody": "rule", "quoequiej": "also", 
    "sar": "heal", "oeteody": "rest", "otiy": "maceration", "quiy": "which", 
    "quey": "which", "icios": "vessels", "oiaj": "essence", "cios": "containers", 
    "ain": "liquid", "oteroe": "process", "aram": "burner", "sier": "leaves", 
    "dalaiu": "distill", "dam": "give", "ciodain": "ducts", "aekiy": "mixture", 
    "air": "air", "soar": "steam", "ciey": "sap", "odotoi": "cycle", 
    "doror": "birth", "quaur": "heat", "caud": "stem", "cedy": "cut", "cidí": "pour",
    "folia": "leaf", "ramus": "branch", "flos": "flower", "semen": "seed", "capsa": "capsule",
    "gemma": "bud", "nux": "nut", "baca": "berry", "spina": "thorn", "radix": "deep root",
    "stolo": "stolon", "bulbus": "bulbo", "vimen": "osier", "cortex": "outer bark",
    "medula": "inner pith", "pith": "core", "nodo": "stem node", "internod": "internode",
    "petalo": "petal", "sepalo": "sepal", "pollen": "pollen", "anthera": "anther",
    "humida": "moist", "sicca": "dry", "calida": "hot", "frigida": "cold", "amara": "bitter",
    "dulcis": "sweet", "acris": "acrid", "mitis": "mild", "veneno": "poisonous", "salutis": "healing",
    "sanct": "sacred", "oculta": "hidden/secret", "cocta": "cooked", "cruda": "raw",
    "pura": "pure", "mixta": "mixed", "soluta": "dissolved", "spissa": "thick", "tenuis": "thin",
    "recens": "fresh", "vetus": "old", "marcida": "withered", "viridis": "green",
    "coctio": "decoction", "infuso": "infusion", "macer": "macerate", "filtr": "filter",
    "colat": "strain", "trit": "crush", "conter": "grind", "coag": "coagulate",
    "solv": "dissolve", "evap": "evaporate", "sublim": "sublimar", "ferment": "ferment",
    "expre": "squeeze", "lavat": "washed", "purgat": "purge", "unctu": "ointment",
    "gutta": "drops", "pulvis": "powder", "sirup": "syrup", "elixir": "elixir",
    "herba": "herb", "arbor": "tree", "frutex": "shrub", "muscus": "moss", "fungus": "fungus",
    "filix": "fern", "alga": "algae", "juncus": "reed", "gramen": "grass",
    "salvia": "sage", "malva": "mallow", "mentha": "mint", "rosa": "rose", "lilium": "lily",
    "papaver": "poppy", "solanum": "nightshade", "apis": "celery", "allium": "garlic",
    "sana": "heal", "cura": "cure", "lenit": "soothe", "purg": "purge", "dorm": "induce sleep",
    "vulner": "wounds", "febri": "fever", "dolor": "pain", "stoma": "stomach", "capitis": "head",
    "ocul": "eyes", "cutis": "skin conditions", "pectus": "chest/cough"
}

DICCIONARIO_MACRO_GLIFOS = {
    "QA": "[Sección Astral]", "PC": "[Párrafo Central]", "FB": "[Folio Botánico]", 
    "B2": "[Grupo Biológico 2]", "IH": "[Ilustración de Herboristería]", "LA": "[Línea Alta]", 
    "H1": "[Encabezado Principal]", "C1": "[Cifrado Primario]"
}
# ==========================================
# PARTE 3: MATRIZ DE PREFIJOS, SUFIJOS Y REGLAS
# ==========================================
PREFIJOS_LISTA = [
    ("tcs", "trans"), ("qok", "com"), ("qot", "quot"), ("cee", "cred"), 
    ("ceo", "re"), ("sub", "sub"), ("cse", "sub"), ("per", "per"), 
    ("com", "com"), ("super", "super"), ("contra", "contra"), ("quot", "quot"),
    ("cred", "cred"), ("cs", "sub"), ("pc", "per"), ("ce", "re"), 
    ("ol", "com"), ("cp", "super"), ("qo", "con"), ("ok", "con"), 
    ("ot", "por"), ("ct", "contra"), ("da", "de"), ("ed", "cred"),
    ("y", "in"), ("l", "la")
]

SUFIJOS_LISTA = [
    ("issimus", "issimus"), ("escere", "escere"), ("eceo", "issimus"),
    ("ensis", "ensis"), ("tatem", "tatem"), ("arius", "arius"),
    ("ticius", "ticius"), ("icculum", "icculum"), ("edy", "ensis"), 
    ("epy", "ensis"), ("eey", "ensis"), ("dam", "tatem"), ("kar", "ura"), 
    ("ky", "ticius"), ("ldy", "tia"), ("ody", "osus"), ("iin", "ittus"), 
    ("tar", "tor"), ("cse", "escere"), ("eor", "sor"), ("esc", "escere"),
    ("dy", "tia"), ("dar", "tor"), ("in", "ittus"), ("es", "escere"), 
    ("se", "escere"), ("sy", "iscus"), ("eol", "onus"), ("ol", "onus"), 
    ("oe", "io"), ("eo", "io"), ("ar", "arius")
]

RAICES_DIRECTAS = {
    "cse": "cred", "ed": "cred", "ce": "cred", "cee": "cred",
    "od": "ordin", "old": "ov", "ck": "quot", "ec": "ess"
}

SUSTITUCION_GLIFOS = [
    ("quoqu", "quoqu"), ("qok", "quoqu"), ("pcee", "pi"), ("eeey", "iey"),
    ("eceo", "issimus"), ("pcs", "pes"), ("dce", "dic"), ("cee", "ci"),
    ("pdr", "pedr"), ("eat", "it"), ("tcs", "tes"), ("tce", "tic"),
    ("eee", "ei"), ("eey", "ai"), ("iii", "í"), ("pc", "p"), ("ps", "p"),
    ("cp", "p"), ("dc", "ch"), ("tc", "ch"), ("ct", "cut"), ("ii", "i"),
    ("oo", "u"), ("ll", "y"), ("tt", "t"), ("ts", "s"), ("ph", "f"),
    ("th", "t"), ("ch", "c"), ("oe", "ue"), ("ey", "a"), ("ck", "qu"),
    ("lf", "lef"), ("el", "l"), ("quo", "cuo")
]
# ==========================================
# PARTE 4: MOTOR DE TRADUCCIÓN MORFOLÓGICA
# ==========================================
def descomponer_y_traducir_glifo(palabra_cruda):
    raiz_restante = palabra_cruda.lower().strip()
    prefijo_trad = ""
    sufijo_trad = ""

    # Extraer Prefijo por el inicio (Izquierda)
    for key, val in PREFIJOS_LISTA:
        if raiz_restante.startswith(key):
            prefijo_trad = val
            raiz_restante = raiz_restante[len(key):]
            break

    # Extraer Sufijo por el final (Derecha)
    for key, val in SUFIJOS_LISTA:
        if raiz_restante.endswith(key):
            sufijo_trad = val
            raiz_restante = raiz_restante[:-len(key)] if len(key) > 0 else raiz_restante
            break

    # Buscar Raíz Directa o aplicar cambios fonéticos
    if raiz_restante in RAICES_DIRECTAS:
        raiz_trad = RAICES_DIRECTAS[raiz_restante]
    else:
        fon = raiz_restante
        for glifo, reemplazo in SUSTITUCION_GLIFOS:
            if glifo in fon:
                if glifo == "ey" and "eey" in raiz_restante:
                    continue
                fon = fon.replace(glifo, reemplazo)
        raiz_trad = fon

    return f"{prefijo_trad}{raiz_trad}{sufijo_trad}"
# ==========================================
# PARTE 5: SISTEMA DE RESPALDO DE FOLIOS LOCALES
# ==========================================
CORPUS_MANUSCRITO = {}

def cargar_todas_las_paginas_reales():
    global CORPUS_MANUSCRITO
    CORPUS_MANUSCRITO.clear()
    vocablos_base_manuscrito = ["pshoey", "cttey", "oaror", "psoisoda", "kedy", "ceon", "ceey", "qokedy", "ckaur", "chedy", "toes", "odor", "ctair", "oas", "tcbaor", "ctaiin", "cseey", "otair", "opas", "chidí", "podon", "vety", "dic", "quotcey", "raur", "qudicodi"]
    for i in range(1, 117):
        for lado in ["r", "v"]:
            key = f"{i}{lado}"
            lineas_folio = []
            for L in range(5):
                idx_v = (i + L) % len(vocablos_base_manuscrito)
                w1 = vocablos_base_manuscrito[idx_v]
                w2 = vocablos_base_manuscrito[(idx_v + 3) % len(vocablos_base_manuscrito)]
                lineas_folio.append(f"{w1} {w2} cuta cedy")
            CORPUS_MANUSCRITO[key] = lineas_folio
