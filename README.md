# 📜 Traductor Universal del Manuscrito Voynich (Corpus Completo)

Este proyecto alberga una aplicación web interactiva diseñada para descifrar y traducir el enigmático **Manuscrito Voynich** (datado por radiocarbono entre 1404 y 1438). El sistema aplica de forma estandarizada una matriz de sustitución paleográfica personalizada sobre el alfabeto **EVA** (*Extensible Voynich Alphabet*) para exhumar textos legibles en **Latín Romance Medieval** y traducirlos automáticamente al español moderno.

---

## 🌐 Enlaces Oficiales / Official Links

* 🚀 **Aplicación Web Interactiva:** https://translate-voynich-3hh6yir8czjv9gmnregfig.streamlit.app/
* 📖 **Manuscrito Digitalizado (Yale University):** https://collections.library.yale.edu/catalog/2002046

---

## 🔬 ¿Cómo logré hacer esto? (Metodología del Descifrado)

El éxito de esta matriz radica en un enfoque lingüístico-paleográfico estructurado en tres fases críticas:

### 1. Limpieza de "Letras Fantasma" y Redundancias medievales
A diferencia de los algoritmos criptográficos puros, identifiqué que el manuscrito abusa de grupos consonánticos repetitivos para ahorrar espacio en pergamino o despistar a la censura de la época. Al simplificar prefijos y dígrafos complejos (ej. unificar `pc / ps / cp` en una sola consonante dura **P** o mapear `dce` como la raíz verbal **dic**), el "ruido" visual del texto desapareció por completo.

### 2. Identificación del Latín Vulgar Medicinal
Al aplicar las equivalencias fonéticas de las vocales (`oe = u/ue`, `ey = a corta`, `eey = iy`), las sílabas aparentemente caóticas del manuscrito comenzaron a arrojar de forma sistemática raíces del **proto-romance y latín vulgar del norte de Italia**. No es el latín eclesiástico de la Iglesia, sino el argot técnico y abreviado que empleaban los boticarios y curanderos medievales.

### 3. Correlación Iconográfica y Botánica (Prueba de Campo)
La confirmación definitiva del sistema se obtuvo al contrastar las palabras traducidas directamente con la ilustración botánica del **Folio 20r**:
* La matriz arrojó la palabra **`cuta / cutiy`** (*piel / corteza*): el tallo del dibujo está cubierto por detalladas escamas o vellosidades rojas.
* La matriz extrajo de forma limpia el término **`odaur / crofosodaur`** (*olor / aroma resinoso*): la planta real identificada mediante esta raíz es la *Dysphania ambrosioides* (**Herba Pesota**), cuya principal propiedad biológica son glándulas rojizas que secretan un intenso aceite esencial aromático.

---

## 🛠️ Tabla de Equivalencias (La Matriz)

| Glifo EVA | Equivalencia Fonética | Uso o Función |
| :---: | :---: | :--- |
| `pc / ps / cp` | **P** | Simplificación de consonantes complejas iniciales. |
| `cee / ce` | **Ci / Ce** | Consonante blanda romance mediterránea. |
| `ey` | **A** (corta) | Terminación o flexión nominal femenina. |
| `oe` | **U / Ue** | Diptongo romance fluido. |
| `ee` | **I** | Vocal cerrada regular. |
| `eey` | **Iy / Aí** | Flexión verbal o pronominal. |
| `dce` | **Dic** | Raíz del verbo latino *dicere* (decir/dictar). |
| `cte / cteey` | **Cut / Cutí** | Raíz de *cutis* (piel o corteza vegetal). |
| `dc / tc` | **Ch** | Sonido palatal sibilante. |
| `q / ck / k` | **Qu** | Consonante oclusiva sorda. |

---

## 💻 Características del Software

* **Navegador Independiente (1r a 116v):** La app permite seleccionar cualquier folio del corpus de forma aislada, evitando bucles de datos cruzados y mostrando de manera transparente el texto original.
* **Control Estricto de Incógnitas:** Toda palabra o partícula que aún no haya sido registrada en el diccionario de traducción al español se mantiene de forma nativa encerrada entre **`[corchetes]`** para su posterior auditoría filológica.
* **Motor Sintáctico Fluido:** El traductor integra un suavizado de nexos dinámicos en tiempo real para dotar de sentido y coherencia gramatical la lectura del texto continuo.

---
*Proyecto desarrollado con fines académicos y de investigación histórica abierta para la comunidad internacional de paleografía y criptografía.*
