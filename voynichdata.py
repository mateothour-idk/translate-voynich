# voynichdata.py
import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """ Pipeline lineal estricto de transliteración sin bucles infinitos. """
    if not texto_eva: return ""
    texto = texto_eva.lower()
    
    # Limpieza profunda de ruidos del transcriptor (comas, corchetes con dudas, etc.)
    texto = re.sub(r'\[\s*\w+\s*:\s*\w+\s*\]', ' ', texto) # Quita dudas tipo [s:r] o [?:d]
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    texto = texto.replace("pceeoe", "piue").replace("x", "sh").replace("pcee", "pi").replace("qok", "quoqu")
    texto = texto.replace("iii", "i").replace("eee", "ei").replace("dce", "dic").replace("cee", "ci").replace("eey", "ai").replace("pcs", "pes").replace("pdr", "pedr")
    texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p").replace("dc", "ch").replace("tc", "ch").replace("ct", "cut").replace("ph", "f").replace("th", "t").replace("ch", "c").replace("ck", "qu").replace("tt", "t").replace("ts", "s")       
    texto = texto.replace("oo", "u").replace("ii", "i").replace("ee", "i").replace("oe", "ue").replace("iu", "u").replace("oi", "oi").replace("ae", "e").replace("cs", "s").replace("ll", "y").replace("ey", "a").replace("ce", "c").replace("ai", "i")      
    
    re_y_aislada = re.compile(r'\by\b')
    re_y_inicial = re.compile(r'\by')
    re_y_final = re.compile(r'y\b')
    texto = re_y_aislada.sub('i', texto)
    texto = re_y_inicial.sub('i', texto)
    texto = re_y_final.sub('i', texto)
    
    texto = texto.replace("k", "qu").replace("q", "qu")
    texto = re.sub(r'\bchseor\b', 'senior', texto)  
    texto = re.sub(r'\bseor\b', 'senior', texto)
    texto = re.sub(r'iin\b', 'am', texto)          
    texto = re.sub(r'eiy\b', 'e', texto)           
    texto = re.sub(r'oitio', 'otio', texto)         
    texto = texto.replace("quu", "qu")
    texto = re.sub(r'(?<!s)(?<!c)h', '', texto)
    return texto.strip()

def resolver_contexto_palabra(palabra: str) -> str:
    p_baja = palabra.lower()
    if "quu" in p_baja: p_baja = p_baja.replace("quu", "qu")
    return p_baja

def calcular_distancia_levenshtein(str1, str2):
    """ Mide la similitud ortográfica entre dos términos mediante matriz numérica 100% independiente """
    m, n = len(str1), len(str2)
    
    # CORREGIDO DEFINITIVO: Matriz inicializada correctamente con ceros [0]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j
    
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
    
    # --- 1. MATRIZ DE CONECTORES Y PARTÍCULAS BASE ---
    if p in ["c", "qui", "oquin", "quoin"]: return "que"
    if p in ["i", "din"]: return "en"
    if p == "o": return "o"
    if p == "l": return "el"
    if p in ["ar", "al", "dal", "del", "dil", "dol", "odal", "ldi"]: return "del"
    if p in ["da", "di", "odi", "dom"]: return "de"
    if p == "qua": return "agua"
    if p in ["olin", "olin"]: return "aceitoso"
    if p in ["itiol", "itidad", "ititad"]: return "un poco"
    if p == "ct": return "cortar"
    
    # --- 2. CAPA AUTOMÁTICA DE RAÍCES MULTISECCIÓN ---
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
    if p == "uefocl": return "agua al fuego (baño maría)"

    # --- 3. EXTRACTOR VERBAL Y DE TIEMPO ---
    if "ctin" in p or "ctan" in p: return "cortando"
    if "quoteo" in p or "quotar" in p or "tolqueol" in p: return "la dosis"
    if "oteodin" in p or "ochdin" in p or "ochin" in p: return "del método (tiempo)"
    if p in ["otin", "otar", "itar"]: return "del reposo"

    # --- 4. TRATAMIENTO AUTOMÁTICO DE SUFIJOS ABSTRACTOS ---
    if p.endswith("dad") or p.endswith("din") or p.endswith("di") or p.endswith("ti"):
        raiz = p[:-3] if p.endswith("dad") or p.endswith("din") else p[:-2]
        if raiz in ["quoc", "quoqu", "qued"]: return "cocimiento"
        if raiz == "shed" or raiz == "sheo" or raiz == "she": return "germinación"
        if raiz == "ofe": return "dosificación"
        if raiz == "if": return "eficacia"
        if raiz == "opal": return "opacidad"
        if raiz == "lqui": return "liquidez"

    # --- 5. ALGORITMO LOCAL DE RESPALDO (Aproximación por Levenshtein) ---
    glosario_claves = {"piue": "más", "codar": "cocer", "oleis": "aceites", "cipi": "tallos", 
                       "seol": "seco", "sequieo": "secado", "otolsai": "extraer"}
    
    for clave, significado in glosario_claves.items():
        if calcular_distancia_levenshtein(p, clave) <= 1:
            return significado

    # Si es una letra residual suelta, la elimina para la lectura fluida
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
        palabra_optimizada = resolver_contexto_palabra(palabra)
        if palabra_optimizada in glosario_maestro:
            palabras_traducidas_oracion.append(glosario_maestro[palabra_optimizada])
        else:
            significado_compuesto = desarmar_palabra_compuesta(palabra_optimizada)
            if significado_compuesto:
                palabras_traducidas_oracion.append(significado_compuesto)

    oracion_completa = re.sub(r'\s+', ' ', " ".join(palabras_traducidas_oracion)).strip()

    for palabra in palabras[:40]:
        if not palabra.strip(): continue
        palabra_optimizada = resolver_contexto_palabra(palabra)
        if palabra_optimizada in glosario_maestro:
            significado_individual = glosario_maestro[palabra_optimizada]
            tipo_match = "Glosario Romance (Posta)"
        else:
            significado_individual = desarmar_palabra_compuesta(palabra_optimizada)
            if significado_individual.startswith("["):
                tipo_match = "Término Abierto Conservado"
            else:
                tipo_match = "Deducción Automática NLP Local"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra_optimizada.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": tipo_match
        })
        
    return analisis_estructurado, oracion_completa
