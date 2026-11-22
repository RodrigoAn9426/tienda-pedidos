import pytest

from confirmacion import (
    PedidoVacioError,
    ProductoNoDisponibleError,
    validar_confirmacion,
)


@pytest.mark.parametrize(
    ("pedido", "existencias"),
    [
        ({1: 2}, {1: 10}),  # un producto disponible
        ({1: 2, 2: 1}, {1: 10, 2: 5}),  # varios, todos disponibles
        ({1: 3}, {1: 3}),  # límite: pide justo lo que hay
    ],
)
def test_pedido_con_existencias_suficientes_se_confirma(pedido, existencias):
    assert validar_confirmacion(pedido, existencias) is True


@pytest.mark.parametrize(
    ("pedido", "existencias"),
    [
        ({1: 4}, {1: 3}),  # límite: una unidad más de las que hay
        ({1: 2}, {1: 0}),  # producto agotado
        ({9: 1}, {1: 10}),  # producto que no está en las existencias
        ({1: 1, 2: 9}, {1: 5, 2: 3}),  # falla el segundo producto
    ],
)
def test_producto_no_disponible_lanza_error(pedido, existencias):
    with pytest.raises(ProductoNoDisponibleError):
        validar_confirmacion(pedido, existencias)


@pytest.mark.parametrize(
    "existencias",
    [
        {1: 10},  # decisión fila 1: pedido vacío con existencias
        {},  # decisión fila 1: pedido vacío sin existencias
    ],
)
def test_pedido_vacio_lanza_error(existencias):
    with pytest.raises(PedidoVacioError, match="Agrega al menos un producto"):
        validar_confirmacion({}, existencias)