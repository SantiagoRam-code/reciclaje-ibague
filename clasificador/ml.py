import logging
import threading

from django.conf import settings

log = logging.getLogger(__name__)

_clasificador = None
_candado = threading.Lock()


def _cargar_clasificador():
    global _clasificador
    with _candado:
        if _clasificador is None:
            from transformers import pipeline

            log.info("Cargando el modelo %s", settings.RECICLAJE_MODEL_ID)
            _clasificador = pipeline("image-classification", model=settings.RECICLAJE_MODEL_ID)
    return _clasificador


def clasificar_imagen(imagen, top_k=3):
    clasificador = _cargar_clasificador()
    resultados = clasificador(imagen, top_k=top_k)
    return [
        {"clave": r["label"].lower(), "confianza": round(r["score"] * 100, 1)}
        for r in resultados
    ]
