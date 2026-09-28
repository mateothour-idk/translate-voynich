# voynichdata.py
import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Pipeline lineal estricto de transliteración sin bucles infinitos.
    Garantiza que kooiin pase correctamente a quin y x pase a sh.
    """
    if not texto_eva:
        return ""
    
    texto = texto_eva.lower()
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\[.*?\]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # --- CAPA 1: PROTECCIONES Y REGLAS ESPECÍFICAS ---
    texto = texto.replace("pceeoe", "piue")
    texto = texto.replace("x", "sh")  # Regla: X pasa a ser SH
    texto = texto.replace("pcee", "pi")
    texto = texto.replace("qok", "quoqu")
    
    # --- CAPA 2: GRUPOS DE 3 CARACTERES ---
    texto = texto.replace("iii", "i")     
    texto = texto.replace("eee", "ei")     
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("eey", "ai")     
    texto = texto.replace("pcs", "pes")
    texto = texto.replace("pdr", "pedr")
    
    # --- CAPA 3: DÍGRAFOS Y BIGRAMAS DE 2 CARACTERES ---
    texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p")
    texto = texto.replace("dc", "ch").replace("tc", "ch").replace("ct", "cut")
    texto = texto.replace("ph", "f")      
    texto = texto.replace("th", "t")
    texto = texto.replace("ch", "c")      
    texto = texto.replace("ck", "qu")
    texto = texto.replace("tt", "t")       
    texto = texto.replace("ts", "s")       
    
    # --- CAPA 4: TRATAMIENTO DE VOCALES DUPLICADAS ---
    texto = texto.replace("oo", "u")      
    texto = texto.replace("ii", "i")      
    texto = texto.replace("ee", "i")
    texto = texto.replace("oe", "ue")     
    texto = texto.replace("iu", "u")
    texto = texto.replace("oi", "oi")
    texto = texto.replace("ae", "e")      
    texto = texto.replace("cs", "s")
    texto = texto.replace("ll", "y")
    texto = texto.replace("ey", "a")      
    texto = texto.replace("ce", "c")
    texto = texto.replace("ai", "i")      
    
    # --- CAPA 5: CONTEXTO DE LA 'Y' ---
    re_y_aislada = re.compile(r'\by\b')
    re_y_inicial = re.compile(r'\by')
    re_y_final = re.compile(r'y\b')
    texto = re_y_aislada.sub('i', texto)
    texto = re_y_inicial.sub('i', texto)
    texto = re_y_final.sub('i', texto)
    
    # --- CAPA 6: SUSTITUCIÓN DE K / Q EN QU ---
    texto = texto.replace("k", "qu")      
    texto = texto.replace("q", "qu")
    
    # --- CAPA 7: CORRECCIONES MEDIEVALES Y BLINDAJE ORTOGRÁFICO ---
    texto = re.sub(r'\bchseor\b', 'senior', texto)  
    texto = re.sub(r'\bseor\b', 'senior', texto)
    texto = re.sub(r'iin\b', 'am', texto)          
    texto = re.sub(r'eiy\b', 'e', texto)           
    texto = re.sub(r'oitio', 'otio', texto)         
    
    # Limpieza final absoluta para corregir quuin -> quin
    texto = texto.replace("quu", "qu")
    
    # Eliminar haches sueltas que no sean de sh o ch
    texto = re.sub(r'(?<!s)(?<!c)h', '', texto)
    
    return texto.strip()

def resolver_contexto_palabra(palabra: str) -> str:
    p_baja = palabra.lower()
    if "quu" in p_baja:
        p_baja = p_baja.replace("quu", "qu")
    return p_baja

def calcular_distancia_levenshtein(str1, str2):
    """ Algoritmo local para buscar similitudes morfológicas sin internet """
    m, n = len(str1), len(str2)
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

def buscar_aproximacion_local(palabra, glosario):
    """ Encuentra de forma autónoma la raíz más cercana en el diccionario """
    mejor_raiz = palabra
    distancia_minima = 99
    for raiz in glosario.keys():
        dist = calcular_distancia_levenshtein(palabra, raiz)
        if dist < distancia_minima:
            distancia_minima = dist
            mejor_raiz = raiz
    # Si la aproximación es muy lejana, la dejamos como término abierto
    if distancia_minima <= 2:
        return glosario[mejor_raiz], f"Aproximación Fonética Local (-{distancia_minima}L)"
    return f"[{palabra.upper()}]", "Transliteración Criptográfica Abierta"

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    palabras = texto_limpio.split()
    analisis_estructurado = []
    target_lang = "es" if idioma == "es" else "en"
    
    # Base de conocimiento extendida local (Latín Romance / Botánica Medieval)
    glosario_maestro = {
        "piue": "más", "piu": "más", "codar": "cocer", "oleis": "aceites", 
        "cipi": "tallos", "seol": "seco", "sequieo": "secado", "otolsai": "extraer",
        "senior": "señor (maestro)", "olse": "aceitoso", "quodam": "un cierto", "oram": "borde",
        "iquiol": "jugo", "otio": "reposo", "cute": "piel (corteza)", "cior": "mover", 
        "cioquai": "infusión", "cut": "cortar", "quin": "quien (que)", "qin": "que",
        "tsheos": "esencia", "ceepy": "cepas / raíces", "ceeor": "ceras / resinas",
        "ceodar": "cocción", "olees": "óleos", "qodaiin": "código (receta)", "olse": "oler",
        "orain": "oración / borde", "iquiol": "líquido extraído", "oteody": "método",
        "cteeey": "cutícula", "ykeeol": "licor"
    } if target_lang == "es" else {
        "piue": "more", "piu": "more", "codar": "cook", "oleis": "oils", 
        "cipi": "stems", "seol": "dry", "sequieo": "dried", "otolsai": "extract",
        "senior": "master", "olse": "oily", "quodam": "a certain", "oram": "edge",
        "iquiol": "juice", "otio": "rest", "cute": "skin (bark)", "cior": "move", 
        "cioquai": "decoction", "cut": "cut", "quin": "which", "qin": "which",
        "tsheos": "essence", "ceepy": "roots", "ceeor": "waxes", "ceodar": "decoction",
        "olees": "oils", "qodaiin": "code", "olse": "smell", "orain": "edge",
        "iquiol": "juice", "oteody": "method", "cteeey": "cuticle", "ykeeol": "liquor"
    }
    
    if not palabras:
        return [], ""

    # 1. TRADUCCIÓN DE LA ORACIÓN EN BLOQUE LOCAL (Cero latencia de red)
    palabras_traducidas_oracion = []
    for palabra in palabras:
        palabra_optimizada = resolver_contexto_palabra(palabra)
        if palabra_optimizada in glosario_maestro:
            palabras_traducidas_oracion.append(glosario_maestro[palabra_optimizada])
        else:
            significado, _ = buscar_aproximacion_local(palabra_optimizada, glosario_maestro)
            palabras_traducidas_oracion.append(significado)

    oracion_completa = " ".join(palabras_traducidas_oracion)

    # 2. CONSTRUCCIÓN DE LA TABLA INTERACTIVA
    for palabra in palabras[:40]:
        if not palabra.strip():
            continue
            
        palabra_optimizada = resolver_contexto_palabra(palabra)
        
        if palabra_optimizada in glosario_maestro:
            significado_individual = glosario_maestro[palabra_optimizada]
            tipo_match = "Glosario Romance (Posta)"
        else:
            significado_individual, tipo_match = buscar_aproximacion_local(palabra_optimizada, glosario_maestro)
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra_optimizada.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": tipo_match
        })
        
    return analisis_estructurado, oracion_completa
