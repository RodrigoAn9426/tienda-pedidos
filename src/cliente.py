"""Validacion de los datos del cliente (HU-04)."""

MIN_DIGITOS_CEDULA = 6
MAX_DIGITOS_CEDULA = 10
DIGITOS_TELEFONO = 10
PREFIJO_CELULAR = "3"


def _son_digitos(texto: str) -> bool:
    """Devuelve True si el texto tiene solo digitos 0-9 (y no esta vacio)."""
    return texto.isascii() and texto.isdigit()


def validar_cliente(nombre: str, cedula: str, telefono: str) -> bool:
    """Comprueba que el nombre, la cedula y el telefono del cliente son validos.

    Recibe:
        nombre: nombre completo, con al menos dos palabras (nombre y apellido).
        cedula: texto con solo digitos, de 6 a 10 digitos.
        telefono: celular colombiano, 10 digitos que empiezan por 3.

    Devuelve:
        True si los tres datos son validos.

    Lanza:
        ValueError: si un dato no cumple la regla. El mensaje empieza con el
            nombre del campo. Se revisan en el orden nombre, cedula, telefono
            y se informa solo el primero que falla.
    """
    if len(nombre.split()) < 2:
        raise ValueError("nombre: escribe nombre y apellido")
    if not (
        _son_digitos(cedula)
        and MIN_DIGITOS_CEDULA <= len(cedula) <= MAX_DIGITOS_CEDULA
    ):
        raise ValueError("cedula: debe tener entre 6 y 10 digitos")
    if not (
        _son_digitos(telefono)
        and len(telefono) == DIGITOS_TELEFONO
        and telefono.startswith(PREFIJO_CELULAR)
    ):
        raise ValueError("telefono: debe tener 10 digitos y empezar por 3")
    return True