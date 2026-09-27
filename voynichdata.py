import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Cada regla tiene asignada la opción fonética más coherente para evitar ambigüedades.
    Las sustituciones se ejecutan estrictamente de mayor a menor longitud.
    """
    if not texto_eva:
        return ""
        
    texto = texto_eva.lower()
    
    # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
    texto = texto.replace("pcee", "pi")
    texto = texto.replace("qok", "quoqu")
    
    # --- 2. REGLAS DE 3 CARACTERES (Trigramas) ---
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")     # Eee = Ie (Evolución romance común)
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("eey", "ai")     # Eey = Ai (Diptongo estable)
    texto = texto.replace("pcs", "pes")
    
    # --- 3. REGLAS DE 2 CARACTERES (Bigramas y Dígrafos) ---
    texto = texto.replace("pc", "p")
    texto = texto.replace("ps", "p")
    texto = texto.replace("cp", "p")
    texto = texto.replace("dc", "ch")     # Dc con sonido de Ch
    texto = texto.replace("tc", "ch")     # Tc con sonido de Ch
    texto = texto.replace("ct", "cut")
    texto = texto.replace("ph", "f")
    texto = texto.replace("sh", "x")
    texto = texto.replace("th", "t")
    texto = texto.replace("ch", "c")      # Ch = C (Prioriza raíz consonántica limpia)
    texto = texto.replace("ck", "qu")
    
    # Reglas Vocálicas y Consonánticas secundarias de 2 letras
    texto = texto.replace("ee", "i")
    texto = texto.replace("oe", "ue")     # Oe = Ue (Diptongo romance como en 'huevo'/'rueda')
    texto = texto.replace("iu", "u")
    texto = texto.replace("oi", "oi")
    texto = texto.replace("ii", "i")
    texto = texto.replace("ae", "e")      # Ae = E (Monoptongación clásica del latín vulgar)
    texto = texto.replace("oo", "u")      # Oo = U (Frecuente en romances tempranos)
    texto = texto.replace("cs", "s")
    texto = texto.replace("ll", "y")
    texto = texto.replace("ey", "a")      # Ey = A corta
    texto = texto.replace("ce", "c")
    texto = texto.replace("ai", "i")      # Ai = I
    
    # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO (Y inicial/final) ---
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. SUSTITUCIÓN FINAL DE CONSONANTES Q / K ---
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")       # M = M
    texto = texto.replace("l", "l")       # L = L
    
    # --- 6. LIMPIEZA TOTAL DE HACHES (H) HUÉRFANAS ---
    texto = texto.replace("h", "")
    texto = texto.replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    """
    Procesa el texto limpio y devuelve una tupla:
    1. Una lista de diccionarios para la tabla analítica.
    2. La oración armada continuamente con las incógnitas entre comillas.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    palabras_oracion = []
    
    # Glosario con significados unificados y coherentes
    diccionario_maestro = {
        "cut": {"es": "cortar", "en": "cut"},
        "ci": {"es": "aquí", "en": "here"},
        "ch": {"es": "clave", "en": "key"},
        "ie": {"es": "ir", "en": "go"},
        "dic": {"es": "decir", "en": "say"},
        "quoqu": {"es": "cocinar", "en": "cook"},
        "f": {"es": "hacer", "en": "make"},
        "x": {"es": "seco", "en": "dry"},
        "pes": {"es": "pie", "en": "foot"},
        "col": {"es": "recolectar", "en": "collect"},
        "quok": {"es": "cocimiento", "en": "decoction"},
        "old": {"es": "antiguo", "en": "ancient"},
        "sho": {"es": "mostrar", "en": "show"},
        "dai": {"es": "dar", "en": "give"},
        "tth": {"es": "tierra", "en": "earth"},
        "cue": {"es": "cuerpo", "en": "body"},
        "xol": {"es": "sol", "en": "sun"},
        "tit": {"es": "título", "en": "title"},
        "pci": {"es": "pequeño", "en": "small"},
        "ole": {"es": "aceite", "en": "oil"},
        "sol": {"es": "disolver", "en": "dissolve"},
        "an": {"es": "año", "en": "year"},
        "ue": {"es": "fuente", "en": "source"},
        "ic": {"es": "imagen", "en": "image"}
    }
    
    for palabra in palabras:
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        palabra_para_oracion = f'"{palabra.upper()}"'  # Incógnita por defecto entre comillas
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        # 1. Match Exacto
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        # 2. Match Raíz 3 Letras
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:3]][idioma]
            palabra_para_oracion = traducida + f"({palabra[3:].upper()})"
            tipo = "Match Raíz (3L)" if idioma == "es" else "Root Match (3L)"
        # 3. Match Raíz 2 Letras
        elif len(palabra) > 1 and palabra[:2] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:2]][idioma]
            palabra_para_oracion = traducida + f"({palabra[2:].upper()})"
            tipo = "Match Raíz (2L)" if idioma == "es" else "Root Match (2L)"
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
        palabras_oracion.append(palabra_para_oracion)
            
    oracion_completa = " ".join(palabras_oracion) + "."
    return analisis_estructurado, oracion_completa
