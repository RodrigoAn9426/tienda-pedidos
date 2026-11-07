class ProductoNoExisteError(Exception):
    pass


class ExistenciasInsuficientesError(Exception):
    pass


def agregar_al_pedido(pedido, producto_id, cantidad, existencias):
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad debe ser un entero mayor que 0")
    if producto_id not in existencias:
        raise ProductoNoExisteError(f"El producto {producto_id} no existe")
    disponibles = existencias[producto_id]
    nuevo_total = pedido.get(producto_id, 0) + cantidad
    if nuevo_total > disponibles:
        raise ExistenciasInsuficientesError(f"Solo hay {disponibles} unidades disponibles")
    nuevo_pedido = dict(pedido)
    nuevo_pedido[producto_id] = nuevo_total
    return nuevo_pedido