import base64
import io
import logging

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from PIL import Image

from .categorias import info_categoria
from .forms import SubirImagenForm
from .ml import clasificar_imagen

log = logging.getLogger(__name__)

UMBRAL_CONFIANZA_BAJA = 60


def _armar_resultado(predicciones):
    principal, *otras = predicciones
    info = info_categoria(principal["clave"])
    return {
        "categoria": info["nombre"],
        "contenedor": info["contenedor"],
        "consejo": info["consejo"],
        "confianza": principal["confianza"],
        "confianza_baja": principal["confianza"] < UMBRAL_CONFIANZA_BAJA,
        "otras": [
            {"nombre": info_categoria(p["clave"])["nombre"], "confianza": p["confianza"]}
            for p in otras
        ],
    }


def _miniatura_base64(imagen, lado=640):
    miniatura = imagen.copy()
    miniatura.thumbnail((lado, lado))
    buffer = io.BytesIO()
    miniatura.save(buffer, format="JPEG", quality=85)
    return base64.b64encode(buffer.getvalue()).decode("ascii")


@require_http_methods(["GET", "POST"])
def inicio(request):
    if request.method == "POST":
        form = SubirImagenForm(request.POST, request.FILES)
    else:
        form = SubirImagenForm()

    contexto = {"form": form, "resultado": None, "error": None}

    if request.method == "POST" and form.is_valid():
        try:
           
            imagen = Image.open(form.cleaned_data["imagen"]).convert("RGB")
            predicciones = clasificar_imagen(imagen)
        except Exception:
            log.exception("No se pudo clasificar la imagen")
            contexto["error"] = "No pudimos analizar la imagen. Intenta de nuevo en unos segundos."
        else:
            contexto["resultado"] = _armar_resultado(predicciones)
            contexto["resultado"]["miniatura"] = _miniatura_base64(imagen)

    return render(request, "clasificador/inicio.html", contexto)