# voynichdata.py
import re
from deep_translator import GoogleTranslator

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Primera y Segunda Capa de Transliteración.
    Transforma caracteres EVA a fonética estructurada de Latín Romance Medieval.
    """
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    
    # Eliminación de anotaciones paleográficas, números y caracteres especiales del corpus
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\[.*?\]', ' ', texto) # Quita notas entre corchetes
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    while True:
        texto_anterior = texto
        
        # --- REGLA DE PROTECCIÓN ANTICIPADA (Fix pceeoe -> piue) ---
        texto = texto.replace("pceeoe", "piue")
        
        # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
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
        
        # --- 3. REGLAS DE 2 CARACTERES (Bigramas y Dígrafos) ---
        texto = texto.replace("pc", "p")
        texto = texto.replace("ps", "p")
        texto = texto.replace("cp", "p")
        texto = texto.replace("dc", "ch")     
        texto = texto.replace("tc", "ch")     
        texto = texto.replace("ct", "cut")
        texto = texto.replace("ph", "f")
        texto = texto.replace("sh", "x")       
        texto = texto.replace("th", "t")
        texto = texto.replace("ch", "c")      
        texto = texto.replace("ck", "qu")
        texto = texto.replace("tt", "t")       
        texto = texto.replace("ts", "s")       
        
        # Reglas Vocálicas y Consonánticas secundarias de 2 letras
        texto = texto.replace("ee", "i")
        texto = texto.replace("oe", "ue")     
        texto = texto.replace("iu", "u")
        texto = texto.replace("oi", "oi")
        texto = texto.replace("ii", "i")
        texto = texto.replace("ae", "e")      
        texto = texto.replace("oo", "u")      
        texto = texto.replace("cs", "s")
        texto = texto.replace("ll", "y")
        texto = texto.replace("ey", "a")      
        texto = texto.replace("ce", "c")
        texto = texto.replace("ai", "i")      
        
        # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO (Y inicial/final) ---
        re_y_aislada = re.compile(r'\by\b')
        re_y_inicial = re.compile(r'\by')
        re_y_final = re.compile(r'y\b')
        texto = re_y_aislada.sub('i', texto)
        texto = re_y_inicial.sub('i', texto)
        texto = re_y_final.sub('i', texto)
        
        # --- 5. SUSTITUCIÓN FINAL DE CONSONANTES Q / K ---
        texto = texto.replace("k", "qu")
        texto = texto.replace("q", "qu")
        
        # --- 6. SEGUNDA CAPA SELECCIONAL: CORRECCIÓN MEDIEVAL FONÉTICA ---
        texto = re.sub(r'\bchseor\b', 'senior', texto)  
        texto = re.sub(r'\bseor\b', 'senior', texto)
        texto = re.sub(r'iin\b', 'am', texto)          
        texto = re.sub(r'eiy\b', 'e', texto)           
        texto = re.sub(r'oitio', 'otio', texto)         
        
        # Limpiezas finales
        texto = texto.replace("h", "")
        texto = texto.replace("quu", "qu")
        
        if texto == texto_anterior:
            break
            
    return texto.strip()

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    """
    Traduce de manera AUTOMÁTICA basándose en la suposición de que el 
    texto resultante está en Latín Romance / Latín Medieval.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    target_lang = "es" if idioma == "es" else "en"
    
    if not palabras:
        return [], ""

    # 1. TRADUCCIÓN CONTEXTUAL EN BLOQUE (Une las palabras para darles sentido de oración)
    try:
        oracion_completa = GoogleTranslator(source='la', target=target_lang).translate(texto_limpio)
    except Exception:
        oracion_completa = "[Error de conexión con la API de traducción]"

    # 2. TRADUCCIÓN PALABRA POR PALABRA PARA LA TABLA
    for palabra in palabras:
        # Filtrar cadenas vacías o raras
        if not palabra.strip():
            continue
        try:
            significado_individual = GoogleTranslator(source='la', target=target_lang).translate(palabra)
        except Exception:
            significado_individual = "[Incógnita]"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": "Traducción Dinámica NLP (Latín)"
        })
        
    return analisis_estructurado, oracion_completa
