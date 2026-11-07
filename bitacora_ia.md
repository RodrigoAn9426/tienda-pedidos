\# Bitácora de uso de IA



Proyecto: App de pedidos para un minimercado de barrio

Estudiante: Rodrigo Andres Rojas Perez

Funcionalidad: HU-02 Agregar un producto al pedido desde el catálogo

Asistente usado: Claude (modo chat)



\## Entradas



\### Entrada 1



\- \*\*Fecha:\*\* 2026-11-07

\- \*\*Prompt o sugerencia:\*\* El asistente propuso el README con la historia HU-02, el contrato de la función (firma, qué recibe, qué devuelve, casos límite, errores y 4 ejemplos) y la forma de ejecutar las pruebas.

\- \*\*Decisión:\*\* Aceptada con cambios

\- \*\*Por qué:\*\* El contrato servía, pero el comando `pytest` no lo reconocía mi terminal (no estaba en el PATH de Windows), así que lo cambié por `python -m pytest`.

\- \*\*Verificación:\*\* Ejecuté `python -m pytest` y funcionó.

\- \*\*Commit relacionado:\*\* 2012555 Inicio del proyecto: README con el contrato de HU-02



\### Entrada 2



\- \*\*Fecha:\*\* 2026-11-07

\- \*\*Prompt o sugerencia:\*\* El asistente propuso 11 pruebas con pytest: 3 normales, 2 de límite y 6 de error (cantidad 0, negativa, no entera, producto inexistente, pedir más de lo que hay y que el total pase de lo que hay).

\- \*\*Decisión:\*\* Aceptada

\- \*\*Por qué:\*\* Cubren el escenario de error de la historia y los casos límite del contrato (pedir justo lo que hay, completar justo las existencias).

\- \*\*Verificación:\*\* Las ejecuté antes de escribir el código y todas fallaron (`ModuleNotFoundError: No module named 'pedidos'`), lo que confirma que estaban en rojo.

\- \*\*Commit relacionado:\*\* db8db1a Pruebas de agregar producto al pedido (en rojo)



\### Entrada 3



\- \*\*Fecha:\*\* 2026-11-07

\- \*\*Prompt o sugerencia:\*\* El asistente propuso una primera versión de `agregar\_al\_pedido` que comparaba solo la cantidad nueva con las existencias.

\- \*\*Decisión:\*\* Aceptada con cambios

\- \*\*Por qué:\*\* No tenía en cuenta lo que ya estaba en el pedido: con 2 unidades en el pedido, pedir 2 más y solo haber 3, el código lo dejaba pasar. Cambié la comparación para usar el total (`nuevo\_total`).

\- \*\*Verificación:\*\* La prueba `test\_error\_si\_el\_total\_con\_lo\_que\_ya\_habia\_pasa\_de\_las\_existencias` falló (1 failed, 10 passed). Después de corregir pasaron las 11.

\- \*\*Commit relacionado:\*\* b76f838 Implementacion de agregar\_al\_pedido: pruebas en verde



\### Entrada 4



\- \*\*Fecha:\*\* 2026-11-07

\- \*\*Prompt o sugerencia:\*\* El asistente propuso un refactor: separar las validaciones en dos funciones con nombre claro, `\_validar\_cantidad` y `\_validar\_existencias`.

\- \*\*Decisión:\*\* Aceptada

\- \*\*Por qué:\*\* La función principal hacía varias cosas a la vez. Con las validaciones separadas se lee mejor y no cambia el comportamiento.

\- \*\*Verificación:\*\* Ejecuté `python -m pytest` sin tocar ninguna prueba y siguieron pasando las 11.

\- \*\*Commit relacionado:\*\* e4837b5 Refactor: separar las validaciones en funciones con nombre claro



\### Entrada 5



\- \*\*Fecha:\*\* 2026-11-07

\- \*\*Prompt o sugerencia:\*\* El asistente mencionó, como idea opcional, rechazar `True` y `False` como cantidad, porque en Python cuentan como enteros.

\- \*\*Decisión:\*\* Rechazada

\- \*\*Por qué:\*\* Cambia el comportamiento y ninguna prueba ni el contrato lo piden, así que no es un refactor. Lo dejo como idea para una próxima funcionalidad.

\- \*\*Verificación:\*\* No lo implementé; confirmé que las 11 pruebas pasan sin ese cambio.

\- \*\*Commit relacionado:\*\* Ninguno (no se implementó)



\### Entrada 6



\- \*\*Fecha:\*\* 2026-11-07

\- \*\*Prompt o sugerencia:\*\* El asistente notó que el contrato del README tenía la firma con tipos y el código no, y propuso agregarlos.

\- \*\*Decisión:\*\* Aceptada

\- \*\*Por qué:\*\* El contrato dice que la firma lleva tipos, y el código debe cumplir el contrato.

\- \*\*Verificación:\*\* Ejecuté `python -m pytest` después del cambio y pasaron las 11.

\- \*\*Commit relacionado:\*\* Agregar tipos a la firma de agregar\_al\_pedido segun el contrato



\## Resumen



| Decisión | Cantidad |

|---|---|

| Aceptadas | 3 |

| Aceptadas con cambios | 2 |

| Rechazadas | 1 |



\## Errores que atraparon las pruebas



La primera versión del código dejaba pasar un pedido que se pasaba de las existencias cuando el producto ya estaba en el pedido. La prueba `test\_error\_si\_el\_total\_con\_lo\_que\_ya\_habia\_pasa\_de\_las\_existencias` falló con `DID NOT RAISE ExistenciasInsuficientesError`. Entendí que había que comparar el total (lo que ya había más lo nuevo) y no solo la cantidad nueva. Lo corregí en el código sin tocar la prueba, y pasaron las 11.



\## Reflexión final (5 a 8 líneas)



El asistente me ayudó más escribiendo las pruebas y armando el código base, porque me ahorró mucho tiempo. Las pruebas atraparon un error real de la primera versión: no sumaba lo que ya había en el pedido. Escribirlas primero me obligó a pensar en los casos raros, como pedir justo lo que hay. También aprendí que el código se pega en el editor y no en la terminal, porque una vez la terminal se llenó de errores por pegar el código ahí. En la próxima funcionalidad le pediría al asistente que me explique cada línea antes de aceptarla, y agregaría una prueba para cantidades como `True` o `False`.

