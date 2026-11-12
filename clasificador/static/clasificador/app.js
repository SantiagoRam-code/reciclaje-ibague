(function () {
  var form = document.getElementById("form-clasificar");
  if (!form) return;

  var input = document.getElementById("imagen");
  var boton = document.getElementById("boton-clasificar");
  var zonaTexto = document.getElementById("zona-texto");
  var vistaPrevia = document.getElementById("vista-previa");
  var imagenPrevia = document.getElementById("imagen-previa");
  var notaCarga = document.getElementById("nota-carga");
  var urlPrevia = null;

  input.addEventListener("change", function () {
    if (urlPrevia) URL.revokeObjectURL(urlPrevia);

    var archivo = input.files[0];
    if (!archivo) {
      urlPrevia = null;
      boton.disabled = true;
      vistaPrevia.hidden = true;
      zonaTexto.hidden = false;
      return;
    }

    urlPrevia = URL.createObjectURL(archivo);
    imagenPrevia.src = urlPrevia;
    vistaPrevia.hidden = false;
    zonaTexto.hidden = true;
    boton.disabled = false;
  });

  form.addEventListener("submit", function () {
    boton.disabled = true;
    boton.textContent = "Analizando…";
    notaCarga.hidden = false;
  });

  var resultado = document.getElementById("resultado");
  if (resultado) {
    resultado.focus({ preventScroll: true });
    resultado.scrollIntoView({ behavior: "smooth", block: "start" });
  }
})();
