def aplicar_matriz_sustitucion(texto_eva: str) -> str:
    """
    Aplica las reglas de sustitución paleográfica al texto EVA de forma segura.
    Ajustado para que 'iii' genere 'ee' y luego se re-translitere recursivamente 
    a 'i' según la regla de la secuencia (iiiet -> eet -> it).
    """
    if not texto_eva:
        return ""
        
    # --- FILTRO CRÍTICO: LIMPIEZA DE RUIDO ACADÉMICO ---
    texto = texto_eva.lower()
    texto = re.sub(r'[0-9\*\-\/\=\+\%\&\$\#\_\@]', ' ', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    
    # --- BUCLE DE RETRANSLITERACIÓN RECURSIVA ---
    while True:
        texto_anterior = texto  # Guardamos el estado anterior para comparar cambios
        
        # --- 1. REGLAS DE 4 CARACTERES (Tetragramas) ---
        texto = texto.replace("pcee", "pi")
        texto = texto.replace("qok", "quoqu")
        
        # --- 2. REGLAS DE 3 CARACTERES AJUSTADAS (Trigramas) ---
        # Cambiado 'iii' -> 'ee' para permitir la evolución recursiva que pediste
        texto = texto.replace("iii", "ee")
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
        # Aquí es donde 'eet' se convierte en 'it' en la segunda pasada del bucle
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
        texto = texto.replace("r", "r")       
        texto = texto.replace("n", "n")       
        texto = texto.replace("o", "o")       
        texto = texto.replace("a", "a")       
        
        # --- 6. LIMPIEZA TOTAL DE HACHES (H) HUÉRFANAS ---
        texto = texto.replace("h", "")
        texto = texto.replace("quu", "qu")
        
        # Condición de parada si ya no hay más cambios en la cadena
        if texto == texto_anterior:
            break
            
    return texto.strip()
