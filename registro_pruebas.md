# Registro de pruebas: tabla de casos y pruebas de la IA

Proyecto: tienda-pedidos (app de pedidos de un minimercado de barrio, en Python)

Estudiante: Rodrigo Andrés Rojas Pérez

Fecha: 2026-11-22

## 1. Tabla de casos

### Regla 1: agregar_al_pedido (HU-02), agregar un producto al pedido

**Regla completa (el oráculo):** HU-02: "Como cliente, quiero agregar un producto a mi pedido desde el mismo catálogo para pedir sin salir de esa pantalla." Contrato del README: la cantidad debe ser un entero mayor que 0 (no se aceptan booleanos). El producto debe estar en las existencias. El total del producto en el pedido (lo que ya había más lo nuevo) no puede pasar de las existencias. Devuelve un pedido nuevo y no modifica el que recibe. Errores: ValueError (cantidad inválida), ProductoNoExisteError, ExistenciasInsuficientesError.

Estas pruebas son las de la semana 5 (tests/test_pedidos.py); en la semana 7 las comparé con la tabla.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Pedido vacío | ({}, 1, 2, {1: 10}) | {1: 2} | test_agrega_producto_a_un_pedido_vacio |
| Partición válida | Producto que ya estaba en el pedido | ({1: 2}, 1, 3, {1: 10}) | {1: 5} | test_suma_la_cantidad_si_el_producto_ya_estaba_en_el_pedido |
| Límite | Primer valor válido de la cantidad (1) | ({1: 2}, 1, 1, {1: 3}) | {1: 3} | test_permite_completar_justo_las_existencias_con_lo_que_ya_habia |
| Límite | Último valor inválido de la cantidad (0) | ({}, 1, 0, {1: 10}) | ValueError | test_error_si_la_cantidad_es_cero |
| Partición inválida | Cantidad negativa | ({}, 1, -2, {1: 10}) | ValueError | test_error_si_la_cantidad_es_negativa |
| Partición inválida | Cantidad decimal | ({}, 1, 2.5, {1: 10}) | ValueError | test_error_si_la_cantidad_no_es_un_entero |
| Partición inválida | Cantidad booleana | cantidad True y False | ValueError | test_error_si_la_cantidad_es_un_booleano[True] y [False] |
| Límite | Total igual a las existencias | ({}, 1, 3, {1: 3}) | {1: 3} | test_permite_pedir_justo_las_unidades_que_hay |
| Límite | Total una unidad por encima de las existencias | ({1: 2}, 1, 2, {1: 3}) | ExistenciasInsuficientesError | test_error_si_el_total_con_lo_que_ya_habia_pasa_de_las_existencias |
| Partición inválida | Pide más de lo que hay y el pedido no cambia | ({}, 1, 5, {1: 3}) | ExistenciasInsuficientesError y pedido igual | test_error_si_pide_mas_de_lo_que_hay_y_el_pedido_no_cambia |
| Partición inválida | Producto que no está en las existencias | ({}, 99, 1, {1: 10}) | ProductoNoExisteError | test_error_si_el_producto_no_existe |
| Partición válida | No modifica el pedido que recibe | pedido {1: 2}, agregar 3 | pedido sigue en {1: 2} | test_no_modifica_el_pedido_que_recibo |

**Ambigüedades encontradas:** Ninguna: la regla está completa en el contrato del README.

### Regla 2: validar_cliente (HU-04), datos del cliente

**Regla completa (el oráculo):** HU-04: "Como cliente, quiero registrar mi nombre completo, cédula y teléfono para que la tienda sepa quién hizo el pedido." Si falta un dato, el sistema pide el dato y no envía el pedido. Decisiones sobre lo que la historia no define: el nombre tiene al menos dos palabras; la cédula tiene solo dígitos 0-9, de 6 a 10; el teléfono tiene 10 dígitos 0-9 y empieza por 3. Si un dato no cumple, lanza ValueError cuyo mensaje empieza con el nombre del campo. Se revisan en el orden nombre, cédula, teléfono y se informa solo el primero que falla.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Datos completos | "Ana Gomez", "1000000001", "3001234567" | True | test_datos_validos_devuelven_true (fila datos completos) |
| Partición válida | Nombre con ñ y apóstrofo | "Ñoño D'Angelo" | True | test_datos_validos_devuelven_true (fila ñ y apóstrofo) |
| Partición válida | Nombre con tildes y tres palabras | "María Núñez Peña" | True | test_datos_validos_devuelven_true (fila tildes) |
| Límite | Nombre: una palabra (último inválido) | "Ana" | ValueError (nombre) | test_dato_invalido_lanza_value_error_con_el_campo (fila una sola palabra) |
| Límite | Nombre: dos palabras (primer válido) | "Ana Gomez" | True | test_datos_validos_devuelven_true (fila datos completos) |
| Partición inválida | Nombre vacío y solo espacios | "" y "   " | ValueError (nombre) | test_dato_invalido_lanza_value_error_con_el_campo (filas nombre vacío y solo espacios) |
| Límite | Cédula de 5 dígitos (último inválido) | "12345" | ValueError (cedula) | test_dato_invalido_lanza_value_error_con_el_campo (fila 5 dígitos) |
| Límite | Cédula de 6 dígitos (primer válido) | "100000" | True | test_datos_validos_devuelven_true (fila cédula de 6 dígitos) |
| Límite | Cédula de 10 dígitos (último válido) | "1000000000" | True | test_datos_validos_devuelven_true (fila cédula de 10) |
| Límite | Cédula de 11 dígitos (primer inválido) | "12345678901" | ValueError (cedula) | test_dato_invalido_lanza_value_error_con_el_campo (fila 11 dígitos) |
| Partición inválida | Cédula con letras, con puntos, vacía | "10000000A1", "1.000.000", "" | ValueError (cedula) | test_dato_invalido_lanza_value_error_con_el_campo (filas con letras, con puntos, vacía) |
| Partición inválida | Cédula con dígitos de otro alfabeto | dígitos arábigo-índicos | ValueError (cedula) | test_dato_invalido_lanza_value_error_con_el_campo (fila otro alfabeto) |
| Límite | Teléfono de 9 dígitos (último inválido) | "300123456" | ValueError (telefono) | test_dato_invalido_lanza_value_error_con_el_campo (fila 9 dígitos) |
| Límite | Teléfono de 10 dígitos (válido) | "3000000000" | True | test_datos_validos_devuelven_true (fila teléfono de 10 con prefijo 3) |
| Límite | Teléfono de 11 dígitos (primer inválido) | "30012345678" | ValueError (telefono) | test_dato_invalido_lanza_value_error_con_el_campo (fila 11 dígitos) |
| Límite | Prefijo 2 en vez de 3 | "2001234567" | ValueError (telefono) | test_dato_invalido_lanza_value_error_con_el_campo (fila prefijo 2) |
| Partición inválida | Teléfono con espacios, con letras, vacío | "300 123 4567", "30012345AB", "" | ValueError (telefono) | test_dato_invalido_lanza_value_error_con_el_campo (filas con espacios, con letras, vacío) |

**Tabla de decisión (3 condiciones, 8 combinaciones simplificadas a 4 porque si un dato anterior falla, los siguientes no importan):**

| Nombre válido | Cédula válida | Teléfono válido | Resultado | Prueba que lo cubre |
|---|---|---|---|---|
| No | no importa | no importa | ValueError (nombre) | test_dato_invalido_lanza_value_error_con_el_campo (fila decisión 1: "Ana", "12", "99") |
| Sí | No | no importa | ValueError (cedula) | test_dato_invalido_lanza_value_error_con_el_campo (fila decisión 2: cédula "12", teléfono "99") |
| Sí | Sí | No | ValueError (telefono) | test_dato_invalido_lanza_value_error_con_el_campo (filas de teléfono inválido con nombre y cédula válidos) |
| Sí | Sí | Sí | True | test_datos_validos_devuelven_true |

**Ambigüedades encontradas:** (1) "Nombre completo" no dice cuántas palabras: decidí al menos dos. (2) La historia no define el formato de la cédula: decidí solo dígitos 0-9, de 6 a 10, sin puntos ni espacios. (3) Tampoco define el del teléfono: decidí 10 dígitos que empiezan por 3 (celular colombiano), sin espacios. (4) Cuando fallan varios datos a la vez, informo solo el primero en el orden nombre, cédula, teléfono. (5) "Solo dígitos" lo interpreto como 0-9; los dígitos de otros alfabetos se rechazan. (6) Si los datos no son texto (None, números) queda fuera del contrato y no se prueba. Estas decisiones las tomé junto con la IA y quedan por confirmar con la dueña de la tienda y con el docente.

### Regla 3: validar_confirmacion (HU-03 y HU-06), confirmar el pedido

**Regla completa (el oráculo):** HU-03, escenario de error: "Dado que mi pedido no tiene productos, cuando intento confirmarlo, entonces el sistema no lo envía y muestra 'Agrega al menos un producto'." HU-06, escenario de error: si un cliente tiene "Gaseosa 1,5 L x 2" en su pedido y esa gaseosa llega a 0 unidades, cuando intenta confirmar, el sistema le avisa que ya no está disponible y no confirma hasta que la quite. Regla de la función: pedido vacío lanza PedidoVacioError con el mensaje "Agrega al menos un producto". Si algún producto no está en las existencias o tiene menos unidades de las pedidas, lanza ProductoNoDisponibleError. Si no, devuelve True.

| Técnica | Partición o límite | Entrada | Esperado | Prueba que lo cubre |
|---|---|---|---|---|
| Partición válida | Un producto disponible | ({1: 2}, {1: 10}) | True | test_pedido_con_existencias_suficientes_se_confirma (fila un producto) |
| Partición válida | Varios productos, todos disponibles | ({1: 2, 2: 1}, {1: 10, 2: 5}) | True | test_pedido_con_existencias_suficientes_se_confirma (fila varios) |
| Límite | Pide justo lo que hay | ({1: 3}, {1: 3}) | True | test_pedido_con_existencias_suficientes_se_confirma (fila límite) |
| Límite | Pide una unidad más de las que hay | ({1: 4}, {1: 3}) | ProductoNoDisponibleError | test_producto_no_disponible_lanza_error (fila una unidad más) |
| Partición inválida | Producto agotado (0 unidades) | ({1: 2}, {1: 0}) | ProductoNoDisponibleError | test_producto_no_disponible_lanza_error (fila agotado) |
| Partición inválida | Producto que no está en las existencias | ({9: 1}, {1: 10}) | ProductoNoDisponibleError | test_producto_no_disponible_lanza_error (fila no está en las existencias) |
| Partición inválida | Falla el segundo producto | ({1: 1, 2: 9}, {1: 5, 2: 3}) | ProductoNoDisponibleError | test_producto_no_disponible_lanza_error (fila falla el segundo) |
| Partición inválida | Pedido vacío | ({}, {1: 10}) y ({}, {}) | PedidoVacioError | test_pedido_vacio_lanza_error |

**Tabla de decisión (2 condiciones, 3 filas porque con pedido vacío la disponibilidad no importa):**

| Pedido vacío | Todo disponible | Resultado | Prueba que lo cubre |
|---|---|---|---|
| Sí | no importa | PedidoVacioError | test_pedido_vacio_lanza_error (dos filas: con y sin existencias) |
| No | Sí | True | test_pedido_con_existencias_suficientes_se_confirma |
| No | No | ProductoNoDisponibleError | test_producto_no_disponible_lanza_error |

**Ambigüedades encontradas:** (1) "Máximo tres pantallas" (HU-03) es de la interfaz y no se prueba con esta función. (2) La historia HU-06 dice que el sistema avisa que el producto "ya no está disponible", pero no dice si el mensaje debe nombrar el producto; decidí que sí lleva el id. (3) HU-06 habla de existencias en 0; decidí tratar igual un producto que no aparece en las existencias.

## 2. Pruebas de la IA descartadas o corregidas

**Prompt usado:** le di a Claude (en el chat) las reglas y las tablas de casos de las tres funciones, y le exigí pruebas con pytest, parametrize con un comentario por fila, pytest.raises con el tipo de error exacto, esperados fijos y sin modificar mi código. Ver las entradas 10 y 11 de la bitácora.

| Prueba generada | Decisión | Por qué | En su lugar |
|---|---|---|---|
| tests/test_agregar_casos.py, filas de pedido vacío, suma, total igual a las existencias, 2+1, 2+2 pasa del tope, cantidad 0, True, False, 2.5 | Descartada | Redundante (pregunta 3): cada fila usa los mismos datos que una prueba de la semana 5 en tests/test_pedidos.py (lo comprobé con grep -n sobre las llamadas a agregar_al_pedido) | Las pruebas de la semana 5. Commit 5ff211a |
| tests/test_agregar_casos.py, filas de cantidad -1 y producto 9 que no existe | Descartada | Redundante: la semana 5 ya prueba -2 y el producto 99, que son la misma partición | Las pruebas de la semana 5 |
| tests/test_agregar_casos.py, test_agrega_la_cantidad_minima_valida (cantidad 1) | Descartada | Redundante: test_permite_completar_justo_las_existencias_con_lo_que_ya_habia ya usa cantidad 1 | La prueba de la semana 5 |
| tests/test_agregar_casos.py, test_una_unidad_mas_de_las_existencias_lanza_error (4 de 3) | Descartada | Redundante: el caso de la semana 5 con 2+2 sobre existencias 3 da total 4, la misma unidad por encima del tope | La prueba de la semana 5 |
| tests/test_agregar_casos.py, test_no_modifica_el_pedido_original | Descartada | Es igual a test_no_modifica_el_pedido_que_recibo | La prueba de la semana 5 |
| tests/test_cliente.py, la suite de la IA no tenía un caso de dígitos de otro alfabeto | Corregida | Pregunta 2: al quitar isascii() del código ninguna prueba fallaba (sección 3) | Agregué CEDULA_ARABE y una fila nueva. Commit 78905a9 |
| tests/test_confirmacion.py, test_pedido_vacio_lanza_error, fila con existencias {} | Conservada | Parece repetir la fila con existencias {1: 10}, pero es la fila "no importa" de la tabla de decisión: con el pedido vacío, las existencias no cambian el resultado | Se conserva |
| tests/test_datos_sinteticos.py, filas de nombre vacío, teléfono vacío y cédula en cero | Conservada | Repiten particiones ya cubiertas en test_cliente.py, pero el Paso 6 pide usar los datos sintéticos en un fixture | Se conservan; los aportes nuevos son los espacios de más, el teléfono en ceros y el pedido armado con agregar_al_pedido |
| Resto de test_cliente.py y test_confirmacion.py | Conservada | El esperado de cada fila sale de la regla y de la tabla de casos, no de ejecutar el código; los límites se comprobaron rompiendo el código (sección 3) | Se conservan |

**Decisión:** Conservada, Corregida o Descartada.

## 3. Romper el código a propósito

| Cambio introducido | Archivo y línea | ¿Alguna prueba falló? | Qué hice |
|---|---|---|---|
| `<` por `<=` en la comparación de existencias | src/confirmacion.py:30 | Sí, test_pedido_con_existencias_suficientes_se_confirma[pedido2-existencias2] (pedir justo lo que hay) | Nada: la suite protege ese borde. Deshice con git restore |
| MIN_DIGITOS_CEDULA de 6 a 7 | src/cliente.py:3 | Sí, test_datos_validos_devuelven_true[Ana Gomez-100000-3001234567] (cédula de 6 dígitos) | Nada: la suite protege ese límite. Deshice con git restore |
| Quitar isascii() de _son_digitos | src/cliente.py:11 | No, las 44 pruebas pasaron | Faltaba el caso: agregué la cédula con dígitos de otro alfabeto. Repetí el error y ahora falla (1 failed, 44 passed). Commit 78905a9. Deshice con git restore |
| PREFIJO_CELULAR de "3" a "2" | src/cliente.py:6 | Sí, 7 pruebas: seis de test_datos_validos_devuelven_true y test_dato_invalido_lanza_value_error_con_el_campo[Ana Gomez-1000000001-2001234567-telefono] | Nada: la suite protege el prefijo. Deshice con git restore |

## 4. Datos de prueba

**Origen:** sintéticos generados con IA (Claude), guardados en tests/conftest.py como fixtures de pytest (cliente_valido, cliente_invalido y existencias_tienda) y usados en tests/test_datos_sinteticos.py. Confirmo que no hay datos de personas reales: los nombres son combinaciones inventadas de nombres y apellidos comunes del Huila, las cédulas son secuencias como 1000000011 y los teléfonos como 3000000011, todos ficticios.

**Casos difíciles incluidos:** tildes (Cuéllar, María, Polanía), ñ (Ñáñez), apóstrofo (D'Amato), espacios de más en el nombre, nombre vacío, nombre de una sola palabra, cédula en cero, cédula de 6 dígitos (el límite), teléfono en ceros, teléfono vacío, producto agotado (0 unidades) y un producto con una sola unidad.

