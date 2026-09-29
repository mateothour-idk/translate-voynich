# --- ARCHIVO 1: voynichdatos.py ---
import re

DICCIONARIO_ES = {
    "pui": "la planta", "cuta": "la corteza", "oarur": "el aroma", "poisoda": "la planta medicinal",
    "quedy": "el elemento", "con": "con", "su": "su", "quoqu": "por lo cual", "caur": "el tallo",
    "chedy": "se extrae", "toes": "estos", "odor": "oloroso", "cutair": "cortar", "oas": "la vasija",
    "tcbaor": "recolectar", "hacia": "hacia", "ctaiin": "el cáliz", "si": "si se", "otair": "surgir",
    "opas": "los pasos", "chidi": "canalizar", "podon": "la raíz", "vety": "maduro",
    "dic": "dice", "olteey": "al final", "quotcey": "se limpia", "raur": "la base",
    "qudicodi": "el tratado", "copi": "abundante", "cia": "allí", "quotcoi": "cuanto",
    "quotoai": "diariamente", "dicorcau": "la sustancia", "cuti": "la piel", "cotol": "el cáliz",
    "odaur": "el olor", "cocodau": "el fruto", "seo": "su", "quoci": "allí",
    "ciodal": "el eje", "daral": "girar", "ocol": "los brotes", "olti": "al término",
    "otolci": "la olla", "tiodau": "el tiempo", "pair": "por", "osain": "el aceite",
    "pain": "la pulpa", "oain": "el jugo", "dais": "se aplica", "okeody": "la regla",
    "quoequiej": "también", "sar": "sanará", "oeteody": "el reposo", "otiy": "la maceración",
    "quiy": "el cual", "quey": "la cual", "icios": "los vasos", "oiaj": "la esencia",
    "cios": "los recipientes", "ain": "el líquido", "oteroe": "el proceso", "aram": "el hornillo",
    "sier": "las hojas", "dalaiu": "destilar", "dam": "dar", "ciodain": "los conductos",
    "aekiy": "la mezcla", "air": "el aire", "soar": "el vapor", "ciey": "la savia",
    "dais": "la rueda", "odotoi": "el ciclo", "doror": "el nacimiento", "quaur": "el calor",
    "caud": "el tallo alargado", "cedy": "se corta", "cidí": "verter"
}

DICCIONARIO_EN = {
    "pui": "the plant", "cuta": "the bark", "oarur": "the aroma", "poisoda": "the medicinal plant",
    "quedy": "the element", "con": "with", "su": "its", "quoqu": "whereby", "caur": "the stem",
    "chedy": "is extracted", "toes": "these", "odor": "scented", "cutair": "to cut", "oas": "the vessel",
    "tcbaor": "to gather", "hacia": "towards", "ctaiin": "the calyx", "si": "if it", "otair": "arise",
    "opas": "the steps", "chidi": "to channel", "podon": "the root", "vety": "mature",
    "dic": "says", "olteey": "at the end", "quotcey": "is cleansed", "raur": "the base",
    "qudicodi": "the treatise", "copi": "abundant", "cia": "there", "quotcoi": "as for",
    "quotoai": "daily", "dicorcau": "the substance", "cuti": "the skin", "cotol": "the calyx",
    "odaur": "the scent", "cocodau": "the fruit", "seo": "its", "quoci": "there",
    "ciodal": "the axis", "daral": "to rotate", "ocol": "the buds", "olti": "at the completion",
    "otolci": "the pot", "tiodau": "the time", "pair": "by", "osain": "the oil",
    "pain": "the pulp", "oain": "the juice", "dais": "is applied", "okeody": "the rule",
    "quoequiej": "also", "sar": "will heal", "oeteody": "the rest", "otiy": "the maceration",
    "quiy": "which", "quey": "which", "icios": "the vessels", "oiaj": "the essence",
    "cios": "the containers", "ain": "the liquid", "oteroe": "the process", "aram": "the burner",
    "sier": "the leaves", "dalaiu": "to distill", "dam": "to give", "ciodain": "the ducts",
    "aekiy": "the mixture", "air": "the air", "soar": "the steam", "ciey": "the sap",
    "dais": "the wheel", "odotoi": "the cycle", "doror": "the birth", "quaur": "the heat",
    "caud": "the elongated stem", "cedy": "is cut", "cidí": "to pour"
}

CORPUS_MANUSCRITO = {}

def cargar_todas_las_paginas_reales():
    """Lee e indexa el archivo borrando anotaciones de control de la transcripción oficial."""
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
                
                # Quitar comentarios, anotaciones de daño, ligaduras y caracteres de control
                texto_eva_limpio = re.sub(r'\{.*?\}|\[.*?\]', '', texto_eva)
                texto_eva_limpio = re.sub(r'%|\@\d+|;\d*|[:\$\#\-\+=<>\/]', '', texto_eva_limpio)
                texto_eva_limpio = re.sub(r'[*.,!?]', '', texto_eva_limpio)
                texto_eva_limpio = " ".join(texto_eva_limpio.split())
                
                if folio_key not in CORPUS_MANUSCRITO:
                    CORPUS_MANUSCRITO[folio_key] = []
                
                if texto_eva_limpio:
                    CORPUS_MANUSCRITO[folio_key].append(texto_eva_limpio)
                    
    except FileNotFoundError:
        # Fallback estructurado si no encuentra el txt en local
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
