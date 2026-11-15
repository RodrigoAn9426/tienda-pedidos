# Informe de revisión de código y seguridad

Proyecto: tienda-pedidos (app de pedidos de un minimercado de barrio, en Python)
Estudiante: Rodrigo Andrés Rojas Pérez
Fecha: 2026-11-14
Commit revisado: 603dda6 (último commit antes de la revisión con IA y las correcciones)

## 1. Herramientas y criterios

- **Linter:** ruff 0.17.5 con las reglas E, F, B y S. Configuración en pyproject.toml. Resultado final: `All checks passed!`.
- **Auditoría de dependencias:** pip-audit sobre requirements-dev.txt (pytest 9.2.0 y ruff 0.17.5, con versión fija) — resultado: sin vulnerabilidades conocidas.
- **Lista de revisión:** la de la semana 6 (corrección y pruebas, diseño y legibilidad, seguridad).
- **Revisión con IA:** Claude (chat) con el prompt de revisión de la semana (ver sección 3 y la entrada 7 de la bitácora).

### Puntos de seguridad revisados

| Punto | ¿Aplica? | Resultado |
|---|---|---|
| Inyección (consultas con parámetros) | No, porque el proyecto todavía no tiene base de datos ni consultas. Cuando la tenga, todas usarán parámetros. | Sin hallazgos |
| Secretos (código, historial, .gitignore, .env.example) | Sí | Corrí `git log -p --all` con grep buscando password, secret, api_key, token y sk-, y `git log --all --full-history -- .env`. Los dos salieron sin resultados. `.env` está en .gitignore y existe .env.example sin valores. Sin hallazgos. |
| Contraseñas (scrypt, bcrypt o argon2 con sal) | No, porque el proyecto no guarda contraseñas. Si más adelante hay inicio de sesión, se usará scrypt, bcrypt o argon2. | Sin hallazgos |
| Control de acceso (rol verificado y prueba de abuso) | No por ahora, porque la función no tiene roles ni usuarios. Queda pendiente para la lista de pedidos de la dueña (HU-05). | Ver Pendientes |
| Dependencias (existen, necesarias, versión fijada, pip-audit) | Sí | Solo pytest y ruff, ambas necesarias, con versión fija; pip-audit sin vulnerabilidades. Sin hallazgos. |

## 2. Tabla de hallazgos

Las líneas son las de src/pedidos.py antes de los cambios.

| Id | Archivo y línea | Problema | Categoría (OWASP o tipo) | Severidad | Corrección | Commit |
|---|---|---|---|---|---|---|
| H-01 | src/pedidos.py:10 | `True` y `False` se aceptaban como cantidad (`agregar_al_pedido({}, 1, True, {1: 10})` devolvía `{1: 1}`) | Validación de entradas | Baja | `_validar_cantidad` rechaza los booleanos; prueba de abuso nueva (`test_error_si_la_cantidad_es_un_booleano`) | 05e5e68 (prueba en rojo), 1120c41 (corrección) |
| H-02 | src/pedidos.py:1, 5, 9, 14, 22 | Clases y funciones sin docstring | Mantenibilidad | Baja | Docstrings con qué recibe, qué devuelve y qué errores lanza | f819373 |
| H-03 | src/pedidos.py (final de `agregar_al_pedido`) | Tres líneas para copiar, asignar y devolver el pedido | Legibilidad | Baja | Una sola expresión: `return {**pedido, producto_id: nuevo_total}` | f8fc7d7 |
| H-04 | Repositorio completo | README sin las ocho secciones | Mantenibilidad | Baja | README con las ocho secciones y contrato actualizado | 2295633 |
| H-05 | Repositorio completo | Sin linter configurado, sin .env.example y sin versiones fijas | Calidad y secretos | Baja | Se agregaron ruff en pyproject.toml, .env.example y requirements-dev.txt con pip-audit | 5f65840, 7d32f1f, 603dda6 |

**Severidad:** alta (permite acceder o cambiar datos sin permiso, o expone secretos), media (error probable o riesgo con condiciones), baja (estilo o mantenibilidad).

Ninguna prueba se modificó para que pasara. Lo comprobé con `git diff 603dda6 05e5e68 -- tests/`: la única línea cambiada fue el salto de línea final de la última prueba anterior.

### Avisos del linter no corregidos

| Regla | Archivo y línea | Por qué se mantiene |
|---|---|---|
| S101 | tests/test_pedidos.py | `assert` es la forma normal de comprobar en pytest; se ignora solo en tests/ con per-file-ignores en pyproject.toml |

## 3. Revisión con IA

**Prompt usado:** prompt de revisión de código senior con criterios (errores no manejados, seguridad, legibilidad y docstrings), con mi `cat -n src/pedidos.py` pegado, pidiendo tabla con línea, problema, categoría, severidad y cómo arreglarlo, y separando problemas seguros de sospechas (entrada 7 de la bitácora).

| Hallazgo de la IA | ¿Real o falso positivo? | Cómo lo verifiqué |
|---|---|---|
| `True` aceptado como cantidad (línea 10) | Real | Corrí la función con `True` y devolvió `{1: 1}`; la prueba nueva falló antes de corregir (H-01) |
| Clases y funciones sin docstring | Real | Lo vi en el archivo (H-02) |
| Existencias negativas dan el mensaje "Solo hay -3 unidades" | Falso positivo | Lo corrí y da ese mensaje, pero el contrato dice que las existencias vienen del sistema, no de un usuario |
| Pedido con valor `'2'` falla con TypeError | Falso positivo | Lo corrí y da TypeError; el contrato exige enteros y quien rompe el contrato recibe el error |
| `ValueError` en vez de `TypeError` para un tipo equivocado | Falso positivo | Lo revisé contra el contrato, que define `ValueError` para una cantidad inválida |
| Mensajes de error con `producto_id` | Falso positivo | Lo revisé en el código: los ids son números enteros por contrato |
| Dos clases con `pass` | Falso positivo | Lo revisé en el código: es la forma normal de crear errores propios |

**Lo que la IA no encontró:** la IA solo revisó un archivo. No pudo ver que el repositorio todavía no tiene control de acceso para la lista de pedidos de la dueña (HU-05), que solo ella debería ver. Tampoco vio que faltaban el .env.example y las versiones fijas de las dependencias (H-05), que son cosas del repositorio completo y no de un archivo.

No usé un agente de código en esta tarea: todos los cambios los hice yo, con commits separados.

## 4. Pendientes

| Pendiente | Por qué no se corrigió todavía | Plan |
|---|---|---|
| Control de acceso para la lista de pedidos (HU-05) | La funcionalidad todavía no existe | Verificar el rol de la dueña y agregar una prueba de abuso cuando se construya |
| Consultas con parámetros | Todavía no hay base de datos | Usar parámetros en todas las consultas cuando se agregue |
| Contraseñas con scrypt, bcrypt o argon2 | Todavía no hay inicio de sesión | Usar una de esas tres con sal si se agrega |
| Volver a pasar pip-audit | Las dependencias no han cambiado | Correrlo cada vez que cambie requirements-dev.txt |

**Claves expuestas:** Ninguna.
