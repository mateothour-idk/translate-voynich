# --- EN TU ARCHIVO: voynichdatos.py ---
# Mantén DICCIONARIO_ES y DICCIONARIO_EN exactamente como los tenías.

CORPUS_MANUSCRITO = {}

def cargar_todas_las_paginas_reales():
    """
    Lee el archivo completo del manuscrito en EVA y organiza 
    todas las páginas de forma dinámica en el diccionario CORPUS_MANUSCRITO.
    """
    global CORPUS_MANUSCRITO
    CORPUS_MANUSCRITO.clear()
    
    try:
        with open("voynich_completo.txt", "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                # Ignorar comentarios o líneas vacías comunes en transcripciones oficiales
                if not linea or linea.startswith("#") or linea.startswith("%"):
                    continue
                
                # Las líneas oficiales suelen empezar con el identificador de folio (ej: <f1r.1> texto)
                # Separamos el identificador del texto de la línea
                partes = linea.split(maxsplit=1)
                if len(partes) < 2:
                    continue
                    
                identificador, texto_eva = partes[0], partes[1]
                
                # Limpiar el identificador para extraer la página (ej: "1r", "2v", "102r")
                # Buscamos patrones comunes como f1r, 1r, f001r
                match = re.search(r'(\d+[rv])', identificador)
                if match:
                    folio_key = match.group(1)
                else:
                    continue
                
                # Limpiar caracteres de control o raros del texto EVA de transcripción original
                texto_eva_limpio = re.sub(r'=[^ ]*', '', texto_eva)  # Quita ligaduras alternativas
                texto_eva_limpio = re.sub(r'[*.,!?]', '', texto_eva_limpio) # Quita marcas de daño
                
                if folio_key not in CORPUS_MANUSCRITO:
                    CORPUS_MANUSCRITO[folio_key] = []
                
                if texto_eva_limpio.strip():
                    CORPUS_MANUSCRITO[folio_key].append(texto_eva_limpio.strip())
    except FileNotFoundError:
        # Fallback por si el archivo no está en local durante pruebas básicas
        CORPUS_MANUSCRITO["1r"] = ["pshoey cttey oaror psoisoda kedy ceon ceey qokedy"]
