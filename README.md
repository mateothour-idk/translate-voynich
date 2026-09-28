# 📜 Intérprete Analítico y Adaptativo del Manuscrito Voynich

Una suite de criptoanálisis paleográfico y traducción automatizada desarrollada para decodificar el corpus completo del *Manuscrito Voynich* (transcrito bajo el estándar EVA). El sistema utiliza un pipeline heurístico de reducción silábica, unificación de ligaduras medievales y un motor de segmentación sintáctica para reconstruir prosa romance y latín vulgar de forma fluida.

---

## 🚀 Características Clave

* **Pipeline de Sustitución Paleográfica de 6 Fases:** Reducción estructurada y determinista de caracteres complejos ordenada estrictamente por longitud de n-gramas.
* **Segmentador de *Scriptura Continua*:** Separación inteligente y dinámica de términos compuestos largos (`diccutt` ➔ `dic` + `cut`) para revelar significados ocultos fusionados por el escriba.
* **Motor Bilingüe Adaptativo:** Traducción contextual simultánea orientada a raíces etimológicas en Español (ES) e Inglés (EN).
* **Matriz Tabular Scannable:** Interfaz en pantalla ancha con desgloses detallados mediante tablas y análisis estadísticos de tasas de descifrado en tiempo real.
* **Autónomo e Independiente de Red:** Base de datos unificada del manuscrito indexada directamente en memoria para mitigar bloqueos por firewalls (CORS/406).

---

## 🧪 Matriz Estabilizada de Sustitución Fonética

El núcleo algorítmico aplica una reducción unificada de glifos orientada a la evolución lingüística del latín vulgar hacia las lenguas romances medievales, mitigando redundancias caligráficas (como el bug de la doble vocal `quu`):

### 🔄 Tabla de Equivalencias Críticas (Orden de Ejecución Coherente)

| Glifo EVA | Fonema Equivalente | Criterio de Coherencia Lingüística |
| :--- | :--- | :--- |
| **PCEE / QOK** | `pi` / `quoqu` | Tetragramas estables y prefijos de cocimiento o acción. |
| **III / PCS** | `í` / `pes` | Trigramas unificados en íes largas y raíces podales/soporte. |
| **EEE / EEY** | `ie` / `ai` | Diptongación romance regular (Evolución romance común / Diptongo estable). |
| **DC / TC** | `ch` | Glifos compuestos africados palatales con sonido de Ch. |
| **CT / PH** | `cut` / `f` | Raíces de incisión/corte y fricativa sorda para la *f* latina. |
| **CH / OE / AE** | `c` / `ue` / `e` | Monoptongación del latín vulgar y diptongos romances (Ej: *huevo*/*rueda*). |
| **OO / EY / AI** | `u` / `a` / `i` | Normalización de vocales cortas, largas y cierres vocálicos (Ai = I). |
| **Y** *(extremos)* | `i` | Posicionamiento de sibilantes/semivocales aisladas al inicio o final. |
| **Q / K / CK** | `qu` | Reestructuración de oclusivas velares sordas en posición final. |
| **H** *(huérfanas)* | *(Eliminado)* | Limpieza total de mudez o trazos decorativos caligráficos descolgados. |

---

## 🛠️ Arquitectura del Repositorio

El proyecto se encuentra modularizado bajo estándares limpios de desarrollo:

* **`voynichapp.py`**: Interfaz gráfica. Maneja el estado de la aplicación, el árbol de navegación jerárquica de las 240 páginas y renderiza las tablas estadísticas.
* **`voynichdata.py`**: Motor lógico y backend criptográfico. Contiene el pipeline de expresiones regulares, el diccionario maestro de raíces medievales y el segmentador de palabras compuestas.

---

## 📈 Próximos Pasos (Roadmap)
- [ ] Expandir el glosario maestro con más de 500 raíces botánicas y alquímicas medievales.
- [ ] Implementar análisis probabilísticos de n-gramas mediante frecuencias estadísticas avanzadas.
- [ ] Desarrollar un parser para variaciones gráficas encerradas entre corchetes `[a:o]` dentro del interlineal.

---
**Desarrollado de forma independiente por Mateo Thour-idk.**  
*Este es un proyecto de investigación estadística y criptoanálisis recreativo basado en paleografía computacional.*
