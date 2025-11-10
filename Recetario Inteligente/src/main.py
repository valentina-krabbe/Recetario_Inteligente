from services.business_logic import BusinessLogic
from services.search_engine import SearchEngine
from models.recommender import Recommender
import pandas as pd

# ----------------------------------------------------------------------
# Funciones auxiliares del Agente
# ----------------------------------------------------------------------

def find_recipes(available_ingredients: list, preferences: dict):
    """Integra Lógica de Negocio (Filtro) -> Búsqueda/Ranqueo (Relevancia)."""
    logic = BusinessLogic()
    search = SearchEngine()
    
    print(f"\n--- 1. LÓGICA: Filtrando por Ingredientes Disponibles ({len(available_ingredients)} ítems) ---")
    
    # 1. Filtrado de Ingredientes
    possible_recipes = logic.filter_by_ingredients(available_ingredients)
    print(f"Recetas posibles inicialmente: {len(possible_recipes)}")
    
    # 2. Aplicar Restricciones
    final_filtered_recipes = logic.apply_restrictions(possible_recipes, preferences)
    print(f"Recetas después de restricciones ({len(preferences)} filtros aplicados): {len(final_filtered_recipes)}")
    
    if final_filtered_recipes.empty:
        return final_filtered_recipes 

    # 3. Ranqueo (solo si hay recetas)
    print("\n--- 3. BÚSQUEDA: Ranqueando por Relevancia (TF-IDF) ---")
    ranked_recipes = search.rank_recipes(final_filtered_recipes, available_ingredients)
    
    return ranked_recipes[['nombre', 'categoria', 'relevance_score']]

def get_recommendations(selected_recipe: str):
    """Módulo de ML (Recomendación)."""
    recommender = Recommender()
    recommendations = recommender.get_recommendations(selected_recipe)
    
    print(f"\n--- 4. MACHINE LEARNING: Recomendaciones post-interacción para '{selected_recipe}' ---")
    return recommendations

def get_user_input():
    """Captura los ingredientes y las preferencias del usuario."""
    
    print("\n================================================")
    print("🤖 Agente Recetario Inteligente: ¡Hola! Iniciemos la búsqueda.")
    print("================================================")
    
    # 1. Entrada de Ingredientes
    ingredientes_str = input(
        "📝 Ingrese los ingredientes que tiene en casa (separados por coma, ej: huevo, leche, tomate): "
    ).lower()
    available_ingredients = [i.strip() for i in ingredientes_str.split(',') if i.strip()]
    
    if not available_ingredients:
        print("❌ Debe ingresar al menos un ingrediente. Terminando.")
        return None, None
    
    # 2. Consulta de Preferencias y Restricciones
    preferences = {}
    
    def ask_boolean(prompt):
        res = input(f"{prompt} (S/N/Omitir): ").upper()
        if res == 'S': return True
        if res == 'N': return False
        return None # Omitir

    print("\n❓ Restricciones Dietéticas:")
    preferences['carne'] = ask_boolean("¿Desea que la receta contenga carne?")
    preferences['gluten'] = ask_boolean("¿Desea que la receta contenga gluten?")
    preferences['lacteos'] = ask_boolean("¿Desea que la receta contenga lácteos?")
    preferences['azucar'] = ask_boolean("¿Desea que la receta contenga azúcar?")
    
    categoria_raw = input("\n¿A qué categoría debe pertenecer la receta (principal, postre, saludable, Omitir)?: ").lower()
    preferences['categoria'] = categoria_raw if categoria_raw in ['principal', 'postre', 'saludable'] else None
    
    return available_ingredients, preferences

# ----------------------------------------------------------------------
# NUEVA FUNCIÓN: Integración de la herramienta de Búsqueda de Google
# ----------------------------------------------------------------------
def search_recipe_online(recipe_name: str):
    """Genera y muestra el link directo de búsqueda en Google para la receta."""
    print("\n--- BÚSQUEDA WEB: Encontrando Instrucciones de la Receta ---")
    
    query = f"Receta completa {recipe_name} instrucciones paso a paso"
    print(f"Buscando en Google con la query: '{query}'...")
    
    # 1. Reemplazar espacios y caracteres especiales para URL (URL Encoding)
    # Ejemplo: 'Budín de Vainilla' -> 'Bud%C3%ADn+de+Vainilla'
    # Usamos f-string y .replace() para simular la codificación más común:
    encoded_query = query.replace(' ', '+').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    
    # 2. Construir el URL de búsqueda de Google
    google_search_url = f"https://www.google.com/search?q={encoded_query}"
    
    print("\n✅ Enlace directo a los resultados de búsqueda:")
    print(f"👉 **{google_search_url}**")
  
    print("-------------------------------------------------------------")

# ----------------------------------------------------------------------
# Punto de Ejecución Principal
# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    # 1. Obtener la entrada del usuario
    ingredientes_disponibles, preferencias_usuario = get_user_input()
    
    if ingredientes_disponibles is None:
        exit()

    # 2. Ejecutar la búsqueda y ranqueo (LÓGICA y BÚSQUEDA)
    results = find_recipes(ingredientes_disponibles, preferencias_usuario)
    
    if not results.empty:
        print("\n✅ RESULTADO FINAL: Recetas posibles ordenadas por relevancia:")
        # Mostrar el top 5
        print(results.head(5).to_markdown(index=False))
        
        best_recipe = results.iloc[0]['nombre']

        # 3. LLAMADA A LA NUEVA FUNCIONALIDAD DE BÚSQUEDA WEB
        search_online = input(f"\n💡 ¿Desea buscar las instrucciones de '{best_recipe}' en Internet? (S/N): ").upper()
        if search_online == 'S':
            search_recipe_online(best_recipe)

        # 4. EJECUCIÓN DE LA RECOMENDACIÓN (ML)
        if input(f"\n¿Le gustaría ver recetas similares a la más relevante ({best_recipe})? (S/N): ").upper() == 'S':
            recommendations = get_recommendations(best_recipe)
            
            if recommendations:
                recommendations_filtered = [r for r in recommendations if r != best_recipe]
                print(f"⭐ Le recomendamos también: {', '.join(recommendations_filtered)}")
            else:
                print("No se encontraron recomendaciones similares.")
            
    else:
        print("\n❌ No se encontraron recetas que cumplan todos los requisitos.")