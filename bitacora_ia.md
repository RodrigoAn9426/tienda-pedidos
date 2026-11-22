# Bitácora de uso de IA



Proyecto: App de pedidos para un minimercado de barrio

Estudiante: Rodrigo Andres Rojas Perez

Funcionalidad: HU-02 Agregar un producto al pedido desde el catálogo

Asistente usado: Claude (modo chat)



## Entradas



### Entrada 1



- **Fecha:** 2026-11-07

- **Prompt o sugerencia:** El asistente propuso el README con la historia HU-02, el contrato de la función (firma, qué recibe, qué devuelve, casos límite, errores y 4 ejemplos) y la forma de ejecutar las pruebas.

- **Decisión:** Aceptada con cambios

- **Por qué:** El contrato servía, pero el comando `pytest` no lo reconocía mi terminal (no estaba en el PATH de Windows), así que lo cambié por `python -m pytest`.

- **Verificación:** Ejecuté `python -m pytest` y funcionó.

- **Commit relacionado:** 2012555 Inicio del proyecto: README con el contrato de HU-02



### Entrada 2



- **Fecha:** 2026-11-07

- **Prompt o sugerencia:** El asistente propuso 11 pruebas con pytest: 3 normales, 2 de límite y 6 de error (cantidad 0, negativa, no entera, producto inexistente, pedir más de lo que hay y que el total pase de lo que hay).

- **Decisión:** Aceptada

- **Por qué:** Cubren el escenario de error de la historia y los casos límite del contrato (pedir justo lo que hay, completar justo las existencias).

- **Verificación:** Las ejecuté antes de escribir el código y todas fallaron (`ModuleNotFoundError: No module named 'pedidos'`), lo que confirma que estaban en rojo.

- **Commit relacionado:** db8db1a Pruebas de agregar producto al pedido (en rojo)



### Entrada 3



- **Fecha:** 2026-11-07

- **Prompt o sugerencia:** El asistente propuso una primera versión de `agregar_al_pedido` que comparaba solo la cantidad nueva con las existencias.

- **Decisión:** Aceptada con cambios

- **Por qué:** No tenía en cuenta lo que ya estaba en el pedido: con 2 unidades en el pedido, pedir 2 más y solo haber 3, el código lo dejaba pasar. Cambié la comparación para usar el total (`nuevo_total`).

- **Verificación:** La prueba `test_error_si_el_total_con_lo_que_ya_habia_pasa_de_las_existencias` falló (1 failed, 10 passed). Después de corregir pasaron las 11.

- **Commit relacionado:** b76f838 Implementacion de agregar_al_pedido: pruebas en verde



### Entrada 4



- **Fecha:** 2026-11-07

- **Prompt o sugerencia:** El asistente propuso un refactor: separar las validaciones en dos funciones con nombre claro, `_validar_cantidad` y `_validar_existencias`.

- **Decisión:** Aceptada

- **Por qué:** La función principal hacía varias cosas a la vez. Con las validaciones separadas se lee mejor y no cambia el comportamiento.

- **Verificación:** Ejecuté `python -m pytest` sin tocar ninguna prueba y siguieron pasando las 11.

- **Commit relacionado:** e4837b5 Refactor: separar las validaciones en funciones con nombre claro



### Entrada 5



- **Fecha:** 2026-11-07

- **Prompt o sugerencia:** El asistente mencionó, como idea opcional, rechazar `True` y `False` como cantidad, porque en Python cuentan como enteros.

- **Decisión:** Rechazada

- **Por qué:** Cambia el comportamiento y ninguna prueba ni el contrato lo piden, así que no es un refactor. Lo dejo como idea para una próxima funcionalidad.

- **Verificación:** No lo implementé; confirmé que las 11 pruebas pasan sin ese cambio.

- **Commit relacionado:** Ninguno (no se implementó)



### Entrada 6



- **Fecha:** 2026-11-07

- **Prompt o sugerencia:** El asistente notó que el contrato del README tenía la firma con tipos y el código no, y propuso agregarlos.

- **Decisión:** Aceptada

- **Por qué:** El contrato dice que la firma lleva tipos, y el código debe cumplir el contrato.

- **Verificación:** Ejecuté `python -m pytest` después del cambio y pasaron las 11.

- **Commit relacionado:** Agregar tipos a la firma de agregar_al_pedido segun el contrato



## Resumen



| Decisión | Cantidad |

|---|---|

| Aceptadas | 3 |

| Aceptadas con cambios | 2 |

| Rechazadas | 1 |



## Errores que atraparon las pruebas



La primera versión del código dejaba pasar un pedido que se pasaba de las existencias cuando el producto ya estaba en el pedido. La prueba `test_error_si_el_total_con_lo_que_ya_habia_pasa_de_las_existencias` falló con `DID NOT RAISE ExistenciasInsuficientesError`. Entendí que había que comparar el total (lo que ya había más lo nuevo) y no solo la cantidad nueva. Lo corregí en el código sin tocar la prueba, y pasaron las 11.



## Reflexión final (5 a 8 líneas)



El asistente me ayudó más escribiendo las pruebas y armando el código base, porque me ahorró mucho tiempo. Las pruebas atraparon un error real de la primera versión: no sumaba lo que ya había en el pedido. Escribirlas primero me obligó a pensar en los casos raros, como pedir justo lo que hay. También aprendí que el código se pega en el editor y no en la terminal, porque una vez la terminal se llenó de errores por pegar el código ahí. En la próxima funcionalidad le pediría al asistente que me explique cada línea antes de aceptarla, y agregaría una prueba para cantidades como `True` o `False`.

### Entrada 7 - Revision con IA del codigo (14/11/2026)
- Prompt o sugerencia: le envie a Claude (en modo chat) un prompt de revision de codigo senior con criterios (errores no manejados, seguridad, legibilidad y docstrings), con mi `cat -n src/pedidos.py` pegado. Pedi una tabla con linea, problema, categoria, severidad y como arreglarlo, separando los problemas seguros de las sospechas.
- Respuesta de la IA: 2 problemas seguros (los booleanos aceptados como cantidad y la falta de docstrings) y 5 sospechas (existencias negativas, pedido con valores que no son numeros, ValueError en vez de TypeError, mensajes con el id del producto y dos clases con pass).
- Decision: acepte los 2 problemas seguros y rechace las 5 sospechas como falsos positivos.
- Razon: las 5 sospechas tienen una explicacion en el contrato del README: las existencias vienen del sistema y no de un usuario, el pedido y los ids son enteros por contrato, el contrato define ValueError para una cantidad invalida y las clases con pass son la forma normal de crear errores propios.
- Verificacion: corri 3 comandos para comprobar los hallazgos y vi el resultado de cada uno. Con True imprimio {1: 1} (real). Con existencias en -3 dio el mensaje raro, pero el contrato lo permite. Con el pedido {1: '2'} dio TypeError, que es lo esperado si se rompe el contrato.
- Algo que la IA no vio: solo reviso un archivo, asi que no pudo ver que el repositorio aun no tiene control de acceso para la lista de pedidos de la duena (HU-05).
- Commit relacionado: 05e5e68, 1120c41 y f819373.

### Entrada 8 - Correccion de los booleanos como cantidad (14/11/2026)
- Prompt o sugerencia: la IA propuso rechazar True y False en `_validar_cantidad`, agregando primero una prueba de abuso que fallara.
- Decision: aceptada.
- Razon: en Python True y False cuentan como enteros, entonces `agregar_al_pedido({}, 1, True, {1: 10})` devolvia {1: 1}, y el contrato del README dice que los booleanos no se aceptan como cantidad.
- Verificacion: agregue la prueba nueva y fallo primero (1 failed, 12 passed), lo que confirmo que el problema era real. Despues de corregir pasaron las 13 pruebas y ruff dijo All checks passed. No modifique ninguna de las 11 pruebas anteriores: con git diff comprobe que lo unico que cambio fue el salto de linea final del archivo.
- Commit relacionado: 05e5e68 (prueba en rojo) y 1120c41 (correccion).

### Entrada 9 - Docstrings de las funciones (14/11/2026)
- Prompt o sugerencia: le pedi a la IA un borrador de docstrings para las funciones y los errores, con que recibe, que devuelve y que errores lanza.
- Decision: aceptada, despues de leer cada docstring y compararlo con el codigo.
- Razon: la tarea pide que el docstring diga lo que de verdad hace la funcion, y el borrador tenia que coincidir con el codigo.
- Verificacion: lei los docstrings uno por uno y comprobe que coincidieran, por ejemplo que `agregar_al_pedido` devuelve un pedido nuevo con `{**pedido, ...}` y no modifica el que recibe, y que lanza los tres errores que dice. Las 13 pruebas siguen pasando y ruff queda limpio.
- Commit relacionado: f819373.

### Entrada 10 - Diseño de casos con IA (22/11/2026)
- Prompt o sugerencia: le pedí a Claude (en el chat) que a partir de las historias HU-02, HU-03, HU-04 y HU-06 propusiera tres funciones con reglas y las tablas de casos, con particiones de equivalencia, valores límite y tablas de decisión.
- Respuesta de la IA: propuso agregar_al_pedido, validar_cliente (HU-04) y validar_confirmacion (HU-03 y HU-06), con sus tablas y con decisiones sobre lo que las historias no dicen (nombre de dos palabras, cédula de 6 a 10 dígitos, teléfono de 10 dígitos que empieza por 3).
- Decisión: acepté las tres funciones y esas decisiones.
- Razón: las tres tienen reglas en mis historias y una combina varias condiciones.
- Verificación: leí la regla de cada función y comprobé que los esperados salieran de las historias y del contrato del README, y anoté seis ambigüedades en el registro.
- Commit relacionado: d71019a (los archivos de las dos funciones nuevas se escribieron con la regla ya definida).

### Entrada 11 - Generación de pruebas con IA (22/11/2026)
- Prompt o sugerencia: le di a Claude mis reglas y tablas y le exigí pytest con parametrize y un comentario por fila, pytest.raises con el tipo de error exacto, esperados fijos y sin modificar mi código.
- Respuesta de la IA: tres archivos de pruebas (test_cliente.py, test_confirmacion.py y test_agregar_casos.py), 58 pruebas en total con las 13 de la semana 5.
- Decisión: conservé test_cliente.py y test_confirmacion.py y descarté test_agregar_casos.py completo.
- Razón: test_agregar_casos.py repetía pruebas que ya tenía de la semana 5, con los mismos datos o la misma partición (pregunta 3).
- Verificación: comparé cada llamada a agregar_al_pedido con tests/test_pedidos.py usando grep -n. Después de descartarlo, las pruebas siguieron en 44 passed y ruff sin avisos.
- Commit relacionado: 5ff211a.

### Entrada 12 - Generación de datos sintéticos (22/11/2026)
- Prompt o sugerencia: le pedí a Claude datos de clientes inventados con contexto del Huila, sin personas reales, con teléfonos ficticios y con casos difíciles (tildes, ñ, apóstrofo, texto vacío, valores en cero), para usarlos en un fixture.
- Respuesta de la IA: tests/conftest.py con cinco clientes válidos, cinco inválidos y unas existencias de tienda con un producto agotado, y tests/test_datos_sinteticos.py.
- Decisión: aceptada.
- Razón: la tarea pide datos sintéticos en un fixture, y con estos las pruebas usan datos más parecidos a los de la tienda.
- Verificación: leí los nombres y las cédulas y confirmé que son inventados y que ninguno es una persona que conozco. Las 57 pruebas pasan y ruff queda limpio.
- Commit relacionado: d71019a.

### Entrada 13 - Romper el código y agregar el caso que faltaba (22/11/2026)
- Prompt o sugerencia: la tarea pide introducir al menos tres errores a propósito; la IA propuso cuatro cambios concretos, uno a la vez, con git restore después de cada uno.
- Decisión: apliqué los cuatro y registré cuál prueba falló en cada uno.
- Razón: una suite que pasa no demuestra que sea buena; hay que comprobar que falle cuando el código tiene un error.
- Verificación: tres de los cuatro errores fueron detectados. El cuarto (quitar isascii) no lo detectó ninguna prueba, así que agregué el caso de la cédula con dígitos de otro alfabeto, repetí el error y esta vez falló (1 failed, 44 passed). Después de cada cambio, git status quedó en working tree clean.
- Commit relacionado: 78905a9.

