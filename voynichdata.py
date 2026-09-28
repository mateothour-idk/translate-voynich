import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Ordenadas estrictamente de mayor a menor longitud.
    """
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    texto = texto.replace("pcee", "pi")
    texto = texto.replace("qok", "quoqu")
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")
    texto = texto.replace("eey", "ai")
    texto = texto.replace("pcs", "pes")
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p")
    texto = texto.replace("dc", "ch").replace("tc", "ch").replace("ct", "cut")
    texto = texto.replace("sh", "x").replace("ph", "f").replace("th", "t").replace("ch", "c").replace("ck", "qu").replace("cs", "s")
    texto = texto.replace("ee", "i").replace("oe", "ue").replace("iu", "u").replace("oi", "oi").replace("ii", "i").replace("ae", "e").replace("oo", "u").replace("ey", "a").replace("ai", "i").replace("ll", "y")
    texto = re.sub(r'\by\b', 'i', texto)
    texto = re.sub(r'\by', 'i', texto)
    texto = re.sub(r'y\b', 'i', texto)
    texto = texto.replace("k", "qu").replace("q", "qu")
    texto = texto.replace("h", "").replace("quu", "qu")
    return texto.strip()


def motor_prosa_fluida(texto_original_eva: str, idioma: str = "es") -> tuple:
    """
    Procesa el texto original en formato EVA y genera la traducción directa.
    """
    diccionario_eva = {
        "qokched": {"es": "extracto concentrado", "en": "concentrated extract"},
        "dcectth": {"es": "hervir en agua de lluvia", "en": "boil in rainwater"},
        "shol": {"es": "exponer al sol", "en": "expose to sun"},
        "dain": {"es": "añadir la infusión", "en": "add the infusion"},
        "pcs": {"es": "la base del tallo", "en": "the base of the stem"},
        "eeet": {"es": "calentar suavemente", "en": "heat gently"},
        "kold": {"es": "remedio añejo", "en": "aged remedy"},
        "ceeoo": {"es": "aplicar sobre la piel", "en": "apply to skin"},
        "kchos": {"es": "hojas secas molidas", "en": "ground dry leaves"},
        "dceae": {"es": "mezclar en caliente", "en": "mix while hot"},
        "thsh": {"es": "reposar una noche", "en": "rest overnight"},
        "cpoche": {"es": "colar el ungüento", "en": "strain the ointment"},
        "ctthsh": {"es": "machacar la raíz", "en": "crush the root"},
        "pceeoe": {"es": "esencia destilada", "en": "distilled essence"},
        "ceeii": {"es": "untar en la zona afectada", "en": "rub on affected area"},
        "iiiet": {"es": "filtrar el jugo", "en": "filter the juice"},
        "eyee": {"es": "hasta espesar", "en": "until thickened"},
        "iiict": {"es": "tomar en ayunas", "en": "take on fasting"},
        "dce": {"es": "indicar la dosis", "en": "indicate dose"},
        "qok": {"es": "cocimiento rápido", "en": "quick decoction"},
        "lllae": {"es": "flores silvestres", "en": "wild flowers"},
        "phoo": {"es": "polvo fino", "en": "fine powder"},
        "dcecee": {"es": "purificar la mezcla", "en": "purify the mixture"},
        "pcee": {"es": "zumo fresco", "en": "fresh juice"},
        "chod": {"es": "beber tibio", "en": "drink warm"},
        "eyct": {"es": "gotas diluidas", "en": "diluted drops"},
        "chold": {"es": "conservar en vasija", "en": "store in a vessel"},
        "dcetcc": {"es": "aplicar con paño limpio", "en": "apply with clean cloth"},
        "chooo": {"es": "gotas para los ojos", "en": "eye drops"},
        "sethol": {"es": "bálsamo reconfortante", "en": "comforting balm"},
        "eeyod": {"es": "guardar en frío", "en": "store in cold"},
        "koldoe": {"es": "ungüento para dolores", "en": "pain relief ointment"}
    }

    palabras_originales = texto_original_eva.split()
    analisis_estructurado = []
    palabras_oracion = []

    for palabra_eva in palabras_originales:
        palabra_eva_clean = palabra_eva.lower()
        palabra_filtrada = aplicar_matriz_sustitucion(palabra_eva_clean).upper()
        
        if palabra_eva_clean in diccionario_eva:
            traducida = diccionario_eva[palabra_eva_clean][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Exacto (EVA)" if idioma == "es" else "Exact Match (EVA)"
        else:
            traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
            palabra_para_oracion = f'"{palabra_filtrada}"'
            tipo = "Desconocido" if idioma == "es" else "Unknown"

        analisis_estructurado.append({
            "Morfología Filtrada": palabra_filtrada,
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
        palabras_oracion.append(palabra_para_oracion)

    oracion_completa = " ".join(palabras_oracion) + "."
    oracion_completa = re.sub(r'\s+', ' ', oracion_completa).replace(" .", ".")
    return analisis_estructurado, oracion_completa
