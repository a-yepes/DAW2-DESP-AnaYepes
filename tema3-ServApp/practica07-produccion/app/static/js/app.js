// =========================================================
//  TimeFlies · JavaScript del navegador
// =========================================================

// ---------- 1. Cuenta atrás de las cápsulas selladas ----------
function actualizarCuentasAtras() {
  const elementos = document.querySelectorAll(".cuenta-atras");

  elementos.forEach(function (el) {
    const fechaApertura = new Date(el.dataset.fecha);   // lee el atributo data-fecha
    const restante = fechaApertura - new Date();          // milisegundos que faltan

    if (restante <= 0) {
      el.textContent = "¡Ya se puede abrir! Recarga la página.";
      return;
    }

    const segundosTotales = Math.floor(restante / 1000);
    const dias = Math.floor(segundosTotales / 86400);
    const horas = Math.floor((segundosTotales % 86400) / 3600);
    const minutos = Math.floor((segundosTotales % 3600) / 60);
    const segundos = segundosTotales % 60;

    el.textContent = "⏳ " + dias + " d " + horas + " h " + minutos + " min " + segundos + " s";
  });
}

actualizarCuentasAtras();                    // la primera vez, al cargar la página
setInterval(actualizarCuentasAtras, 1000);   // y después cada segundo

// ---------- 2. Botones de atajo para la fecha de apertura ----------
function aFormatoDatetimeLocal(fecha) {
  // El campo datetime-local necesita el formato "AAAA-MM-DDTHH:MM"
  const dosCifras = (n) => String(n).padStart(2, "0");
  return fecha.getFullYear() + "-" + dosCifras(fecha.getMonth() + 1) + "-" + dosCifras(fecha.getDate())
    + "T" + dosCifras(fecha.getHours()) + ":" + dosCifras(fecha.getMinutes());
}

document.querySelectorAll("[data-minutos]").forEach(function (boton) {
  boton.addEventListener("click", function () {
    const minutos = Number(boton.dataset.minutos);
    const fecha = new Date(Date.now() + minutos * 60 * 1000);
    document.getElementById("fecha_apertura").value = aFormatoDatetimeLocal(fecha);
  });
});