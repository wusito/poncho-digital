// Evento para la validación al enviar el formulario de registro de artesano.
document.getElementById("formRegistroArtesano").addEventListener("submit", validarFormArtesano);

// Función con la lógica para validar el formulario de artesanos.
function validarFormArtesano(e) {
    
    e.preventDefault(); // evita envío si hay errores.

    const formularioActual = e.target; // Captura cuál formulario se disparó.
    const nombre=document.getElementById("nombre").value;
    const dni = document.getElementById("dni");
    const cuil = document.getElementById("cuil");
    const fechaNacimiento = document.getElementById("fechaNacimiento");
    const email = document.getElementById("email");
    const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    let errores = [];

    // Validaciones básicas.
    if (dni.value.trim().length !== 8 || isNaN(dni.value.trim())) {
        errores.push("El DNI debe contener exactamente 8 dígitos numéricos.");
    }

    if (!regexEmail.test(email.value.trim())) {
        errores.push("Ingrese un correo electrónico válido (ej: usuario@dominio.com).");
    }

    if (!fechaNacimiento.value) {
        errores.push("Debe ingresar una fecha de nacimiento.");
    }
    if(nombre.length<2){
        errores.push("debe ingresar un nombre valido")
    }

    // Validaciones intermedias (Edad y Fecha).
    if (fechaNacimiento.value) {
        const fechaIngresada = new Date(fechaNacimiento.value + "T00:00:00");
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);

        if (fechaIngresada > hoy) {
            errores.push("La fecha de nacimiento no puede ser posterior a la fecha actual.");
        } else {
            // Cálculo de edad exacta
            let edad = hoy.getFullYear() - fechaIngresada.getFullYear();
            const diferenciaMeses = hoy.getMonth() - fechaIngresada.getMonth();
            if (diferenciaMeses < 0 || (diferenciaMeses === 0 && hoy.getDate() < fechaIngresada.getDate())) {
                edad--;
            }
            if (edad < 18) {
                errores.push("El artesano debe ser mayor de 18 años.");
            }
        }
    }

    // Validaciones avanzadas (Algoritmo CUIL/CUIT).
    const cuilVal = cuil.value.trim();
    if (cuilVal.length !== 11 || isNaN(cuilVal)) {
        errores.push("El CUIL/CUIT debe tener exactamente 11 números sin guiones.");
    } else {
        const multiplicadores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2];
        let suma = 0;

        for (let i = 0; i < 10; i++) {
            suma += parseInt(cuilVal[i]) * multiplicadores[i];
        }

        let resto = suma % 11;
        let digitoVerificador = 11 - resto;

        if (digitoVerificador === 11) digitoVerificador = 0;
        if (digitoVerificador === 10) digitoVerificador = 9;

        if (digitoVerificador !== parseInt(cuilVal[10])) {
            errores.push("El CUIL/CUIT ingresado no es válido (Fallo en el algoritmo de verificación).");
        }
    }

    // Mostrar errores.
    if (errores.length > 0) {
        alert("Errores:\n\n" + errores.join("\n"));
        return;
    }

    this.submit();
}