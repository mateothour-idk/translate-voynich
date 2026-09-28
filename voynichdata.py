# voynichdata.py
import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    texto = re.sub(r'[0-9\*\-\/\=\+\%\&\$\#\_\@]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    while True:
        texto_anterior = texto
        texto = texto.replace("pcee", "pi")
        texto = texto.replace("qok", "quoqu")
        texto = texto.replace("iii", "ee")     
        texto = texto.replace("eee", "ie")     
        texto = texto.replace("dce", "dic")
        texto = texto.replace("cee", "ci")
        texto = texto.replace("eey", "ai")     
        texto = texto.replace("pcs", "pes")
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
        texto = re.sub(r'\by\b', 'i', texto) 
        texto = re.sub(r'\by', 'i', texto)  
        texto = re.sub(r'y\b', 'i', texto)  
        texto = texto.replace("k", "qu")
        texto = texto.replace("q", "qu")
        texto = texto.replace("m", "m")       
        texto = texto.replace("l", "l")       
        texto = texto.replace("r", "r")       
        texto = texto.replace("n", "n")       
        texto = texto.replace("o", "o")       
        texto = texto.replace("a", "a")       
        texto = texto.replace("h", "")
        texto = texto.replace("quu", "qu")
        if texto == texto_anterior:
            break
    return texto.strip()

def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> tuple:
    palabras = texto_limpio.split()
    analisis_estructurado = []
    palabras_oracion = []
    
    diccionario_maestro = {
        "cut": {"es": "cortar", "en": "cut"},
        "ci": {"es": "aquí / este", "en": "here / this"},
        "ch": {"es": "clave / secreto", "en": "key / secret"},
        "ie": {"es": "ir / avanzar", "en": "go / advance"},
        "dic": {"es": "decir / dictar", "en": "say / dictate"},
        "quoqu": {"es": "cocinar / hervir", "en": "cook / boil"},
        "f": {"es": "hacer / crear", "en": "make / create"},
        "x": {"es": "seco / planta", "en": "dry / plant"},
        "pes": {"es": "pie / base", "en": "foot / base"},
        "col": {"es": "recolectar / colar", "en": "collect / strain"},
        "quok": {"es": "cocimiento", "en": "decoction"},
        "old": {"es": "antiguo / viejo", "en": "ancient / old"},
        "sho": {"es": "mostrar / ver", "en": "show / see"},
        "dai": {"es": "dar / aplicar", "en": "give / apply"},
        "tth": {"es": "tierra / suelo", "en": "earth / soil"},
        "cue": {"es": "cuerpo", "en": "body"},
        "xol": {"es": "sol / calor", "en": "sun / heat"},
        "tit": {"es": "título / marca", "en": "title / mark"},
        "pci": {"es": "pequeño / pizca", "en": "small / pinch"},
        "ole": {"es": "aceite / óleo", "en": "oil"},
        "sol": {"es": "disolver / mezcla", "en": "dissolve / mixture"},
        "an": {"es": "año / ciclo", "en": "year / cycle"},
        "ue": {"es": "fuente / agua", "en": "source / water"},
        "ic": {"es": "imagen / signo", "en": "image / sign"},
        "aqu": {"es": "agua", "en": "water"},
        "erb": {"es": "hierba", "en": "herb"},
        "rad": {"es": "raíz", "en": "root"},
        "suc": {"es": "jugo / savia", "en": "juice / sap"},
        "med": {"es": "médico", "en": "medical"},
        "san": {"es": "sano / curado", "en": "healthy / cured"},
        "coo": {"es": "cocer", "en": "boil"},
        "fol": {"es": "hoja", "en": "leaf"},
        "flo": {"es": "flor / brote", "en": "flower / bud"},
        "vax": {"es": "vaso / frasco", "en": "vessel / jar"},
        "mix": {"es": "mezclar", "en": "mix"},
        "pur": {"es": "puro / limpio", "en": "pure / clean"},
        "ext": {"es": "extracto", "en": "extract"},
        "nat": {"es": "natural", "en": "natural"},
        "cur": {"es": "cuidado / cura", "en": "care / cure"},
        "el": {"es": "el / este", "en": "the / this"},
        "lo": {"es": "lo / aquello", "en": "it / that"},
        "un": {"es": "un / uno", "en": "a / one"},
        "de": {"es": "de / desde", "en": "of / from"},
        "en": {"es": "en / dentro", "en": "in / inside"},
        "al": {"es": "al / hacia", "en": "to the / towards"},
        "con": {"es": "con / junto a", "en": "with"},
        "per": {"es": "por / mediante", "en": "by / through"},
        "is": {"es": "ese / esto", "en": "this / it"},
        "et": {"es": "y", "en": "and"},
        "ut": {"es": "para que / como", "en": "so that / as"},
        "non": {"es": "no", "en": "not"},
        "sic": {"es": "así", "en": "so"}
    }
    
    anagramas_raices = { "".join(sorted(k)): k for k in diccionario_maestro.keys() if len(k) >= 3 }

    for palabra in palabras:
        palabra_compuesta_detectada = False
        for i in range(2, len(palabra) - 1):
            sub1, sub2 = palabra[:i], palabra[i:]
            if sub1 in diccionario_maestro and sub2 in diccionario_maestro:
                trad1, trad2 = diccionario_maestro[sub1][idioma], diccionario_maestro[sub2][idioma]
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
            
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        palabra_para_oracion = f'"{palabra.upper()}"'  
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:3]][idioma]
            palabra_para_oracion = traducida + f"({palabra[3:].upper()})"
            tipo = "Match Raíz (3L)" if idioma == "es" else "Root Match (3L)"
        elif len(palabra) > 1 and palabra[:2] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:2]][idioma]
            palabra_para_oracion = traducida + f"({palabra[2:].upper()})"
            tipo = "Match Raíz (2L)" if idioma == "es" else "Root Match (2L)"
        else:
            # 1. Intentar Anagramas primero
            anagrama_encontrado = False
            longitud_analisis = min(len(palabra), 4)
            for l in range(longitud_analisis, 2, -1):
                segmento_ordenado = "".join(sorted(palabra[:l]))
                if segmento_ordenado in anagramas_raices:
                    raiz_encontrada = anagramas_raices[segmento_ordenado]
                    traducida = diccionario_maestro[raiz_encontrada][idioma]
                    excedente = palabra[l:].upper()
                    palabra_para_oracion = traducida + (f"({excedente})" if excedente else "") + "*"
                    tipo = f"Anagrama Raíz ({raiz_encontrada.upper()})" if idioma == "es" else f"Anagram Match ({raiz_encontrada.upper()})"
                    anagrama_encontrado = True
                    break
            
            # 2. SISTEMA DE RESCATE: Si sigue siendo incógnita, busca proximidad fonética consonántica
            if not anagrama_encontrado:
                consonantes_palabra = "".join([c for c in palabra if c not in 'aeiouíue'])
                if consonantes_palabra:
                    for raiz in diccionario_maestro.keys():
                        consonantes_raiz = "".join([c for c in raiz if c not in 'aeiouíue'])
                        if consonantes_raiz and consonantes_palabra.startswith(consonantes_raiz[:2]):
                            traducida = diccionario_maestro[raiz][idioma]
                            palabra_para_oracion = traducida + "?"
                            tipo = f"Aproximación Fonética ({raiz.upper()})" if idioma == "es" else f"Phonetic Match ({raiz.upper()})"
                            break
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
        palabras_oracion.append(palabra_para_oracion)
            
    oracion_completa = " ".join(palabras_oracion) + "."
    return analisis_estructurado, oracion_completa
