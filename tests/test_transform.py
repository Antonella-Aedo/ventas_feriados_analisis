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
from etl.transform.transform import crear_variables, transformar_csv

class TestTransform(unittest.TestCase):

    def test_manejo_de_fechas_mixtas(self):
        """Prueba que los formatos de fecha con barras y guiones se parseen bien."""
        # Creamos datos falsos con el desorden que tenía tu dataset original
        datos_locos = pd.DataFrame({
            "Order Date": ["1/29/14", "09-09-2015", "11/28/2015"],
            "Ship Date": ["1/31/14", "09-11-2015", "11/30/2015"]
        })
        
        df_limpio = transformar_csv(datos_locos)
        
        # Verificamos que Pandas ya no los vea como texto, sino como fechas reales (datetime)
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df_limpio["Order Date"]))
        # Validamos que no se hayan generado nulos falsos (NaT)
        self.assertEqual(df_limpio["Order Date"].isnull().sum(), 0)

    def test_reemplazo_de_nulos_en_feriados(self):
        """Valida que los NaN de la API se cambien por 'Día Regular / No Feriado'."""
        # Simulamos un dataset combinado donde una venta no cayó en feriado (NaN)
        df_prueba = pd.DataFrame({
            "Order Date": pd.to_datetime(["2016-05-30", "2016-06-15"]),
            "Nombre_Feriado": ["Memorial Day", None], # El None representa el nulo
            "Nombre_Local": ["Memorial Day", None],
            "Fecha": ["2016-05-30", None],
            "Sales": [100.0, 50.0],
            "meta_ventas": [40000.0, 40000.0]
        })
        
        df_resultado = crear_variables(df_prueba)
        
        # Verificamos que el nulo (None) haya desaparecido y tenga la etiqueta corporativa
        self.assertEqual(df_resultado["Nombre_Feriado"].iloc[1], "Día Regular / No Feriado")
        # Verificamos que el conteo total de nulos en esa columna sea 0
        self.assertEqual(df_resultado["Nombre_Feriado"].isnull().sum(), 0)
        # Verificamos que 'Es_Feriado' sea 1 para el feriado real y 0 para el día regular
        self.assertEqual(df_resultado["Es_Feriado"].iloc[0], 1)
        self.assertEqual(df_resultado["Es_Feriado"].iloc[1], 0)

if __name__ == "__main__":
    unittest.main()