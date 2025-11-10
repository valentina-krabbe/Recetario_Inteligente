## 🤖 Recetario Inteligente: Agente Integral de Inteligencia Artificial

🌟 1. Objetivo y Alcance del Proyecto

El objetivo central fue consolidar habilidades técnicas mediante el diseño, desarrollo y comunicación de un Sistema Integral que articula tres pilares tecnológicos clave: Lógica, Búsqueda y Machine Learning (ML).


### **Propósito del Agente**

El Recetario Inteligente funciona como un agente conversacional que guía al usuario para encontrar las mejores recetas posibles que se ajusten estrictamente a:

- Ingredientes disponibles en casa (Búsqueda por disponibilidad).

- Restricciones dietéticas (Lógica de Negocio).

- Priorización por Relevancia (Búsqueda avanzada).

- Acceso a Instrucciones (Integración Externa).

### **Arquitectura del proyecto**

recetario_inteligente/
├── app.py                      # Interfaz de Usuario Web (Streamlit)
├── README.md
├── requirements.txt
├── data/
│   └── recetas_dataset.csv       # Dataset de 71 recetas
└── src/                          # Módulos de Código Fuente
    ├── models/                   # Módulo de Machine Learning (Recomendación)
    │   └── recommender.py        
    ├── services/                 # Módulos de Lógica de Negocio y Búsqueda
    │   ├── business_logic.py     # Reglas de negocio y Filtrado Estricto
    │   └── search_engine.py      # Motor de Ranqueo (TF-IDF)
    └── main.py                   # Agente de Interacción por Consola (Alternativo)

### Componentes

**1. Lógica de Negocio y Filtrado Estricto (Módulo business_logic.py)**
Este módulo implementa las reglas de negocio, siendo la primera capa de filtrado:

- Reglas Booleanas: Aplica filtros estrictos basados en las preferencias del usuario (carne, gluten, lácteos, azúcar, etc.).

- Disponibilidad: Verifica que la receta sea "posible" de elaborar con los ingredientes proporcionados.

**2. Módulo de Búsqueda y Salida Web (Ranqueo e Integración Externa)**
Este módulo gestiona el ranqueo de las recetas y su salida final:

- Ranqueo por Relevancia: Utiliza TF-IDF (Term Frequency-Inverse Document Frequency) y Similitud de Coseno para ordenar las recetas por su relevance_score, priorizando el uso eficiente de los ingredientes.

- Integración Externa: El agente resuelve la falta de instrucciones de preparación en el dataset. Al final del proceso, construye un URL de Google Search codificado (URL Encoding) con la consulta exacta de la receta. El agente no solo dice qué cocinar, sino que proporciona el enlace directo de Google que le dice al usuario cómo cocinarlo, cerrando el ciclo de valor.

**3. Machine Learning (Recomendación) (Módulo recommender.py)**
Este módulo añade la capa de inteligencia artificial post-decisión:

- Modelo: Sistema de Recomendación Basado en Contenido (Content-Based).

- Función: Sugiere recetas que son similares a la mejor opción ranqueada (misma categoría y restricciones dietéticas), ampliando las opciones de elección del usuario.

**4.  Interfaz de Usuario (Streamlit)**

La interacción con el agente se realiza mediante una interfaz web desarrollada en Streamlit. Esto permite a los usuarios interactuar con los filtros (inputs de texto y selectores) y visualizar los resultados (tablas de DataFrames y enlaces) de forma intuitiva, lo que facilita la demostración del sistema.