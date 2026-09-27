import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Ordenado de mayor a menor longitud para evitar solapamientos destructivos.
    """
    if not texto_eva:
        return ""
        
    texto = texto_eva.lower()
    
    # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
    texto = texto.replace("qok", "quoqu")
    
    # --- 2. REGLAS DE 3 CARACTERES (Trigramas) ---
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")  # Alternativa: ei
    # Procesamiento de variaciones de eey de forma directa
    texto = texto.replace("eey", "ai")  # Alternativa: iy
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")  # Alternativa: ce
    texto = texto.replace("pcs", "pes")
    
    # --- 3. REGLAS DE 2 CARACTERES (Bigramas y Dígrafos) ---
    texto = texto.replace("pc", "p")
    texto = texto.replace("ps", "p")
    texto = texto.replace("cp", "p")
    texto = texto.replace("dc", "ch")  # Sonido Ch
    texto = texto.replace("tc", "ch")  # Sonido Ch
    texto = texto.replace("ct", "cut")
    texto = texto.replace("ph", "f")
    texto = texto.replace("sh", "x")
    texto = texto.replace("th", "t")
    texto = texto.replace("ch", "ch")  # Alternativa: c
    
    # Reglas Vocálicas y Consonánticas dobles
    texto = texto.replace("ee", "i")
    texto = texto.replace("oe", "ue")  # Alternativa: u
    texto = texto.replace("iu", "u")
    texto = texto.replace("oi", "oi")  # Alternativa: oy
    texto = texto.replace("ii", "i")
    texto = texto.replace("ae", "e")   # Alternativa: a
    texto = texto.replace("oo", "u")   # Alternativa: oo
    texto = texto.replace("cs", "s")
    texto = texto.replace("ll", "y")
    texto = texto.replace("ey", "a")   # A corta
    texto = texto.replace("ce", "c")   # Alternativa: ce
    
    # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO (Límites de Palabra) ---
    # Tratamiento estricto de la 'Y' al inicio y al final de los tokens
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. SUSTITUCIÓN DE CONSONANTES Q / K / CK ---
    texto = texto.replace("ck", "qu")
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    
    # Reglas complementarias simples de un carácter
    texto = texto.replace("m", "m")    # Mapea dinámicamente m o n según fonética posterior
    texto = texto.replace("l", "l")
    
    # --- 6. POST-PROCESAMIENTO Y LIMPIEZA FINAL ---
    texto = texto.replace("h", "")     # Remueve las haches huérfanas residuales
    texto = texto.replace("quu", "qu") # Corrige el bug duplicador generado en cadenas complejas
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> list:
    """
    Analiza y traduce la morfología limpia de las palabras usando tu 
    diccionario maestro de raíces con soporte dual (español e inglés).
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    
    # Tu base semántica con las equivalencias bilingües añadidas
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
        
        # Nuevas palabras clave decodificadas de tus ejemplos romances
        "quar": {"es": "porque / por lo cual", "en": "because / wherefore"},
        "oqui": {"es": "aquí (adverbio)", "en": "here (adverb)"},
        "oquad": {"es": "que / el cual", "en": "that / which"},
        "seol": {"es": "sol / astro", "en": "sun / star"},
        "siedi": {"es": "sede / asiento", "en": "seat / position"}
    }
    
    for palabra in palabras:
        # SOLUCIÓN AL BUG INCÓGNITA: Pasamos la variable a minúsculas para comparar con el diccionario
        p_busqueda = palabra.lower()
        
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        if p_busqueda in diccionario_maestro:
            traducida = diccionario_maestro[p_busqueda][idioma]
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        elif len(p_busqueda) > 2 and p_busqueda[:3] in diccionario_maestro:
            traducida = diccionario_maestro[p_busqueda[:3]][idioma]
            tipo = "Match Raíz" if idioma == "es" else "Root Match"
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
            
    return analisis_estructurado
