# Documentación de API

## API de Feriados

El proyecto utiliza la API pública Nager.Date.

### Endpoint

GET

https://date.nager.at/api/v3/PublicHolidays/{anio}/US

### Parámetros

| Parámetro | Tipo    | Descripción     |
| --------- | ------- | --------------- |
| anio      | Integer | Año a consultar |

### Ejemplo

GET

https://date.nager.at/api/v3/PublicHolidays/2017/US

### Respuesta

```json
[
  {
    "date":"2017-01-01",
    "localName":"New Year's Day",
    "name":"New Year's Day"
  }
]
```

### Uso en el proyecto

El módulo:

```python
api/feriados.py
```

consume este endpoint para obtener los feriados que posteriormente son integrados al dataset de ventas.
