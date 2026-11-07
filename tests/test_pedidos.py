import pytest

from pedidos import (
    ExistenciasInsuficientesError,
    ProductoNoExisteError,
    agregar_al_pedido,
)


# ---------- Casos normales ----------

def test_agrega_producto_a_un_pedido_vacio():
    resultado = agregar_al_pedido({}, 1, 2, {1: 10})
    assert resultado == {1: 2}


def test_suma_la_cantidad_si_el_producto_ya_estaba_en_el_pedido():
    resultado = agregar_al_pedido({1: 2}, 1, 3, {1: 10})
    assert resultado == {1: 5}


def test_no_modifica_el_pedido_que_recibio():
    pedido = {1: 2}
    agregar_al_pedido(pedido, 1, 3, {1: 10})
    assert pedido == {1: 2}


# ---------- Casos limite ----------

def test_permite_pedir_justo_las_unidades_que_hay():
    resultado = agregar_al_pedido({}, 1, 3, {1: 3})
    assert resultado == {1: 3}


def test_permite_completar_justo_las_existencias_con_lo_que_ya_habia():
    resultado = agregar_al_pedido({1: 2}, 1, 1, {1: 3})
    assert resultado == {1: 3}


# ---------- Casos de error ----------

def test_error_si_pide_mas_de_lo_que_hay_y_el_pedido_no_cambia():
    pedido = {}
    with pytest.raises(ExistenciasInsuficientesError, match="Solo hay 3 unidades disponibles"):
        agregar_al_pedido(pedido, 1, 5, {1: 3})
    assert pedido == {}


def test_error_si_el_total_con_lo_que_ya_habia_pasa_de_las_existencias():
    with pytest.raises(ExistenciasInsuficientesError):
        agregar_al_pedido({1: 2}, 1, 2, {1: 3})


def test_error_si_la_cantidad_es_cero():
    with pytest.raises(ValueError):
        agregar_al_pedido({}, 1, 0, {1: 10})


def test_error_si_la_cantidad_es_negativa():
    with pytest.raises(ValueError):
        agregar_al_pedido({}, 1, -2, {1: 10})


def test_error_si_la_cantidad_no_es_un_entero():
    with pytest.raises(ValueError):
        agregar_al_pedido({}, 1, 2.5, {1: 10})


def test_error_si_el_producto_no_existe():
    with pytest.raises(ProductoNoExisteError):
        agregar_al_pedido({}, 99, 1, {1: 10})