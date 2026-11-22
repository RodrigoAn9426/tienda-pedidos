import pytest

from pedidos import (
    ExistenciasInsuficientesError,
    ProductoNoExisteError,
    agregar_al_pedido,
)


@pytest.mark.parametrize(
    ("pedido", "producto_id", "cantidad", "existencias", "esperado"),
    [
        ({}, 1, 2, {1: 10}, {1: 2}),  # pedido vacío
        ({1: 2}, 1, 3, {1: 10}, {1: 5}),  # el producto ya estaba: suma
        ({}, 1, 1, {1: 10}, {1: 1}),  # límite: primera cantidad válida
        ({}, 1, 3, {1: 3}, {1: 3}),  # límite: total igual a las existencias
        ({1: 2}, 1, 1, {1: 3}, {1: 3}),  # límite con suma: justo en el tope
    ],
)
def test_agrega_cantidades_validas(pedido, producto_id, cantidad, existencias, esperado):
    assert agregar_al_pedido(pedido, producto_id, cantidad, existencias) == esperado


@pytest.mark.parametrize(
    "cantidad",
    [
        0,  # límite: último valor inválido
        -1,  # negativa
        True,  # booleano
        False,  # booleano
        2.5,  # decimal
    ],
)
def test_cantidad_invalida_lanza_value_error(cantidad):
    with pytest.raises(ValueError):
        agregar_al_pedido({}, 1, cantidad, {1: 10})


@pytest.mark.parametrize(
    ("pedido", "cantidad"),
    [
        ({}, 4),  # límite: una unidad más que las existencias
        ({1: 2}, 2),  # límite con suma: 2 + 2 pasa de 3
    ],
)
def test_total_mayor_a_las_existencias_lanza_error(pedido, cantidad):
    with pytest.raises(ExistenciasInsuficientesError):
        agregar_al_pedido(pedido, 1, cantidad, {1: 3})


def test_producto_que_no_existe_lanza_error():
    with pytest.raises(ProductoNoExisteError):
        agregar_al_pedido({}, 9, 1, {1: 10})


def test_no_modifica_el_pedido_original():
    pedido = {1: 2}
    agregar_al_pedido(pedido, 1, 3, {1: 10})
    assert pedido == {1: 2}