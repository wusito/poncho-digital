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
    const rubroSelec = selectFiltroRubro.value.toLowerCase().trim();

    // Función radical para limpiar espacios, guiones y mayúsculas
    const normalizar = (texto) => {
        if (!texto) return "";
        return String(texto)
            .toLowerCase()
            .trim()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "") // Elimina tildes y acentos (ej: ú -> u)
            .replace(/[-_\s]+/g, "");        // Elimina guiones y espacios
    };

    const rubroLimpio = normalizar(rubroSelec);

    const filtrados = artesanosYProductosData.filter(item => {
        const coincidenciaTexto = item.nombre.toLowerCase().includes(query) ||
                                  (item.localidad && item.localidad.toLowerCase().includes(query)) ||
                                  (item.detalle && item.detalle.toLowerCase().includes(query));
        
        const itemRubro = normalizar(item.rubro);
        const itemCategoria = normalizar(item.categoria);
        const itemSubcategoria = normalizar(item.subcategoria);

        const coincidenciaRubro = rubroLimpio === "" || 
            itemRubro === rubroLimpio || 
            itemCategoria === rubroLimpio || 
            itemSubcategoria === rubroLimpio;

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
                        <p class="card-text small mb-1"><strong>Subcategoría:</strong> ${item.subcategoria || 'N/A'}</p>
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
   ========================================================================== */
let modeloStands = [];
let standsJsonValido = true;
const scriptStandsData = document.getElementById("datos-stands-json");

if (scriptStandsData) {
    try {
        modeloStands = JSON.parse(scriptStandsData.textContent);
        if (!Array.isArray(modeloStands)) {
            throw new TypeError("El listado de stands no tiene el formato esperado.");
        }
    } catch (error) {
        standsJsonValido = false;
        console.error("Error al parsear los datos del modelo Stand:", error);
    }
}

const capaMarcadores = document.getElementById("capaMarcadoresStands");
const infoStandContenedor = document.getElementById("infoStandSeleccionado");

function mostrarMensajeStand(mensaje) {
    if (!infoStandContenedor) return;
    infoStandContenedor.replaceChildren();
    const parrafo = document.createElement("p");
    parrafo.className = "text-muted fs-6";
    parrafo.textContent = mensaje;
    infoStandContenedor.appendChild(parrafo);
}

function agregarDatoStand(contenedor, etiqueta, valor) {
    const fila = document.createElement("p");
    fila.className = "mb-2";
    const titulo = document.createElement("strong");
    titulo.textContent = `${etiqueta}: `;
    fila.append(titulo, document.createTextNode(valor));
    contenedor.appendChild(fila);
}

function consultarUbicacionStand(stand) {
    if (!infoStandContenedor) return;

    infoStandContenedor.replaceChildren();
    const titulo = document.createElement("h5");
    titulo.className = "mb-3";
    titulo.textContent = `Stand ${stand.numero_stand}`;
    infoStandContenedor.appendChild(titulo);

    const estado = document.createElement("span");
    const claseEstado = stand.estado === "Asignado"
        ? "bg-danger"
        : stand.estado === "Mantenimiento"
            ? "bg-warning text-dark"
            : "bg-success";
    estado.className = `badge ${claseEstado} align-self-center mb-3`;
    estado.textContent = stand.estado_display || stand.estado;
    infoStandContenedor.appendChild(estado);
    agregarDatoStand(infoStandContenedor, "Ubicación en el mapa", stand.ubicacion_mapa);

    if (stand.artesano_nombre) {
        const subtitulo = document.createElement("h6");
        subtitulo.className = "mt-3";
        subtitulo.textContent = "Artesano asignado";
        infoStandContenedor.appendChild(subtitulo);
        agregarDatoStand(infoStandContenedor, "Nombre comercial", stand.artesano_nombre);
        agregarDatoStand(infoStandContenedor, "Rubro", stand.artesano_rubro || "No especificado");
        agregarDatoStand(infoStandContenedor, "Localidad", stand.artesano_localidad || "No especificada");
    }
}

function leerCoordenadasStand(ubicacion) {
    if (typeof ubicacion !== "string") return null;
    const coincidencia = /^\s*(\d{1,3}(?:\.\d{1,4})?)\s*,\s*(\d{1,3}(?:\.\d{1,4})?)\s*$/.exec(ubicacion);
    if (!coincidencia) return null;

    const x = Number(coincidencia[1]);
    const y = Number(coincidencia[2]);
    if (x < 0 || x > 100 || y < 0 || y > 100) return null;
    return {x, y};
}

if (capaMarcadores && infoStandContenedor) {
    if (!standsJsonValido) {
        mostrarMensajeStand("No fue posible cargar los stands del mapa. Actualizá la página o contactá al administrador.");
    } else if (modeloStands.length === 0) {
        mostrarMensajeStand("Todavía no hay stands registrados en el mapa.");
    } else {
        const coordenadasInvalidas = [];

        modeloStands.forEach(stand => {
            const coordenadas = leerCoordenadasStand(stand.ubicacion_mapa);
            if (!coordenadas) {
                coordenadasInvalidas.push(`Stand ${stand.numero_stand}: ${stand.ubicacion_mapa}`);
                return;
            }

            const pin = document.createElement("button");
            pin.type = "button";
            pin.className = "btn btn-sm position-absolute rounded-circle marcador-pin";
            pin.classList.add(
                stand.estado === "Asignado"
                    ? "btn-danger"
                    : stand.estado === "Mantenimiento"
                        ? "btn-warning"
                        : "btn-success",
                stand.estado === "Mantenimiento" ? "text-dark" : "text-white"
            );
            pin.style.left = `${coordenadas.x}%`;
            pin.style.top = `${coordenadas.y}%`;
            pin.style.transform = "translate(-50%, -50%)";
            pin.textContent = stand.numero_stand;
            pin.setAttribute(
                "aria-label",
                `Ver stand ${stand.numero_stand}, ${stand.estado_display || stand.estado}`
            );
            pin.addEventListener("click", () => consultarUbicacionStand(stand));
            capaMarcadores.appendChild(pin);
        });

        if (coordenadasInvalidas.length > 0) {
            const aviso = document.getElementById("erroresCoordenadas");
            if (aviso) {
                aviso.hidden = false;
                aviso.textContent = `No se pudieron ubicar estos stands. Corregí sus coordenadas X,Y (0–100) desde la gestión: ${coordenadasInvalidas.join("; ")}.`;
            }
        }

        if (capaMarcadores.childElementCount === 0) {
            mostrarMensajeStand("No hay stands con coordenadas válidas para mostrar. Revisá las coordenadas indicadas.");
        }
    }
}