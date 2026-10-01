# ==========================================
# PARTE 1: DICCIONARIO ESPAÑOL EXPANDIDO (A-M)
# ==========================================
import re

DICCIONARIO_ES = {
    # --- Raíces Originales de Tu Matriz ---
    "pui": "planta", "cuta": "corteza", "oarur": "aroma", "poisoda": "poción (medicina)",
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
    "air": "aire", "soar": "vapor", "ciey": "savia", "odotoi": "ciclo", 
    "doror": "nacimiento", "quaur": "calor", "caud": "tallo largo", "cedy": "cortar", "cidí": "verter",

    # --- Novedad: Mapeo de Combinaciones de Tu Matriz Lingüística ---
    "transtor": "el que transfiere / canalizador",
    "subtor": "el que sostiene desde abajo / base inferior",
    "subperensis": "perteneciente a lo más profundo / subterráneo",
    "superosus": "abundante en la superficie / rebosante",
    "infotia": "sustancia que introduce fuerza / información interna",
    "confoquotensis": "proporción medida en conjunto / confluencia",
    "porcredensis": "con capacidad de filtración / poroso confiable",
    "lefcensis": "recolectado en el sector lateral o izquierdo",
    "daittus": "lo que ha sido separado u otorgado formalmente",
    "intercredensis": "vínculo intermedio de confianza / canal interno",
    "conarius": "perteneciente o relativo a la glándula pineal / cono central",
    "credticius": "que merece crédito / elemento fidedigno",
    "quotatia": "medida calculada por partes / cantidad exacta",
    "conquotatia": "suma total de las proporciones medidas",
    "porarius": "relacionado con los poros / conductor de fluidos",
    "ovarius": "lugar donde se resguardan las semillas o embriones",
    "quotarius": "recipiente dosificado / medidor de porciones",
    "porariustatem": "propiedad o cualidad de la porosidad absoluta",

    # --- Anatomía Botánica Avanzada ---
    "folia": "hoja", "ramus": "rama", "flos": "flor", "semen": "semilla", "capsa": "cápsula",
    "gemma": "yema", "nux": "nuez", "baca": "baya", "spina": "espina", "radix": "raíz profunda",
    "stolo": "estolón", "bulbus": "bulbo", "vimen": "mimbre", "cortex": "corteza externa",
    "medula": "médula interior", "pith": "núcleo", "nodo": "nudo del tallo", "internod": "entrenudo",
    "petalo": "pétalo", "sepalo": "sépalo", "pollen": "polen", "anthera": "antera",
    "foliolo": "hoja pequeña", "peduncul": "pedúnculo/rabillo del fruto", "frond": "follaje/fronda",
    "stigma": "estigma (receptor del polen)", "carpel": "carpelo (órgano femenino)",
    "rhizoma": "tallo subterráneo", "tuber": "tubérculo", "filament": "filamento de la flor",
# ==========================================
# PARTE 2: DICCIONARIO ESPAÑOL (N-Z) Y MACRO_GLIFOS
# ==========================================
    # --- Cualidades Alquímicas y Estados ---
    "humida": "húmedo", "sicca": "seco", "calida": "caliente", "frigida": "frío", "amara": "amargo",
    "dulcis": "dulce", "acris": "acre", "mitis": "suave", "veneno": "venenoso", "salutis": "curativo",
    "sanct": "sagrado", "oculta": "secreto/oculto", "cocta": "cocido", "cruda": "crudo",
    "pura": "puro", "mixta": "mezclado", "soluta": "disuelto", "spissa": "espeso", "tenuis": "delgado",
    "recens": "fresco", "vetus": "viejo", "marcida": "marchito", "viridis": "verde",
    "alba": "blanco", "nigra": "negro", "rubra": "rojo", "lutea": "amarillo", "tosta": "tostado",
    "viscosa": "pegajoso/viscoso", "fluida": "corriente/líquido", "odorata": "fragante",

    # --- Operaciones de Laboratorio Medieval ---
    "coctio": "cocción", "infuso": "infusión", "macer": "macerar", "filtr": "filtrar",
    "colat": "colar", "trit": "triturar", "conter": "moler", "coag": "coagular",
    "solv": "disolver", "evap": "evaporar", "sublim": "sublimar", "ferment": "fermentar",
    "expre": "exprimir", "lavat": "lavado", "purgat": "purga", "unctu": "ungüento",
    "gutta": "gotas", "pulvis": "polvo", "sirup": "jarabe", "elixir": "elixir",
    "decoct": "hervido concentrado", "calcina": "reducir a cenizas", "ole": "extracción aceitosa",
    "balneu": "baño de vapor/María", "amalgama": "unión de elementos", "tinctura": "tintura madre",

    # --- Clasificación y Géneros de Plantas ---
    "herba": "hierba", "arbor": "árbol", "frutex": "arbusto", "muscus": "musgo", "fungus": "hongo",
    "filix": "helecho", "alga": "alga", "juncus": "junco", "gramen": "gramínea",
    "salvia": "salvia", "malva": "malva", "mentha": "menta", "rosa": "rosa", "lilium": "lirio",
    "papaver": "amapola", "solanum": "solano", "apis": "apio", "allium": "ajo",
    "abrotan": "abrótano", "aconit": "acónito", "mandrag": "mandrágora", "hellebor": "eléboro",

    # --- Virtudes Curativas y Órganos Humanos ---
    "sana": "sanar", "cura": "curar", "lenit": "aliviar", "purg": "purgar", "dorm": "hacer dormir",
    "vulner": "heridas", "febri": "fiebre", "dolor": "dolor", "stoma": "estómago", "capitis": "cabeza",
    "ocul": "ojos", "cutis": "afecciones de la piel", "pectus": "pecho/tos",
    "hepar": "hígado", "renes": "riñones", "cor": "corazón", "arteria": "vasos sanguíneos",
    "uterus": "matriz/útero", "vulva": "órgano femenino", "membrana": "tejido delgado"
}

DICCIONARIO_MACRO_GLIFOS = {
    "QA": "[Sección Astral]", "PC": "[Párrafo Central]", "FB": "[Folio Botánico]", 
    "B2": "[Grupo Biológico 2]", "IH": "[Ilustración de Herboristería]", "LA": "[Línea Alta]", 
    "H1": "[Encabezado Principal]", "C1": "[Cifrado Primario]"
}
# ==========================================
# PARTE 3: DICCIONARIO INGLÉS COMPLETO
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
    
    # Matriz transliterations
    "transtor": "the one who transfers / channeler", "subtor": "lower supporting base",
    "subperensis": "subterranean / deepest layer", "superosus": "overflowing on surface",
    "infotia": "internal information / force", "confoquotensis": "measured proportion",
    "porcredensis": "porous reliable filter", "lefcensis": "gathered from left side",
    "daittus": "separated or granted element", "intercredensis": "internal trust channel",
    "conarius": "relating to pineal gland / cone", "credticius": "trustworthy element",
    "quotatia": "exact calculated quantity", "conquotatia": "sum of measured parts",
    "porarius": "pore relative / fluid conductor", "ovarius": "seed or embryo holder",
    "quotarius": "dosed vessel / proportioner", "porariustatem": "property of absolute porosity",

    # Botanical terms
    "folia": "leaf", "ramus": "branch", "flos": "flower", "semen": "seed", "capsa": "capsule",
    "gemma": "bud", "nux": "nut", "baca": "berry", "spina": "thorn", "radix": "deep root",
    "stolo": "stolon", "bulbus": "bulb", "vimen": "osier", "cortex": "outer bark",
    "medula": "inner pith", "pith": "core", "nodo": "stem node", "internod": "internode",
    "petalo": "petal", "sepalo": "sepal", "pollen": "pollen", "anthera": "anther",
    "foliolo": "leaflet", "peduncul": "fruit stem", "frond": "foliage", "stigma": "stigma",
    "carpel": "carpel", "rhizoma": "rhizome", "tuber": "tuber", "filament": "stamen filament",

    # Alchemical and processing states
    "humida": "moist", "sicca": "dry", "calida": "hot", "frigida": "cold", "amara": "bitter",
    "dulcis": "sweet", "acris": "acrid", "mitis": "mild", "veneno": "poisonous", "salutis": "healing",
    "sanct": "sacred", "oculta": "hidden/secret", "cocta": "cooked", "cruda": "raw",
    "pura": "pure", "mixta": "mixed", "soluta": "dissolved", "spissa": "thick", "tenuis": "thin",
    "recens": "fresh", "vetus": "old", "marcida": "withered", "viridis": "green",
    "alba": "white", "nigra": "black", "rubra": "red", "lutea": "yellow", "tosta": "roasted",
    "viscosa": "viscous", "fluida": "fluid", "odorata": "fragrant",

    # Medieval Lab procedures
    "coctio": "decoction", "infuso": "infusion", "macer": "macerate", "filtr": "filter",
    "colat": "strain", "trit": "crush", "conter": "grind", "coag": "coagulate",
    "solv": "dissolve", "evap": "evaporate", "sublim": "sublimar", "ferment": "ferment",
    "expre": "squeeze", "lavat": "washed", "purgat": "purge", "unctu": "ointment",
    "gutta": "drops", "pulvis": "powder", "sirup": "syrup", "elixir": "elixir",
    "decoct": "concentrated boiling", "calcina": "calcination", "ole": "oil extraction",
    "balneu": "steam bath", "amalgama": "amalgam", "tinctura": "mother tincture",

    # Plant families and health
    "herba": "herb", "arbor": "tree", "frutex": "shrub", "muscus": "moss", "fungus": "fungus",
    "filix": "fern", "alga": "algae", "juncus": "reed", "gramen": "grass",
    "salvia": "sage", "malva": "mallow", "mentha": "mint", "rosa": "rose", "lilium": "lily",
    "papaver": "poppy", "solanum": "nightshade", "apis": "celery", "allium": "garlic",
    "abrotan": "southernwood", "aconit": "aconite", "mandrag": "mandrake", "hellebor": "hellebore",
    "sana": "heal", "cura": "cure", "lenit": "soothe", "purg": "purge", "dorm": "induce sleep",
    "vulner": "wounds", "febri": "fever", "dolor": "pain", "stoma": "stomach", "capitis": "head",
    "ocul": "eyes", "cutis": "skin conditions", "pectus": "chest/cough",
    "hepar": "liver", "renes": "kidneys", "cor": "heart", "arteria": "blood vessels",
    "uterus": "womb", "vulva": "female organ", "membrana": "membrane"
}
# ==========================================
# PARTE 4: MATRICES, MOTOR Y RESPALDO LOCAL
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

CORPUS_MANUSCRITO = {}

def descomponer_y_traducir_glifo(palabra_cruda):
    raiz_restante = palabra_cruda.lower().strip()
    prefijo_trad = ""
    sufijo_trad = ""

    # Extraer Prefijo
    for key, val in PREFIJOS_LISTA:
        if raiz_restante.startswith(key):
            prefijo_trad = val
            raiz_restante = raiz_restante[len(key):]
            break

    # Extraer Sufijo
    for key, val in SUFIJOS_LISTA:
        if raiz_restante.endswith(key):
            sufijo_trad = val
            raiz_restante = raiz_restante[:-len(key)] if len(key) > 0 else raiz_restante
            break

    # Resolver Raíz
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
