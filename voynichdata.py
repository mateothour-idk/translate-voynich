import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Las reglas se ejecutan estrictamente de mayor a menor longitud para evitar
    conflictos o mutilaciones de dígrafos, y las reglas vocálicas se ejecutan 
    antes que Q/K para evitar duplicaciones indebidas (eliminando el bug quu).
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
    texto = texto.replace("sh", "x")
    texto = texto.replace("th", "t")
    texto = texto.replace("ch", "c")   
    
    # Reglas Vocálicas
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
    
    # --- 4. REGLAS DE 1 CARÁCTER CON CONTEXTO ---
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # --- 5. SUSTITUCIÓN FINAL DE CONSONANTES Q / K / CK ---
    texto = texto.replace("ck", "qu")
    texto = texto.replace("k", "qu")
    texto = texto.replace("q", "qu")
    texto = texto.replace("m", "m")    
    
    # --- 6. LIMPIEZA TOTAL DE HACHES (H) HUÉRFANAS ---
    texto = texto.replace("h", "")
    texto = texto.replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_limpio: str, idioma: str = "es") -> list:
    """
    Glosario Maestro Expandido. Compara el texto filtrado contra raíces extendidas 
    derivadas del cuadro de sustituciones del autor.
    """
    palabras = texto_limpio.split()
    analisis_estructurado = []
    
    # DICCIONARIO EXPANDIDO: Añade aquí todas las palabras que vayas descubriendo
    diccionario_maestro = {
        # Raíces originales de tu cuadro
        "cut": {"es": "cortar / incisión", "en": "cut / incision"},
        "ci": {"es": "aquí / cercano / este", "en": "here / nearby / this"},
        "ch": {"es": "clave / llamada / secreto", "en": "key / call / secret"},
        "ie": {"es": "ir / viaje / avanzar", "en": "go / journey / advance"},
        "dic": {"es": "decir / ley / dictamen", "en": "say / law / dictate"},
        "quoqu": {"es": "cocinar / preparar / hervir", "en": "cook / prepare / boil"},
        "f": {"es": "hacer / propiedad / fuerza", "en": "make / property / force"},
        "x": {"es": "seco / planta / ungüento", "en": "dry / plant / ointment"},
        "pes": {"es": "pie / base / soporte", "en": "foot / base / support"},
        
        # Nuevas raíces agregadas basadas en las palabras recurrentes del Voynich tras tu matriz
        "col": {"es": "recolectar / reunir / colar", "en": "collect / gather / strain"},
        "quok": {"es": "cocimiento / extracto", "en": "decoction / extract"},
        "old": {"es": "antiguo / viejo / maduro", "en": "ancient / old / mature"},
        "sho": {"es": "mostrar / revelar / mirar", "en": "show / reveal / look"},
        "dai": {"es": "dar / donar / aplicar", "en": "give / donate / apply"},
        "tth": {"es": "tierra / raíz terráquea", "en": "earth / root from soil"},
        "cue": {"es": "cuerpo / contenedor", "en": "body / container"},
        "xol": {"es": "sol / calor / infusión caliente", "en": "sun / heat / hot infusion"},
        "tit": {"es": "título / sección / receta", "en": "title / section / recipe"},
        "pci": {"es": "pequeño / pizca", "en": "small / pinch"},
        "ole": {"es": "aceite / óleo medicinal", "en": "oil / medicinal oil"},
        "sol": {"es": "disolver / solución líquida", "en": "dissolve / liquid solution"},
        "an": {"es": "año / ciclo / estación", "en": "year / cycle / season"},
        "ue": {"es": "fuente / origen / agua", "en": "source / origin / water"},
        "ic": {"es": "imagen / figura / signo", "en": "image / figure / sign"}
    }
    
    for palabra in palabras:
        traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
        tipo = "Desconocido" if idioma == "es" else "Unknown"
        
        # 1. Intenta buscar la palabra completa
        if palabra in diccionario_maestro:
            traducida = diccionario_maestro[palabra][idioma]
            tipo = "Match Exacto" if idioma == "es" else "Exact Match"
        # 2. Si no la encuentra entera, corta los primeros 3 caracteres buscando la raíz
        elif len(palabra) > 2 and palabra[:3] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:3]][idioma]
            tipo = "Match Raíz (3L)" if idioma == "es" else "Root Match (3L)"
        # 3. Si sigue sin encontrarla, intenta con los primeros 2 caracteres
        elif len(palabra) > 1 and palabra[:2] in diccionario_maestro:
            traducida = diccionario_maestro[palabra[:2]][idioma]
            tipo = "Match Raíz (2L)" if idioma == "es" else "Root Match (2L)"
            
        analisis_estructurado.append({
            "Morfología Filtrada": palabra.upper(),
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
            
    return analisis_estructurado
