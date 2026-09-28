# voynichdata.py
import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Primera y Segunda Capa de TransliteraciÃ³n.
    Transforma caracteres EVA a fonÃ©tica estructurada de LatÃ­n Romance Medieval.
    """
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    texto = re.sub(r'[0-9\*\-\/\=\+\%\&\$\#\_\@]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    while True:
        texto_anterior = texto
        
        # --- REGLA DE PROTECCIÃ“N ANTICIPADA (Fix pceeoe -> piue) ---
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
        
        # --- 3. REGLAS DE 2 CARACTERES (Bigramas y DÃ­grafos) ---
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
        
        # Reglas VocÃ¡licas y ConsonÃ¡nticas secundarias de 2 letras
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
        
        # --- 4. REGLAS DE 1 CARÃCTER CON CONTEXTO (Y inicial/final) ---
        re_y_aislada = re.compile(r'\by\b')
        re_y_inicial = re.compile(r'\by')
        re_y_final = re.compile(r'y\b')
        texto = re_y_aislada.sub('i', texto)
        texto = re_y_inicial.sub('i', texto)
        texto = re_y_final.sub('i', texto)
        
        # --- 5. SUSTITUCIÃ“N FINAL DE CONSONANTES Q / K ---
        texto = texto.replace("k", "qu")
        texto = texto.replace("q", "qu")
        
        # --- 6. SEGUNDA CAPA SELECCIONAL: CORRECCIÃ“N MEDIEVAL FONÃ‰TICA ---
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
    Analiza el texto ya procesado por la doble transliteraciÃ³n y asocia
    las raÃ­ces reconstrucidas con su significado botÃ¡nico eclesiÃ¡stico/romance.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    palabras_oracion = []
    
    # Glosario maestro adaptado para la fonÃ©tica romance obtenida
    diccionario_maestro = {
        "piue": {"es": "mÃ¡s (ademÃ¡s)", "en": "more (furthermore)"},
        "piu": {"es": "mÃ¡s", "en": "more"},
        "codar": {"es": "cocer (hervir)", "en": "to cook (boil)"},
        "oleis": {"es": "con aceites", "en": "with oils"},
        "cipi": {"es": "tallos (bulbos)", "en": "stems (bulbs)"},
        "seol": {"es": "seco", "en": "dry"},
        "sequieo": {"es": "secar (dejar secar)", "en": "to dry out"},
        "otolsai": {"es": "extraer", "en": "extract"},
        "senior": {"es": "el maestro (autor)", "en": "the master (author)"},
        "olse": {"es": "aceitoso (oler)", "en": "oily (to smell)"},
        "quodam": {"es": "un cierto (el cual)", "en": "a certain (which)"},
        "quoquior": {"es": "tambiÃ©n (asimismo)", "en": "also (likewise)"},
        "oram": {"es": "el borde (perÃ­metro)", "en": "the edge (margin)"},
        "iquiol": {"es": "jugo extraÃ­do", "en": "extracted juice"},
        "otio": {"es": "en reposo", "en": "at rest"},
        "cute": {"es": "en la piel (corteza)", "en": "on the skin (bark)"},
        "cior": {"es": "mover", "en": "to move"},
        "cioquai": {"es": "hervido", "en": "decocted"},
        "cut": {"es": "cortar", "en": "cut"},
        "ci": {"es": "este", "en": "this"},
        "ch": {"es": "secreto", "en": "secret"},
        "ie": {"es": "ir", "en": "go"},
        "dic": {"es": "decir", "en": "say"},
        "quoqu": {"es": "cocinar", "en": "cook"},
        "f": {"es": "hacer", "en": "make"},
        "x": {"es": "planta", "en": "plant"},
        "pes": {"es": "base", "en": "base"},
        "col": {"es": "recolectar", "en": "collect"},
        "quok": {"es": "cocimiento", "en": "decoction"},
        "old": {"es": "antiguo", "en": "ancient"},
        "sho": {"es": "mostrar", "en": "show"},
        "dai": {"es": "aplicar", "en": "apply"},
        "tth": {"es": "tierra", "en": "earth"},
        "cue": {"es": "cuerpo", "en": "body"},
        "xol": {"es": "calor", "en": "heat"},
        "tit": {"es": "marca", "en": "mark"},
        "pci": {"es": "pequeÃ±o", "en": "small"},
        "ole": {"es": "aceite", "en": "oil"},
        "sol": {"es": "disolver", "en": "dissolve"},
        "an": {"es": "ciclo", "en": "cycle"},
        "ue": {"es": "agua", "en": "water"},
        "ic": {"es": "signo", "en": "sign"},
        "et": {"es": "y", "en": "and"}
    }
    
    anagramas_raices = { "".join(sorted(k)): k for k in diccionario_maestro.keys() if len(k) >= 3 }

    def limpiar_prosa(texto):
        if not texto: 
            return ""
        lista_palabras = texto.split("/")
        termino_limpio = lista_palabras[0]
        return termino_limpio.strip().replace("?", "").replace("*", "")

    for palabra in palabras:
        palabra_compuesta_detectada = False
        for i in range(2, len(palabra) - 1):
            sub1, sub2 = palabra[:i], palabra[i:]
            if sub1 in diccionario_maestro and sub2 in diccionario_maestro:
                trad1 = diccionario_maestro[sub1][idioma]
                trad2 = diccionario_maestro[sub2][idioma]
                
                palabras_oracion.append(f"{limpiar_prosa(trad1)} {limpiar_prosa(trad2)}")
                palabra_compuesta_detectada = True
                analisis_estructurado.append({
                    "Palabra Filtrada": palabra.upper(),
                    "Equivalencia SemÃ¡ntica": f"{trad1} / {trad2}",
                    "Tipo de Match": "Compuesta Separada" if idioma == "es" else "Split Compound"
                })
                break
        if palabra_compuesta_detectada:
            continue
            
        traducida = "[IncÃ³gnita]" if idioma == "es" else "[Unknown]"
        palabra_para_oracion = f'"{palabra.upper()}"'  
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            palabra_para_oracion = limpiar_prosa(traducida)
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:3]][idioma]
            palabra_para_oracion = limpiar_prosa(traducida)
            tipo = "Match RaÃ­z (3L)" if idioma == "es" else "Root Match (3L)"
        elif len(palabra) > 1 and palabra[:2] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:2]][idioma]
            palabra_para_oracion = limpiar_prosa(traducida)
            tipo = "Match RaÃ­z (2L)" if idioma == "es" else "Root Match (2L)"
        else:
            anagrama_encontrado = False
            longitud_analisis = min(len(palabra), 4)
            for l in range(longitud_analisis, 2, -1):
                segmento_ordenado = "".join(sorted(palabra[:l]))
                if segmento_ordenado in anagramas_raices:
                    raiz_encontrada = anagramas_raices[segmento_ordenado]
                    traducida = diccionario_maestro[raiz_encontrada][idioma]
                    palabra_para_oracion = limpiar_prosa(traducida)
                    tipo = f"Anagrama RaÃ­z ({raiz_encontrada.upper()})" if idioma == "es" else f"Anagram Match ({raiz_encontrada.upper()})"
                    anagrama_encontrado = True
                    break
            
            if not anagrama_encontrado:
                consonantes_palabra = "".join([c for c in palabra if c not in 'aeiouÃ­ue'])
                if consonantes_palabra:
                    for raiz in diccionario_maestro.keys():
                        consonantes_raiz = "".join([c for c in raiz if c not in 'aeiouÃ­ue'])
                        if consonantes_raiz and consonantes_palabra.startswith(consonantes_raiz[:2]):
                            traducida = diccionario_maestro[raiz][idioma]
                            palabra_para_oracion = limpiar_prosa(traducida)
                            tipo = f"AproximaciÃ³n FonÃ©tica ({raiz.upper()})" if idioma == "es" else f"Phonetic Match ({raiz.upper()})"
                            break
            
        analisis_estructurado.append({
            "Palabra Filtrada": palabra.upper(),
            "Equivalencia SemÃ¡ntica": traducida,
            "Tipo de Match": tipo
        })
        palabras_oracion.append(palabra_para_oracion)
            
    oracion_completa = " ".join(palabras_oracion).strip()
    oracion_completa = re.sub(r'\s+', ' ', oracion_completa) + "."
    return analisis_estructurado, oracion_completa
