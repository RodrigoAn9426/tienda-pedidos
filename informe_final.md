# Informe final del proyecto integrador

Proyecto: Aplicación de pedidos para un minimercado de barrio (tienda-pedidos)
Estudiante: Rodrigo Andrés Rojas Pérez
Repositorio: https://github.com/RodrigoAn9426/tienda-pedidos
Fecha: 2026-11-26

## 1. Resumen

El problema del proyecto es que los requisitos se entienden mal: un cliente dice "que sea fácil de usar" y cada persona del equipo entiende algo distinto. Para practicarlo trabajé el caso de una dueña de un minimercado de barrio que quiere recibir pedidos de sus vecinos desde el celular. Usé IA (Claude, en modo chat) en cada fase: en la propuesta, para sacar necesidades de una entrevista y convertirlas en historias, para comparar alternativas de arquitectura y escribir un ADR, para escribir y revisar código, para proponer casos de prueba y pruebas, para escribir el pipeline de integración continua y el Dockerfile, y para armar una interfaz web mínima.

Lo construido es la lógica de negocio de tres funciones en Python (agregar un producto al pedido, validar los datos del cliente y validar que un pedido se puede confirmar), con 57 pruebas que pasan, 100 % de cobertura de líneas y ramas sobre esos tres módulos, un linter sin avisos y un pipeline en GitHub Actions. Al final agregué una interfaz web mínima de dos pantallas (cliente y dueña), con un servidor de Python que usa esas tres funciones; es una demostración: los datos viven solo en memoria y esa interfaz no tiene pruebas automatizadas, la probé a mano. **No está construido el servidor en Laravel ni la base de datos del diseño**, y los pedidos se pierden al apagar el programa (sección 5).

El resultado principal de la verificación es que la IA se equivocó en todas las fases, y que lo que más me sirvió para detectarlo fueron las comprobaciones que no dependen de ella: comparar contra la transcripción, comparar contra el contrato, ejecutar el código y romperlo a propósito. El caso más claro: la suite tenía 100 % de cobertura y aun así ninguna prueba fallaba cuando quité una condición del código (caso 4).

## 2. Problema y usuario

**Quién tiene el problema.** La dueña de un minimercado de barrio y sus clientes, que son vecinos. Hoy los pedidos y los cambios los revisa ella a mano; en la entrevista dijo que necesita revisar «qué productos van a pedir o están pidiendo los clientes» y que quiere que sus vecinos, que «no tienen conocimientos amplios en aplicaciones», puedan hacer el pedido «en dos o tres pasos».

**Cómo se levantó la necesidad.** La propuesta del módulo 1 es [Rojas_Rodrigo_S2_Propuesta.docx](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-1-fundamentos/Rojas_Rodrigo_S2_Propuesta.docx). La entrevista del módulo 2 la hice a mi esposa, que interpretó a la dueña con un nombre ficticio («Andrea»), el 24/10/2026. **No fue una clienta real**, y duró 8 minutos y 20 segundos, menos de los 15 que pedía la tarea; así quedó declarado en [Rojas_Rodrigo_S3_Requisitos.docx](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Requisitos.docx). La grabé con su permiso y no está en el repositorio, porque es público. Aparte hice un ejercicio de práctica con la IA en el papel de otra dueña, «Doña Marta» ([Rojas_Rodrigo_Entrevista_IA_Dona_Marta.docx](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_Entrevista_IA_Dona_Marta.docx)); ese ejercicio no es la base de los requisitos.

**Qué necesita.** De la entrevista salieron 12 necesidades con su cita, 8 historias de usuario con dos criterios cada una (uno de error), 4 requisitos no funcionales y una priorización MoSCoW: 4 Must, 2 Should y 2 Could.

## 3. La IA en el ciclo de vida

| Módulo y fase | Qué hice con IA | Herramienta | Evidencia | Cómo verifiqué |
|---|---|---|---|---|
| 1. Fundamentos | Sugerir ideas de proyecto y mejorar la redacción de la propuesta; probar y evaluar 10 prompts | Claude (chat) | [Propuesta](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-1-fundamentos/Rojas_Rodrigo_S2_Propuesta.docx), [Banco de prompts](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-1-fundamentos/Rojas_Rodrigo_S2_Banco.docx) | El problema, la fase y la herramienta los decidí yo; ejecuté el código de los prompts con pytest y califiqué cada respuesta |
| 2. Requisitos | Guion de entrevista, necesidades con cita, historias y criterios, requisitos no funcionales, MoSCoW y matriz de trazabilidad | Claude (chat) | [Requisitos](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Requisitos.docx), [Bitácora del módulo](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Bitacora.docx) | Busqué cada una de las 12 citas en mi transcripción; revisé cada historia buscando requisitos inventados, ambigüedades y omisiones |
| 3. Diseño | Alternativas de arquitectura, matriz ponderada, diagramas C4, ADR-001, modelo de datos y acciones de la API | Claude (chat) | [Diseño](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-3-diseno/Rojas_Rodrigo_S4_Diseno.docx) | Comparé cada elemento y flecha de los diagramas con el ADR y con las historias; descarté lo que nadie pidió |
| 4. Código | Contrato de HU-02, función `agregar_al_pedido`, revisión de código y de seguridad, refactor, docstrings, README e interfaz web mínima (`app.py` y carpeta `frontend/`) | Claude (chat), ruff, pytest, pip-audit | [README](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/README.md), [src/pedidos.py](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/src/pedidos.py), [app.py](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/app.py), [revision_seguridad.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/revision_seguridad.md) | Pruebas en rojo antes del código; verifiqué cada hallazgo de la IA corriendo el código: 2 reales y 5 falsos positivos; la interfaz la comparé con los criterios de aceptación de mis historias y la probé a mano |
| 5. Pruebas | Reglas escritas, tablas de casos (particiones, límites, decisión), pruebas con pytest, datos sintéticos | Claude (chat), pytest, pytest-cov | [registro_pruebas.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/registro_pruebas.md), [carpeta tests](https://github.com/RodrigoAn9426/tienda-pedidos/tree/master/tests) | Revisé cada prueba con tres preguntas; descarté un archivo entero por redundante; rompí el código 4 veces |
| 6. Operación | Pipeline de GitHub Actions, Dockerfile, guía de despliegue y plan de operación | Claude (chat), GitHub Actions | [ci.yml](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/.github/workflows/ci.yml), [Dockerfile](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/Dockerfile), [guía de despliegue](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-6-operacion/guia_despliegue.md), [plan de operación](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-6-operacion/plan_operacion.md) | Lo corrí primero en mi equipo; ejecución en verde en GitHub y una ejecución en rojo a propósito; revisé mi pipeline y mi Dockerfile con la lista de la semana 9 |

## 4. Verificación: lo que la IA hizo mal y cómo lo encontré

### Caso 1: requisitos que la IA inventó

- **Fase:** requisitos.
- **Qué propuso la IA:** historias y requisitos a partir de mi transcripción, con control de existencias por cantidad de unidades (HU-02, HU-06 y HU-07), una cifra de 5 segundos de carga (RNF-03) y textos para los mensajes de error.
- **Qué estaba mal:** la dueña solo dijo que no quería mostrar lo que «no tengo en existencia». No habló de cantidades, no dio una cifra de segundos ni dijo cómo debían decirse los errores. Además, HU-03 dependía de HU-04, y la IA había omitido una necesidad que sí estaba en la entrevista: revisar la disponibilidad cuando el cliente cambia el pedido (N-12).
- **Cómo lo detecté:** comparé cada historia y cada requisito con la transcripción y busqué cada cita con Ctrl+F. Lo que no tenía cita no podía ser requisito.
- **Qué hice:** marqué las cantidades y la cifra como datos de ejemplo o propuestas por confirmar (preguntas P-01 y P-03), quité de HU-03 la dependencia con HU-04 y agregué N-12. Evidencia: sección 7 de [Requisitos](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Requisitos.docx) y [Bitácora del módulo](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Bitacora.docx).

### Caso 2: diseño con piezas sin origen

- **Fase:** diseño.
- **Qué propuso la IA:** tres alternativas de arquitectura, dos diagramas, un modelo de datos y las acciones de la API.
- **Qué estaba mal:** los requisitos traían tres actores y los diagramas dos; una flecha no decía la tecnología; el modelo de datos tenía un precio y una tabla de usuarios que ninguna historia pedía; el campo de existencias llevaba cantidades que la dueña no había pedido.
- **Cómo lo detecté:** comparé cada elemento y cada flecha con el ADR-001 y con las historias, y exigí que cada endpoint tuviera una historia de origen.
- **Qué hice:** quité lo que no tenía origen, junté a la dueña y su ayudante en un solo actor porque hacen lo mismo en las historias, y dejé un solo servidor en vez de varias partes. Evidencia: sección 7 de [Diseño](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-3-diseno/Rojas_Rodrigo_S4_Diseno.docx).

### Caso 3: una función que aceptaba `True` como cantidad

- **Fase:** código.
- **Qué propuso la IA:** la función `agregar_al_pedido`, que validaba que la cantidad fuera un entero mayor que 0. Después, en la segunda revisión, la IA devolvió 2 problemas "seguros" y 5 "sospechas".
- **Qué estaba mal:** en Python `True` cuenta como el entero 1, así que `agregar_al_pedido({}, 1, True, {1: 10})` devolvía `{1: 1}`, y el contrato dice que los booleanos no se aceptan como cantidad. Las otras cinco sospechas no eran defectos: ya estaban definidas en el contrato.
- **Cómo lo detecté:** verifiqué cada hallazgo ejecutando el código. Con `True` imprimió `{1: 1}`; con las otras cinco, el comportamiento era el del contrato.
- **Qué hice:** escribí primero la prueba, que falló (1 failed, 12 passed), y después corregí. Commits [05e5e68](https://github.com/RodrigoAn9426/tienda-pedidos/commit/05e5e68) (prueba en rojo) y [1120c41](https://github.com/RodrigoAn9426/tienda-pedidos/commit/1120c41) (corrección). Evidencia: [revision_seguridad.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/revision_seguridad.md).

### Caso 4: una suite con 100 % de cobertura que no detectaba un error

- **Fase:** pruebas.
- **Qué propuso la IA:** pruebas con pytest a partir de mis reglas y mis tablas, tres archivos y 58 pruebas en total.
- **Qué estaba mal:** dos cosas. Un archivo entero repetía pruebas que yo ya tenía de la semana 5 (redundante). Y, aunque la cobertura llegaba al 100 %, cuando quité `isascii()` de la función que revisa los dígitos de la cédula, ninguna prueba falló: una cédula escrita con dígitos de otro alfabeto pasaba como válida.
- **Cómo lo detecté:** comparé cada llamada del archivo con las pruebas de la semana 5 usando `grep -n`, y rompí el código a propósito, un error a la vez, con `git restore` después de cada uno. De 4 errores, 3 fueron detectados y 1 no.
- **Qué hice:** descarté el archivo redundante (commit [5ff211a](https://github.com/RodrigoAn9426/tienda-pedidos/commit/5ff211a)), agregué el caso de la cédula con dígitos de otro alfabeto, repetí el error y esta vez falló (commit [78905a9](https://github.com/RodrigoAn9426/tienda-pedidos/commit/78905a9)). Guardé también la versión de la IA sin revisar en [2d2a614](https://github.com/RodrigoAn9426/tienda-pedidos/commit/2d2a614). Evidencia: [registro_pruebas.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/registro_pruebas.md).

### Caso 5: un pipeline con versiones viejas, y la prueba de que sí detecta errores

- **Fase:** operación.
- **Qué propuso la IA:** el pipeline de GitHub Actions y el Dockerfile.
- **Qué estaba mal:** el pipeline usaba `actions/checkout@v4` y `actions/setup-python@v5`, que corren con Node.js 20, versión que GitHub está retirando. Salió en verde, pero con dos advertencias.
- **Cómo lo detecté:** GitHub lo avisó en la ejecución #1, que salió en verde. Para saber si el pipeline detectaba errores de verdad, metí a propósito el error de cambiar `<` por `<=` en una rama aparte y abrí un pull request.
- **Qué hice:** actualicé las acciones a `checkout@v5` y `setup-python@v6` (commit [6267215](https://github.com/RodrigoAn9426/tienda-pedidos/commit/6267215)); la [ejecución #2](https://github.com/RodrigoAn9426/tienda-pedidos/actions/runs/45742809443) salió en verde y ya sin las advertencias. El pull request [#1](https://github.com/RodrigoAn9426/tienda-pedidos/pull/1) salió en rojo, con 2 pruebas falladas y el trabajo de la imagen omitido: [ejecución en rojo](https://github.com/RodrigoAn9426/tienda-pedidos/actions/runs/45743111697/job/139652651578?pr=1). No hice merge; `master` sigue con 57 pruebas pasando.

## 5. Estado final del sistema

- **Arquitectura:** el diseño ([ADR-001](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-3-diseno/Rojas_Rodrigo_S4_Diseno.docx)) es una página web con servidor en Laravel y base de datos PostgreSQL. **Lo construido no sigue ese diseño:** es la lógica de negocio de tres funciones, escrita en Python para practicar la regla de las pruebas, y encima una interfaz mínima: un backend en `app.py` (servidor de la librería estándar de Python, que aplica las tres funciones) y un frontend en la carpeta `frontend/` (HTML, CSS y JavaScript) con dos pantallas, `/` para el cliente y `/duena` para la dueña. Frente al diseño hay diferencias que declaro: los datos viven en memoria y no en PostgreSQL; las rutas son `/agregar` y `/confirmar` con formularios, y no la API de JSON (`/productos`, `/pedidos`) del diseño; el pedido en curso se guarda en el servidor y es uno solo para todos los visitantes; y el pedido no guarda fecha, hora ni estado. Esa diferencia está declarada en el [README](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/README.md). El pipeline no ejecuta la interfaz: el Dockerfile crea una imagen que ejecuta las pruebas.
- **Funcionalidades terminadas:**

| Historia | Prioridad | Estado |
|---|---|---|
| HU-01 Ver el catálogo | Must | Demostración: la pantalla del cliente muestra los productos de ejemplo y, si no hay ninguno, «Aún no hay productos disponibles»; productos y existencias escritos en el código, sin base de datos |
| HU-02 Agregar un producto al pedido | Must | Lógica terminada (`agregar_al_pedido`) y conectada a la interfaz: el pedido muestra «Gaseosa 1,5 L x 2» y avisa si pido más de lo que hay |
| HU-03 Confirmar el pedido | Must | Demostración: valida con `validar_confirmacion`, en una sola pantalla, con el mensaje «Recoge tu pedido en la tienda» y «Agrega al menos un producto» si está vacío; el pedido se guarda solo en memoria |
| HU-04 Datos del cliente | Should | Validación terminada (`validar_cliente`) y la interfaz pide nombre, cédula y teléfono; se guardan en memoria con el pedido (no en base de datos) y la dueña no ve la cédula |
| HU-05 Lista de pedidos de la dueña | Must | Demostración: pantalla `/duena` con nombre, celular y productos de cada pedido, y «No hay pedidos nuevos»; sin ingreso con clave (P-08) |
| HU-06 No mostrar productos agotados | Should | Demostración: los agotados no aparecen en el catálogo y se vuelve a comprobar la disponibilidad al confirmar |
| HU-07 Cambiar un producto del pedido | Could | No construida |
| HU-08 Historial de mensajes | Could | No construida |

- **Pruebas:** 57 pruebas pasan. La cobertura es de 100 % sobre `src/cliente.py`, `src/confirmacion.py` y `src/pedidos.py` (39 sentencias y 18 ramas), con un mínimo exigido de 90 % en el pipeline. Ejecución en verde con las acciones actualizadas: [ejecución #2](https://github.com/RodrigoAn9426/tienda-pedidos/actions/runs/45742809443) (pruebas en 20 s e imagen en 22 s, sin advertencias); todas las ejecuciones, incluida la última, están en [Actions](https://github.com/RodrigoAn9426/tienda-pedidos/actions). La interfaz (`app.py`) no tiene pruebas automatizadas y no entra en la medición de cobertura; el linter sí la revisa y la probé a mano con datos inventados. Estos criterios de aceptación de mis historias quedaron cubiertos por pruebas unitarias:

| Criterio | Prueba |
|---|---|
| HU-02, escenario 1 (agregar 2 unidades) | `test_agrega_producto_a_un_pedido_vacio` en tests/test_pedidos.py |
| HU-02, escenario 2 (pedir 5 con 3 disponibles) | `test_error_si_pide_mas_de_lo_que_hay_y_el_pedido_no_cambia` en tests/test_pedidos.py |
| HU-03, escenario 2 (pedido vacío) | `test_pedido_vacio_lanza_error` en tests/test_confirmacion.py |
| HU-04, escenario 2 (teléfono vacío) | caso `telefono-vacio` en tests/conftest.py, usado en tests/test_datos_sinteticos.py |
| HU-06, escenario 2 (se agotó mientras pedía) | `test_pedido_con_producto_agotado_no_se_confirma` en tests/test_datos_sinteticos.py |

- **Pendientes:**
  - El servidor en Laravel, la base de datos PostgreSQL y guardar los pedidos: hoy todo vive en memoria y se pierde al apagar el programa. Elegí construir primero y bien la lógica con pruebas.
  - Límites de la interfaz: un solo pedido en curso compartido por todos los visitantes, sin ingreso con clave para la dueña (P-08), productos y existencias escritos en el código (P-03), y solo abre en mi computador, no desde otro celular.
  - HU-07 y HU-08, que son Could.
  - Los requisitos no funcionales (RNF-01 a RNF-04) no se midieron: el pedido se arma en una sola pantalla, pero no hice la prueba con tres vecinos sin experiencia (RNF-02), ni con 50 productos (RNF-03), ni desde un celular de la dueña (RNF-04).
  - Pruebas de aceptación automatizadas sobre la interfaz: en las semanas 8 y 9 el docente entregó solo código de práctica en clase y no una tarea para el proyecto.
  - Confirmar con una clienta real las ocho preguntas pendientes del documento de requisitos (P-01 a P-08) y hacer una entrevista real de al menos 15 minutos.

## 6. Reflexión ética y legal

| Principio | Decisión en mi proyecto | Evidencia |
|---|---|---|
| Datos personales (Ley 1581 de 2012) | Todos los datos de prueba son sintéticos: nombres inventados, cédulas como `1000000011` y teléfonos como `3000000011`. La entrevista la hizo una persona de mi familia con permiso grabado, con nombre ficticio, y la grabación no está en el repositorio, que es público. HU-04 pide cédula y teléfono; quién puede verlos quedó como pregunta pendiente P-08. Antes de subir los documentos revisé que no tuvieran nombres, teléfonos ni cédulas reales. | [tests/conftest.py](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/tests/conftest.py), [Requisitos](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Requisitos.docx) |
| Sesgo | Elegí los datos de prueba con tildes, ñ, apóstrofo y nombres de la región para que la validación no rechace nombres comunes. Pero mis reglas tienen un sesgo que reconozco: exigir dos palabras en el nombre deja fuera a quien tiene una sola; una cédula de 6 a 10 dígitos y un celular que empieza por 3 dejan fuera a extranjeros, menores sin cédula y a quien solo tiene teléfono fijo. Son decisiones mías, no de la dueña, y están anotadas como ambigüedades por confirmar. | [registro_pruebas.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/registro_pruebas.md) |
| Transparencia | Cada documento tiene una sección de uso de IA; la bitácora registra cada uso con prompt, decisión, razón y verificación; guardé la versión de las pruebas de la IA sin revisar en un commit aparte; declaré la duración real de la entrevista y que fue simulada. | [bitacora_ia.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/bitacora_ia.md), commit [2d2a614](https://github.com/RodrigoAn9426/tienda-pedidos/commit/2d2a614) |
| Información al usuario | Hoy la interfaz guarda nombre, cédula y teléfono solo en la memoria del programa, nada en disco, y muestra un aviso de que la dueña ve el nombre y el celular y de que la cédula no se muestra. Falta pedir la autorización explícita del cliente antes de recoger los datos; está escrito como requisito pendiente y no está construido. Quién puede ver esos datos sigue como pregunta P-08. | [plan_operacion.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-6-operacion/plan_operacion.md), [Requisitos](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Requisitos.docx) |
| Responsabilidad | Quien responde por un error es la persona que aceptó el resultado de la IA: yo, en el código y en los documentos; la dueña, en los productos y existencias que cargue (por confirmar, P-03). Cada hallazgo y cada prueba de la IA se verificó antes de aceptarlo. Ninguna prueba se cambió para que pasara. El pipeline falla si una prueba falla o si la cobertura baja del 90 %, y el error de prueba nunca llegó a `master`. Puedo explicar de dónde sale el esperado de cada prueba. | [revision_seguridad.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/revision_seguridad.md), [pull request #1](https://github.com/RodrigoAn9426/tienda-pedidos/pull/1) |
| Propiedad intelectual y política de uso | Usé la IA como el curso lo permite y declaré dónde. Las herramientas de código (pytest, ruff, pytest-cov y pip-audit) son de código abierto y están con versión fija en requirements-dev.txt; revisé las dependencias con pip-audit, sin vulnerabilidades conocidas. No usé código ni datos de terceros en el proyecto. | [requirements-dev.txt](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/requirements-dev.txt), [README](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/README.md) |

El dilema más importante fue el de la entrevista. En el módulo 2, la IA se negó a escribir las respuestas de la clienta, porque entonces la transcripción sería inventada y el trabajo pedía una entrevista de verdad. Yo no tenía una clienta disponible, así que la hizo mi esposa en ese papel, en 8 minutos y 20 segundos, menos del mínimo. La salida fácil era presentarla como una entrevista real y más larga. Elegí declararla simulada y corta, y marcar como "por confirmar" todo lo que la entrevista no sustentaba. El costo es que mis requisitos tienen menos respaldo del que quisiera; la ventaja es que cada afirmación del informe se puede comprobar.

## 7. Aprendizajes

Ahora sé escribir primero la regla y la tabla de casos y recién después pedirle las pruebas a la IA, de modo que el resultado esperado salga de la regla y no del código. Sé medir si una suite sirve rompiendo el código a propósito, y sé leer un pipeline línea por línea con una lista de revisión. También aprendí que un mismo error se puede detectar con varias herramientas distintas, y que cada una ve algo que las otras no.

Confié de más en tres cosas. Primero, en la cobertura: llegué al 100 % y una condición quitada del código no hacía fallar nada. Segundo, en los textos de la IA que sonaban completos: los requisitos con cifras y cantidades que nadie había dicho parecían parte de la entrevista. Tercero, en el pipeline que salió en verde a la primera, que igual traía versiones viejas. Me volvió a pasar con la interfaz: la primera versión dejaba los productos agotados visibles con la etiqueta «Agotado», y la IA dijo que eso cumplía HU-06, pero mi criterio dice que el producto no debe aparecer. Lo encontré al comparar la interfaz con los criterios de aceptación de mis historias, y lo corregí.

Lo haría distinto en cuatro cosas: haría una entrevista real de al menos 15 minutos con una clienta de verdad; empezaría el servidor y la interfaz desde el módulo 4, porque la interfaz mínima la hice al final y con prisa, y quedó en memoria y sin pruebas automatizadas; probaría con código roto a propósito desde el primer lote de pruebas que me dé la IA, y pediría desde el principio que el pipeline use versiones fijas y recientes.

## 8. Anexos

- Bitácora de uso de IA: [bitacora_ia.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/bitacora_ia.md)
- Registro de pruebas: [registro_pruebas.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/registro_pruebas.md)
- Informe de revisión de código y seguridad: [revision_seguridad.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/revision_seguridad.md)
- Módulo 1: [Propuesta](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-1-fundamentos/Rojas_Rodrigo_S2_Propuesta.docx) y [Banco de prompts](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-1-fundamentos/Rojas_Rodrigo_S2_Banco.docx)
- Módulo 2: [Requisitos](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Requisitos.docx), [Bitácora del módulo](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_S3_Bitacora.docx) y [Entrevista con IA](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-2-requisitos/Rojas_Rodrigo_Entrevista_IA_Dona_Marta.docx)
- Módulo 3: [Diseño y ADR-001](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-3-diseno/Rojas_Rodrigo_S4_Diseno.docx)
- Módulo 4: [Revisión de código y seguridad](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/revision_seguridad.md) y [README](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/README.md)
- Módulo 5, plan y registro de pruebas: [registro_pruebas.md](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/registro_pruebas.md)
- Módulo 6: [Guía de despliegue](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-6-operacion/guia_despliegue.md) y [Plan de operación](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/docs/modulo-6-operacion/plan_operacion.md)
- Pipeline: [ci.yml](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/.github/workflows/ci.yml), [Dockerfile](https://github.com/RodrigoAn9426/tienda-pedidos/blob/master/Dockerfile), [todas las ejecuciones](https://github.com/RodrigoAn9426/tienda-pedidos/actions)
