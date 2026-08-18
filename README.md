# Sistema de inferencia con Regresión Logística

Esta aplicación estima la probabilidad de que un cliente contrate un depósito a plazo.

```text
Frontend -> API -> Modelo -> Resultado
```

El resultado es una estimación, no una certeza.

## Estructura

```text
data/       Dataset
training/   Entrenamiento
models/     Modelo y métricas guardadas
app/        API con FastAPI
frontend/   HTML, CSS y JavaScript
tests/      Pruebas
evidence/   Evidencias
```

## Dataset

Se usó el dataset [Bank Marketing de UCI](https://archive.ics.uci.edu/dataset/222/bank+marketing).
El archivo está incluido en `data/bank.csv`.

Variables utilizadas:

- `age`: edad.
- `job`: ocupación.
- `marital`: estado civil.
- `education`: educación.
- `balance`: balance anual.
- `housing`: crédito hipotecario.
- `loan`: préstamo personal.
- `campaign`: contactos realizados.

La variable que se quiere predecir es `y`, que puede ser `yes` o `no`.

No se usa `duration` porque la duración de la llamada se conoce después de contactar al cliente.

## Instalación

Se recomienda Python 3.12.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecutar la aplicación

El modelo ya está entrenado. Para iniciar la aplicación:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

La documentación de la API está en `http://127.0.0.1:8000/docs`.

## Entrenar nuevamente

Para volver a entrenar el modelo:

```powershell
.\.venv\Scripts\python.exe -m training.train
```

El entrenamiento:

1. Lee el dataset.
2. Separa datos de entrenamiento y prueba.
3. Prepara las variables numéricas y categóricas.
4. Entrena una Regresión Logística.
5. Guarda el pipeline en `models/bank_marketing_pipeline.joblib`.

## Métricas

| Métrica | Resultado |
|---|---:|
| Accuracy | 0.6099 |
| Precision | 0.1608 |
| Recall | 0.5673 |
| F1-score | 0.2505 |

- **Accuracy:** porcentaje total de respuestas correctas.
- **Precision:** cuántos de los clientes marcados como `yes` realmente eran `yes`.
- **Recall:** cuántos clientes `yes` logró encontrar.
- **F1-score:** combina precision y recall.

El modelo es básico y todavía comete errores. Se usó `class_weight="balanced"`
porque el dataset tiene muchos más casos `no` que `yes`.

## API

Endpoint:

```text
POST /predict
```

Ejemplo de solicitud:

```json
{
  "age": 41,
  "job": "technician",
  "marital": "married",
  "education": "secondary",
  "balance": 3200,
  "housing": "yes",
  "loan": "no",
  "campaign": 2
}
```

Ejemplo de respuesta:

```json
{
  "prediction": "no",
  "probability": 0.4009,
  "classification": "Baja propensión"
}
```

La probabilidad corresponde a la clase `yes`.

## Errores

La API responde con código `422` cuando los datos no son válidos.

Ejemplos:

```json
{ "age": "hola" }
```

```json
{ "age": -10 }
```

## Evidencias

- [Inferencia válida](evidence/valid_prediction.json)
- [Error por tipo incorrecto](evidence/invalid_type_prediction.json)
- [Error por edad fuera de rango](evidence/invalid_range_prediction.json)

![Frontend funcionando](evidence/frontend-prediction.png)

## Pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Preguntas

### ¿Por qué el modelo se entrena fuera de la API?

Porque entrenar toma tiempo. La API solamente carga el modelo guardado y realiza predicciones.

### ¿Por qué se usa el mismo preprocesamiento?

Porque el modelo necesita recibir los datos de la misma manera en que los recibió durante el entrenamiento.

### ¿Cuál es la diferencia entre `predict()` y `predict_proba()`?

`predict()` devuelve `yes` o `no`. `predict_proba()` devuelve la probabilidad de cada clase.

### ¿Qué significa una probabilidad de 0.72?

Significa que el modelo estima 72 % para la clase `yes`. No significa que el cliente contratará con seguridad ni que el modelo tenga 72 % de accuracy.

### ¿Por qué no se usa `duration`?

Porque la duración se conoce después de la llamada y la predicción debe hacerse antes.

### ¿Qué pasa si cambia la información del frontend?

La API puede rechazar la solicitud. Si cambian las variables del modelo, también se debe actualizar el entrenamiento y guardar un nuevo pipeline.

