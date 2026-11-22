"""Datos de prueba sinteticos (generados con IA, sin personas reales)."""

import pytest

CLIENTES_VALIDOS = [
    pytest.param(
        {
            "nombre": "Yeimy Tatiana Cuéllar Trujillo",
            "cedula": "1000000011",
            "telefono": "3000000011",
        },
        id="tildes",
    ),
    pytest.param(
        {
            "nombre": "Jhon Fredy Ñáñez Perdomo",
            "cedula": "1000000012",
            "telefono": "3000000012",
        },
        id="enie",
    ),
    pytest.param(
        {
            "nombre": "Luz Dary D'Amato",
            "cedula": "1000000013",
            "telefono": "3000000013",
        },
        id="apostrofo",
    ),
    pytest.param(
        {
            "nombre": "  Ana   María  Vargas  ",
            "cedula": "1000000014",
            "telefono": "3000000014",
        },
        id="espacios-de-mas",
    ),
    pytest.param(
        {"nombre": "Nelly Polanía", "cedula": "100000", "telefono": "3000000015"},
        id="cedula-de-6-digitos",
    ),
]

CLIENTES_INVALIDOS = [
    pytest.param(
        {
            "nombre": "",
            "cedula": "1000000021",
            "telefono": "3000000021",
            "campo": "nombre",
        },
        id="nombre-vacio",
    ),
    pytest.param(
        {
            "nombre": "Marlon",
            "cedula": "1000000022",
            "telefono": "3000000022",
            "campo": "nombre",
        },
        id="nombre-de-una-palabra",
    ),
    pytest.param(
        {
            "nombre": "Ana Vargas",
            "cedula": "0",
            "telefono": "3000000023",
            "campo": "cedula",
        },
        id="cedula-en-cero",
    ),
    pytest.param(
        {
            "nombre": "Ana Vargas",
            "cedula": "1000000024",
            "telefono": "0000000000",
            "campo": "telefono",
        },
        id="telefono-en-ceros",
    ),
    pytest.param(
        {
            "nombre": "Ana Vargas",
            "cedula": "1000000025",
            "telefono": "",
            "campo": "telefono",
        },
        id="telefono-vacio",
    ),
]


@pytest.fixture(params=CLIENTES_VALIDOS)
def cliente_valido(request):
    """Un cliente sintetico con datos validos, uno por cada caso."""
    return request.param


@pytest.fixture(params=CLIENTES_INVALIDOS)
def cliente_invalido(request):
    """Un cliente sintetico con un dato invalido; "campo" dice cual debe fallar."""
    return request.param


@pytest.fixture
def existencias_tienda():
    """Existencias de la tienda: 1 gaseosa, 2 arroz, 3 panela (agotada), 4 cafe."""
    return {1: 10, 2: 8, 3: 0, 4: 1}