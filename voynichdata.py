# voynichdata.py
import re
from deep_translator import GoogleTranslator

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Primera y Segunda Capa de Transliteración.
    Genera la base fonética respetando las reglas de combinación de caracteres.
    """
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\[.*?\]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    while True:
        texto_anterior = texto
        
        # --- NUEVAS REGLAS Y PROTECCIONES ---
        texto = texto.replace("pceeoe", "piue")
        texto = texto.replace("x", "sh")
        
        # --- 1. REGLAS DE 4 CARACTERES ---
        texto = texto.replace("pcee", "pi")
        texto = texto.replace("qok", "quoqu")
        
        # --- 2. REGLAS DE 3 CARACTERES ---
        texto = texto.replace("iii", "i")     
        texto = texto.replace("eee", "ei")     
        texto = texto.replace("dce", "dic")
        texto = texto.replace("cee", "ci")
        texto = texto.replace("eey", "ai")     
        texto = texto.replace("pcs", "pes")
        texto = texto.replace("pdr", "pedr")
        
        # --- 3. REGLAS DE 2 CARACTERES ---
        texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p")
        texto = texto.replace("dc", "ch").replace("tc", "ch").replace("ct", "cut")
        texto = texto.replace("ph", "f").replace("sh", "x").replace("th", "t")
        texto = texto.replace("ch", "c").replace("ck", "qu").replace("tt", "t").replace("ts", "s")       
        
        # Reducción de duplicados antes de vocales
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
        
        # --- 4. CONTEXTO DE LA 'Y' ---
        re_y_aislada = re.compile(r'\by\b')
        re_y_inicial = re.compile(r'\by')
        re_y_final = re.compile(r'y\b')
        texto = re_y_aislada.sub('i', texto)
        texto = re_y_inicial.sub('i', texto)
        texto = re_y_final.sub('i', texto)
        
        # --- 5. REGLAS DE LA K / Q (Aquí aplicamos tu regla adaptativa) ---
        texto = texto.replace("k", "qu")      
        texto = texto.replace("q", "qu")
        
        # --- 6. SEGUNDA CAPA SELECCIONAL MEDIEVAL ---
        texto = re.sub(r'\bchseor\b', 'senior', texto)  
        texto = re.sub(r'\bseor\b', 'senior', texto)
        texto = re.sub(r'iin\b', 'am', texto)          
        texto = re.sub(r'eiy\b', 'e', texto)           
        texto = re.sub(r'oitio', 'otio', texto)         
        
        texto = texto.replace("h", "")
        
        if texto == texto_anterior:
            break
            
    return texto.strip()

def resolver_contexto_palabra(palabra: str) -> str:
    """
    Toma una palabra transliterada y evalúa las variantes / de tus reglas.
    Si tiene 'qu', genera la opción con 'q' para ver cuál acepta el diccionario.
    """
    p_baja = palabra.lower()
    
    # Si la palabra termina o empieza con patrones de tu regla Q=Qu/Q o O=O/U
    # Probamos reemplazando el exceso 'quu' o 'qu' por 'q' o 'u' por 'o'
    if "quu" in p_baja:
        return p_baja.replace("quu", "qu")
    if p_baja.startswith("qu") and len(p_baja) > 2:
        # Genera una alternativa corta (ej: quuin -> quin -> qin)
        opcion_q = p_baja.replace("qu", "q", 1)
        return f"{p_baja}/{opcion_q}"
        
    return p_baja

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    """
    Analiza las variantes contextuales de las palabras y le pide a la IA
    que elija la traducción que mejor encaje en el español/inglés medieval.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    target_lang = "es" if idioma == "es" else "en"
    
    # Glosario base de apoyo paleográfico
    glosario_auxilio = {
        "piue": "más", "piu": "más", "codar": "cocer", "oleis": "aceites", 
        "cipi": "tallos", "seol": "seco", "sequieo": "secado", "otolsai": "extraer",
        "senior": "señor", "olse": "aceitoso", "quodam": "un cierto", "oram": "borde",
        "iquiol": "jugo", "otio": "reposo", "cute": "piel", "cior": "mover", 
        "cioquai": "infusión", "cut": "cortar"
    } if target_lang == "es" else {
        "piue": "more", "piu": "more", "codar": "cook", "oleis": "oils", 
        "cipi": "stems", "seol": "dry", "sequieo": "dried", "otolsai": "extract",
        "senior": "master", "olse": "oily", "quodam": "a certain", "oram": "edge",
        "iquiol": "juice", "otio": "rest", "cute": "skin", "cior": "move", 
        "cioquai": "decoction", "cut": "cut"
    }
    
    if not palabras:
        return [], ""

    palabras_traducidas_oracion = []
    
    # 1. PROCESAMIENTO CONTEXTUAL INTELIGENTE
    for palabra in palabras:
        palabra_optimizada = resolver_contexto_palabra(palabra)
        
        # Si la palabra base (o su variante) está en el glosario manual, la tomamos directo
        encontrada = False
        for opcion in palabra_optimizada.split("/"):
            if opcion in glosario_auxilio:
                palabras_traducidas_oracion.append(glosario_auxilio[opcion])
                encontrada = True
                break
        
        if encontrada:
            continue
            
        # Si no está en el glosario, mandamos las opciones separadas por barra a la IA.
        # Los traductores modernos al ver "quin/qin" o "quuin/quin" analizan el texto 
        # circundante y descartan la opción que no existe en el diccionario.
        try:
            traduccion = GoogleTranslator(source='auto', target=target_lang).translate(palabra_optimizada)
            # Limpieza por si la IA devuelve ambas opciones separadas por barra
            traduccion_limpia = traduccion.split("/")[0].split("\\")[0]
            palabras_traducidas_oracion.append(traduccion_limpia)
        except Exception:
            palabras_traducidas_oracion.append(palabra)

    oracion_completa = " ".join(palabras_traducidas_oracion)

    # 2. LLENADO DE LA TABLA INTERACTIVA
    for palabra in palabras[:30]:
        if not palabra.strip():
            continue
            
        palabra_optimizada = resolver_contexto_palabra(palabra)
        opciones = palabra_optimizada.split("/")
        
        significado_individual = "[Desconocido]"
        for op in opciones:
            if op in glosario_auxilio:
                significado_individual = glosario_auxilio[op]
                break
        
        if significado_individual == "[Desconocido]":
            try:
                # Le pasamos la cadena con barra para que la IA elija en la celda
                trad = GoogleTranslator(source='auto', target=target_lang).translate(palabra_optimizada)
                significado_individual = trad.split("/")[0]
                if significado_individual.lower() == palabra_optimizada.lower():
                    significado_individual = "[Desconocido]"
            except Exception:
                significado_individual = "[Incógnita]"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra_optimizada.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": "Evaluación de Contexto"
        })
        
    return analisis_estructurado, oracion_completa
