from django import forms
from django.conf import settings


class SubirImagenForm(forms.Form):
    imagen = forms.ImageField(
        label="Foto del residuo",
        error_messages={
            "required": "Selecciona una foto antes de clasificar.",
            "invalid_image": "El archivo no es una imagen válida. Prueba con JPG, PNG o WEBP.",
        },
        widget=forms.FileInput(
            attrs={
                "accept": "image/jpeg,image/png,image/webp",
                "id": "imagen",
            }
        ),
    )

    def clean_imagen(self):
        archivo = self.cleaned_data["imagen"]
        limite = settings.RECICLAJE_MAX_UPLOAD_BYTES
        if archivo.size > limite:
            raise forms.ValidationError(
                f"La imagen pesa más de {limite // (1024 * 1024)} MB. Usa una más pequeña."
            )
        return archivo
