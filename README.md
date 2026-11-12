# EcoIbagué · Clasificador de residuos

Aplicación Django que recibe una foto de un residuo, la analiza con un modelo preentrenado de Hugging Face y dice en qué contenedor va.

Modelo por defecto: `yangy50/garbage-classification` (ViT, categorías: cartón, vidrio, metal, papel, plástico y basura).

## 1. Instalar

En Windows (PowerShell), desde la carpeta del proyecto:

```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Si `torch` tarda mucho, puedes instalar la versión solo CPU (más liviana):

```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

## 2. Preparar y ejecutar

```powershell
python manage.py migrate
python manage.py test clasificador
python manage.py runserver
```

Abre http://127.0.0.1:8000/

La primera vez que clasifiques una foto, el modelo se descarga desde Hugging Face (unos cientos de MB) y se guarda en caché. Las siguientes veces responde mucho más rápido.

## 3. Cambiar de modelo

Puedes usar otro modelo de clasificación de imágenes sin tocar el código:

```powershell
set RECICLAJE_MODEL_ID=otro-usuario/otro-modelo
python manage.py runserver
```

Si el modelo usa etiquetas distintas, agrégalas en `clasificador/categorias.py`. Para ver las etiquetas de un modelo:

```powershell
python -c "from transformers import AutoConfig; print(AutoConfig.from_pretrained('yangy50/garbage-classification').id2label)"
```

Las etiquetas que aparezcan ahí deben coincidir con las claves de `CATEGORIAS` (en minúscula).

## Estructura

```
clasificador/
  ml.py            # carga el modelo una sola vez y lo usa
  categorias.py    # nombres, contenedor y consejo en español por categoría
  forms.py         # validación de la imagen (tipo y tamaño)
  views.py         # recibe la foto, clasifica y muestra el resultado
  templates/       # plantillas HTML
  static/          # CSS y JS (vista previa, estado de carga)
  tests.py         # pruebas con el clasificador simulado
```

La imagen no se guarda en disco: se analiza en memoria y se descarta.

## Notas

- Las predicciones son orientativas. Antes de usarlas en un proyecto formal, prueba el modelo con fotos reales de Ibagué.
- Los colores de los contenedores no están en la app. Si los agregas, verifica con el operador de aseo de la ciudad.
- Para producción, define `DJANGO_SECRET_KEY` y `DJANGO_DEBUG=0`.
