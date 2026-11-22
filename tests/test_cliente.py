import pytest

from cliente import validar_cliente

NOMBRE_OK = "Ana Gomez"
CEDULA_OK = "1000000001"
TELEFONO_OK = "3001234567"


@pytest.mark.parametrize(
    ("nombre", "cedula", "telefono"),
    [
        ("Ana Gomez", "1000000001", "3001234567"),  # datos completos
        ("Ñoño D'Angelo", "1000000001", "3001234567"),  # ñ y apóstrofo
        ("María Núñez Peña", "1000000001", "3001234567"),  # tildes, 3 palabras
        ("Ana Gomez", "100000", "3001234567"),  # límite: cédula de 6 dígitos
        ("Ana Gomez", "1000000000", "3001234567"),  # límite: cédula de 10
        ("Ana Gomez", "1000000001", "3000000000"),  # teléfono de 10 con prefijo 3
    ],
)
def test_datos_validos_devuelven_true(nombre, cedula, telefono):
    assert validar_cliente(nombre, cedula, telefono) is True


@pytest.mark.parametrize(
    ("nombre", "cedula", "telefono", "campo"),
    [
        ("Ana", CEDULA_OK, TELEFONO_OK, "nombre"),  # límite: una sola palabra
        ("", CEDULA_OK, TELEFONO_OK, "nombre"),  # nombre vacío
        ("   ", CEDULA_OK, TELEFONO_OK, "nombre"),  # solo espacios
        (NOMBRE_OK, "12345", TELEFONO_OK, "cedula"),  # límite: 5 dígitos
        (NOMBRE_OK, "12345678901", TELEFONO_OK, "cedula"),  # límite: 11 dígitos
        (NOMBRE_OK, "10000000A1", TELEFONO_OK, "cedula"),  # con letras
        (NOMBRE_OK, "1.000.000", TELEFONO_OK, "cedula"),  # con puntos
        (NOMBRE_OK, "", TELEFONO_OK, "cedula"),  # vacía
        (NOMBRE_OK, CEDULA_OK, "300123456", "telefono"),  # límite: 9 dígitos
        (NOMBRE_OK, CEDULA_OK, "30012345678", "telefono"),  # límite: 11 dígitos
        (NOMBRE_OK, CEDULA_OK, "2001234567", "telefono"),  # límite: prefijo 2
        (NOMBRE_OK, CEDULA_OK, "300 123 4567", "telefono"),  # con espacios
        (NOMBRE_OK, CEDULA_OK, "30012345AB", "telefono"),  # con letras
        (NOMBRE_OK, CEDULA_OK, "", "telefono"),  # vacío
        ("Ana", "12", "99", "nombre"),  # decisión fila 1: nombre falla, informa nombre
        (NOMBRE_OK, "12", "99", "cedula"),  # decisión fila 2: informa cédula
    ],
)
def test_dato_invalido_lanza_value_error_con_el_campo(
    nombre, cedula, telefono, campo
):
    with pytest.raises(ValueError, match=f"^{campo}:"):
        validar_cliente(nombre, cedula, telefono)