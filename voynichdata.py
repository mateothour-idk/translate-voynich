import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """ Aplica las 42 reglas de transliteración estructuradas en capas de longitud para evitar colisiones """
    if not texto_eva: return ""
    texto = texto_eva.lower()
    
    # Limpieza profunda de ruidos del transcriptor (comas, corchetes con dudas, etc.)
    texto = re.sub(r'\[\s*\w+\s*:\s*\w+\s*\]', ' ', texto)
    texto = re.sub(r'[*-/=+%&$#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Diccionarios ordenados por capas estrictas de reemplazo (Tetragramas -> Trigramas -> Bigramas)
    capa_0 = {"pceeoe": "piue", "pcee": "pi", "qok": "quoqu"}
    capa_1 = {"iii": "i", "eee": "ei", "dce": "dic", "cee": "ci", "eey": "ai", "pcs": "pes", "pdr": "pedr", "eat": "it"}
    capa_2 = {"pc": "p", "ps": "p", "cp": "p", "dc": "ch", "tc": "ch", "cs": "s", "ck": "qu", "ct": "cut", "ph": "f", "th": "t", "tt": "t", "ts": "s", "ll": "y"}  # CORREGIDO AQUÍ
    capa_3 = {"ee": "i", "oe": "ue", "iu": "u", "oi": "oi", "ii": "i", "ae": "e", "oo": "u", "ey": "a", "iy": "i", "ai": "i", "x": "sh"}
    
    for capa in [capa_0, capa_1, capa_2, capa_3]:
        for k, v in capa.items():
            texto = texto.replace(k, v)
            
    # Capa 4: Reglas contextuales de borde y finales de palabra
    texto = re.sub(r'\by', 'i', texto)
    texto = re.sub(r'y\b', 'i', texto)
    texto = re.sub(r'\by\b', 'i', texto)
    texto = re.sub(r'm\b', 'n', texto) # Regla M = M / N al final de palabra
    
    # Sustitución base de K / Q / QUO y blindaje ortográfico
    texto = texto.replace("quo", "qu").replace("k", "qu").replace("q", "qu").replace("quu", "qu")
    texto = re.sub(r'\bchseor\b', 'senior', texto)
    st_texto = re.sub(r'\bseor\b', 'senior', texto)
    texto = re.sub(r'iin\b', 'am', texto)
    texto = re.sub(r'eiy\b', 'e', texto)
    texto = re.sub(r'oitio', 'otio', texto)
    texto = re.sub(r'(?<!s)(?<!c)h', '', texto)
    
    return texto.strip()

def resolver_contexto_palabra(palabra: str) -> list:
    """ Genera la lista de variaciones permitidas por las reglas con barra cruzada (/) """
    p = palabra.lower()
    variaciones = [p]
    if p.startswith("qu") and len(p) > 2: variaciones.append(p.replace("qu", "q", 1))
    if "ue" in p: variaciones.append(p.replace("ue", "u"))
    if p.endswith("c"): variaciones.append(p + "e")
    if p.startswith("l") and len(p) > 1: variaciones.append("e" + p)
    return list(set(variaciones))

def desarmar_palabra_compuesta(palabra: str) -> str:
    """ Motor universal adaptativo sin internet. Resuelve morfemas de forma autónoma. """
    p = palabra.lower()
    if not p: return ""
    
    # --- CONECTORES ROMANCES BASE ---
    if p in ["c", "qui", "oquin", "quoin"]: return "que"
    if p in ["i", "din"]: return "en"
    if p == "o": return "o"
    if p in ["l", "el"]: return "el"
    if p in ["ar", "al", "dal", "del", "dil", "dol", "odal", "ldi"]: return "del"
    if p in ["da", "di", "odi", "dom"]: return "de"
    if p in ["qua", "oqua"]: return "agua"
    if p in ["olin", "olun"]: return "aceite"
    return p

def motor_prosa_fluida(texto_filtrado: str, idioma: str = "es") -> tuple:
    """ 
    Procesa el texto filtrado mapeando equivalencias analíticas básicas independientes 
    para retornar los datos de la tabla y una oración estructurada simplificada.
    """
    palabras = texto_filtrado.split()
    datos_tabla = []
    palabras_traducidas = []
    
    # Diccionario semántico simulado/heurístico de raíces paleográficas (Latín simplificado)
    diccionario_raices = {
        "senior": ("señor", "lord"),
        "piue": ("lluvia", "rain"),
        "pi": ("pío / sagrado", "pious / holy"),
        "cut": ("piel / corteza", "skin / bark"),
        "ch": ("luz", "light"),
        "otio": ("ocio / descanso", "leisure"),
    }
    
    for pal in palabras:
        idx_idioma = 0 if idioma == "es" else 1
        pal_limpia = desarmar_palabra_compuesta(pal)
        
        if pal_limpia in diccionario_raices:
            significado = diccionario_raices[pal_limpia][idx_idioma]
            tipo = "Exact Match"
        else:
            significado = pal_limpia
            tipo = "Morfema Raíz"
            
        datos_tabla.append([pal, significado, tipo])
        palabras_traducidas.append(significado)
        
    oracion_completa = " ".join(palabras_traducidas).capitalize() + "."
    return datos_tabla, oracion_completa
