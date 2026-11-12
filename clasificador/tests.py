import io
from unittest import mock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, override_settings
from django.urls import reverse
from PIL import Image


def imagen_png(color=(200, 200, 200)):
    buffer = io.BytesIO()
    Image.new("RGB", (32, 32), color).save(buffer, format="PNG")
    return SimpleUploadedFile("residuo.png", buffer.getvalue(), content_type="image/png")


PREDICCIONES_FALSAS = [
    {"clave": "glass", "confianza": 91.2},
    {"clave": "plastic", "confianza": 6.1},
    {"clave": "metal", "confianza": 1.4},
]


class PaginaInicioTests(SimpleTestCase):
    def test_pagina_carga_en_espanol(self):
        respuesta = self.client.get(reverse("clasificador:inicio"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'lang="es"')
        self.assertContains(respuesta, "¿Qué residuo tienes?")

    @mock.patch("clasificador.views.clasificar_imagen", return_value=PREDICCIONES_FALSAS)
    def test_clasificacion_muestra_resultado_y_consejo(self, _mock):
        respuesta = self.client.post(reverse("clasificador:inicio"), {"imagen": imagen_png()})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Vidrio")
        self.assertContains(respuesta, "91,2%")
        self.assertContains(respuesta, 'style="width: 91.2%"')
        self.assertContains(respuesta, "Otras posibilidades")
        self.assertContains(respuesta, "Plástico")

    @mock.patch("clasificador.views.clasificar_imagen", return_value=PREDICCIONES_FALSAS)
    def test_resultado_incluye_la_foto_analizada(self, _mock):
        respuesta = self.client.post(reverse("clasificador:inicio"), {"imagen": imagen_png()})
        self.assertContains(respuesta, "data:image/jpeg;base64,")

    def test_sin_archivo_muestra_error_amable(self):
        respuesta = self.client.post(reverse("clasificador:inicio"), {})
        self.assertContains(respuesta, "Selecciona una foto antes de clasificar.")

    def test_archivo_que_no_es_imagen_se_rechaza(self):
        texto = SimpleUploadedFile("nota.png", b"esto no es una imagen", content_type="image/png")
        respuesta = self.client.post(reverse("clasificador:inicio"), {"imagen": texto})
        self.assertContains(respuesta, "no es una imagen válida")

    @override_settings(RECICLAJE_MAX_UPLOAD_BYTES=10)
    def test_imagen_muy_pesada_se_rechaza(self):
        respuesta = self.client.post(reverse("clasificador:inicio"), {"imagen": imagen_png()})
        self.assertContains(respuesta, "pesa más de")

    @mock.patch("clasificador.views.clasificar_imagen", side_effect=RuntimeError("fallo"))
    def test_error_del_modelo_no_rompe_la_pagina(self, _mock):
        respuesta = self.client.post(reverse("clasificador:inicio"), {"imagen": imagen_png()})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "No pudimos analizar la imagen")

    @mock.patch(
        "clasificador.views.clasificar_imagen",
        return_value=[{"clave": "paper", "confianza": 42.0}, {"clave": "cardboard", "confianza": 40.0}],
    )
    def test_confianza_baja_muestra_aviso(self, _mock):
        respuesta = self.client.post(reverse("clasificador:inicio"), {"imagen": imagen_png()})
        self.assertContains(respuesta, "no es muy segura")