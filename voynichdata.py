import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA.
    Ordenado de mayor a menor longitud para evitar conflictos de n-gramas.
    """
    if not texto_eva:
        return ""
        
    # Pasar a minúsculas para estandarizar la entrada del corpus
    texto = texto_eva.lower()
    
    # --- 1. REGLAS DE 4 CARACTERES ---
    texto = texto.replace("qok", "quoqu")
    
    # --- 2. REGLAS DE 3 CARACTERES ---
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("eey", "ai")
    texto = texto.replace("pcs", "pes")
    
    # --- 3. REGLAS DE 2 CARACTERES ---
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
    texto = texto.replace("ck", "qu")
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
    
    # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO (Y inicial/final) ---
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. REGLAS DE 1 CARÁCTER GENERALES ---
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")    
    
    # --- 6. FILTRO CRÍTICO: LIMPIEZA DE HACHES (H) HUÉRFANAS ---
    texto = texto.replace("h", "")
    
    return texto.strip()

def motor_prosa_fluida(texto_limpio: str) -> str:
    """
    Simulación adaptativa de traducción basada en raíces romances/latín.
    Sustituye esta lógica por la base de datos de palabras reales que usas.
    """
    palabras = texto_limpio.split()
    resultado = []
    
    # Diccionario de prueba basado en las raíces de tu cuadro
    diccionario_romance = {
        "cut": "cortar / incisión",
        "ci": "aquí / cercano",
        "ch": "clave / llamada",
        "ie": "ir / viaje",
        "dic": "decir / ley",
        "quoqu": "cocinar / preparar",
        "f": "hacer / propiedad",
        "x": "seco / planta"
    }
    
    for palabra in palabras:
        # Busca coincidencias aproximadas o literales
        if palabra in diccionario_romance:
            resultado.append(diccionario_romance[palabra])
        elif len(palabra) > 2 and palabra[:3] in diccionario_romance:
            resultado.append(diccionario_romance[palabra[:3]])
        else:
            # Si no hay traducción exacta, devuelve la transliteración limpia en mayúsculas
            resultado.append(palabra.upper())
            
    return " ".join(resultado)
