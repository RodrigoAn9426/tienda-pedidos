# Plan de operación

Proyecto: tienda-pedidos. Autor: Rodrigo Andrés Rojas Pérez. Fecha: 2026-11-25.

**Alcance honesto:** hoy el sistema son tres funciones con sus pruebas y un pipeline; no hay servicio en producción ni datos reales. Este plan dice cómo se cuidaría lo que existe y lo que haría falta al publicarlo. Todo lo marcado "por confirmar" depende de la dueña de la tienda: no inventé cifras ni plazos.

## 1. Quién responde

| Rol | Quién | Responsabilidad |
|---|---|---|
| Desarrollador | Rodrigo Andrés Rojas Pérez | Código, pipeline, dependencias y correcciones. Responde por lo que la IA produjo y él aceptó |
| Dueña de la tienda | Cliente | Carga los productos y las existencias (por confirmar, P-03) y atiende los pedidos |
| Ayudante de la dueña | Su madre, según los requisitos | Atiende pedidos con la dueña |

Cuando la aplicación falle, hoy la dueña llamaría a los clientes. Si la aplicación debe guardar los pedidos pendientes, está por confirmar (P-07).

## 2. Qué se vigila

- Que el pipeline de `master` esté en verde (GitHub Actions). Si está en rojo, no se publica.
- Que las dependencias no tengan vulnerabilidades: `pip-audit` corre en cada push.
- Que las versiones de las acciones y de Python estén vigentes. Ejemplo real: GitHub avisó que dos acciones usaban Node.js 20 y las actualicé (commit 6267215).

## 3. Datos personales

- **Qué se guardaría:** nombre, cédula y teléfono de los clientes (HU-04). Hoy no se guarda ningún dato real; las pruebas usan datos sintéticos.
- **Aviso y autorización:** antes de pedir esos tres datos, la pantalla debe decir quién los recoge y para qué, y pedir la autorización del cliente (Ley 1581 de 2012). Está por construir.
- **Acceso:** solo la dueña y su ayudante verían la cédula y el teléfono. Por confirmar (P-08).
- **Cuidados:** no poner cédulas ni teléfonos en registros de errores, y no subir `.env` al repositorio.
- **Cuánto tiempo guardarlos:** por confirmar con la dueña.

## 4. Si algo falla

1. Detectarlo: pipeline en rojo o aviso de la dueña.
2. Revisar el último commit.
3. Revertirlo con `git revert <commit>` y subir el cambio.
4. Confirmar que el pipeline vuelve a verde.
5. Escribir en la bitácora qué pasó y por qué.

## 5. Cómo se hacen los cambios

Cada cambio va en una rama y por pull request, como en el pull request #1. No se acepta un cambio con el pipeline en rojo.

## 6. Copias de seguridad

Pendiente: cuando exista la base de datos de pedidos habrá que copiarla. La frecuencia se define con la dueña.

## 7. Pendiente

Vigilar el servicio en internet, el alojamiento y la conexión segura (HTTPS), que dependen de construir el servicio web del diseño.
