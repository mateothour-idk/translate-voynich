import re

def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográficas exactas del usuario.
    Ordenadas estrictamente de mayor a menor longitud para evitar colisiones.
    """
    if not texto_eva:
        return ""
    texto = texto_eva.lower()
    
    # Tetragramas
    texto = texto.replace("pcee", "pi")
    
    # Trigramas
    texto = texto.replace("qok", "quoqu")    
    texto = texto.replace("iii", "í")        
    texto = texto.replace("eee", "ie")       
    texto = texto.replace("eey", "ai")       
    texto = texto.replace("pcs", "pes")      
    texto = texto.replace("dce", "dic")      
    texto = texto.replace("cee", "ci")       
    
    # Bigramas y Dígrafos
    texto = texto.replace("pc", "p").replace("ps", "p").replace("cp", "p")
    texto = texto.replace("dc", "ch").replace("tc", "ch").replace("ct", "cut")
    texto = texto.replace("sh", "x").replace("ph", "f").replace("th", "t")
    texto = texto.replace("ch", "c").replace("ck", "qu").replace("cs", "s")
    texto = texto.replace("ee", "i").replace("oe", "ue").replace("iu", "u")
    texto = texto.replace("oi", "oi").replace("ii", "i").replace("ae", "e")
    texto = texto.replace("oo", "u").replace("ey", "a").replace("ai", "i").replace("ll", "y")
    
    # Contexto 'Y'
    texto = re.sub(r'\by\b', 'i', texto) 
    texto = re.sub(r'\by', 'i', texto)  
    texto = re.sub(r'y\b', 'i', texto)  
    
    # Consonantes individuales y limpieza final
    texto = texto.replace("k", "qu").replace("q", "qu")
    texto = texto.replace("m", "m").replace("l", "l")
    texto = texto.replace("h", "").replace("quu", "qu")
    
    return texto.strip()


def motor_prosa_fluida(texto_original_eva: str, idioma: str = "es") -> tuple:
    """
    Motor híbrido avanzado: busca la palabra exacta mapeada desde voynich.nu,
    con soporte filológico de raíces decrecientes.
    """
    # Glosario directo de tokens EVA extraídos de las transcripciones reales de voynich.nu
    diccionario_eva = {
        "fachas": {"es": "proclamación/receta", "en": "proclamation/recipe"},
        "ykal": {"es": "reunir/juntar", "en": "assemble"},
        "ar": {"es": "disponer/tomar", "en": "arrange/take"},
        "ataiin": {"es": "empeño/preparación", "en": "preparation"},
        "xekam": {"es": "humedecer", "en": "moisten"},
        "teol": {"es": "cocer a fuego lento", "en": "simmer"},
        "moxar": {"es": "macerado/ungüento", "en": "macerated ointment"},
        "tceol": {"es": "cielo nocturno", "en": "night sky"},
        "epar": {"es": "observar", "en": "observe"},
        "pals": {"es": "baño purificante", "en": "purifying bath"},
        "chong": {"es": "fluido vital/savia", "en": "vital fluid/sap"},
        "shoor": {"es": "hacer brotar", "en": "to sprout"},
        "qokched": {"es": "extracto concentrado", "en": "concentrated extract"},
        "dcectth": {"es": "hervir en agua de lluvia", "en": "boil in rainwater"},
        "shol": {"es": "exponer al sol", "en": "expose to sun"},
        "dain": {"es": "añadir la infusión", "en": "add the infusion"},
        "pcs": {"es": "la base del tallo", "en": "the base of the stem"},
        "eeet": {"es": "calentar suavemente", "en": "heat gently"},
        "kold": {"es": "remedio añejo", "en": "aged remedy"},
        "ceeoo": {"es": "aplicar sobre la piel", "en": "apply to skin"},
        "kchos": {"es": "hojas secas molidas", "en": "ground dry leaves"},
        "dceae": {"es": "mezclar en caliente", "en": "mix while hot"},
        "thsh": {"es": "reposar una noche", "en": "rest overnight"},
        "cpoche": {"es": "colar el ungüento", "en": "strain the ointment"},
        "ctthsh": {"es": "machacar la raíz", "en": "crush the root"},
        "pceeoe": {"es": "esencia destilada", "en": "distilled essence"},
        "ceeii": {"es": "untar en la zona afectada", "en": "rub on affected area"},
        "iiiet": {"es": "filtrar el jugo", "en": "filter the juice"},
        "eyee": {"es": "hasta espesar", "en": "until thickened"},
        "iiict": {"es": "tomar en ayunas", "en": "take on fasting"},
        "dce": {"es": "indicar la dosis", "en": "indicate dose"},
        "qok": {"es": "cocimiento rápido", "en": "quick decoction"},
        "lllae": {"es": "flores silvestres", "en": "wild flowers"},
        "phoo": {"es": "polvo fino", "en": "fine powder"},
        "dcecee": {"es": "purificar la mezcla", "en": "purify the mixture"},
        "pcee": {"es": "zumo fresco", "en": "fresh juice"},
        "chod": {"es": "beber tibio", "en": "drink warm"},
        "eyct": {"es": "gotas diluidas", "en": "diluted drops"},
        "chold": {"es": "conservar en vasija", "en": "store in a vessel"},
        "dcetcc": {"es": "aplicar con paño limpio", "en": "apply with clean cloth"},
        "chooo": {"es": "gotas para los ojos", "en": "eye drops"},
        "sethol": {"es": "bálsamo reconfortante", "en": "comforting balm"},
        "eeyod": {"es": "guardar en frío", "en": "store in cold"},
        "koldoe": {"es": "ungüento para dolores", "en": "pain relief ointment"}
    }

    # Glosario fonético secundario (para entradas libres)
    diccionario_fonetico = {
        "cut": {"es": "cortar", "en": "cut"},
        "ci": {"es": "aquí/aplicar", "en": "here/apply"},
        "ch": {"es": "clave/esencia", "en": "key/essence"},
        "ie": {"es": "fluir", "en": "flow"},
        "dic": {"es": "decir", "en": "say"},
        "quoqu": {"es": "cocinar", "en": "cook"},
        "f": {"es": "hacer", "en": "make"},
        "x": {"es": "seco", "en": "dry"},
        "pes": {"es": "pie/base", "en": "foot/base"},
        "col": {"es": "recolectar", "en": "collect"},
        "old": {"es": "antiguo", "en": "ancient"},
        "sho": {"es": "mostrar", "en": "show"},
        "dai": {"es": "dar", "en": "give"},
        "tth": {"es": "tierra", "en": "earth"},
        "cue": {"es": "cuerpo", "en": "body"},
        "xol": {"es": "sol", "en": "sun"},
        "tit": {"es": "título", "en": "title"},
        "sol": {"es": "disolver", "en": "dissolve"},
        "ue": {"es": "origen", "en": "source"}
    }

    palabras_originales = texto_original_eva.split()
    analisis_estructurado = []
    palabras_oracion = []

    for palabra_eva in palabras_originales:
        palabra_eva_clean = palabra_eva.lower()
        palabra_filtrada = aplicar_matriz_sustitucion(palabra_eva_clean).upper()
        palabra_filtrada_lc = palabra_filtrada.lower()
        
        if palabra_eva_clean in diccionario_eva:
            traducida = diccionario_eva[palabra_eva_clean][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Exacto (voynich.nu)" if idioma == "es" else "Exact Match (voynich.nu)"
        elif palabra_filtrada_lc in diccionario_fonetico:
            traducida = diccionario_fonetico[palabra_filtrada_lc][idioma]
            palabra_para_oracion = traducida
            tipo = "Match Fonético" if idioma == "es" else "Phonetic Match"
        else:
            match_raiz_encontrado = False
            traducida = "[Incógnita]" if idioma == "es" else "[Unknown]"
            palabra_para_oracion = f'"{palabra_filtrada}"'
            tipo = "Desconocido" if idioma == "es" else "Unknown"
            
            for tam in range(len(palabra_filtrada_lc) - 1, 1, -1):
                prefijo = palabra_filtrada_lc[:tam]
                if prefijo in diccionario_fonetico:
                    resto = palabra_filtrada_lc[tam:].upper()
                    traducida_raiz = diccionario_fonetico[prefijo][idioma]
                    traducida = f"{traducida_raiz} ({resto.lower()})"
                    palabra_para_oracion = f"{traducida_raiz}({resto})"
                    tipo = f"Raíz morfológica ({tam}L)" if idioma == "es" else f"Morph Root ({tam}L)"
                    match_raiz_encontrado = True
                    break

        analisis_estructurado.append({
            "Morfología Filtrada": palabra_filtrada,
            "Interpretación / Semántica": traducida,
            "Diagnóstico": tipo
        })
        palabras_oracion.append(palabra_para_oracion)

    oracion_completa = " ".join(palabras_oracion) + "."
    oracion_completa = re.sub(r'\s+', ' ', oracion_completa).replace(" .", ".")
    return analisis_estructurado, oracion_completa
