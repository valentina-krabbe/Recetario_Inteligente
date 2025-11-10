# app.py

import streamlit as st
import pandas as pd
from src.services.business_logic import BusinessLogic
from src.services.search_engine import SearchEngine
from src.models.recommender import Recommender
import urllib.parse # Necesario para codificar la URL de Google

# Inicialización de servicios
logic = BusinessLogic()
search = SearchEngine()
recommender = Recommender()

# ----------------------------------------------------------------------
# LÓGICA CENTRAL DEL AGENTE (Copiada de src/main.py)
# ----------------------------------------------------------------------

def find_recipes(available_ingredients: list, preferences: dict):
    """
    Integra Lógica de Negocio (Filtro) -> Búsqueda/Ranqueo (Relevancia).
    IMPORTANTE: No usa 'print()' ya que se corre en Streamlit.
    """
    
    # 1. Filtrado de Ingredientes y Restricciones
    possible_recipes = logic.filter_by_ingredients(available_ingredients)
    final_filtered_recipes = logic.apply_restrictions(possible_recipes, preferences)
    
    if final_filtered_recipes.empty:
        # Devuelve un DataFrame vacío si no hay resultados, no None.
        return final_filtered_recipes 

    # 2. Ranqueo
    ranked_recipes = search.rank_recipes(final_filtered_recipes, available_ingredients)
    
    # Devuelve el DataFrame ranqueado con las columnas necesarias
    return ranked_recipes[['nombre', 'categoria', 'relevance_score']]

def get_recommendations(selected_recipe: str):
    """Módulo de ML (Recomendación)."""
    # NO usa 'print()'
    return recommender.get_recommendations(selected_recipe)

# ----------------------------------------------------------------------
# INTERFAZ DE USUARIO CON STREAMLIT
# ----------------------------------------------------------------------

st.set_page_config(page_title="Recetario Inteligente 🤖", layout="wide")
st.title("🍽️ Agente Recetario Inteligente")
st.markdown("Encuentra la receta perfecta con tus ingredientes y preferencias.")

# --- 1. Entrada de Ingredientes ---
with st.expander("📝 Tus Ingredientes Disponibles", expanded=True):
    ingredientes_str = st.text_input(
        "Ingresa los ingredientes que tienes (separados por coma):",
        "huevo, harina, leche, tomate, cebolla"
    )

# --- 2. Restricciones de Usuario (Inputs de Lógica) ---
st.subheader("Filtros y Restricciones")

# Usamos columnas para un layout más limpio
col1, col2, col3, col4, col5 = st.columns(5)

# Función para formatear las opciones de True/False/None
format_func = lambda x: {True: "Sí", False: "No", None: "Omitir"}.get(x, "Omitir")

with col1:
    carne_op = st.selectbox("¿Contiene Carne?", [None, True, False], format_func=format_func)
with col2:
    gluten_op = st.selectbox("¿Contiene Gluten?", [None, True, False], format_func=format_func)
with col3:
    lacteos_op = st.selectbox("¿Contiene Lácteos?", [None, True, False], format_func=format_func)
with col4:
    azucar_op = st.selectbox("¿Contiene Azúcar?", [None, True, False], format_func=format_func)
with col5:
    categoria_op = st.selectbox("Categoría:", [None, "principal", "postre", "saludable"])

# --- Botón de Ejecución ---
if st.button("Buscar Recetas y Ranqueo", type="primary"):
    
    # Preprocesar inputs
    available_ingredients = [i.strip() for i in ingredientes_str.lower().split(',') if i.strip()]
    
    preferences = {
        'carne': carne_op,
        'gluten': gluten_op,
        'lacteos': lacteos_op,
        'azucar': azucar_op,
        'categoria': categoria_op
    }

    if not available_ingredients:
        st.error("❌ Por favor, ingresa al menos un ingrediente para comenzar la búsqueda.")
        st.stop()

    # Ejecutar la Lógica y Búsqueda
    with st.spinner('Analizando ingredientes y ranqueando recetas...'):
        ranked_results = find_recipes(available_ingredients, preferences)

    # --- Mostrar Resultados ---
    if ranked_results.empty:
        st.warning("❌ No se encontraron recetas que cumplan todos los requisitos.")
    else:
        st.success(f"✅ ¡Éxito! Encontramos {len(ranked_results)} recetas posibles, ranqueadas por relevancia.")
        
        # 1. Mostrar Tabla de Ranqueo
        st.subheader("Top Recetas Sugeridas (Ranqueo TF-IDF)")
        st.dataframe(
            ranked_results.head(10).style.format({"relevance_score": "{:.4f}"}), 
            use_container_width=True
        )

        # --- 2. Búsqueda Externa y Recomendación ---
        best_recipe = ranked_results.iloc[0]['nombre']
        st.markdown(f"### 🥇 Receta más Relevante: {best_recipe}")
        
        # Generar Link de Búsqueda de Google (Integración Externa)
        base_query = f"Receta completa {best_recipe} instrucciones paso a paso"
        # Usamos urllib.parse.quote_plus para codificar la URL de forma segura
        encoded_query = urllib.parse.quote_plus(base_query)
        google_search_url = f"https://www.google.com/search?q={encoded_query}"
        
        # Mostrar el enlace como un botón o un markdown con link
        st.markdown(f"""
            **Instrucciones:** <a href="{google_search_url}" target="_blank" style="text-decoration: none;">
                <button style="background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">
                    🔎 Ver '{best_recipe}' en Google
                </button>
            </a>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Módulo de Recomendación ML
        st.subheader("⭐ Recomendaciones (Machine Learning)")
        recommendations = get_recommendations(best_recipe)
        
        if recommendations:
            recommendations_filtered = [r for r in recommendations if r != best_recipe]
            if recommendations_filtered:
                st.info(f"Otras recetas similares que podrían interesarte: **{', '.join(recommendations_filtered)}**")
            else:
                 st.info(f"No se encontraron otras recomendaciones, solo la mejor receta: {best_recipe}.")
        else:
            st.info("No se encontraron recomendaciones similares.")