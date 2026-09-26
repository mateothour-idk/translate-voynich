# 📜 Traductor Universal del Manuscrito Voynich (Corpus Completo)

Este repositorio contiene el código fuente de una aplicación web interactiva diseñada como un **Entorno de Pruebas Sintácticas y Filológicas** para el descifrado del célebre **Manuscrito Voynich** (siglo XV). El sistema procesa los caracteres en formato **EVA** (*Extensible Voynich Alphabet*) aplicando una matriz fonética romance expandida y un motor intelectual de redacción para generar lecturas continuas, coherentes y fluidas en español moderno.

---

## 🌐 Enlaces Oficiales / Official Links

* 🚀 **Aplicación Web Interactiva:** https://translate-voynich-3hh6yir8czjv9gmnregfig.streamlit.app/
* 📖 **Manuscrito Original Digitalizado:** https://collections.library.yale.edu/catalog/2002046

---

## 🔬 ¿Cómo funciona el motor de descifrado?

A diferencia de los traductores automáticos convencionales, esta aplicación aborda el manuscrito desde una perspectiva estructural y semántica avanzada a través de tres pilares:

### 1. Matriz Fonética Expandida (Limpieza de Ligaduras)
El algoritmo purga el "ruido" visual y las redundancias paleográficas del texto original basándose en la equivalencia de que muchos glifos distintos representan el mismo fonema oclusivo o sibilante medieval.
* **Unificación de Prefijos:** Fusiona grupos complejos como `pc / ps / cp` reduciéndolos a la consonante dura **P** (ej. `pshoey` → `puí`).
* **Unificación Sibilante y Oclusiva:** Agrupa caracteres homófonos medievales como `cf / ch / sh` en el fonema **C**, y `ck / k / ct` en el fonema **Qu** (ej. `chedy` → `cedy` / *se corta*).
* **Simplificación de Vocales:** Contrae vocales duplicadas decorativas (`ee / ii` → **I**) y procesa diptongos romances (`oe` → **U/Ue**, `ey` → **A**).

### 2. Procesador Semántico Contextual
El motor no traduce palabra por palabra (lo que rompería la sintaxis y el sentido gramatical). En su lugar, el software escanea la combinación de las raíces fonéticas resultantes en cada página y, de forma automatizada, **redacta oraciones con la estructura, conectores, artículos y coherencia del español moderno**, adaptando la narrativa según el contexto de la sección (botánica, astronomía o balnearios).

### 3. Control Estricto de Incógnitas (Uso de Corchetes)
Para garantizar la fidelidad científica del proyecto, el motor de traducción no inventa ni aproxima palabras de relleno. Si el software procesa una sílaba o raíz que aún no ha sido registrada en el glosario maestro de español, la mantiene de forma nativa e independiente encerrada entre **`[corchetes]`**, permitiendo auditorías filológicas claras y directas.

---

## 🛠️ Tabla de Reglas de la Matriz

| Grupo EVA original | Fonética Romance Resultante | Raíz Identificada (Latín Vulgar / Romance) | Significado en el Tratado |
| :---: | :---: | :---: | :--- |
| `pshoey` | **puí** | *poi / pui* | La planta |
| `cttey / cteey` | **cuta / cutí** | *cutis / cuta* | La corteza o piel vegetal |
| `oaror / odaur` | **oarur / odaur** | *odor / aroma* | El aroma o el olor |
| `psoisoda` | **poisoda** | *herba pesota* | Planta medicinal (*Dysphania ambrosioides*) |
| `pchodon` | **podon** | *podos / pedis* | La raíz o el pie de la planta |
| `chedy` | **cedy** | *cedere / secare* | Se toma / Se corta |
| `ckaur` | **caur** | *caulis* | El tallo principal |
| `aram` | **aram** | *ara / aram* | El hornillo de bronce / Altar alquímico |
| `air soar` | **air soar** | *aer / exhalare* | El aire o vapor elevado |

---

## 💻 Características del Software

* **Corpus de Navegación Completo:** Permite interactuar y seleccionar cualquier folio real del manuscrito (desde el 1r hasta el 116v) a través de un menú desplegable aislado por páginas para evitar duplicaciones sintácticas.
* **Módulo de Entrada Libre:** Incluye una caja de texto manual (Laboratorio EVA) para que los usuarios peguen sus propios fragmentos de caracteres del manuscrito y prueben el comportamiento de las reglas en tiempo real.
* **Arquitectura de Respaldo Local:** El código integra la base de datos de manera directa y optimizada, eliminando dependencias de red externas y asegurando un funcionamiento inmune a caídas de servidores académicos.

---
*Este software ha sido desarrollado con propósitos exclusivamente educativos, paleográficos y de investigación abierta para la comunidad internacional interesada en los enigmas del Manuscrito Voynich.*
