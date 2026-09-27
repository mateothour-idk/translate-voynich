import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    if not texto_eva:
        return ""
        
    texto = texto_eva.lower()
    
    # 1. PROCESAR TRIGRAMAS Y TETRAGRAMAS PRIMERO
    texto = texto.replace("qok", "quoqu")
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("eey", "ai")
    texto = texto.replace("pcs", "pes")
    
    # 2. PROCESAR BIGRAMAS DE CONSONANTES Y LIGADURAS (Protegiendo raíces)
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
    
    # 3. PROCESAR VOCALES COMPUESTAS (Antes de generar nuevas 'u' con Q/K)
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
    
    # 4. CONTEXTO PARA LA 'Y'
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # 5. REGLAS DE Q / K / CK INTERCALADAS AL FINAL
    # Al ponerlas aquí abajo, la 'u' generada por 'qu' YA NO SERÁ AFECTADA 
    # por las reglas de vocales anteriores, eliminando el bug de "quu".
    texto = texto.replace("ck", "qu")
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")    
    
    # 6. LIMPIEZA DE HACHES HUÉRFANAS
    texto = texto.replace("h", "")
    
    # Arreglo de seguridad por si alguna otra regla duplicó la u al final
    texto = texto.replace("quu", "qu")
    
    return texto.strip()

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> str:
    """
    Motor adaptativo que ahora soporta traducción tanto a Español ('es') como Inglés ('en').
    """
    palabras = texto_limpio.split()
    resultado = []
    
    # Diccionario bilingüe expandido con las raíces de tu cuadro
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
        if palabra in diccionario_maestro:
            resultado.append(diccionario_maestro[palabra][idioma])
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            resultado.append(diccionario_maestro[palabra[:3]][idioma])
        else:
            # Si no se encuentra, deja el token limpio estructurado
            resultado.append(palabra.upper())
            
    return " ".join(resultado)
