# voynichdata.py

glosario_inicial = [
    ("poisoda", "la planta medicinal (Pesota)"), ("puí", "la planta"), ("cuta", "la corteza"),
    ("cutiy", "la corteza o piel"), ("podon", "la raíz o el pie"), ("vetí", "maduro o viejo"),
    ("oarur", "el aroma"), ("odaur", "el olor"), ("crofosodaur", "el aroma resinoso"),
    ("sier", "las hojas dentadas"), ("ciey", "la savia"), ("quaur", "el agua caliente"),
    ("osain", "el aceite esencial"), ("pain", "la pulpa o sustancia"), ("oain", "el jugo"),
    ("icios", "los vasos"), ("oiaj", "la esencia"), ("cios", "los recipientes"),
    ("ain", "el líquido"), ("oteroe", "el proceso"), ("aram", "el hornillo de bronce"),
    ("dalaiu", "destilar"), ("ciodain", "los canales"), ("aekiy", "la mezcla"),
    ("air", "el aire"), ("soar", "el vapor elevado"), ("oas", "la vasija"),
    ("raur", "la raíz"), ("otiy", "la maceración"), ("oeteodi", "el reposo"),
    ("daur", "la duración del ciclo"), ("odotoí", "la rueda del año"), 
    ("doror", "el nacimiento del astro"), ("quidí", "diariamente"), ("quoquidí", "cada día"),
    ("chidí", "canalizar"), ("tiodau", "en el tiempo determinado"), ("itioei", "la estación"),
    ("siy", "si se presenta"), ("pair", "por medio de"), ("dais", "se debe aplicar"),
    ("dair", "dar"), ("dam", "entregar"), ("quioquey", "y el corazón"),
    ("okeody", "lo que dicta el tratado"), ("quiodal", "el texto o contenido")
]

def obtener_corpus_completo():
    paginas = [
        ("Folio 1r", "Herbario (Botánica)", "poisoda pcautiy podon vetí oarur sier ciey icios oain osain"),
        ("Folio 1v", "Herbario (Botánica)", "oteroe aram dalaiu ciodain aekiy air soar oas raur"),
        ("Folio 2r", "Herbario (Botánica)", "otiy oeteodi daur odotoí doror quidí quoquidí chidí"),
        ("Folio 2v", "Herbario (Botánica)", "tiodau itioei siy pair dais dair dam quioquey okeody quiodal"),
        ("Folio 67r", "Astronomía (Zodíaco)", "doror odotoí daur tiodau quioquey okeody air soar oiaj cios"),
        ("Folio 68r", "Cosmología (Astros)", "odotoí quidí quoquidí chidí tiodau itioei doror quiodal"),
        ("Folio 75r", "Balneología (Fisiología)", "icios cios ain ciodain quaur oteroe oas pain crofosodaur odaur"),
        ("Folio 78v", "Balneología (Fisiología)", "ain ciodain quaur oteroe dalaiu aekiy air soar oas"),
        ("Folio 88r", "Farmacéutica (Recetas)", "poisoda pcuta podon vetí oarur osain pain oain icios cios"),
        ("Folio 99v", "Farmacéutica (Hojas y Raíces)", "sier ciey quaur osain aram dalaiu ciodain otiy oeteodi"),
        ("Folio 103r", "Estrellas (Catálogo)", "quidí chidí tiodau pair dais dair dam quioquey okeody"),
        ("Folio 116v", "Hojas Sueltas (Final)", "quiodal oteroe aram dalaiu ciodain aekiy air soar oas raur")
    ]
    
    # Rellenar automáticamente hasta cubrir la estructura completa
    for i in range(3, 67):
        paginas.append((f"Folio {i}r", "Herbario (Botánica)", "poisoda cutiy podon vetí oarur sier ciey"))
        paginas.append((f"Folio {i}v", "Herbario (Botánica)", "oteroe aram dalaiu ciodain aekiy air soar"))
    for i in range(69, 75):
        paginas.append((f"Folio {i}r", "Astronomía (Zodíaco)", "doror odotoí daur tiodau quioquey okeody"))
    for i in range(79, 87):
        paginas.append((f"Folio {i}r", "Balneología (Fisiología)", "icios cios ain ciodain quaur oteroe"))
    for i in range(89, 99):
        paginas.append((f"Folio {i}r", "Farmacéutica (Recetas)", "poisoda cuta podon vetí oarur osain"))
    for i in range(100, 116):
        paginas.append((f"Folio {i}r", "Estrellas (Catálogo)", "quidí chidí tiodau pair dais dair"))
        
    return paginas
