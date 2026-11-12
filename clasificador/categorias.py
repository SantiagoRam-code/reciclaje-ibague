
CATEGORIAS = {
    "cardboard": {
        "nombre": "Cartón",
        "contenedor": "Papel y cartón",
        "consejo": "Aplánalo, quita cintas y etiquetas, y que esté seco.",
    },
    "paper": {
        "nombre": "Papel",
        "contenedor": "Papel y cartón",
        "consejo": "Sin grasa ni restos de comida. Si está muy sucio, va a residuos ordinarios.",
    },
    "glass": {
        "nombre": "Vidrio",
        "contenedor": "Vidrio",
        "consejo": "Enjuágalo y deposítalo sin tapa. Los vidrios rotos van envueltos en papel.",
    },
    "metal": {
        "nombre": "Metal",
        "contenedor": "Metales",
        "consejo": "Enjuaga las latas y aplástalas si es posible.",
    },
    "plastic": {
        "nombre": "Plástico",
        "contenedor": "Plásticos",
        "consejo": "Enjuágalo y aplástalo para que ocupe menos espacio.",
    },
    "trash": {
        "nombre": "No reciclable",
        "contenedor": "Residuos ordinarios",
        "consejo": "Este material no se recicla. Va al contenedor de residuos ordinarios.",
    },
}

_DESCONOCIDA = {
    "contenedor": "Consulta con tu operador de aseo",
    "consejo": "No tenemos una recomendación para esta categoría.",
}


def info_categoria(clave):
    if clave in CATEGORIAS:
        return CATEGORIAS[clave]
    return {"nombre": clave.capitalize(), **_DESCONOCIDA}
