import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Las reglas se ejecutan estrictamente de mayor a menor longitud para evitar
    conflictos o mutilaciones de dígrafos, y las reglas vocálicas se ejecutan 
    antes que Q/K para evitar duplicaciones indebidas (eliminando el bug quu).
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
    texto = texto.replace("sh", "s")       # Procesado por defecto como 's' antes de limpiar h
    texto = texto.replace("th", "t")
    texto = texto.replace("ch", "c")      # Ch = C (Prioriza raíz consonántica limpia)
    texto = texto.replace("ck", "qu")
    
    # Reglas Vocálicas y Consonánticas secundarias de 2 letras
    texto = texto.replace("ee", "i")
    texto = texto.replace("oe", "ue")     # Oe = Ue (Diptongo romance común)
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
    texto = texto.replace("m", "m")       
    texto = texto.replace("l", "l")       
    
    # --- 6. LIMPIEZA TOTAL DE HACHES (H) HUÉRFANAS ---
    texto = texto.replace("h", "")
    texto = texto.replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    """
    Procesa el texto limpio y devuelve una tupla:
    1. Una lista de diccionarios para la tabla analítica.
    2. La oración armada continuamente, separando palabras compuestas de forma inteligente.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    palabras_oracion = []
    
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
        # --- DETECTOR Y SEPARADOR DE COMPUESTAS ---
        palabra_compuesta_detectada = False
        for i in range(2, len(palabra) - 1):
            sub1 = palabra[:i]
            sub2 = palabra[i:]
            if sub1 in diccionario_maestro and sub2 in diccionario_maestro:
                trad1 = diccionario_maestro[sub1][idioma]
                trad2 = diccionario_maestro[sub2][idioma]
                
                palabras_oracion.append(f"{trad1}+{trad2}")
                palabra_compuesta_detectada = True
                
                analisis_estructurado.append({
                    "Morfología Filtrada": palabra.upper(),
                    "Interpretación / Semántica": f"{trad1} / {trad2}",
                    "Diagnóstico": "Compuesta Separada" if idioma == "es" else "Split Compound"
                })
                break
                
        if palabra_compuesta_detectada:
            continue
            
        # --- PROCESAMIENTO ESTÁNDAR SI NO ES COMPUESTA ---
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        palabra_para_oracion = f'"{palabra.upper()}"'  # Incógnita entre comillas
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:3]][idioma]
            palabra_para_oracion = traducida + f"(= {palabra[3:].upper()})"
            tipo = "Match Raíz (3L)" if idioma == "es" else "Root Match (3L)"
        elif len(palabra) > 1 and palabra[:2] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:2]][idioma]
            palabra_para_oracion = traducida + f"(= {palabra[2:].upper()})"
            tipo = "Match Raíz (2L)" if idioma == "es" else "Root Match (2L)"
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
        palabras_oracion.append(palabra_para_oracion)
            
    oracion_completa = " ".join(palabras_oracion) + "."
    return analisis_estructurado, oracion_completa
