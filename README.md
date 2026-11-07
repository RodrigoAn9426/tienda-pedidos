# App de pedidos para un minimercado de barrio

Proyecto final del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software.

Estudiante: Rodrigo Andres Rojas Perez

## Funcionalidad de la semana 5

### Historia de usuario

**HU-02.** Como cliente, quiero agregar un producto a mi pedido desde el mismo catalogo para pedir sin salir de esa pantalla. (Necesidad de origen: N-02)

Criterios de aceptacion:

- **Escenario 1: agregar producto.** Dado que "Gaseosa 1,5 L" tiene 10 unidades, cuando agrego 2 unidades desde el catalogo, entonces mi pedido muestra "Gaseosa 1,5 L x 2".
- **Escenario 2 (error): mas de lo que hay.** Dado que "Gaseosa 1,5 L" tiene 3 unidades, cuando intento agregar 5, entonces el sistema me avisa que solo hay 3 y no agrega las 5.

### Contrato de la funcion

Archivo: `src/pedidos.py`

```python
def agregar_al_pedido(
    pedido: dict[int, int],
    producto_id: int,
    cantidad: int,
    existencias: dict[int, int],
) -> dict[int, int]:
```

**Que recibe**

- `pedido`: el pedido actual. Cada llave es el id de un producto y el valor es la cantidad que ya esta en el pedido. Puede estar vacio.
- `producto_id`: el id del producto que se quiere agregar.
- `cantidad`: cuantas unidades se quieren agregar. Debe ser un numero entero mayor que 0.
- `existencias`: las unidades que hay de cada producto. Cada llave es el id de un producto y el valor son las unidades disponibles.

**Que devuelve**

Un pedido nuevo (un diccionario) con la cantidad agregada. No modifica el pedido que recibio.

**Supuestos**

- Los ids de producto son numeros enteros.
- Las existencias ya vienen cargadas; la funcion no las cambia.
- El total del producto en el pedido (lo que ya habia mas lo nuevo) no puede pasar de las existencias.

**Casos limite**

- Pedir justo las unidades que hay (por ejemplo 3 de 3) esta permitido.
- Agregar a un pedido vacio funciona.
- Agregar un producto que ya estaba en el pedido suma las cantidades.
- Cantidad 0 o negativa es un error.
- Un producto que no esta en las existencias es un error.
- Pedir mas de lo que hay es un error y el pedido no cambia.

**Errores**

- `ValueError` si la cantidad no es un entero mayor que 0.
- `ProductoNoExisteError` si el producto no esta en las existencias.
- `ExistenciasInsuficientesError` si el total pasa de las existencias. Su mensaje dice cuantas unidades hay, por ejemplo: "Solo hay 3 unidades disponibles".

**Ejemplos**

| Entrada | Salida |
|---|---|
| `agregar_al_pedido({}, 1, 2, {1: 10})` | `{1: 2}` |
| `agregar_al_pedido({1: 2}, 1, 3, {1: 10})` | `{1: 5}` |
| `agregar_al_pedido({}, 1, 3, {1: 3})` | `{1: 3}` |
| `agregar_al_pedido({}, 1, 5, {1: 3})` | Error: `ExistenciasInsuficientesError("Solo hay 3 unidades disponibles")` |

### Como ejecutar las pruebas

```
pip install pytest
python -m pytest
```

### Nota de diseno

El diseno del proyecto (ADR-001) usa Laravel y PostgreSQL. Esta primera funcionalidad se escribio en Python para practicar la regla de las existencias con pruebas primero; la misma regla se llevara despues al servidor de la app.