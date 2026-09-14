
const formNovedades = document.getElementById("formNovedades");
const campoEmail = document.getElementById("correoNovedades");
const botonNovedades = document.getElementById("botonNovedades");
const mensajeError = document.getElementById("errorNovedades");
const mensajeExito = document.getElementById("exitoNovedades");

const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

mensajeError.style.color = "#E8A2A8";
mensajeError.style.fontSize = "0.85rem";
mensajeError.style.marginTop = "0.5rem";
mensajeExito.style.color = "#8FBF8F";
mensajeExito.style.fontSize = "0.85rem";
mensajeExito.style.marginTop = "0.5rem";


function validarEmail(valor) {
    return regexEmail.test(valor.trim());
}

function mostrarError(texto) {
    mensajeError.textContent = texto;
    mensajeError.classList.remove("d-none");
    mensajeExito.classList.add("d-none");
    campoEmail.classList.add("is-invalid");
    campoEmail.classList.remove("is-valid");
}

function limpiarError() {
    mensajeError.textContent = "";
    mensajeError.classList.add("d-none");
    campoEmail.classList.remove("is-invalid");
    campoEmail.classList.add("is-valid");
}

function actualizarBotonNovedades() {
    botonNovedades.disabled = !validarEmail(campoEmail.value);
}

campoEmail.addEventListener("input", function () {
    if (campoEmail.value.trim() === "") {
        mensajeError.classList.add("d-none");
        campoEmail.classList.remove("is-invalid", "is-valid");
    } else if (validarEmail(campoEmail.value)) {
        limpiarError();
    } else {
        campoEmail.classList.remove("is-valid");
    }

    mensajeExito.classList.add("d-none");
    actualizarBotonNovedades();
});

campoEmail.addEventListener("blur", function () {
    if (campoEmail.value.trim() === "") {
        mostrarError("Ingresá tu correo electrónico.");
    } else if (!validarEmail(campoEmail.value)) {
        mostrarError("El formato del correo no es válido (ejemplo: usuario@dominio.com).");
    } else {
        limpiarError();
    }
});

campoEmail.addEventListener("keydown", function (evento) {
    if (evento.key === " ") {
        evento.preventDefault();
    }
});


formNovedades.addEventListener("submit", function (evento) {
    evento.preventDefault(); 

    if (!validarEmail(campoEmail.value)) {
        mostrarError("El formato del correo no es válido (ejemplo: usuario@dominio.com).");
        campoEmail.focus();
        return;
    }

    mensajeError.classList.add("d-none");
    mensajeExito.classList.remove("d-none");
    formNovedades.reset();
    campoEmail.classList.remove("is-valid", "is-invalid");
    botonNovedades.disabled = true;
});


const menuPrincipal = document.getElementById("menuPrincipal");

if (menuPrincipal) {
    const enlacesMenu = menuPrincipal.querySelectorAll("a.nav-link");

    enlacesMenu.forEach(function (enlace) {
        enlace.addEventListener("click", function () {
            if (menuPrincipal.classList.contains("show")) {
                const instanciaMenu = bootstrap.Collapse.getOrCreateInstance(menuPrincipal);
                instanciaMenu.hide();
            }
        });
    });
}

actualizarBotonNovedades();
