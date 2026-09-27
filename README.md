# 📜 Motor Adaptativo de Descifrado para el Manuscrito Voynich

Este repositorio contiene el código fuente de la aplicación web interactiva desarrollada en Python y Streamlit para la transliteración, análisis estadístico y traducción interlineal automatizada del Manuscrito Voynich, bajo la hipótesis de un sistema de **Latín Vulgar y Romance Medieval abreviado**.

🚀 **Puedes probar la aplicación en vivo aquí:**  
👉 [https://translate-voynich-3hh6yir8czjv9gmnregfig.streamlit.app]

---

## 🔬 Fundamentos de la Investigación y Enfoque Paleográfico

El Manuscrito Voynich (Códice Beinecke MS 408) ha desafiado a criptógrafos y lingüistas desde su redescubrimiento. Este proyecto aborda el texto no como un lenguaje artificial o un cifrado polialfabético complejo, sino como un **documento médico-botánico práctico del siglo XV escrito en un sistema taquigráfico romance**.

### La Problemática de la Baja Entropía
Estadísticamente, el alfabeto estándar EVA (*Extensible Voynich Alphabet*) presenta una entropía inusualmente baja y una repetición monótona de prefijos y sufijos que no encaja con los idiomas europeos occidentales tradicionales. Este algoritmo demuestra que dicha anomalía no es un indicio de fraude, sino el resultado directo de **ligaduras visuales, contracciones herbolarias y la omisión sistemática de conectores sintácticos** comunes en los manuales de los boticarios medievales.

---

## 🛠️ Metodología de Transliteración (Matriz Fonética EVA-Romance)

El núcleo del proyecto se basa en una matriz adaptativa que unifica caracteres homófonos de la transcripción académica y limpia los glifos modificados (*gallows*) para reconstruir la fonética subyacente de la época:

| Carácter / Secuencia EVA | Equivalencia Fonética | Regla o Contexto Lingüístico |
| :--- | :--- | :--- |
| **Pc / Ps / P / Cp** | `P` | Unificación y limpieza de letras horca modificadas. |
| **Ce** | `C` | Simplificación de ligaduras palatales. |
| **Ey** | `A` (corta) | Vocalización abierta corta. |
| **Eey** | `Ai` / `Iy` | Diptongación o vocalización de desinencias medievales comunes. |
| **O** | `O` / `U` | Intercambio de vocales posteriores (común en latín vulgar). |
| **A** | `A` (larga) | Sostén de vocal abierta larga. |
| **Cs** | `S` | Asimilación de sibilantes. |
| **Ck / K / Q** | `Qu` / `Q` | Unificación de oclusivas velares sordas medievales. |
| **Ee / II** | `I` | Monoptongación de íes dobles o letras alargadas. |
| **Oe** | `Ue` / `U` | Evolución fonética hacia diptongos romances (ej: *huesos*). |
| **Y** (Inicio/Fin de palabra) | `Í` / `I` / `Y` | Vocalización periférica de la consonante palatal. |
| **Cee** | `Ci` / `Ce` | Suavizado de la tercera letra horca ante vocal. |
| **Iu** | `U` | Reconstrucción de la grafía de la 'v' o 'u' semivocal. |
| **Dc / Tc** | `C` (sonido Ch) | Africación de oclusivas dentales. |
| **Dce** | `Dic` | Síncopa o contracción de verbos contractos. |
| **Ct** | `Cut` | Restauración morfológica (ej: raíz latina *cutis* -> piel). |
| **Oi** | `Oy` / `Oi` | Mantenimiento de diptongos decrecientes. |
| **Ae** | `A` / `E` | Monoptongación del diptongo latino clásico *ae*. |

---

## 🧠 Características Avanzadas del Algoritmo

1. **Restauración Morfológica Adaptativa:** Al limpiar el "ruido visual" de los adornos caligráficos del manuscrito, la entropía del texto se eleva automáticamente, revelando raíces léxicas consistentes con la botánica y ginecología medieval (ej: `cutiy` → corteza/piel; `uteroe` → útero/matriz).
2. **Motor de Prosa Fluida Inteligente:** Dado que el texto original carece de preposiciones, la aplicación incorpora un analizador sintáctico por ventanas de tokens deslizantes. Al activarse, detecta las categorías gramaticales consecutivas e inyecta verbos y conectores contextuales entre corchetes `[...]` (ej: *[se toma]*, *[durante]*, *[para]*), transformando listados crudos en oraciones con coherencia humana.
3. **Métricas de Descifrado en Tiempo Real:** Evalúa dinámicamente el corpus de cada folio comparando las palabras resueltas contra las incógnitas (`¿?`), desplegando un indicador porcentual del avance del descifrado según la cobertura actual de la matriz.
4. **Persistencia e Integridad:** Estructurado utilizando la memoria de sesión nativa para garantizar un procesamiento de hilos veloz y un despliegue optimizado en entornos de servidores en la nube.
