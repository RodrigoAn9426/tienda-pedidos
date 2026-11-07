class ProductoNoExisteError(Exception):
    pass


class ExistenciasInsuficientesError(Exception):
    pass


def _validar_cantidad(cantidad):
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero mayor que 0")


def _validar_existencias(producto_id, nuevo_total, existencias):
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
    _validar_cantidad(cantidad)
    nuevo_total = pedido.get(producto_id, 0) + cantidad
    _validar_existencias(producto_id, nuevo_total, existencias)

    nuevo_pedido = dict(pedido)
    nuevo_pedido[producto_id] = nuevo_total
    return nuevo_pedido