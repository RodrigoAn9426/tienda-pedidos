# Informe de revision de calidad y seguridad

Proyecto: tienda-pedidos (app de pedidos de un minimercado). Autor: Rodrigo Andres Rojas Perez. Fecha: 14/11/2026.

## 1. Herramientas y criterios usados

- Linter: ruff 0.17.5, configurado en `pyproject.toml` con las reglas E, F (estilo y errores), B (errores probables) y S (seguridad). En `tests/` se ignora S101 porque `assert` es normal en pytest. Resultado: `All checks passed!`.

- Pruebas: pytest 9.2.0, 13 pruebas pasando (11 originales y 2 nuevas de abuso).

- Dependencias: `requirements-dev.txt` con versiones fijas; `pip-audit` dijo `No known vulnerabilities found`.

- Segunda revision con un asistente de IA (Claude), con un prompt que pedia criterios, tabla con linea y severidad, y separar problemas seguros de sospechas.

Revision de los cinco puntos:

| Punto | Resultado |
|---|---|
| Inyeccion | No aplica: el proyecto todavia no tiene base de datos ni consultas. Cuando la tenga, todas usaran parametros. |
| Secretos | Revisado. Corri `git log -p --all` con grep buscando password, secret, api_key, token y sk-, y `git log --all --full-history -- .env`. Los dos salieron sin ningun resultado. Nunca subi una clave al repositorio. `.env` esta en `.gitignore` y existe `.env.example` sin valores. |
| Contrasenas | No aplica: el proyecto no guarda contrasenas. Si despues hay inicio de sesion, se usara scrypt, bcrypt o argon2. |
| Control de acceso | No aplica por ahora: la funcion no tiene roles. Queda pendiente para la lista de pedidos de la duena (HU-05). |
| Dependencias | Solo pytest y ruff, con version fija y pip-audit sin vulnerabilidades. |

## 2. Tabla de hallazgos

Las lineas son las del archivo `src/pedidos.py` antes de los cambios.

| Linea | Problema | Categoria | Severidad | Correccion | Commit |
|---|---|---|---|---|---|
| 10 | `True` y `False` se aceptaban como cantidad (`agregar_al_pedido({}, 1, True, {1: 10})` daba `{1: 1}`) | Validacion de entradas | Baja | `_validar_cantidad` rechaza los booleanos; prueba de abuso nueva | `05e5e68` (prueba), `1120c41` (arreglo) |
| 1, 5, 9, 14, 22 | Clases y funciones sin docstring | Documentacion | Baja | Docstrings con que recibe, que devuelve y que errores lanza | `f819373` |
| Final de la funcion | Tres lineas para copiar, asignar y devolver el pedido | Legibilidad | Baja | Una sola expresion: `return {**pedido, producto_id: nuevo_total}` | `f8fc7d7` |
| Todo el repositorio | README sin las ocho secciones | Documentacion | Baja | README con las ocho secciones y contrato actualizado | `2295633` |
| Todo el repositorio | Sin linter, sin `.env.example` y sin versiones fijas | Calidad y secretos | Baja | Se agregaron ruff, `.env.example` y `requirements-dev.txt` con pip-audit | `5f65840`, `7d32f1f`, `603dda6` |

Ninguna prueba se modifico para que pasara. Lo comprobe con `git diff 603dda6 05e5e68 -- tests/`: la unica linea cambiada fue el salto de linea final de la ultima prueba.

## 3. Revision con IA

La IA devolvio estos hallazgos. Yo verifique cada uno corriendo el codigo.

| Hallazgo de la IA | Que comprobe | Clasificacion |
|---|---|---|
| `True` aceptado como cantidad | Imprimio `{1: 1}` | Real (corregido) |
| Sin docstrings | Es cierto | Real (corregido) |
| Existencias negativas dan el mensaje "Solo hay -3 unidades" | Da `ExistenciasInsuficientesError` con ese texto | Falso positivo: segun el contrato las existencias vienen del sistema, no de un usuario |
| Pedido con valor `'2'` falla con TypeError | Da `TypeError` | Falso positivo: el contrato exige enteros y quien rompe el contrato recibe el error |
| `ValueError` en vez de `TypeError` para un tipo equivocado | Lo revise contra el contrato | Falso positivo: el contrato define `ValueError` para cantidad invalida |
| Mensajes de error con `producto_id` | Lo revise contra el contrato | Falso positivo: los ids son numeros enteros por contrato |
| Dos clases con `pass` | Lo revise en el codigo | Falso positivo: es la forma normal de crear errores propios |

**Algo importante que la IA no encontro:** la IA solo reviso un archivo. No pudo ver que el repositorio todavia no tiene control de acceso para la lista de pedidos de la duena (HU-05), que solo ella deberia ver. Tampoco vio que faltaba el `.env.example` ni las versiones fijas de las dependencias, que son cosas del repositorio completo y no de un archivo.

No use un agente de codigo en esta tarea: todos los cambios los hice yo, a mano, con commits separados.

## 4. Pendientes

- Control de acceso para la lista de pedidos (HU-05), con su prueba de abuso, cuando exista.

- Si se agrega base de datos: consultas con parametros.

- Si se agrega inicio de sesion: contrasenas con scrypt, bcrypt o argon2.

- Volver a pasar `pip-audit` cada vez que cambien las dependencias.

