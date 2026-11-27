# App de pedidos para un minimercado de barrio

## 1. Que es

Proyecto final del Seminario de Inteligencia Artificial Aplicada al Ciclo de Vida del Software. La idea es una app de pedidos para un minimercado de barrio: los vecinos ven los productos y piden desde el celular, y la dueña ve los pedidos en un solo lugar.

**Estado real del proyecto:** este repositorio tiene la logica de negocio de tres funciones, con sus pruebas, y el pipeline que las comprueba. **Todavia no tiene pagina web, servidor ni base de datos.** El diseno completo (ADR-001) usa Laravel y PostgreSQL; la logica se escribio en Python para practicar la regla de las pruebas primero, y la misma regla se llevara despues al servidor de la app.

| Funcion | Archivo | Historia | Que hace |
|---|---|---|---|
| `agregar_al_pedido` | `src/pedidos.py` | HU-02 | Agrega un producto al pedido sin pasarse de las existencias |
| `validar_cliente` | `src/cliente.py` | HU-04 | Comprueba el nombre, la cedula y el telefono del cliente |
| `validar_confirmacion` | `src/confirmacion.py` | HU-03 y HU-06 | Comprueba que un pedido no este vacio y que haya unidades de cada producto |

Los documentos de cada modulo (propuesta, requisitos, diseno, despliegue y operacion) estan en la carpeta `docs/`.

## 2. Requisitos

- Python 3.10 o superior (se probo con Python 3.14.5).
- Git.
- Docker, solo si quieres ejecutar la imagen (opcional).
- Dependencias de desarrollo, con versiones fijas en `requirements-dev.txt`: `pytest==9.2.0`, `ruff==0.17.5`, `pytest-cov==7.1.0` y `pip-audit==2.10.1`.

## 3. Instalacion

```
git clone https://github.com/RodrigoAn9426/tienda-pedidos.git
cd tienda-pedidos
pip install -r requirements-dev.txt
```

## 4. Ejecucion

Esta version son funciones, no una app con pantalla. Se pueden probar desde la terminal (Git Bash):

```
PYTHONPATH=src python -c "from pedidos import agregar_al_pedido; print(agregar_al_pedido({}, 1, 2, {1: 10}))"
PYTHONPATH=src python -c "from cliente import validar_cliente; print(validar_cliente('Ana Gomez', '1000000001', '3001234567'))"
PYTHONPATH=src python -c "from confirmacion import validar_confirmacion; print(validar_confirmacion({1: 2}, {1: 10}))"
```

Deben imprimir `{1: 2}`, `True` y `True`.

Con Docker, la imagen ejecuta las pruebas del proyecto (ver `docs/modulo-6-operacion/guia_despliegue.md`):

```
docker build -t tienda-pedidos .
docker run --rm tienda-pedidos
```

## 5. Pruebas

```
python -m pytest
```

Deben pasar las 57 pruebas. Para medir la cobertura:

```
python -m pytest --cov=src --cov-branch --cov-report=term-missing
```

La cobertura de las tres funciones es del 100 %. Para pasar el linter con reglas de estilo, errores y seguridad:

```
python -m ruff check .
```

Debe decir `All checks passed!`. Para revisar las dependencias:

```
python -m pip_audit -r requirements-dev.txt
```

El pipeline (`.github/workflows/ci.yml`) hace todo esto con cada push a `master` y cada pull request: corre ruff, pytest con una cobertura minima del 90 %, pip-audit, y construye la imagen y ejecuta las pruebas dentro. Las ejecuciones estan en https://github.com/RodrigoAn9426/tienda-pedidos/actions

## 6. Estructura

```
tienda-pedidos/
  src/pedidos.py           agregar_al_pedido y sus errores (HU-02)
  src/cliente.py           validar_cliente (HU-04)
  src/confirmacion.py      validar_confirmacion y sus errores (HU-03 y HU-06)
  tests/                   las 57 pruebas y los datos sinteticos (conftest.py)
  docs/                    documentos de los modulos 1, 2, 3 y 6
  .github/workflows/ci.yml pipeline de integracion continua
  Dockerfile               imagen que ejecuta las pruebas
  .dockerignore            archivos que no entran a la imagen
  bitacora_ia.md           registro de uso de IA
  registro_pruebas.md      reglas, tablas de casos y revision de las pruebas de la IA
  revision_seguridad.md    informe de la revision de calidad y seguridad
  informe_final.md y .pdf  informe final del proyecto
  requirements-dev.txt     dependencias con version fija
  pyproject.toml           configuracion del linter (ruff)
  pytest.ini               configuracion de las pruebas
  .env.example             ejemplo de variables de entorno (sin valores)
  .gitignore               archivos que no se suben (incluye .env)
```

## 7. Uso de IA

Se uso Claude (en modo chat) como asistente en todas las fases: la propuesta, los requisitos, el diseno, el codigo, las pruebas y el pipeline. Cada sugerencia se verifico ejecutando, comparando con la fuente o con el linter. Ninguna prueba se modifico para que el codigo pasara. El detalle esta en `bitacora_ia.md` (que se acepto, que se ajusto y que se rechazo), en `revision_seguridad.md`, en `registro_pruebas.md` y en `informe_final.md`.

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