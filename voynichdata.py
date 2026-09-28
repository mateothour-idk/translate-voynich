import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Las sustituciones se ejecutan estrictamente de mayor a menor longitud.
    """
    if not texto_eva:
        return ""
        
    texto = texto_eva.lower()
    
    # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
    texto = texto.replace("pcee", "pi")
    texto = texto.replace("qok", "quoqu")
    
    # --- 2. REGLAS DE 3 CARACTERES (Trigramas) ---
    texto = texto.replace("iii", "í")
    texto = texto.replace("eee", "ie")     
    texto = texto.replace("dce", "dic")
    texto = texto.replace("cee", "ci")
    texto = texto.replace("eey", "ai")     
    texto = texto.replace("pcs", "pes")
    
    # --- 3. REGLAS DE 2 CARACTERES (Bigramas y Dígrafos) ---
    texto = texto.replace("pc", "p")
    texto = texto.replace("ps", "p")
    texto = texto.replace("cp", "p")
    texto = texto.replace("dc", "ch")     
    texto = texto.replace("tc", "ch")     
    texto = texto.replace("ct", "cut")
    texto = texto.replace("ph", "f")
    texto = texto.replace("sh", "s")       
    texto = texto.replace("th", "t")
    texto = texto.replace("ch", "c")      
    texto = texto.replace("ck", "qu")
    
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
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. SUSTITUCIÓN FINAL DE CONSONANTES Q / K ---
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")       
    texto = texto.replace("l", "l")       
    
    # --- 6. LIMPIEZA TOTAL DE HACHES (H) HUÉRFANAS ---
    texto = texto.replace("h", "")
    texto = texto.replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    """
    Procesa el texto limpio y devuelve una tupla:
    1. Una lista de diccionarios para la tabla analítica.
    2. La oración armada continuamente, resolviendo anagramas si no hay match directo.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    palabras_oracion = []
    
    # Glosario ampliado con raíces botánicas y farmacéuticas medievales
    diccionario_maestro = {
        "cut": {"es": "cortar", "en": "cut"},
        "ci": {"es": "aquí", "en": "here"},
        "ch": {"es": "clave", "en": "key"},
        "ie": {"es": "ir", "en": "go"},
        "dic": {"es": "decir", "en": "say"},
        "quoqu": {"es": "cocinar", "en": "cook"},
        "f": {"es": "hacer", "en": "make"},
        "x": {"es": "seco", "en": "dry"},
        "pes": {"es": "pie", "en": "foot"},
        "col": {"es": "recolectar", "en": "collect"},
        "quok": {"es": "cocimiento", "en": "decoction"},
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
        "ic": {"es": "imagen", "en": "image"},
        
        # Nuevas raíces críticas del Latín Vulgar/Médico añadidas
        "aqu": {"es": "agua", "en": "water"},
        "erb": {"es": "hierba / planta", "en": "herb / plant"},
        "rad": {"es": "raíz / base", "en": "root"},
        "suc": {"es": "jugo / savia", "en": "juice / sap"},
        "med": {"es": "médico / cura", "en": "heal / medical"},
        "san": {"es": "santo / sano", "en": "holy / healthy"},
        "coo": {"es": "cocer / calentar", "en": "boil / heat"}
    }
    
    # Precalculamos las letras ordenadas de las raíces para la detección de anagramas
    anagramas_raices = {}
    for raiz, traducciones in diccionario_maestro.items():
        if len(raiz) >= 3: # Solo buscamos anagramas en raíces significativas de 3 o más letras
            llave_ordenada = "".join(sorted(raiz))
            if llave_ordenada not in anagramas_raices:
                anagramas_raices[llave_ordenada] = raiz

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
            
        # --- 2. PROCESAMIENTO ESTÁNDAR Y FILTRO DE ANAGRAMAS ---
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        palabra_para_oracion = f'"{palabra.upper()}"'  
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        # Match Exacto
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
            
        # Match Raíz Estándar (3L)
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:3]][idioma]
            palabra_para_oracion = traducida + f"({palabra[3:].upper()})"
            tipo = "Match Raíz (3L)" if idioma == "es" else "Root Match (3L)"
            
        # Match Raíz Estándar (2L)
        elif len(palabra) > 1 and palabra[:2] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:2]][idioma]
            palabra_para_oracion = traducida + f"({palabra[2:].upper()})"
            tipo = "Match Raíz (2L)" if idioma == "es" else "Root Match (2L)"
            
        # --- DETECTOR DE ANAGRAMAS ACTIVO ---
        # Si la palabra sigue siendo incógnita, reordenamos sus primeras 3 o 4 letras 
        # para ver si el escriba mezcló los caracteres de una raíz conocida
        else:
            longitud_analisis = min(len(palabra), 4)
            for l in range(longitud_analisis, 2, -1):
                segmento_ordenado = "".join(sorted(palabra[:l]))
                if segmento_ordenado in anagramas_raices:
                    raiz_encontrada = anagramas_raices[segmento_ordenado]
                    traducida = diccionario_maestro[raiz_encontrada][idioma]
                    
                    excedente = palabra[l:].upper()
                    sufijo_exc = f"({excedente})" if excedente else ""
                    palabra_para_oracion = traducida + sufijo_exc + "*"
                    
                    tipo = f"Anagrama Raíz ({raiz_encontrada.upper()})" if idioma == "es" else f"Anagram Match ({raiz_encontrada.upper()})"
                    break
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
        palabras_oracion.append(palabra_para_oracion)
            
    oracion_completa = " ".join(palabras_oracion) + "."
    return analisis_estructurado, oracion_completa
