import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Se han integrado las nuevas reglas del usuario, ordenadas estrictamente 
    de mayor a menor longitud para evitar que los bigramas rompan los trigramas.
    """
    if not texto_eva:
        return ""
        
    texto = texto_eva.lower()
    
    # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
    texto = texto.replace("pcee", "pi")
    
    # --- 2. REGLAS DE 3 CARACTERES (Trigramas) ---
    texto = texto.replace("qok", "quoqu")    # Qok = Quoqu
    texto = texto.replace("iii", "í")        # Iii = Í
    texto = texto.replace("eee", "ie")       # Eee = Ie (Evolución romance preferida para verbos como 'ir')
    texto = texto.replace("eey", "ai")       # Eey = Ai / Iy
    texto = texto.replace("pcs", "pes")      # Pcs = Pes (Raíz de 'pie')
    texto = texto.replace("dce", "dic")      # Dce = Dic (Raíz de 'decir')
    texto = texto.replace("cee", "ci")       # Cee = Ci / Ce
    
    # --- 3. REGLAS DE 2 CARACTERES (Bigramas y Dígrafos) ---
    # Unificación de Letras Horca (Gallows)
    texto = texto.replace("pc", "p")
    texto = texto.replace("ps", "p")
    texto = texto.replace("cp", "p")
    
    # Africadas y Oclusivas Dentales
    texto = texto.replace("dc", "ch")        # Dc / Tc = C con sonido Ch
    texto = texto.replace("tc", "ch")
    texto = texto.replace("ct", "cut")       # Ct = Cut (Raíz cutis/cortar)
    
    # Sibilantes y Fricativas (Restauración de SH = X)
    texto = texto.replace("sh", "x")        # Sh = X (Crucial para términos como xol/sol)
    texto = texto.replace("ph", "f")        # Ph = F
    texto = texto.replace("th", "t")        # Th = T
    texto = texto.replace("ch", "c")        # Ch = C / Ch
    texto = texto.replace("ck", "qu")       # Ck / K = Qu
    texto = texto.replace("cs", "s")         # Cs = S
    
    # Transiciones Vocálicas y Diptongos Romances
    texto = texto.replace("ee", "i")
    texto = texto.replace("oe", "ue")       # Oe = Ue / U
    texto = texto.replace("iu", "u")        # Iu = U
    texto = texto.replace("oi", "oi")       # Oi = Oy / Oi
    texto = texto.replace("ii", "i")
    texto = texto.replace("ae", "e")        # Ae = A / E
    texto = texto.replace("oo", "u")        # Oo = U / Oo
    texto = texto.replace("ey", "a")        # Ey = A corta
    texto = texto.replace("ai", "i")        # Ai = I / Ai
    texto = texto.replace("ll", "y")        # Ll = Y
    
    # Nota: 'ce' se mantiene como 'ce' según la matriz original (Ce = Ce)
    
    # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO (Y inicial/final) ---
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. SUSTITUCIÓN DE CONSONANTES INDIVIDUALES ---
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")          # M = M / N (Estable en el alfabeto del motor)
    texto = texto.replace("l", "l")       
    
    # --- 6. DEPURACIÓN DE HACHES HUÉRFANAS Y REDUNDANCIAS ---
    texto = texto.replace("h", "")
    texto = texto.replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    """
    Procesa el texto limpio y devuelve una tupla:
    1. Una lista de diccionarios para la tabla analítica de Streamlit.
    2. La oración armada continuamente con separaciones inteligentes.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    palabras_oracion = []
    
    # Glosario maestro balanceado para la fonética romance resultante
    diccionario_maestro = {
        "cut": {"es": "cortar", "en": "cut"},
        "ci": {"es": "aquí", "en": "here"},
        "ch": {"es": "clave", "en": "key"},
        "ie": {"es": "ir", "en": "go"},
        "dic": {"es": "decir", "en": "say"},
        "quoqu": {"es": "cocinar/cocimiento", "en": "cook/decoction"},
        "f": {"es": "hacer", "en": "make"},
        "x": {"es": "seco", "en": "dry"},
        "pes": {"es": "pie", "en": "foot"},
        "col": {"es": "recolectar", "en": "collect"},
        "old": {"es": "antiguo", "en": "ancient"},
        "sho": {"es": "mostrar", "en": "show"},
        "dai": {"es": "dar", "en": "give"},
        "tth": {"es": "tierra", "en": "earth"},
        "cue": {"es": "cuerpo", "en": "body"},
        "xol": {"es": "sol", "en": "sun"},
        "tit": {"es": "título", "en": "title"},
        "pci": {"es": "pequeño", "en": "small"},
        "ole": {"es": "aceite", "en": "oil"},
        "sol": {"es": "disolver", "en": "dissolve"},
        "an": {"es": "año", "en": "year"},
        "ue": {"es": "fuente", "en": "source"},
        "ic": {"es": "imagen", "en": "image"}
    }
    
    for palabra in palabras:
        # --- 1. DETECTOR Y SEPARADOR DE COMPUESTAS ---
        palabra_compuesta_detectada = False
        for i in range(2, len(palabra) - 1):
            sub1 = palabra[:i]
            sub2 = palabra[i:]
            if sub1 in diccionario_maestro and sub2 in diccionario_maestro:
                trad1 = diccionario_maestro[sub1][idioma]
                trad2 = diccionario_maestro[sub2][idioma]
                
                palabras_oracion.append(f"{trad1}+{trad2}")
                palabra_compuesta_detectada = True
                
                analisis_estructurado.append({
                    "Morfología Filtrada": palabra.upper(),
                    "Interpretación / Semántica": f"{trad1} / {trad2}",
                    "Diagnóstico": "Compuesta Separada" if idioma == "es" else "Split Compound"
                })
                break
                
        if palabra_compuesta_detectada:
            continue
            
        # --- 2. PROCESAMIENTO ESTÁNDAR Y BÚSQUEDA DE RAÍCES DINÁMICA ---
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        palabra_para_oracion = f'"{palabra.upper()}"'
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        else:
            # Escaneo decreciente de prefijos para admitir raíces de cualquier longitud (ej: 'quoqu')
            match_raiz_encontrado = False
            for tam in range(len(palabra) - 1, 1, -1):
                prefijo = palabra[:tam]
                if prefijo in diccionario_maestro:
                    resto = palabra[tam:].upper()
                    traducida = diccionario_maestro[prefijo][idioma]
                    palabra_para_oracion = traducida + f"(= {resto})"
                    tipo = f"Match Raíz ({tam}L)" if idioma == "es" else f"Root Match ({tam}L)"
                    match_raiz_encontrado = True
                    break
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
        palabras_oracion.append(palabra_para_oracion)
            
    oracion_completa = " ".join(palabras_oracion) + "."
    return analisis_estructurado, oracion_completa
