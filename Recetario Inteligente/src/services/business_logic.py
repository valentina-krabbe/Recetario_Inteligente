import pandas as pd

class BusinessLogic:
    def __init__(self, data_path='data/recetas_dataset.csv'):
        # Carga el dataset al inicializar el módulo
        self.df = pd.read_csv(data_path)
        # Convertir TRUE/FALSE a booleanos
        self.df[['carne', 'gluten', 'lacteos', 'azucar']] = self.df[['carne', 'gluten', 'lacteos', 'azucar']].astype(bool)

    def filter_by_ingredients(self, available_ingredients: list) -> pd.DataFrame:
        """Filtra recetas que contienen al menos UN ingrediente disponible."""
        
        df_temp = self.df.copy()
        df_temp['ingredientes_list'] = df_temp['ingredientes'].apply(lambda x: [i.strip() for i in x.split(',')])

        # Verificar si al menos un ingrediente de la receta está en los ingredientes disponibles
        def check_availability(recipe_ingredients, available):
            return any(ing in available for ing in recipe_ingredients)
        
        df_temp['is_possible'] = df_temp['ingredientes_list'].apply(
            lambda x: check_availability(x, available_ingredients)
        )
        
        return df_temp[df_temp['is_possible']]

    def apply_restrictions(self, df: pd.DataFrame, preferences: dict) -> pd.DataFrame:
        """Aplica filtros de restricciones booleanas y categoría."""
        
        filtered_df = df.copy()
        
        # Restricciones booleanas (carne, gluten, lacteos, azucar)
        for restriction, value in preferences.items():
            if restriction in ['carne', 'gluten', 'lacteos', 'azucar']:
                # Si el usuario desea filtrar por una restricción (value no es None)
                if value is not None:
                    filtered_df = filtered_df[filtered_df[restriction] == value]
            elif restriction == 'categoria' and value:
                filtered_df = filtered_df[filtered_df['categoria'] == value]
                
        return filtered_df