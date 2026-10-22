/* 1. VALIDACIÓN FORMULARIO NOVEDADES */
const formNovedades = document.getElementById("formNovedades");
const campoEmail = document.getElementById("correoNovedades");
const botonNovedades = document.getElementById("botonNovedades");
const mensajeError = document.getElementById("errorNovedades");
const mensajeExito = document.getElementById("exitoNovedades");

const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

if (mensajeError && mensajeExito) {
    mensajeError.style.color = "#E8A2A8";
    mensajeError.style.fontSize = "0.85rem";
    mensajeError.style.marginTop = "0.5rem";
    mensajeExito.style.color = "#8FBF8F";
    mensajeExito.style.fontSize = "0.85rem";
    mensajeExito.style.marginTop = "0.5rem";
}

function validarEmail(valor) {
    return regexEmail.test(valor.trim());
}

function mostrarError(texto) {
    if (!mensajeError || !campoEmail) return;
    mensajeError.textContent = texto;
    mensajeError.classList.remove("d-none");
    mensajeExito.classList.add("d-none");
    campoEmail.classList.add("is-invalid");
    campoEmail.classList.remove("is-valid");
}

function limpiarError() {
    if (!mensajeError || !campoEmail) return;
    mensajeError.textContent = "";
    mensajeError.classList.add("d-none");
    campoEmail.classList.remove("is-invalid");
    campoEmail.classList.add("is-valid");
}

function actualizarBotonNovedades() {
    if (!botonNovedades || !campoEmail) return;
    botonNovedades.disabled = !validarEmail(campoEmail.value);
}

if (campoEmail) {
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
}

if (formNovedades) {
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
}

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

if (campoEmail) {
    actualizarBotonNovedades();
}


/* ==========================================================================
   HU-08: INTERACTIVIDAD BÚSQUEDAS / FILTROS DE LA FERIA
   Obtención de datos reales desde Django/PostgreSQL
   ========================================================================== */
let artesanosYProductosData = [];
const scriptBusquedaData = document.getElementById("datos-busqueda-json");

if (scriptBusquedaData) {
    try {
        artesanosYProductosData = JSON.parse(scriptBusquedaData.textContent);
    } catch (e) {
        console.error("Error al parsear los datos de búsqueda de la BD:", e);
    }
}

const formBusqueda = document.getElementById("formBusqueda");
const inputBusqueda = document.getElementById("inputBusqueda");
const selectFiltroRubro = document.getElementById("selectFiltroRubro");
const contenedorResultados = document.getElementById("resultadosBusqueda");
const mensajeBusqueda = document.getElementById("mensajeBusqueda");

function realizarBusqueda() {
    if (!inputBusqueda || !contenedorResultados) return;

    const query = inputBusqueda.value.toLowerCase().trim();
    const rubroSelec = selectFiltroRubro.value;

    const filtrados = artesanosYProductosData.filter(item => {
        const coincidenciaTexto = item.nombre.toLowerCase().includes(query) ||
                                  (item.localidad && item.localidad.toLowerCase().includes(query)) ||
                                  (item.detalle && item.detalle.toLowerCase().includes(query));
        const coincidenciaRubro = rubroSelec === "" || item.rubro === rubroSelec || item.categoria === rubroSelec;
        return coincidenciaTexto && coincidenciaRubro;
    });

    contenedorResultados.innerHTML = "";

    if (filtrados.length === 0) {
        mensajeBusqueda.textContent = "No se encontraron artesanos ni productos registrados en la base de datos que coincidan con la búsqueda.";
        mensajeBusqueda.classList.remove("d-none");
    } else {
        mensajeBusqueda.classList.add("d-none");
        filtrados.forEach(item => {
            const div = document.createElement("div");
            div.className = "col-12 col-md-6 col-lg-4";
            div.innerHTML = `
                <div class="card h-100 shadow-sm border-start border-4 ${item.tipo === 'Artesano' ? 'border-primary' : 'border-success'}">
                    <div class="card-body">
                        <span class="badge ${item.tipo === 'Artesano' ? 'bg-primary' : 'bg-success'} mb-2">${item.tipo}</span>
                        <h5 class="card-title h6">${item.nombre}</h5>
                        <p class="card-text small mb-1"><strong>Rubro/Categoría:</strong> ${item.rubro_display || item.rubro || item.categoria}</p>
                        <p class="card-text small mb-1"><strong>Localidad:</strong> ${item.localidad || 'Catamarca'}</p>
                        <p class="card-text small mb-2"><strong>Stand Asignado:</strong> ${item.stand || 'Sin asignar'}</p>
                        <p class="card-text text-muted small">${item.detalle || ''}</p>
                    </div>
                </div>
            `;
            contenedorResultados.appendChild(div);
        });
    }
}

if (formBusqueda) {
    formBusqueda.addEventListener("submit", function (e) {
        e.preventDefault();
        realizarBusqueda();
    });
    inputBusqueda.addEventListener("input", realizarBusqueda);
    selectFiltroRubro.addEventListener("change", realizarBusqueda);
    realizarBusqueda();
}


/* ==========================================================================
   HU-07: MÓDULO DE STANDS & MAPA INTERACTIVO (static/img/mapa.jpg)
   Obtención de los modelos 'Stand' y 'Artesano' desde PostgreSQL
   ========================================================================== */
let modeloStands = [];
const scriptStandsData = document.getElementById("datos-stands-json");

if (scriptStandsData) {
    try {
        modeloStands = JSON.parse(scriptStandsData.textContent);
    } catch (e) {
        console.error("Error al parsear los datos del modelo Stand:", e);
    }
}

const capaMarcadores = document.getElementById("capaMarcadoresStands");
const infoStandContenedor = document.getElementById("infoStandSeleccionado");

function renderizarMarcadoresEnMapa() {
    if (!capaMarcadores) return;

    capaMarcadores.innerHTML = "";
    if (modeloStands.length === 0) {
        capaMarcadores.innerHTML = '<div class="p-3 text-center text-muted small">No hay stands registrados en la base de datos.</div>';
        return;
    }

    modeloStands.forEach(stand => {
        const pin = document.createElement("button");
        pin.type = "button";
        
        let colorEstado = "btn-success";
        if (stand.estado === "Asignado" || stand.estado === "ocupado") colorEstado = "btn-danger";
        if (stand.estado === "Mantenimiento" || stand.estado === "reservado") colorEstado = "btn-warning text-dark";

        pin.className = `btn ${colorEstado} btn-sm position-absolute rounded-circle marcador-pin`;
        
        // Separa las coordenadas configuradas en el modelo Stand (por ejemplo "25%,30%")
        const coords = stand.ubicacion_mapa ? stand.ubicacion_mapa.split(",") : ["50%", "50%"];
        pin.style.left = coords[0] ? coords[0].trim() : "50%";
        pin.style.top = coords[1] ? coords[1].trim() : "50%";
        
        pin.style.transform = "translate(-50%, -50%)";
        pin.setAttribute("title", `Stand ${stand.numero_stand}`);
        pin.innerHTML = `<strong>${stand.numero_stand}</strong>`;

        pin.addEventListener("click", () => consultarUbicacionStand(stand));
        capaMarcadores.appendChild(pin);
    });
}

function consultarUbicacionStand(stand) {
    if (!infoStandContenedor) return;

    let badgeClass = "bg-success";
    if (stand.estado === "Asignado" || stand.estado === "ocupado") badgeClass = "bg-danger";
    if (stand.estado === "Mantenimiento" || stand.estado === "reservado") badgeClass = "bg-warning text-dark";

    infoStandContenedor.innerHTML = `
        <div class="text-start">
            <div class="d-flex justify-content-between align-items-center mb-3 pb-2 border-bottom">
                <h5 class="mb-0">Stand ${stand.numero_stand}</h5>
                <span class="badge ${badgeClass}">${stand.estado.toUpperCase()}</span>
            </div>
            <p class="mb-2"><strong>Artesano Asignado:</strong> ${stand.artesano_nombre ? stand.artesano_nombre : '<em>Sin asignar / Disponible</em>'}</p>
            <p class="mb-2"><strong>Rubro:</strong> ${stand.artesano_rubro ? stand.artesano_rubro : '-'}</p>
            <p class="mb-0"><strong>Localidad de Origen:</strong> ${stand.artesano_localidad ? stand.artesano_localidad : '-'}</p>
        </div>
    `;
}

if (capaMarcadores) {
    renderizarMarcadoresEnMapa();
}