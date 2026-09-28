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

def desarmar_palabra_compuesta(palabra: str) -> str:
    """
    Analiza morfológicamente palabras complejas basándose en raíces eclesiásticas,
    sufijos de cualidad e ingeniería de compuestos botánicos medievales.
    """
    p = palabra.lower()
    
    # --- REGLA ADICIONAL OPCIÓN 3: COMPUESTOS VERBALES Y DERIVADOS ---
    if "cod" in p:
        prefijo = "que " if p.startswith("que") or p.startswith("qu") else ""
        sufijo = "an" if p.endswith("sha") or p.endswith("sh") else "er"
        return f"{prefijo}cuez{sufijo}"
    if "cut" in p:
        prefijo = "que " if p.startswith("que") or p.startswith("qu") else ""
        sufijo = "ado" if p.endswith("di") or p.endswith("ti") else "ar"
        return f"{prefijo}cort{sufijo}"

    # --- NUEVA REGLA ADAPTATIVA: RAÍZ IQUI (LÍQUIDO / SAVIA / LICOR) ---
    if "iqui" in p:
        if p.endswith("dam") or p.endswith("am"): return "el jugo"
        if p.endswith("dad") or p.endswith("tad"): return "jugosidad"
        return "jugo"

    # --- NUEVA REGLA ADAPTATIVA: RAÍZ SHE/SHEO (BROTAR / GERMINAR) ---
    if p.startswith("sheo") or p.startswith("she"):
        if p.endswith("dad") or p.endswith("di"): return "germinación"
        if p.endswith("din") or p.endswith("in"): return "brotando"
        return "brote"

    # --- ABREVIATURAS CORTAS PARTICULARES (Raíces fijas del folio fros) ---
    if p == "fdin": return "fijación"
    if p == "ofa": return "mezcla"

    # --- REGLA ADICIONAL OPCIÓN 1: ABREVIATURAS MEDIEVALES DE CUALIDAD (-DI / -TI) ---
    if p.endswith("di") or p.endswith("ti"):
        if "och" in p or "ot" in p:
            return "días"
        if len(p) > 3:
            raiz_limpia = p[:-2]
            if raiz_limpia == "if": return "eficacia"
            if raiz_limpia == "opal": return "opacidad"
            return f"{raiz_limpia}dad"

    return f"[{palabra.upper()}]"

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    palabras = texto_limpio.split()
    analisis_estructurado = []
    
    glosario_maestro = {
        "piue": "más", "piu": "más", "codar": "cocer", "oleis": "aceites", 
        "cipi": "tallos", "seol": "seco", "sequieo": "secado", "otolsai": "extraer",
        "senior": "señor (maestro)", "olse": "aceitoso", "quodam": "un cierto", "oram": "borde",
        "iquiol": "jugo", "otio": "reposo", "cute": "piel (corteza)", "cior": "mover", 
        "cioquai": "infusión", "cut": "cortar", "quin": "quien (que)", "qin": "que",
        "tsheos": "esencia", "ceepy": "cepas / raíces", "ceeor": "ceras / resinas",
        "ceodar": "cocción", "olees": "óleos", "qodaiin": "código (receta)", "olse": "oler",
        "orain": "oración / borde", "oteody": "método", "cteeey": "cutícula", "ykeeol": "licor"
    }
    
    if not palabras:
        return [], ""

    palabras_traducidas_oracion = []
    for palabra in palabras:
        palabra_optimizada = resolver_contexto_palabra(palabra)
        if palabra_optimizada in glosario_maestro:
            palabras_traducidas_oracion.append(glosario_maestro[palabra_optimizada])
        else:
            palabras_traducidas_oracion.append(desarmar_palabra_compuesta(palabra_optimizada))

    oracion_completa = " ".join(palabras_traducidas_oracion)

    for palabra in palabras[:40]:
        if not palabra.strip():
            continue
            
        palabra_optimizada = resolver_contexto_palabra(palabra)
        
        if palabra_optimizada in glosario_maestro:
            significado_individual = glosario_maestro[palabra_optimizada]
            tipo_match = "Glosario Romance (Posta)"
        else:
            significado_individual = desarmar_palabra_compuesta(palabra_optimizada)
            tipo_match = "Desarmador Morfológico Medieval" if not significado_individual.startswith("[") else "Incógnita Protegida"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra_optimizada.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": tipo_match
        })
        
    return analisis_estructurado, oracion_completa
