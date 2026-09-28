# voynichdata.py
import re
import os

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """ Lee las 42 reglas desde el archivo externo reglas.txt de forma segura """
    if not texto_eva: return ""
    texto = texto_eva.lower()
    
    # Limpieza profunda de ruidos del transcriptor
    texto = re.sub(r'\[\s*\w+\s*:\s*\w+\s*\]', ' ', texto)
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # Cargar y aplicar las reglas desde el archivo externo de forma lineal
    ruta_reglas = os.path.join(os.path.dirname(__file__), "reglas.txt")
    if os.path.exists(ruta_reglas):
        with open(ruta_reglas, "r", encoding="utf-8") as f:
            for linea in f:
                if "=" in linea:
                    k, v = linea.strip().split("=")
                    texto = texto.replace(k, v)
                    
    # Reglas contextuales finales de borde de palabra
    texto = re.sub(r'\by', 'i', texto)
    texto = re.sub(r'y\b', 'i', texto)
    texto = re.sub(r'\by\b', 'i', texto)
    texto = re.sub(r'm\b', 'n', texto)  # Regla M = M / N al final
    
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

def desarmar_palabra_compuesta(palabra: str) -> str:
    """ Motor universal adaptativo. Resuelve morfemas de forma autónoma sin internet. """
    p = palabra.lower()
    if not p: return ""
    
    # Conectores romances base
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
    
    # Conectores avanzados de laboratorio multiseCCIÓN
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
    if p == "uefocl" or p == "uefol"]: return "agua al fuego (baño maría)"

    # Desacoplamiento de artículos aglutinados
    if p.startswith("l") and len(p) > 2 and p not in ["a", "e", "i", "o", "u"]:
        sig_l = desarmar_palabra_compuesta(p[1:])
        if sig_l and not sig_l.startswith("["): return f"la {sig_l}"
    if p.startswith("ch") and len(p) > 3 and p not in ["a", "e", "i", "o", "u"]:
        sig_ch = desarmar_palabra_compuesta(p[2:])
        if sig_ch and not sig_ch.startswith("["): return f"este {sig_ch}"

    # Extractores de tiempo, procesos verbales y sufijos abstractos
    if "ctin" in p or "ctan" in p: return "cortando"
    if "quoteo" in p or "quotar" in p or "tolqueol" in p: return "la dosis"
    if "oteodin" in p or "ochdin" in p or "ochin" in p or "ochdad" in p: return "del método (tiempo)"
    if p in ["otin", "otar", "itar"]: return "del reposo"

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
            "Tipo de Match": tipo_match
        })
        
    return analisis_estructurado, oracion_completa
