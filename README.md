# 📜 Motor Adaptativo de Descifrado para el Manuscrito Voynich

Este repositorio contiene el código fuente de la aplicación web interactiva desarrollada en Python y Streamlit para la transliteración, análisis estadístico y traducción interlineal automatizada del Manuscrito Voynich, bajo la hipótesis de un sistema de **Latín Vulgar y Romance Medieval abreviado**.

🚀 **Puedes probar la aplicación en vivo aquí:**  
👉 [https://translate-voynich-3hh6yir8czjv9gmnregfig.streamlit.app/](https://translate-voynich-3hh6yir8czjv9gmnregfig.streamlit.app/)

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

## 🔍 Análisis Expandido de Reglas Fonéticas Clave

Para comprender la efectividad del algoritmo, es necesario profundizar en la lógica filológica aplicada a los glifos más problemáticos del manuscrito:

* **Desmitificación de las Letras Horca (`Pc / Ps / P / Cp` ➔ `P`):** La criptografía tradicional asume que las variaciones de bucles en los caracteres altos (*gallows*) representan letras o números diferentes. Nuestro análisis demuestra que son meras variaciones caligráficas decorativas de un mismo escriba. Al unificarlas en la consonante oclusiva bilabial sorda `P`, el algoritmo reconstruye raíces médicas esenciales como `pheador` ➔ *pedur/pedor* (relacionado con el pecho o la base del tallo).
* **El Fenómeno del Diptongo Romance (`Oe` ➔ `Ue / U`):** Una de las firmas morfológicas del castellano y otros romances tempranos es la diptongación de las vocales breves latinas (ej: del latín *os* u *ossu* hacia el romance *ueso / hueso*). La matriz procesa la secuencia EVA `oe` bajo esta regla de transición, permitiendo que oraciones botánicas inconexas revelen de inmediato aplicaciones directas para el tratamiento de los huesos humanos.
* **Restauración por Elisión de Oclusivas (`Ct` ➔ `Cut`):** Los copistas medievales utilizaban la taquigrafía para ahorrar espacio en pergaminos costosos, eliminando vocales intermedias átonas. Al interceptar la raíz abreviada `ct` y restaurarla sistemáticamente como `cut`, el motor automatiza el hallazgo de la raíz botánica *cutis* (piel o corteza exterior), resolviendo la semántica de folios herbolarios críticos como el Folio 33v (el Girasol).
* **Vocalización Periférica e Intercambio Posterior (`O` ➔ `O / U` e `Y` ➔ `Í / I / Y`):** El latín vulgar difuminó la barrera entre las vocales posteriores largas y cortas (`o` y `u`), un fenómeno que el manuscrito arrastra de forma consistente. La matriz dota al motor de la flexibilidad necesaria para oscilar fonéticamente entre ambas, logrando estabilizar cierres de palabras monótonas en desinencias romances legibles.

---

## 🧠 Características Avanzadas del Algoritmo

1. **Restauración Morfológica Adaptativa:** Al limpiar el "ruido visual" de los adornos caligráficos del manuscrito, la entropía del texto se eleva automáticamente, revelando raíces léxicas consistentes con la botánica y ginecología medieval.
2. **Motor de Prosa Fluida Inteligente:** Dado que el texto original carece de preposiciones, la aplicación incorpora un analizador sintáctico por ventanas de tokens deslizantes. Al activarse, detecta las categorías gramaticales consecutivas e inyecta verbos y conectores contextuales entre corchetes `[...]` (ej: *[se toma]*, *[durante]*, *[para]*), transformando listados crudos en oraciones con coherencia humana.
3. **Métricas de Descifrado en Tiempo Real:** Evalúa dinámicamente el corpus de cada folio comparando las palabras resueltas contra las incógnitas (`¿?`), desplegando un indicador porcentual del avance del descifrado según la cobertura actual de la matriz.
4. **Persistencia e Integridad:** Estructurado utilizando la memoria de sesión nativa para garantizar un procesamiento de hilos veloz y un despliegue optimizado en entornos de servidores en la nube.
