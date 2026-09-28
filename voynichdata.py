# voynichdata.py
import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """ Aplica las 42 reglas de transliteración estructuradas en capas de longitud para evitar colisiones """
    if not texto_eva: return ""
    texto = texto_eva.lower()
    
    # Limpieza profunda de ruidos del transcriptor (comas, corchetes con dudas, etc.)
    texto = re.sub(r'\[\s*\w+\s*:\s*\w+\s*\]', ' ', texto)
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Diccionarios ordenados por capas estrictas de reemplazo (Tetragramas -> Trigramas -> Bigramas)
    capa_0 = {"pceeoe": "piue", "pcee": "pi", "qok": "quoqu"}
    capa_1 = {"iii": "i", "eee": "ei", "dce": "dic", "cee": "ci", "eey": "ai", "pcs": "pes", "pdr": "pedr", "eat": "it"}
    capa_2 = {"pc": "p", "ps": "p", "cp": "p", "dc": "ch", "tc": "ch", "cs": "s", "ck": "qu", "ct": "cut", "ph": "f", "th": "t", "tt": "t", "ts", "s", "ll": "y"}
    capa_3 = {"ee": "i", "oe": "ue", "iu": "u", "oi": "oi", "ii": "i", "ae": "e", "oo": "u", "ey": "a", "iy": "i", "ai": "i", "x": "sh"}
    
    for capa in [capa_0, capa_1, capa_2, capa_3]:
        for k, v in capa.items():
            texto = texto.replace(k, v)
            
    # Capa 4: Reglas contextuales de borde y finales de palabra
    texto = re.sub(r'\by', 'i', texto)
    texto = re.sub(r'y\b', 'i', texto)
    texto = re.sub(r'\by\b', 'i', texto)
    texto = re.sub(r'm\b', 'n', texto)  # Regla M = M / N al final de palabra
    
    # Sustitución base de K / Q / QUO y blindaje ortográfico
    texto = texto.replace("quo", "qu").replace("k", "qu").replace("q", "qu").replace("quu", "qu")
    texto = re.sub(r'\bchseor\b', 'senior', texto)
    texto = re.sub(r'\bseor\b', 'senior', texto)
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

def calcular_distancia_levenshtein(str1, str2):
    """ Mide la similitud ortográfica mediante matriz numérica 100% independiente en la memoria """
    m, n = len(str1), len(str2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    
    # CORREGIDO: Asignación indexando la celda exacta de los bordes [INDEX]
    for i in range(m + 1): 
        dp[i][0] = i
    for j in range(n + 1): 
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
    return dp[m][n]

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
    if p in ["olin", "olin"]: return "aceitoso"
    if p in ["itiol", "itidad", "ititad"]: return "un poco"
    if p == "ct": return "cortar"
    
    # --- CONECTORES AVANZADOS DE LABORATORIO MULTISECCIÓN ---
    if p in ["quo", "quol", "quon"]: return "el cual (que)"
    if p in ["ca", "cap"]: return "porque (ya que)"
    if p in ["ari", "ori", "oro", "oram"]: return "contorno (borde)"
    if p == "ci": return "este (aquí)"
    if p == "sh": return "brote"
    if p in ["far", "fer", "fcar", "ifca", "ifcha"]: return "hacer (activar)"
    if p in ["ti", "te", "tosi", "tochsi"]: return "dosificar / para sí"
    if p in ["chor", "ichor", "ichedad"]: return "savia pura (ícor)"
    if p in ["quofor", "quofeo"]: return "lo que será"
    if p == "chychi": return "pizca"
    if p == "cri": return "filtrar"
    if p in ["ocor", "ocor", "oqueo", "ipdi"]: return "fomento / yema"
    if p in ["uefocl", "uefol"]: return "agua al fuego (baño maría)"

    # Desacoplamiento de artículos aglutinados (L- / CH-)
    if p.startswith("l") and len(p) > 2 and p not in ["a", "e", "i", "o", "u"]:
        significado_raiz = desarmar_palabra_compuesta(p[1:])
        if significado_raiz and not significado_raiz.startswith("["): return f"la {significado_raiz}"
    if p.startswith("ch") and len(p) > 3 and p not in ["a", "e", "i", "o", "u"]:
        significado_raiz = desarmar_palabra_compuesta(p[2:])
        if significado_raiz and not significado_raiz.startswith("["): return f"este {significado_raiz}"

    # --- EXTRACTOR VERBAL Y DE TIEMPO ---
    if "ctin" in p or "ctan" in p: return "cortando"
    if "quoteo" in p or "quotar" in p or "tolqueol" in p: return "la dosis"
    if "oteodin" in p or "ochdin" in p or "ochin" in p or "ochdad" in p: return "del método (tiempo)"
    if p in ["otin", "otar", "itar"]: return "del reposo"

    # --- ADAPTACIÓN DE SUFIJOS ABSTRACTOS MODIFICADOS ---
    if p.endswith("dad") or p.endswith("din") or p.endswith("di") or p.endswith("ti"):
        raiz = p[:-3] if p.endswith("dad") or p.endswith("din") else p[:-2]
        if raiz in ["quoc", "quoqu", "qued", "ququ", "qqu"]: return "cocimiento"
        if raiz in ["shed", "sheo", "she"]: return "germinación"
        if raiz == "ofe": return "dosificación"
        if raiz == "if": return "eficacia"
        if raiz == "opal": return "opacidad"
        if raiz == "lqui": return "liquidez"
        if raiz in ["iqu", "iquch"]: return "jugosidad"
        if raiz in ["po", "pod"]: return "propiedad (potencia)"
        if raiz in ["ited", "it"]: return "repetición (proceso)"
        if len(raiz) > 1: return f"{raiz}dad"

    # --- ALGORITMO LOCAL DE RESPALDO (Levenshtein) ---
    glosario_claves = {"piue": "más", "codar": "cocer", "oleis": "aceites", "cipi": "tallos", "seol": "seco", "sequieo": "secado", "otolsai": "extraer"}
    for clave, significado in glosario_claves.items():
        if calcular_distancia_levenshtein(p, clave) <= 1: return significado

    if len(p) == 1: return ""
    return f"[{palabra.upper()}]"

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    palabras = texto_limpio.split()
    analisis_estructurado = []
    glosario_maestro = {"piue": "más", "piu": "más", "codar": "cocer", "oleis": "aceites", "cipi": "tallos", "seol": "seco", "sequieo": "secado", "otolsai": "extraer", "senior": "señor (maestro)", "olse": "aceitoso", "quodam": "un cierto", "oram": "borde", "iquiol": "jugo", "cute": "piel (corteza)", "cior": "mover", "cioquai": "infusión", "cut": "cortar", "quin": "quien (que)", "qin": "que", "tsheos": "esencia", "ceepy": "cepas / raíces", "ceeor": "ceras / resinas", "ceodar": "cocción", "olees": "óleos", "qodaiin": "código (receta)", "olse": "oler", "orain": "oración / borde", "oteody": "método", "cteeey": "cutícula", "ykeeol": "licor"}
    
    if not palabras: return [], ""

    palabras_traducidas_oracion = []
    for palabra in palabras:
        opciones_palabra = resolver_contexto_palabra(palabra)
        traducida = False
        for opcion in opciones_palabra:
            if opcion in glosario_maestro:
                palabras_traducidas_oracion.append(glosario_maestro[opcion])
                traducida = True
                break
            else:
                sig_comp = desarmar_palabra_compuesta(opcion)
                if sig_comp and not sig_comp.startswith("["):
                    palabras_traducidas_oracion.append(sig_comp)
                    traducida = True
                    break
        if not traducida: palabras_traducidas_oracion.append(desarmar_palabra_compuesta(palabra))

    oracion_completa = re.sub(r'\s+', ' ', " ".join(palabras_traducidas_oracion)).strip()

    for palabra in palabras[:40]:
        if not palabra.strip(): continue
        opciones_palabra = resolver_contexto_palabra(palabra)
        significado_individual = ""
        tipo_match = "Término Abierto Conservado"
        
        for opcion in opciones_palabra:
            if opcion in glosario_maestro:
                significado_individual = glosario_maestro[opcion]
                tipo_match = "Glosario Romance (Ramas /)"
                break
            else:
                sig = desarmar_palabra_compuesta(opcion)
                if sig and not sig.startswith("["):
                    significado_individual = sig
                    tipo_match = "Deducción NLP Multirrama"
                    break
                    
        if not significado_individual: significado_individual = desarmar_palabra_compuesta(palabra)
            
        analisis_estructurado.append({
            "Palabra Filtrada": "/".join(opciones_palabra).upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": type_match
        })
        
    return analisis_estructurado, oracion_completa
