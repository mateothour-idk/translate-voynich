# ==========================================
# REGLAS ACTUALIZADAS Y MOTOR EN voynichdatos.py
# ==========================================

SUSTITUCION_GLIFOS = [
    ("quoqu", "quoqu"), ("qok", "quoqu"), ("pcee", "pi"), ("eeey", "iey"),
    ("eceo", "issimus"), ("pcs", "pes"), ("dce", "dic"), ("cee", "ci"),
    ("pdr", "pedr"), ("eat", "it"), ("tcs", "tes"), ("tce", "tic"),
    ("eee", "ei"), ("eey", "ai"), ("iii", "í"), ("pc", "p"), ("ps", "p"),
    ("cp", "p"), ("dc", "ch"), ("tc", "ch"), ("ct", "cut"), ("ii", "i"),
    ("oo", "u"), ("ll", "y"), ("tt", "t"), ("ts", "s"), ("ph", "f"),
    ("th", "t"), ("ch", "c"), ("oe", "ue"), ("ey", "a"), ("ck", "qu"),
    ("lf", "lef"), ("el", "l"), ("quo", "cuo"),
    # --- Nuevas reglas para glifos complejos tipo 'shk' ---
    ("shk", "sc"),  # shkcor -> sccor -> sc-orarius
    ("sh", "s"),    # Glifo Bench alto solo
    ("k", "c")      # Glifo Gallows corto solo
]

def descomponer_y_traducir_glifo(palabra_cruda):
    raiz_restante = palabra_cruda.lower().strip()
    prefijo_trad = ""
    sufijo_trad = ""

    # Extraer Prefijo por el inicio (Izquierda)
    for key, val in PREFIJOS_LISTA:
        if raiz_restante.startswith(key):
            prefijo_trad = val
            raiz_restante = raiz_restante[len(key):]
            break

    # Extraer Sufijo por el final (Derecha)
    for key, val in SUFIJOS_LISTA:
        if raiz_restante.endswith(key):
            sufijo_trad = val
            raiz_restante = raiz_restante[:-len(key)] if len(key) > 0 else raiz_restante
            break

    # Buscar Raíz Directa o aplicar cambios fonéticos
    if raiz_restante in RAICES_DIRECTAS:
        raiz_trad = RAICES_DIRECTAS[raiz_restante]
    else:
        fon = raiz_restante
        for glifo, reemplazo in SUSTITUCION_GLIFOS:
            if glifo in fon:
                if glifo == "ey" and "eey" in raiz_restante:
                    continue
                fon = fon.replace(glifo, reemplazo)
        raiz_trad = fon

    # Devolvemos los componentes por separado para que el combinador inteligente los analice
    return prefijo_trad, raiz_trad, sufijo_trad
# ==========================================
# NUEVO MOTOR COMBINATORIO EN voynichapp.py
# ==========================================

def traducir_a_romance(texto):
    dicc_activo = voynichdatos.DICCIONARIO_ES if idioma == "Español" else voynichdatos.DICCIONARIO_EN
    texto_limpio = texto.lower().replace('.', ' ')
    texto_limpio = re.sub(r'[^a-z\s]', '', texto_limpio)
    palabras = texto_limpio.split()
    
    fon_l = []  # Almacena la estructura morfológica reconstruida
    trad_l = [] # Almacena la traducción literal combinada
    
    # Diccionario inverso auxiliar de traducción de morfemas sueltos
    significados_morfemas = {
        # Prefijos
        "trans": "a través de / trans-", "sub": "bajo / sub-", "per": "completamente / per-",
        "re": "reiteración / re-", "com": "junto con / con-", "con": "asociado a / con-",
        "super": "en exceso / super-", "in": "hacia dentro / in-", "por": "en favor de / por-",
        "contra": "en oposición / contra-", "de": "derivado de / de-", "quot": "proporción de / quot-",
        # Sufijos
        "issimus": " en grado sumo / -ísimo", "escere": " en desarrollo / -ecer", 
        "ensis": " perteneciente a / -ense", "tatem": " la cualidad de / -dad", 
        "arius": " relativo a / -ario", "ticius": " de naturaleza / -ticio", 
        "icculum": " diminutivo de / -ículo", "tia": " el estado de / -cia", 
        "tor": " el agente que / -dor", "sor": " el ejecutor de / -sor", 
        "osus": " abundante en / -oso", "ittus": " pequeño / -ito", 
        "onus": " protector de / -ón", "io": " el efecto de / -ción", "iscus": " propio de / -isco"
    } if idioma == "Español" else {
        "trans": "across / trans-", "sub": "under / sub-", "per": "thoroughly / per-",
        "re": "again / re-", "com": "together with / com-", "con": "associated with / con-",
        "super": "excessively / super-", "in": "inside / in-", "por": "on behalf of / por-",
        "contra": "against / contra-", "de": "derived from / de-", "quot": "proportion of / quot-",
        "issimus": "extremely / -issimus", "escere": "developing / -esce", 
        "ensis": "belonging to / -ensis", "tatem": "quality of / -ty", 
        "arius": "relative to / -ary", "ticius": "nature of / -ticius", 
        "icculum": "small / -cule", "tia": "state of / -ce", 
        "tor": "agent of / -tor", "sor": "executor of / -sor", 
        "osus": "abundant in / -ous", "ittus": "little / -ite", 
        "onus": "protector of / -on", "io": "effect of / -tion", "iscus": "characteristic of / -ish"
    }

    for pal in palabras:
        if not pal.strip() or len(pal) <= 1: 
            continue
        
        # 1. Obtener la descomposición de morfemas limpia desde voynichdatos
        p_fix, r_fix, s_fix = voynichdatos.descomponer_y_traducir_glifo(pal)
        forma_romance_completa = f"{p_fix}{r_fix}{s_fix}"
        fon_l.append(forma_romance_completa)
        
        # 2. INTELIGENCIA COMBINATORIA LITERAL (Opción 2)
        # Caso A: La palabra completa está definida en el diccionario histórico
        if pal in dicc_activo:
            significado = dicc_activo[pal]
        elif forma_romance_completa in dicc_activo:
            significado = dicc_activo[forma_romance_completa]
        
        # Caso B: No existe completa -> Descomposición semántica literal por morfema
        else:
            partes_traducidas = []
            
            # Traducir Prefijo si existe
            if p_fix and p_fix in significados_morfemas:
                partes_traducidas.append(significados_morfemas[p_fix])
            
            # Traducir Raíz (busca si la raíz resultante existe en el diccionario botánico)
            if r_fix:
                if r_fix in dicc_activo:
                    partes_traducidas.append(dicc_activo[r_fix])
                else:
                    partes_traducidas.append(f"[{r_fix}]") # Muestra la raíz fonética si es nueva
            
            # Traducir Sufijo si existe
            if s_fix and s_fix in significados_morfemas:
                partes_traducidas.append(significados_morfemas[s_fix])
            
            # Combinación y ensamblaje final de significados
            if partes_traducidas:
                significado = " + ".join(partes_traducidas)
            else:
                significado = f"[{forma_romance_completa}]"
                
        trad_l.append(significado)
        
    return " ".join(fon_l), " ".join(trad_l)
