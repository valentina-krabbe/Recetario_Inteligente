from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

class SearchEngine:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def rank_recipes(self, filtered_recipes: pd.DataFrame, user_ingredients: list) -> pd.DataFrame:
        """
        Calcula la similitud de coseno entre los ingredientes disponibles del usuario 
        y los ingredientes de la receta (usando TF-IDF) para ranquearlas.
        """
        
        # Control de robustez: Si el DataFrame está vacío, no se hace el cálculo
        if filtered_recipes.empty:
            return filtered_recipes

        # 1. Crear un 'documento' de consulta a partir de los ingredientes disponibles
        user_query = " ".join(user_ingredients)
        
        # 2. Combinar los ingredientes de todas las recetas filtradas para el entrenamiento del vectorizador
        all_texts = filtered_recipes['ingredientes'].tolist() + [user_query]
        
        # 3. Fit y Transform: TF-IDF
        try:
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        except ValueError:
            # En caso de que no haya vocabulario útil (raro, pero posible)
            filtered_recipes['relevance_score'] = 0.0
            return filtered_recipes

        # Separar la matriz: recetas (primeros N) y consulta (último)
        recipe_vectors = tfidf_matrix[:-1]
        query_vector = tfidf_matrix[-1]
        
        # 4. Similitud de Coseno para ranquear
        cosine_sim = cosine_similarity(query_vector, recipe_vectors).flatten()
        
        # 5. Agregar el score y ordenar
        filtered_recipes['relevance_score'] = cosine_sim
        
        # Retorna ordenado de mayor a menor score
        return filtered_recipes.sort_values(by='relevance_score', ascending=False)