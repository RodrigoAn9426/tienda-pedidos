"""Validacion para confirmar un pedido (HU-03 y HU-06)."""


class PedidoVacioError(Exception):
    """El pedido no tiene productos."""


class ProductoNoDisponibleError(Exception):
    """Un producto del pedido ya no tiene las unidades pedidas."""


def validar_confirmacion(pedido: dict[int, int], existencias: dict[int, int]) -> bool:
    """Comprueba que un pedido se puede confirmar.

    Recibe:
        pedido: llave = id del producto, valor = unidades pedidas (enteros > 0).
        existencias: llave = id del producto, valor = unidades que hay.

    Devuelve:
        True si el pedido tiene productos y hay unidades para todos.

    Lanza:
        PedidoVacioError: si el pedido no tiene productos. Se revisa primero.
        ProductoNoDisponibleError: si algun producto no esta en las
            existencias o tiene menos unidades de las pedidas.
    """
    if not pedido:
        raise PedidoVacioError("Agrega al menos un producto")
    for producto_id, cantidad in pedido.items():
        if existencias.get(producto_id, 0) < cantidad:
            raise ProductoNoDisponibleError(
                f"El producto {producto_id} ya no esta disponible"
            )
    return True