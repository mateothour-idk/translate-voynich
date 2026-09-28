# voynichdata.py
import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """ Pipeline lineal estricto de transliteración sin bucles infinitos. """
    if not texto_eva: return ""
    texto = texto_eva.lower()
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\[.*?\]', ' ', texto)
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

def desarmar_palabra_compuesta(palabra: str) -> str:
    """ Desarma morfológicamente las palabras del efecto eco del manuscrito """
    p = palabra.lower()
    
    # --- CONECTORES, DETERMINANTES Y CONTRACCIONES ROMANCES ---
    if p in ["c", "qui", "oquin"]: return "que"
    if p in ["i", "din"]: return "en"
    if p in ["o", "qui"]: return "o"
    if p == "l": return "el"
    if p in ["ar", "al", "dal", "del", "dil", "dol", "odal", "ldi"]: return "del"
    if p in ["da", "di", "odi"]: return "de"
    if p == "qua": return "agua"
    if p in ["olin", "olin"]: return "aceitoso"
    if p in ["itiol", "itidad", "itidad"]: return "un poco"
    
    # --- NUEVAS REGLAS: TRATAMIENTO DE TIEMPO, DOSIS Y VERBOS ---
    if "ctin" in p or "ctan" in p: return "cortando"
    if "quoteo" in p or "quotar" in p or "tolqueol" in p: return "la dosis"
    if "oteodin" in p or "ochdin" in p: return "del método (tiempo)"

    # --- ENLACE DIRECTO DE SUFIJOS (Efecto Eco / Sufijos) ---
    if "itedad" in p or "itidad" in p or "ititad" in p: return "repetición (proceso)"
    if "tedad" in p or "tedin" in p: return "entibiamiento"
    if "shdad" in p or "shdi" in p: return "jarabe (elixir)"
    if "lquidad" in p: return "liquidez"
    if "ichedad" in p: return "savia pura"
    if "oqueo" in p or "ochdi" in p: return "humedad (reposo)"
    if "quoc" in p or "quoqu" in p or "qued" in p: return "cocimiento"
    if "ofe" in p: return "dosificación"
    if "shed" in p or "sheo" in p: return "germinación"

    # --- COMPUESTOS VERBALES BASE ---
    if "cod" in p:
        prefijo = "que " if p.startswith("que") or p.startswith("qu") else ""
        sufijo = "an" if p.endswith("sha") or p.endswith("sh") else "er"
        return f"{prefijo}cuez{sufijo}"
    if "cut" in p:
        prefijo = "que " if p.startswith("que") or p.startswith("qu") else ""
        sufijo = "ado" if p.endswith("di") or p.endswith("ti") else "ar"
        return f"{prefijo}cort{sufijo}"

    # --- RAÍCES BOTÁNICAS EXTRACTORAS ---
    if "iqui" in p:
        if p.endswith("dam") or p.endswith("am"): return "el jugo"
        if p.endswith("dad") or p.endswith("tad"): return "jugosidad"
        return "jugo"
    if p.startswith("sheo") or p.startswith("she"):
        if p.endswith("dad") or p.endswith("di"): return "germinación"
        if p.endswith("din") or p.endswith("in"): return "brotando"
        return "brote"

    if p == "fdin": return "fijación"
    if p == "ofa": return "mezcla"

    if p.endswith("di") or p.endswith("ti"):
        if "och" in p or "ot" in p: return "días"
        if len(p) > 3:
            raiz_limpia = p[:-2]
            if raiz_limpia == "if": return "eficacia"
            if raiz_limpia == "opal": return "opacidad"
            return f"{raiz_limpia}dad"

    return ""

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
            if not significado_individual:
                significado_individual = f"[{palabra_optimizada.upper()}]"
                tipo_match = "Incógnita Guardada"
            else:
                tipo_match = "Desarmador Morfológico Medieval"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra_optimizada.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": tipo_match
        })
        
    return analisis_estructurado, oracion_completa
