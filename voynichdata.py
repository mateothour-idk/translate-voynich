# voynichdata.py
import re
from deep_translator import GoogleTranslator  # Reemplaza el diccionario manual

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """ Conserva tus capas de transliteración originales intactas """
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    texto = re.sub(r'[0-9\*\-\/\=\+\%\&\$\#\_\@]', ' ', texto)
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
        texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p")
        texto = texto.replace("dc", "ch").replace("tc", "ch").replace("ct", "cut")
        texto = texto.replace("ph", "f").replace("sh", "x").replace("th", "t")
        texto = texto.replace("ch", "c").replace("ck", "qu").replace("tt", "t").replace("ts", "s")       
        texto = texto.replace("ee", "i").replace("oe", "ue").replace("iu", "u")
        texto = texto.replace("ii", "i").replace("ae", "e").replace("oo", "u")      
        texto = texto.replace("cs", "s").replace("ll", "y").replace("ey", "a")      
        texto = texto.replace("ce", "c").replace("ai", "i")      
        
        # Corrección fonética medieval de tu segunda capa
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
    """
    Traduce de manera AUTOMÁTICA basándose en la suposición de que el 
    texto resultante está en Latín Romance / Latín Medieval.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    
    # Intentamos traducir el bloque completo de texto como si fuera Latín
    # Esto elimina la necesidad de tener un diccionario guardado línea por línea
    target_lang = "es" if idioma == "es" else "en"
    
    try:
        # Forzamos al traductor a leer el texto procesado asumiendo que es Latín ('la')
        oracion_completa = GoogleTranslator(source='la', target=target_lang).translate(texto_limpio)
    except Exception:
        # En caso de falla de conexión o palabra inválida, junta el texto procesado
        oracion_completa = texto_limpio + " (Fallo en traducción automática)"

    # Rellenamos la tabla para que la interfaz de la App no se rompa
    for palabra in palabras:
        try:
            # Traduce palabra por palabra solo para el desglose visual de la tabla
            significado_individual = GoogleTranslator(source='la', target=target_lang).translate(palabra)
        except Exception:
            significado_individual = "[No Latino]"
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra.upper(),
            "Equivalencia Semántica": significado_individual,
            "Tipo de Match": "Traducción Dinámica NLP"
        })
        
    return analisis_estructurado, oracion_completa
