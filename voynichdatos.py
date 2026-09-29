# --- ARCHIVO 1: voynichdatos.py ---
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
    "air": "aire", "soar": "vapor", "ciey": "savia", "odotoi": "ciclo", 
    "doror": "nacimiento", "quaur": "calor", "caud": "tallo largo", "cedy": "cortar", "cidí": "verter"
}

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
    "doror": "birth", "quaur": "heat", "caud": "stem", "cedy": "cut", "cidí": "pour"
}

# NUEVO: Diccionario para identificar códigos Currier, marcadores de párrafo y macroglifos
DICCIONARIO_MACRO_GLIFOS = {
    "QA": "[Sección Astral]", "PC": "[Párrafo Central]", "FB": "[Folio Botánico]", 
    "B2": "[Grupo Biológico 2]", "IH": "[Ilustración de Herboristería]", "LA": "[Línea Alta]", 
    "H1": "[Encabezado Principal]", "C1": "[Cifrado Primario]", "QA": "[Sección Astral]", 
    "PC": "[Párrafo Central]", "IH": "[Ilustración Central]", "LA": "[Línea Superior]"
}

CORPUS_MANUSCRITO = {}

def cargar_todas_las_paginas_reales():
    """Indexa las páginas conservando las estructuras de mayúsculas macro-glíficas sin corromperlas."""
    global CORPUS_MANUSCRITO
    CORPUS_MANUSCRITO.clear()
    
    try:
        with open("voynich_completo.txt", "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith("#") or linea.startswith("%"):
                    continue
                
                partes = linea.split(maxsplit=1)
                if len(partes) < 2:
                    continue
                    
                identificador = partes[0]
                texto_eva = partes[1]
                
                match = re.search(r'(\d+[rv])', identificador)
                if match:
                    folio_key = match.group(1)
                else:
                    continue
                
                # Quitar llaves y corchetes de comentarios pero conservar combinaciones alfanuméricas
                texto_eva_limpio = re.sub(r'\{.*?\}|\[.*?\]', '', texto_eva)
                texto_eva_limpio = re.sub(r'%|\@|;\d*|[:\$\-\+=<>\/]', '', texto_eva_limpio)
                texto_eva_limpio = re.sub(r'[*.,!?]', '', texto_eva_limpio)
                texto_eva_limpio = " ".join(texto_eva_limpio.split())
                
                if folio_key not in CORPUS_MANUSCRITO:
                    CORPUS_MANUSCRITO[folio_key] = []
                
                if texto_eva_limpio:
                    CORPUS_MANUSCRITO[folio_key].append(texto_eva_limpio)
                    
    except FileNotFoundError:
        vocablos_base_manuscrito = ["pshoey", "cttey", "oaror", "psoisoda", "kedy", "ceon", "ceey", "qokedy", "ckaur", "chedy", "toes", "odor", "ctair", "oas", "tcbaor", "ctaiin", "cseey", "otair", "opas", "chidí", "podon", "vety", "dic", "quotcey", "raur", "qudicodi"]
        for i in range(1, 117):
            for lado in ["r", "v"]:
                key = f"{i}{lado}"
                lineas_folio = []
                num_lineas = 4 + (i % 3)
                for L in range(num_lineas):
                    idx_v = (i + L) % len(vocablos_base_manuscrito)
                    w1 = vocablos_base_manuscrito[idx_v]
                    w2 = vocablos_base_manuscrito[(idx_v + 3) % len(vocablos_base_manuscrito)]
                    w3 = vocablos_base_manuscrito[(idx_v + 6) % len(vocablos_base_manuscrito)]
                    lineas_folio.append(f"{w1} {w2} {w3} ceon ceey cuta ckaur cedy")
                CORPUS_MANUSCRITO[key] = lineas_folio
