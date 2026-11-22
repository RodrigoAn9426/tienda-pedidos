import pytest

from cliente import validar_cliente
from confirmacion import ProductoNoDisponibleError, validar_confirmacion
from pedidos import agregar_al_pedido


def test_cliente_sintetico_valido_se_acepta(cliente_valido):
    resultado = validar_cliente(
        cliente_valido["nombre"], cliente_valido["cedula"], cliente_valido["telefono"]
    )
    assert resultado is True


def test_cliente_sintetico_invalido_falla_en_su_campo(cliente_invalido):
    with pytest.raises(ValueError, match=f"^{cliente_invalido['campo']}:"):
        validar_cliente(
            cliente_invalido["nombre"],
            cliente_invalido["cedula"],
            cliente_invalido["telefono"],
        )


def test_pedido_armado_con_existencias_de_la_tienda_se_confirma(existencias_tienda):
    pedido = agregar_al_pedido({}, 1, 2, existencias_tienda)  # 2 gaseosas
    pedido = agregar_al_pedido(pedido, 4, 1, existencias_tienda)  # el ultimo cafe
    assert pedido == {1: 2, 4: 1}
    assert validar_confirmacion(pedido, existencias_tienda) is True


def test_pedido_con_producto_agotado_no_se_confirma(existencias_tienda):
    pedido = {1: 2, 3: 1}  # la panela (id 3) tiene 0 unidades
    with pytest.raises(ProductoNoDisponibleError):
        validar_confirmacion(pedido, existencias_tienda)