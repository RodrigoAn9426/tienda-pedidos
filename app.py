"""Backend de tienda-pedidos (solo libreria estandar).

Dos pantallas: "/" para el cliente y "/duena" para la dueña de la tienda.
El backend aplica las reglas del negocio (src/) y sirve el frontend, que
vive en la carpeta frontend/ (HTML, CSS y JavaScript).
Los datos viven en memoria: se pierden al apagar el programa.
"""

import html
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from cliente import validar_cliente
from confirmacion import (
    PedidoVacioError,
    ProductoNoDisponibleError,
    validar_confirmacion,
)
from pedidos import agregar_al_pedido

FRONTEND = Path(__file__).parent / "frontend"
ESTATICOS = {
    "/estilo.css": ("estilo.css", "text/css; charset=utf-8"),
    "/interfaz.js": ("interfaz.js", "application/javascript; charset=utf-8"),
}

# Datos de ejemplo (las cantidades las dejo "por confirmar", ver P-03).
PRODUCTOS = {
    1: "Gaseosa 1,5 L",
    2: "Arroz 500 g",
    3: "Leche 1 L",
    4: "Huevos x 30",
    5: "Panela",
}
ICONOS = {
    1: "\U0001F964",
    2: "\U0001F35A",
    3: "\U0001F95B",
    4: "\U0001F95A",
    5: "\U0001F36F",
}
EXISTENCIAS = {1: 10, 2: 8, 3: 3, 4: 0, 5: 5}
estado = {"pedido": {}, "mensaje": ""}
PEDIDOS_CONFIRMADOS: list[dict] = []


def plantilla(nombre: str, valores: dict[str, str]) -> str:
    """Lee un HTML del frontend y reemplaza los {{MARCADORES}}."""
    texto = (FRONTEND / nombre).read_text(encoding="utf-8")
    return re.sub(r"\{\{(\w+)\}\}", lambda m: valores[m.group(1)], texto)


def pagina() -> str:
    """Pantalla del cliente: catalogo, pedido y formulario con sus datos."""
    tarjetas = ""
    for pid, nombre in PRODUCTOS.items():
        if EXISTENCIAS[pid] <= 0:
            continue  # HU-06: los agotados no aparecen en el catalogo
        poco = " poco" if EXISTENCIAS[pid] <= 3 else ""
        tarjetas += (
            "<div class='prod'>"
            f"<div class='ico'>{ICONOS[pid]}</div>"
            f"<h3>{html.escape(nombre)}</h3>"
            f"<span class='stock{poco}'>Quedan {EXISTENCIAS[pid]}</span>"
            "<form method='post' action='/agregar'>"
            f"<input type='hidden' name='producto_id' value='{pid}'>"
            "<div class='cant'><button type='button' data-paso='-1'>&minus;"
            "</button><input type='number' name='cantidad' value='1' min='1'>"
            "<button type='button' data-paso='1'>+</button></div>"
            "<button class='principal'>Agregar</button></form></div>"
        )
    if tarjetas:
        catalogo = f"<div class='rejilla'>{tarjetas}</div>"
    else:
        catalogo = "<p class='vacio'>Aún no hay productos disponibles</p>"
    items = "".join(
        f"<li>{html.escape(PRODUCTOS[pid])} x {cantidad}</li>"
        for pid, cantidad in estado["pedido"].items()
    ) or "<li class='vacio'>Todavia no agregaste nada</li>"
    mensaje = estado["mensaje"]
    estado["mensaje"] = ""  # el aviso se muestra una sola vez
    if mensaje:
        malo = mensaje.startswith(("No se pudo", "La cantidad", "Agrega"))
        clase = "err" if malo else "ok"
        icono = "&#9888;&#65039;" if malo else "&#9989;"
        aviso = f"<div class='aviso {clase}'>{icono} {html.escape(mensaje)}</div>"
    else:
        aviso = ""
    return plantilla(
        "cliente.html",
        {
            "MENSAJE": aviso,
            "CATALOGO": catalogo,
            "ITEMS": items,
            "TOTAL": str(sum(estado["pedido"].values())),
        },
    )


def pagina_duena() -> str:
    """Pantalla de la dueña: lista de pedidos confirmados (HU-05)."""
    tarjetas = ""
    unidades = 0
    numerados = list(enumerate(PEDIDOS_CONFIRMADOS, start=1))
    for numero, pedido in reversed(numerados):
        unidades += sum(pedido["items"].values())
        lineas = "".join(
            f"<li>{html.escape(PRODUCTOS[pid])} x {cantidad}</li>"
            for pid, cantidad in pedido["items"].items()
        )
        nombre = html.escape(pedido["nombre"])
        tarjetas += (
            "<div class='pedido'>"
            f"<div class='avatar'>{nombre[:1].upper()}</div>"
            f"<div><h3>{nombre}</h3>"
            f"<small>Celular: {html.escape(pedido['telefono'])}</small>"
            f"<ul>{lineas}</ul></div>"
            f"<span class='etiqueta'>Pedido {numero}</span></div>"
        )
    if not tarjetas:
        tarjetas = "<p class='vacio'>No hay pedidos nuevos</p>"
    return plantilla(
        "duena.html",
        {
            "NUM_PEDIDOS": str(len(PEDIDOS_CONFIRMADOS)),
            "NUM_UNIDADES": str(unidades),
            "PEDIDOS": tarjetas,
        },
    )


def agregar(campo: dict[str, str]) -> str:
    """Agrega un producto al pedido y devuelve el mensaje para el usuario."""
    try:
        producto_id = int(campo.get("producto_id", ""))
        cantidad = int(campo.get("cantidad", ""))
    except ValueError:
        return "La cantidad debe ser un numero entero"
    try:
        estado["pedido"] = agregar_al_pedido(
            estado["pedido"], producto_id, cantidad, EXISTENCIAS
        )
    except Exception as error:  # el contrato define errores propios
        return f"No se pudo agregar: {error}"
    return "Producto agregado"


def confirmar(campo: dict[str, str]) -> str:
    """Valida el pedido y los datos; si todo esta bien, lo confirma."""
    if not estado["pedido"]:
        return "Agrega al menos un producto"  # HU-03, escenario 2
    try:
        validar_cliente(
            campo.get("nombre", ""),
            campo.get("cedula", ""),
            campo.get("telefono", ""),
        )
        validar_confirmacion(estado["pedido"], EXISTENCIAS)
    except (ValueError, PedidoVacioError, ProductoNoDisponibleError) as error:
        return f"No se pudo confirmar: {error}"
    PEDIDOS_CONFIRMADOS.append(
        {
            "nombre": campo["nombre"].strip(),
            "cedula": campo["cedula"],  # se guarda (HU-04), no se muestra
            "telefono": campo["telefono"],
            "items": dict(estado["pedido"]),
        }
    )
    for producto_id, cantidad in estado["pedido"].items():
        EXISTENCIAS[producto_id] -= cantidad
    estado["pedido"] = {}
    return "Pedido confirmado. Recoge tu pedido en la tienda"


class Manejador(BaseHTTPRequestHandler):
    """Atiende las pantallas (GET) y los formularios (POST)."""

    def responder(self, codigo: int, cuerpo: bytes, tipo: str) -> None:
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def do_GET(self) -> None:
        html_tipo = "text/html; charset=utf-8"
        if self.path == "/":
            self.responder(200, pagina().encode("utf-8"), html_tipo)
        elif self.path == "/duena":
            self.responder(200, pagina_duena().encode("utf-8"), html_tipo)
        elif self.path in ESTATICOS:
            archivo, tipo = ESTATICOS[self.path]
            cuerpo = (FRONTEND / archivo).read_bytes()
            self.responder(200, cuerpo, tipo)
        else:
            self.responder(404, b"No encontrado", "text/plain; charset=utf-8")

    def do_POST(self) -> None:
        largo = int(self.headers.get("Content-Length", 0))
        datos = parse_qs(self.rfile.read(largo).decode("utf-8"))
        campo = {llave: valores[0] for llave, valores in datos.items()}
        if self.path == "/agregar":
            estado["mensaje"] = agregar(campo)
        elif self.path == "/confirmar":
            estado["mensaje"] = confirmar(campo)
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


if __name__ == "__main__":
    servidor = ThreadingHTTPServer(("127.0.0.1", 8000), Manejador)
    print("Cliente: http://127.0.0.1:8000 | Duena: http://127.0.0.1:8000/duena")
    servidor.serve_forever()
