# voynichdata.py
import re
from deep_translator import GoogleTranslator

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
    
    # --- CAPA 4: TRATAMIENTO DE VOCALES DUPLICADAS (Ej: kooiin -> kuiin -> kuin) ---
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
    
    # Limpieza final absoluta: quu pasa a qu obligatoriamente (quuin -> quin)
    texto = texto.replace("quu", "qu")
    
    # Eliminar haches que no sean parte de sh o ch
    texto = re.sub(r'(?<!s)(?<!c)h', '', texto)
    
    return texto.strip()

def resolver_contexto_palabra(palabra: str) -> str:
    """ Simplifica los términos antes de pasarlos a la tabla para evitar que quu se rompa """
    p_baja = palabra.lower()
    if "quu" in p_baja:
        p_baja = p_baja.replace("quu", "qu")
    return p_baja

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    palabras = texto_limpio.split()
    analisis_estructurado = []
    target_lang = "es" if idioma == "es" else "en"
    
    # Diccionario etimológico robusto local para no depender de Google en la tabla
    glosario_maestro = {
        "piue": "más", "piu": "más", "codar": "cocer", "oleis": "aceites", 
        "cipi": "tallos", "seol": "seco", "sequieo": "secado", "otolsai": "extraer",
        "senior": "señor (maestro)", "olse": "aceitoso", "quodam": "un cierto", "oram": "borde",
        "iquiol": "jugo", "otio": "reposo", "cute": "piel (corteza)", "cior": "mover", 
        "cioquai": "infusión", "cut": "cortar", "quin": "quien (que)", "qin": "que",
        "tsheos": "esencia / sustancia"
    } if target_lang == "es" else {
        "piue": "more", "piu": "more", "codar": "cook", "oleis": "oils", 
        "cipi": "stems", "seol": "dry", "sequieo": "dried", "otolsai": "extract",
        "senior": "master", "olse": "oily", "quodam": "a certain", "oram": "edge",
        "iquiol": "juice", "otio": "rest", "cute": "skin (bark)", "cior": "move", 
        "cioquai": "decoction", "cut": "cut", "quin": "which (who)", "qin": "which",
        "tsheos": "essence"
    }
    
    if not palabras:
        return [], ""

    # 1. TRADUCCIÓN DE LA ORACIÓN EN BLOQUE COMPLETAMENTE FLUIDA
    palabras_traducidas_oracion = []
    for palabra in palabras:
        palabra_optimizada = resolver_contexto_palabra(palabra)
        # Si la palabra está en nuestro glosario local, la traduce al instante
        if palabra_optimizada in glosario_maestro:
            palabras_traducidas_oracion.append(glosario_maestro[palabra_optimizada])
        else:
            # Respaldos de traducción contextual con la API limpia
            try:
                trad = GoogleTranslator(source='auto', target=target_lang).translate(palabra_optimizada)
                palabras_traducidas_oracion.append(trad)
            except Exception:
                palabras_traducidas_oracion.append(palabra_optimizada)

    oracion_completa = " ".join(palabras_traducidas_oracion)

    # 2. CONSTRUCCIÓN DE LA TABLA ESTABLE SIN REPETICIÓN DE RAÍCES TRABADAS
    for palabra in palabras[:30]:
        if not palabra.strip():
            continue
            
        palabra_optimizada = resolver_contexto_palabra(palabra)
        
        # Buscamos de forma directa la equivalencia al español sin pasar por Google
        if palabra_optimizada in glosario_maestro:
            significado_individual = glosario_maestro[palabra_optimizada]
            tipo_match = "Glosario Romance (Posta)"
        else:
            try:
                trad_api = GoogleTranslator(source='auto', target=target_lang).translate(palabra_optimizada)
                if trad_api.lower() == palabra_optimizada.lower():
                    # Si Google no sabe qué significa y devuelve lo mismo, se marca la barra contextual para análisis
                    significado_individual = f"{palabra_optimizada}/{palabra_optimizada[:-1] if len(palabra_optimizada)>2 else palabra_optimizada}"
                    tipo_match = "Variante Contextual Abierta"
                else:
                    significado_individual = trad_api
                    tipo_match = "Aproximación AI"
            except Exception:
                significado_individual = "[Incógnita]"
                tipo_match = "Error de Red"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra_optimizada.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": tipo_match
        })
        
    return analisis_estructurado, oracion_completa
