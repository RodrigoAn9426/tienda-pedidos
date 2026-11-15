# App de pedidos para un minimercado de barrio

## 1. Que es

Proyecto final del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software. La idea es una app de pedidos para un minimercado de barrio: los vecinos ven los productos y piden desde el celular, y la dueña ve los pedidos en un solo lugar.

Este primer incremento tiene una funcionalidad: agregar un producto a un pedido sin pasarse de las existencias (HU-02). El diseno completo del proyecto (ADR-001) usa Laravel y PostgreSQL; esta primera pieza se escribio en Python para practicar la regla de las existencias con pruebas primero, y la misma regla se llevara despues al servidor de la app.

## 2. Requisitos

- Python 3.10 o superior (se probo con Python 3.14.5).
- Git.
- Dependencias de desarrollo, con versiones fijas en `requirements-dev.txt`: `pytest==9.2.0` y `ruff==0.17.5`.

## 3. Instalacion

```
git clone https://github.com/RodrigoAn9426/tienda-pedidos.git
cd tienda-pedidos
pip install -r requirements-dev.txt
```

## 4. Ejecucion

Esta primera version es una funcion, no una app con pantalla. Se puede probar desde la terminal (Git Bash):

```
PYTHONPATH=src python -c "from pedidos import agregar_al_pedido; print(agregar_al_pedido({}, 1, 2, {1: 10}))"
```

Debe imprimir `{1: 2}`.

## 5. Pruebas

```
python -m pytest
```

Deben pasar las 13 pruebas. Para pasar el linter con reglas de estilo, errores y seguridad:

```
python -m ruff check .
```

Debe decir `All checks passed!`. Para revisar las dependencias:

```
pip install pip-audit
python -m pip_audit -r requirements-dev.txt
```

## 6. Estructura

```
tienda-pedidos/
  src/pedidos.py              la funcion agregar_al_pedido y sus errores
  tests/test_pedidos.py       las 13 pruebas
  bitacora_ia.md              registro de uso de IA
  revision_seguridad.md       informe de la revision de calidad y seguridad
  requirements-dev.txt        dependencias con version fija
  pyproject.toml              configuracion del linter (ruff)
  pytest.ini                  configuracion de las pruebas
  .env.example                ejemplo de variables de entorno (sin valores)
  .gitignore                  archivos que no se suben (incluye .env)
```

## 7. Uso de IA

Se uso Claude (en modo chat) como asistente para proponer el contrato, las pruebas, la primera version del codigo, el refactor, los docstrings y una segunda revision de seguridad. Cada sugerencia se verifico ejecutando las pruebas y el linter. Ninguna prueba se modifico para que el codigo pasara. El detalle esta en `bitacora_ia.md` (que se acepto, que se ajusto y que se rechazo) y en `revision_seguridad.md` (hallazgos de la revision y cuales eran reales).

## 8. Autor y licencia

Autor: Rodrigo Andres Rojas Perez, Fundacion Escuela Tecnologica Jesus Oviedo Perez (Neiva, Huila), 2026.

Licencia: proyecto academico de uso educativo, sin licencia de distribucion.

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
- Las existencias ya vienen cargadas y son correctas; la funcion no las cambia.
- El total del producto en el pedido (lo que ya habia mas lo nuevo) no puede pasar de las existencias.

**Casos limite**

- Pedir justo las unidades que hay (por ejemplo 3 de 3) esta permitido.
- Agregar a un pedido vacio funciona.
- Agregar un producto que ya estaba en el pedido suma las cantidades.
- Cantidad 0 o negativa es un error.
- `True` y `False` no se aceptan como cantidad (es un error).
- Un producto que no esta en las existencias es un error.
- Pedir mas de lo que hay es un error y el pedido no cambia.

**Errores**

- `ValueError` si la cantidad no es un entero mayor que 0 (incluye 0, negativos, decimales y booleanos).
- `ProductoNoExisteError` si el producto no esta en las existencias.
- `ExistenciasInsuficientesError` si el total pasa de las existencias. Su mensaje dice cuantas unidades hay, por ejemplo: "Solo hay 3 unidades disponibles".

**Ejemplos**

| Entrada | Salida |
|---|---|
| `agregar_al_pedido({}, 1, 2, {1: 10})` | `{1: 2}` |
| `agregar_al_pedido({1: 2}, 1, 3, {1: 10})` | `{1: 5}` |
| `agregar_al_pedido({}, 1, 3, {1: 3})` | `{1: 3}` |
| `agregar_al_pedido({}, 1, 5, {1: 3})` | Error: `ExistenciasInsuficientesError("Solo hay 3 unidades disponibles")` |
| `agregar_al_pedido({}, 1, True, {1: 10})` | Error: `ValueError` |