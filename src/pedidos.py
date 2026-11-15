class ProductoNoExisteError(Exception):
    """Se lanza cuando el producto que se quiere agregar no esta en las existencias."""


class ExistenciasInsuficientesError(Exception):
    """Se lanza cuando el total pedido de un producto pasa de las unidades disponibles."""


def _validar_cantidad(cantidad):
    """Revisa que la cantidad sea un entero mayor que 0 (los booleanos no cuentan).

    Recibe:
        cantidad: el valor que se quiere validar.

    Lanza:
        ValueError: si no es un entero, es True o False, o es 0 o negativo.
    """
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero mayor que 0")


def _validar_existencias(producto_id, nuevo_total, existencias):
    """Revisa que el producto exista y que el total pedido no pase de las existencias.

    Recibe:
        producto_id: el id del producto.
        nuevo_total: las unidades que tendria el pedido de ese producto.
        existencias: las unidades disponibles de cada producto.

    Lanza:
        ProductoNoExisteError: si el producto no esta en las existencias.
        ExistenciasInsuficientesError: si el total pasa de las unidades disponibles.
    """
    if producto_id not in existencias:
        raise ProductoNoExisteError(f"El producto {producto_id} no existe")
    disponibles = existencias[producto_id]
    if nuevo_total > disponibles:
        raise ExistenciasInsuficientesError(f"Solo hay {disponibles} unidades disponibles")


def agregar_al_pedido(
    pedido: dict[int, int],
    producto_id: int,
    cantidad: int,
    existencias: dict[int, int],
) -> dict[int, int]:
    """Agrega un producto a un pedido sin pasarse de las existencias.

    Recibe:
        pedido: el pedido actual; cada llave es un id de producto y el valor es
            la cantidad que ya tiene. Puede estar vacio.
        producto_id: el id del producto que se quiere agregar.
        cantidad: cuantas unidades se quieren agregar (entero mayor que 0).
        existencias: las unidades disponibles de cada producto.

    Devuelve:
        Un pedido nuevo con la cantidad sumada. No modifica el pedido que recibio.

    Lanza:
        ValueError: si la cantidad no es un entero mayor que 0.
        ProductoNoExisteError: si el producto no esta en las existencias.
        ExistenciasInsuficientesError: si el total del producto pasa de las
            existencias; el mensaje dice cuantas unidades hay.
    """
    _validar_cantidad(cantidad)
    nuevo_total = pedido.get(producto_id, 0) + cantidad
    _validar_existencias(producto_id, nuevo_total, existencias)

    return {**pedido, producto_id: nuevo_total}