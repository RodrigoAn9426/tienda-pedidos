// Botones + y - de la cantidad (la pagina tambien funciona sin JavaScript).
document.querySelectorAll(".cant").forEach(function (caja) {
  var campo = caja.querySelector("input");
  caja.querySelectorAll("button").forEach(function (boton) {
    boton.addEventListener("click", function () {
      var nuevo = parseInt(campo.value || "1", 10) + parseInt(boton.dataset.paso, 10);
      campo.value = Math.max(1, nuevo);
    });
  });
});
