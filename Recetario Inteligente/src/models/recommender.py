from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

class Recommender:
    def __init__(self, data_path='data/recetas_dataset.csv'):
        self.df = pd.read_csv(data_path)
        self.vectorizer = TfidfVectorizer(stop_words=None)
        
        # Crear una 'meta-columna' con todas las características para el modelo Content-Based
        self.df['features'] = (
            self.df['categoria'] + ' ' + 
            self.df['ingredientes'] + ' ' + 
            self.df['carne'].astype(str) + ' ' + 
            self.df['gluten'].astype(str)
        )
        
        # Entrenar el vectorizador TF-IDF con las 'features'
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['features'])

    def get_recommendations(self, recipe_name: str, num_recommendations=3) -> list:
        """Sugiere recetas similares basadas en las características (ML Content-Based)."""
        
        # 1. Obtener el índice de la receta seleccionada
        try:
            idx = self.df[self.df['nombre'] == recipe_name].index[0]
        except IndexError:
            return [] # Receta no encontrada

        # 2. Calcular la Similitud de Coseno
        cosine_sim = linear_kernel(self.tfidf_matrix[idx], self.tfidf_matrix).flatten()

        # 3. Obtener los índices de las recetas más similares
        # La tupla (score, index)
        sim_scores = list(enumerate(cosine_sim))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Excluir la receta propia (score 1.0) y tomar las siguientes
        sim_scores = sim_scores[1:num_recommendations+1]
        
        recipe_indices = [i[0] for i in sim_scores]
        
        # 4. Devolver los nombres de las recetas recomendadas
        return self.df['nombre'].iloc[recipe_indices].tolist()