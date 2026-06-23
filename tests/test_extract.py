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
from etl.extract.extract_csv import leer_csv
# ... (el resto de tu código del test sigue exactamente igual abajo)
class TestExtract(unittest.TestCase):
    
    def test_leer_csv_retorna_dataframe(self):
        """Valida que la lectura del CSV principal de la Superstore funcione."""
        ruta_prueba = "data/raw/Sample_ Superstore.csv"
        try:
            df = leer_csv(ruta_prueba)
            # Verificamos que sea un DataFrame de Pandas
            self.assertIsInstance(df, pd.DataFrame)
            # Verificamos que no venga vacío
            self.assertFalse(df.empty)
        except Exception as e:
            self.fail(f"La lectura del CSV falló críticamente: {e}")

if __name__ == "__main__":
    unittest.main()