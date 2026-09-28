# voynichdata.py
import re
from deep_translator import GoogleTranslator

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    texto = re.sub(r'[*\-/\=+%\&$\#_@.!?,;:]', ' ', texto)
    texto = re.sub(r'\[.*?\]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    while True:
        texto_anterior = texto
        texto = texto.replace("pceeoe", "piue")
        texto = texto.replace("pcee", "pi")
        texto = texto.replace("qok", "quoqu")
        texto = texto.replace("iii", "i")     
        texto = texto.replace("eee", "ei")     
        texto = texto.replace("dce", "dic")
        texto = texto.replace("cee", "ci")
        texto = texto.replace("eey", "ai")     
        texto = texto.replace("pcs", "pes")
        texto = texto.replace("pdr", "pedr")
        texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p")
        texto = texto.replace("dc", "ch").replace("tc", "ch").replace("ct", "cut")
        texto = texto.replace("ph", "f").replace("sh", "x").replace("th", "t")
        texto = texto.replace("ch", "c").replace("ck", "qu").replace("tt", "t").replace("ts", "s")       
        texto = texto.replace("ee", "i").replace("oe", "ue").replace("iu", "u")
        texto = texto.replace("ii", "i").replace("ae", "e").replace("oo", "u")      
        texto = texto.replace("cs", "s").replace("ll", "y").replace("ey", "a")      
        texto = texto.replace("ce", "c").replace("ai", "i")      
        
        texto = re.sub(r'\bchseor\b', 'senior', texto)  
        texto = re.sub(r'\bseor\b', 'senior', texto)
        texto = re.sub(r'iin\b', 'am', texto)          
        texto = re.sub(r'eiy\b', 'e', texto)           
        texto = re.sub(r'oitio', 'otio', texto)         
        texto = texto.replace("h", "").replace("quu", "qu")
        
        if texto == texto_anterior:
            break
    return texto.strip()

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    palabras = texto_limpio.split()
    analisis_estructurado = []
    target_lang = "es" if idioma == "es" else "en"
    
    if not palabras:
        return [], ""

    # 1. TRADUCCIÓN CONTEXTUAL EN BLOQUES PEQUEÑOS
    palabras_traducidas_oracion = []
    chunk_size = 5
    for i in range(0, len(palabras), chunk_size):
        sub_bloque = " ".join(palabras[i:i + chunk_size])
        if not sub_bloque.strip():
            continue
        try:
            traduccion_fragmento = GoogleTranslator(source='la', target=target_lang).translate(sub_bloque)
            palabras_traducidas_oracion.append(traduccion_fragmento)
        except Exception:
            palabras_traducidas_oracion.append(sub_bloque)

    oracion_completa = " ".join(palabras_traducidas_oracion)

    # 2. TRADUCCIÓN PARA LA TABLA CON FILTRO DE RAÍCES REALES
    for palabra in palabras[:30]:
        if not palabra.strip() or len(palabra) < 2:
            continue
        try:
            significado_individual = GoogleTranslator(source='la', target=target_lang).translate(palabra)
            # Si el traductor nos devuelve exactamente la misma palabra (porque no la entendió),
            # intentamos decodificarla asumiendo una aproximación del latín vulgar / italiano antiguo
            if significado_individual.lower() == palabra.lower():
                significado_individual = GoogleTranslator(source='it', target=target_lang).translate(palabra)
        except Exception:
            significado_individual = "[Incógnita]"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": "Traducción Dinámica NLP"
        })
        
    if len(palabras) > 30:
        analisis_estructurado.append({
            "Palabra Filtrada": "...",
            "Equivalencia Semántica": "Texto truncado para conservar velocidad",
            "Tipo de Match": "Límite de API"
        })
        
    return analisis_estructurado, oracion_completa
