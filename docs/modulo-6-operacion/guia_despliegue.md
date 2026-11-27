# Guía de despliegue

Proyecto: tienda-pedidos. Autor: Rodrigo Andrés Rojas Pérez. Fecha: 2026-11-25.

**Alcance honesto:** hoy lo que se despliega es un contenedor que ejecuta las 57 pruebas del proyecto. El servicio web del diseño (Laravel y PostgreSQL, ADR-001) no está construido, así que no hay un servidor que publicar. La sección 6 dice qué faltaría.

## 1. Qué se despliega hoy

Una imagen Docker (archivo `Dockerfile`) que instala las dependencias con versión fija y ejecuta `python -m pytest -q`. Sirve para comprobar que el código funciona igual en otro equipo que el mío.

## 2. Requisitos

- Docker, o bien Python 3.14 con `pip`.
- Los archivos del repositorio. No se necesita ninguna clave ni archivo `.env`: el proyecto no usa secretos (existe `.env.example` sin valores).

## 3. Pasos

Con Docker:

```
docker build -t tienda-pedidos .
docker run --rm tienda-pedidos
```

Sin Docker:

```
pip install -r requirements-dev.txt
python -m pytest -q
```

Resultado esperado: `57 passed`. Si sale otra cosa, no se publica nada.

No tengo Docker instalado en mi computador, así que la imagen no la construí allí. Se construye y se ejecuta en GitHub Actions, en el trabajo `imagen` del pipeline (ejecución #2: 22 segundos, en verde).

## 4. Qué hace el pipeline

El archivo `.github/workflows/ci.yml` corre con cada push a `master` y con cada pull request hacia `master`.

| Trabajo y paso | Qué comprueba |
|---|---|
| pruebas: ruff | Estilo, errores probables y reglas de seguridad |
| pruebas: pytest con cobertura | Que las 57 pruebas pasen y que la cobertura sea de al menos 90 % |
| pruebas: pip-audit | Que las dependencias no tengan vulnerabilidades conocidas |
| imagen: docker build y docker run | Que la imagen se construye y que las pruebas pasan dentro del contenedor |

El trabajo `imagen` solo corre si `pruebas` pasó. Lo comprobé con un error a propósito en una rama aparte: el pull request #1 salió en rojo, con 2 pruebas falladas y `imagen` omitido.

## 5. Revisión de mi configuración con la lista de la semana 9

| Pregunta | Pipeline (`ci.yml`) | Dockerfile |
|---|---|---|
| Eventos o imagen base | Solo push a `master` y pull requests a `master` | Imagen `python:3.14-slim`, una versión concreta y pequeña |
| Permisos o usuario | `permissions: contents: read`, el mínimo | Usuario `appuser` sin privilegios, no root |
| Secretos | Ninguno | Ninguno; `.dockerignore` excluye `.env` y `.git` |
| Versiones | Acciones `checkout@v5` y `setup-python@v6`; dependencias con versión fija | Dependencias con versión fija |
| Si fallan las pruebas | El pipeline falla (demostrado en el pull request #1) | El contenedor termina con error |
| Modo desarrollo | No aplica | No hay servidor de desarrollo; el comando es pytest |

Límites que reconozco: las acciones están fijadas por etiqueta y no por código de commit; `ubuntu-latest` cambia con el tiempo; y no configuré la protección de la rama `master`. Si la configuro, GitHub exigirá el pipeline en verde antes de aceptar un cambio. Hoy solo evité subir el error porque decidí no hacer merge.

## 6. Despliegue del servicio web (pendiente)

Para publicar la página que describe el ADR-001 haría falta, y nada de esto está hecho:

- Construir el servidor en Laravel y la base de datos en PostgreSQL.
- Contratar un alojamiento en internet (el ADR lo lista como costo).
- Guardar los secretos fuera del repositorio, en variables de entorno, siguiendo `.env.example`.
- Decidir con la dueña quién carga los productos y las existencias (pregunta P-03).

## 7. Cómo volver atrás

Si un cambio rompe `master`: `git revert <commit>` y push. Luego se revisa que el pipeline vuelva a verde.
