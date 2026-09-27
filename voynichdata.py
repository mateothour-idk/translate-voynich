# voynichdata.py

# Glosario con mapeo bilingüe nativo: (Clave Voynich, Español, Inglés)
glosario_inicial = [
    ("poisoda", "la planta medicinal (Pesota)", "the medicinal plant (Pesota)"),
    ("puí", "la planta", "the plant"),
    ("cuta", "la corteza", "the bark"),
    ("cutiy", "la corteza o piel", "the bark or skin"),
    ("podon", "la raíz o el pie", "the root or foot"),
    ("vetí", "maduro o viejo", "mature or old"),
    ("oarur", "el aroma", "the aroma"),
    ("odaur", "el olor", "the smell"),
    ("crofosodaur", "el aroma resinoso", "the resinous aroma"),
    ("sier", "las hojas dentadas", "the serrated leaves"),
    ("ciey", "la savia", "the sap"),
    ("quaur", "el agua caliente", "the hot water"),
    ("osain", "el aceite esencial", "the essential oil"),
    ("pain", "la pulpa o sustancia", "the pulp or substance"),
    ("oain", "el jugo", "the juice"),
    ("icios", "los vasos", "the vessels"),
    ("oiaj", "la esencia", "the essence"),
    ("cios", "los recipientes", "the containers"),
    ("ain", "el líquido", "the liquid"),
    ("oteroe", "el proceso", "the process"),
    ("aram", "el hornillo de bronce", "the bronze burner"),
    ("dalaiu", "destilar", "to distill"),
    ("ciodain", "los canales", "the channels"),
    ("aekiy", "la mezcla", "the mixture"),
    ("air", "el aire", "the air"),
    ("soar", "el vapor elevado", "the rising vapor"),
    ("oas", "la vasija", "the vessel"),
    ("raur", "la raíz", "the root"),
    ("otiy", "la maceración", "the maceration"),
    ("oeteodi", "el reposo", "the rest"),
    ("daur", "la duración del ciclo", "the cycle duration"),
    ("odotoí", "la rueda del año", "the wheel of the year"),
    ("doror", "el nacimiento del astro", "the birth of the star"),
    ("quidí", "diariamente", "daily"),
    ("quoquidí", "cada día", "every day"),
    ("chidí", "canalizar", "to channel"),
    ("tiodau", "en el tiempo determinado", "at the determined time"),
    ("itioei", "la estación", "the season"),
    ("siy", "si se presenta", "if it occurs"),
    ("pair", "por medio de", "by means of"),
    ("dais", "se debe aplicar", "it must be applied"),
    ("dair", "dar", "to give"),
    ("dam", "entregar", "to deliver"),
    ("quioquey", "y el corazón", "and the heart"),
    ("okeody", "lo que dicta el tratado", "what the treaty dictates"),
    ("quiodal", "el texto o contenido", "the text or content")
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
    
    # Rellenar automáticamente los 240 folios estructurales
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
