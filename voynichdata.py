# voynichdata.py (Parte 1 de 2)
import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las 42 reglas de transliteración y normalización ortográfica
    estructuradas en capas estrictas de longitud para evitar colisiones.
    """
    if not texto_eva: return ""
    texto = texto_eva.lower()
    
    # Limpieza profunda de ruidos del transcriptor (comas, corchetes con dudas, etc.)
    texto = re.sub(r'\[\s*\w+\s*:\s*\w+\s*\]', ' ', texto)
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # --- CAPA 0: PROTECCIONES Y TETRAGRAMAS (4 letras) ---
    texto = texto.replace("pceeoe", "piue")
    texto = texto.replace("pcee", "pi")
    texto = texto.replace("qok", "quoqu")
    
    # --- CAPA 1: TRIGRAMAS (3 letras) ---
    texto = texto.replace("iii", "i")      # iii = í / i
    texto = texto.replace("eee", "ei")     # eee = ei / ie
    texto = texto.replace("dce", "dic")    # dce = dic
    texto = texto.replace("cee", "ci")     # cee = ci / ce
    texto = texto.replace("eey", "ai")     # eey = ai / iy
    texto = texto.replace("pcs", "pes")    # pcs = pes
    texto = texto.replace("pdr", "pedr")   # pdr = pedr
    texto = texto.replace("eat", "it")     # eat = it
    
    # --- CAPA 2: BIGRAMAS Y DÍGRAFOS (2 letras) ---
    texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p") # pc/ps/cp = p
    texto = texto.replace("dc", "ch").replace("tc", "ch")                  # dc/tc = ch
    texto = texto.replace("cs", "s")                                       # cs = s
    texto = texto.replace("ck", "qu")                                      # ck = qu
    texto = texto.replace("ct", "cut")                                     # ct = cut
    texto = texto.replace("ph", "f")                                       # ph = f
    texto = texto.replace("th", "t")                                       # th = t
    texto = texto.replace("tt", "t")                                       # tt = t
    texto = texto.replace("ts", "s")                                       # ts = s
    texto = texto.replace("ll", "y")                                       # ll = y
    
    # Reglas Vocálicas y Mutaciones
    texto = texto.replace("ee", "i")       # ee = i
    texto = texto.replace("oe", "ue")      # oe = ue / u
    texto = texto.replace("iu", "u")       # iu = u
    texto = texto.replace("oi", "oi")      # oi = oy / oi
    texto = texto.replace("ii", "i")       # ii = i
    texto = texto.replace("ae", "e")       # ae = a / e
    texto = texto.replace("oo", "u")       # oo = u / oo
    texto = texto.replace("ey", "a")       # ey = a corta
    texto = texto.replace("iy", "i")       # iy = í
    texto = texto.replace("ai", "i")       # ai = i / ai
    
    # Reglas Singulares Directas
    texto = texto.replace("x", "sh")       # x = sh
    
    # --- CAPA 3: REGLAS CONTEXTUALES DE BORDE Y FINALES ---
    # Y al principio o final de palabra = i / í / y
    texto = re.sub(r'\by', 'i', texto)
    texto = re.sub(r'y\b', 'i', texto)
    texto = re.sub(r'\by\b', 'i', texto)
    
    # Normalización de Nasales M = M / N al final de bloque
    texto = re.sub(r'm\b', 'n', texto)
    
    # Sustitución base de K / Q / QUO
    texto = texto.replace("quo", "qu")     # quo = cuo / quo
    texto = texto.replace("k", "qu")       # k = qu
    texto = texto.replace("q", "qu")       # q = qu / q
    
    # Blindaje y limpieza ortográfica residual
    texto = texto.replace("quu", "qu")
    texto = re.sub(r'(?<!s)(?<!c)h', '', texto) # Quita haches huérfanas
    
    return texto.strip()

def resolver_contexto_palabra(palabra: str) -> list:
    """
    Genera de forma automática la lista de variaciones permitidas
    por las reglas con barra cruzada (/) de tu matriz.
    """
    p = palabra.lower()
    variaciones = [p]
    
    if p.startswith("qu") and len(p) > 2:
        variaciones.append(p.replace("qu", "q", 1))
    if "ue" in p:
        variaciones.append(p.replace("ue", "u"))
    if p.endswith("c"):
        variaciones.append(p + "e")
    if p.startswith("l") and len(p) > 1:
        variaciones.append("e" + p)
        
    return list(set(variaciones))

# voynichdata.py (Parte 2 de 2)

def calcular_distancia_levenshtein(str1, str2):
    """ Mide la similitud ortográfica mediante matriz numérica 100% independiente """
    m, n = len(str1), len(str2)
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
    for i in range(m + 1): dp[i] = i
    for j in range(n + 1): dp[j] = j
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
    
    # --- CONECTORES, DETERMINANTES Y CONTRACCIONES ROMANCES ---
    if p in ["c", "qui", "oquin", "quoin"]: return "que"
    if p in ["i", "din"]: return "en"
    if p == "o": return "o"
    if p == "l" or p == "el": return "el"
    if p in ["ar", "al", "dal", "del", "dil", "dol", "odal", "ldi"]: return "del"
    if p in ["da", "di", "odi", "dom"]: return "de"
    if p == "qua": return "agua"
    if p in ["olin", "olin"]: return "aceitoso"
    if p in ["itiol", "itidad", "ititad"]: return "un poco"
    if p == "ct": return "cortar"
    
    # --- CAPA DE CONECTORES, POSICIÓN Y ACCIONES DE LABORATORIO ---
    if p in ["quo", "quol", "quon"]: return "el cual (que)"
    if p in ["ca", "cap"]: return "porque (ya que)"
    if p in ["ari", "ori", "oro", "oram"]: return "contorno (borde)"
    if p == "ci": return "este (aquí)"
    if p == "sh": return "brote"
    if p in ["far", "fer", "fcar", "ifca"]: return "hacer (activar)"
    if p in ["ti", "te", "tosi"]: return "dosificar / para sí"
    if p in ["chor", "ichor", "ichedad"]: return "savia pura (ícor)"
    if p in ["quofor", "quofeo"]: return "lo que será"
    if p == "chychi": return "pizca"
    if p == "cri": return "filtrar"
    if p in ["ocor", "ocor", "oqueo"]: return "humedad / yema"
    if p == "ipdi": return "fomento (aplicación)"
    if p == "uefocl" or p == "uefol": return "agua al fuego (baño maría)"

    # --- DESACOPLAMIENTO DE ARTÍCULO 'L/EL' AGLUTINADO ---
    if p.startswith("l") and len(p) > 2 and p not in ["a", "e", "i", "o", "u"]:
        raiz_restante = p[1:]
        significado_raiz = desarmar_palabra_compuesta(raiz_restante)
        if significado_raiz and not significado_raiz.startswith("["):
            return f"la {significado_raiz}"

    # --- EXTRACTOR VERBAL Y DE TIEMPO ---
    if "ctin" in p or "ctan" in p: return "cortando"
    if "quoteo" in p or "quotar" in p or "tolqueol" in p: return "la dosis"
    if "oteodin" in p or "ochdin" in p or "ochin" in p: return "del método (tiempo)"
    if p in ["otin", "otar", "itar"]: return "del reposo"

    # --- TRATAMIENTO AUTOMÁTICO DE SUFIJOS ABSTRACTOS ---
    if p.endswith("dad") or p.endswith("din") or p.endswith("di") or p.endswith("ti"):
        raiz = p[:-3] if p.endswith("dad") or p.endswith("din") else p[:-2]
        if raiz in ["quoc", "quoqu", "qued"]: return "cocimiento"
        if raiz in ["shed", "sheo", "she"]: return "germinación"
        if raiz == "ofe": return "dosificación"
        if raiz == "if": return "eficacia"
        if raiz == "opal": return "opacidad"
        if raiz == "lqui": return "liquidez"
        if raiz == "po" or raiz == "pod": return "propiedad (potencia)"
        if raiz == "ited" or raiz == "it": return "repetición (proceso)"
        if len(raiz) > 1: return f"{raiz}dad"

    # --- ALGORITMO LOCAL DE RESPALDO (Levenshtein) ---
    glosario_claves = {"piue": "más", "codar": "cocer", "oleis": "aceites", "cipi": "tallos", 
                       "seol": "seco", "sequieo": "secado", "otolsai": "extraer"}
    
    for clave, significado in glosario_claves.items():
        if calcular_distancia_levenshtein(p, clave) <= 1:
            return significado

    if len(p) == 1: return ""
    return f"[{palabra.upper()}]"

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    palabras = texto_limpio.split()
    analisis_estructurado = []
    
    glosario_maestro = {
        "piue": "más", "piu": "más", "codar": "cocer", "oleis": "aceites", 
        "cipi": "tallos", "seol": "seco", "sequieo": "secado", "otolsai": "extraer",
        "senior": "señor (maestro)", "olse": "aceitoso", "quodam": "un cierto", "oram": "borde",
        "iquiol": "jugo", "cute": "piel (corteza)", "cior": "mover", 
        "cioquai": "infusión", "cut": "cortar", "quin": "quien (que)", "qin": "que",
        "tsheos": "esencia", "ceepy": "cepas / raíces", "ceeor": "ceras / resinas",
        "ceodar": "cocción", "olees": "óleos", "qodaiin": "código (receta)", "olse": "oler",
        "orain": "oración / borde", "oteody": "método", "cteeey": "cutícula", "ykeeol": "licor"
    }
    
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
                    
        if not traducida:
            palabras_traducidas_oracion.append(desarmar_palabra_compuesta(opciones_palabra))

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
                    
        if not significado_individual:
            significado_individual = desarmar_palabra_compuesta(opciones_palabra)
            
        analisis_estructurado.append({
            "Palabra Filtrada": opciones_palabra.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": tipo_match
        })
        
    return analisis_estructurado, oracion_completa
