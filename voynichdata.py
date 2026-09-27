import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Ordenado de mayor a menor longitud para evitar conflictos y con reglas 
    vocálicas ejecutadas antes de Q/K para eliminar el bug 'quu'.
    """
    if not texto_eva:
        return ""
        
    texto = texto_eva.lower()
    
    # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
    texto = texto.replace("qok", "quoqu")
    
    # --- 2. REGLAS DE 3 CARACTERES (Trigramas) ---
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("eey", "ai")
    texto = texto.replace("pcs", "pes")
    
    # --- 3. REGLAS DE 2 CARACTERES (Bigramas y Dígrafos) ---
    texto = texto.replace("pc", "p")
    texto = texto.replace("ps", "p")
    texto = texto.replace("cp", "p")
    texto = texto.replace("dc", "ch") 
    texto = texto.replace("tc", "ch") 
    texto = texto.replace("ct", "cut")
    texto = texto.replace("ph", "f")
    texto = texto.replace("sh", "x")
    texto = texto.replace("th", "t")
    texto = texto.replace("ch", "c")   
    
    # Reglas Vocálicas (Paso crítico: evitan duplicaciones en Q/K)
    texto = texto.replace("ee", "i")
    texto = texto.replace("oe", "ue")  
    texto = texto.replace("iu", "u")
    texto = texto.replace("oi", "oi")  
    texto = texto.replace("ii", "i")
    texto = texto.replace("ae", "e")   
    texto = texto.replace("oo", "u")
    texto = texto.replace("cs", "s")
    texto = texto.replace("ll", "y")
    texto = texto.replace("ey", "a")   
    texto = texto.replace("ce", "c")
    
    # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO ---
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. SUSTITUCIÓN FINAL DE CONSONANTES Q / K / CK ---
    texto = texto.replace("ck", "qu")
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")    
    
    # --- 6. LIMPIEZA TOTAL DE HACHES (H) HUÉRFANAS ---
    texto = texto.replace("h", "")
    texto = texto.replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> list:
    """
    Analiza y traduce la morfología limpia de las palabras usando tu 
    diccionario maestro de raíces con soporte dual (español e inglés).
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    
    diccionario_maestro = {
        "cut": {"es": "cortar / incisión", "en": "cut / incision"},
        "ci": {"es": "aquí / cercano", "en": "here / nearby"},
        "ch": {"es": "clave / llamada", "en": "key / call"},
        "ie": {"es": "ir / viaje", "en": "go / journey"},
        "dic": {"es": "decir / ley", "en": "say / law"},
        "quoqu": {"es": "cocinar / preparar", "en": "cook / prepare"},
        "f": {"es": "hacer / propiedad", "en": "make / property"},
        "x": {"es": "seco / planta", "en": "dry / plant"},
        "pes": {"es": "pie / base", "en": "foot / base"},
        "quar": {"es": "porque / por lo cual", "en": "because / wherefore"},
        "oqui": {"es": "aquí (adverbio)", "en": "here (adverb)"},
        "oquad": {"es": "que / el cual", "en": "that / which"},
        "seol": {"es": "sol / astro", "en": "sun / star"},
        "siedi": {"es": "sede / asiento", "en": "seat / position"}
    }
    
    for palabra in palabras:
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:3]][idioma]
            tipo = "Match Raíz" if idioma == "es" else "Root Match"
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
            
    return analisis_estructurado
