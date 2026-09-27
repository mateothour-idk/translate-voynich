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
        
    # Estandarizar a minúsculas
    texto = texto_eva.lower()
    
    # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
    # Procesamos 'pcee' aquí arriba para que 'pc' o 'cee' no la muten antes de tiempo
    texto = texto.replace("pcee", "pi")
    texto = texto.replace("qok", "quoqu")
    
    # --- 2. REGLAS DE 3 CARACTERES (Trigramas) ---
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("eey", "ai")
    texto = texto.replace("pcs", "pes")
    
    # --- 3. REGLAS DE 2 CARACTERES (Bigramas y Dígrafos) ---
    # Combinaciones Consonánticas
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
    
    # Reglas Vocálicas (Se integra la nueva reducción 'ai' -> 'i')
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
    texto = texto.replace("ai", "i")
    
    # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO ---
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. SUSTITUCIÓN FINAL DE CONSONANTES Q / K / CK ---
    # Al estar aquí abajo, la 'u' de 'qu' no vuelve a procesarse por las vocales,
    # eliminando para siempre el bug que generaba "quu".
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
    Examina las palabras reducidas por la matriz y busca aproximaciones 
    en un glosario maestro bilingüe (Español / Inglés).
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    
    # Glosario bilingüe de raíces basado en las equivalencias de tu cuadro
    diccionario_maestro = {
        "cut": {"es": "cortar / incisión", "en": "cut / incision"},
        "ci": {"es": "aquí / cercano", "en": "here / nearby"},
        "ch": {"es": "clave / llamada", "en": "key / call"},
        "ie": {"es": "ir / viaje", "en": "go / journey"},
        "dic": {"es": "decir / ley", "en": "say / law"},
        "quoqu": {"es": "cocinar / preparar", "en": "cook / prepare"},
        "f": {"es": "hacer / propiedad", "en": "make / property"},
        "x": {"es": "seco / planta", "en": "dry / plant"},
        "pes": {"es": "pie / base", "en": "foot / base"}
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
