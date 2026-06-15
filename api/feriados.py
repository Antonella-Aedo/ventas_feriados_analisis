import requests

def consultar_feriados(anio):
    """
    Consulta la API Nager.Date.
    Devuelve los feriados de Estados Unidos.
    """

    url = f"https://date.nager.at/api/v3/PublicHolidays/{anio}/US"

    try:
        respuesta = requests.get(url)

        if respuesta.status_code == 200:
            print("Conexión exitosa con la API.")

            return respuesta.json()

        else:
            print(f"Error en la API: {respuesta.status_code}")
            return None

    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return None