import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA.
    Ordenado estrictamente de mayor a menor longitud para evitar que 
    los caracteres individuales mutilen combinaciones caligráficas estables.
    """
    if not texto_eva:
        return ""
        
    # Estandarizar el texto a minúsculas
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
    # Combinaciones consonánticas
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
    
    # Vocales y ligaduras compuestas (Procesadas ANTES de generar la 'u' de Q/K)
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
    # Posicionamiento de la 'Y' en los extremos o aislada de la palabra
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. REGLAS DE SUSTITUCIÓN DE Q / K / CK ---
    # Al procesarse al final, la 'u' de 'qu' ya no es alterada por 
    # las reglas de diptongos o vocales anteriores, mitigando el bug.
    texto = texto.replace("ck", "qu")
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")    
    
    # --- 6. FILTRO DE LIMPIEZA CRÍTICO ---
    # Eliminación definitiva de las haches (h) huérfanas o decorativas
    texto = texto.replace("h", "")
    
    # Seguro final por si alguna combinación externa forzó una doble vocal
    texto = texto.replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> str:
    """
    Busca raíces transformadas en el texto procesado por la matriz 
    y entrega una correspondencia bilingüe en Español ('es') o Inglés ('en').
    """
    palabras = texto_limpio.split()
    resultado = []
    
    # Diccionario bilingüe maestro mapeado según las reglas de tu cuadro
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
        # 1. Comprobación de coincidencia exacta
        if palabra in diccionario_maestro:
            resultado.append(diccionario_maestro[palabra][idioma])
        # 2. Comprobación por raíz de tres caracteres iniciales
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            resultado.append(diccionario_maestro[palabra[:3]][idioma])
        # 3. Fallback: Si no hay match, muestra el token limpio en mayúsculas
        else:
            resultado.append(palabra.upper())
            
    return " ".join(resultado)
