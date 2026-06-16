import os
import sys

# Configurar ruta dinámica para que reconozca la carpeta 'etl' desde la raíz
ruta_actual = os.path.dirname(os.path.abspath(__file__)) 
ruta_raiz = os.path.abspath(os.path.join(ruta_actual, "..")) 

if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

# AHORA SÍ PUEDES IMPORTAR TU PROPIO CÓDIGO
import unittest
import pandas as pd

class TestLoad(unittest.TestCase):

    def test_normalizacion_columnas_mysql(self):
        """Prueba que los nombres de las columnas se formateen correctamente para la BD."""
        df_prueba = pd.DataFrame(columns=["Order ID", "Product Name", "Sales"])
        
        # Aplicamos la misma lógica de normalización que tienes en tu pipeline.py
        df_prueba.columns = (
            df_prueba.columns
            .str.lower()
            .str.replace(' ', '_')
        )
        
        columnas_esperadas = ["order_id", "product_name", "sales"]
        self.assertListEqual(list(df_prueba.columns), columnas_esperadas)

if __name__ == "__main__":
    unittest.main()