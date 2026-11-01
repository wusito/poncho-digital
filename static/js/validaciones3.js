// --------------------------------------- SECCIÓN: CATEGORÍAS Y SUBCATEGORÍAS ---------------------------------------

const subcategoriasPorCategoria = {
    "textiles-tradicionales": [
        { valor: "prendas-de-vicuna", texto: "Prendas de Vicuña" },
        { valor: "fajas", texto: "Fajas" },
        { valor: "mantas", texto: "Mantas" },
        { valor: "chalinas", texto: "Chalinas" }
    ],
    "artesanias-articulos-hogar": [
        { valor: "ceramica", texto: "Cerámica" },
        { valor: "accesorios", texto: "Accesorios" },
        { valor: "madera-tallada", texto: "Madera tallada" },
        { valor: "cesteria", texto: "Cestería" },
        { valor: "decoracion", texto: "Decoración" }
    ],
    "productos-regionales-delicatessen": [
        { valor: "dulces", texto: "Dulces" },
        { valor: "miel", texto: "Miel" },
        { valor: "frutos-secos", texto: "Frutos secos" },
        { valor: "vinos-regionales", texto: "Vinos regionales" }
    ],
    "sector-comercial": [
        { valor: "souvenirs", texto: "Souvenirs" },
        { valor: "accesorios-comercial", texto: "Accesorios" },
        { valor: "regalos", texto: "Regalos" },
        { valor: "merchandising", texto: "Merchandising" }
    ]
};



function actualizarSubcategorias(categoria, selector, subcategoriaSeleccionada = "") {
    const subcategorias = subcategoriasPorCategoria[categoria];
    selector.replaceChildren();

    if (!subcategorias) {
        selector.disabled = true;
        selector.add(new Option("Selecciona primero una categoría.", ""));
        return;
    }

    selector.disabled = false;
    selector.add(new Option("Selecciona una subcategoría...", ""));
    subcategorias.forEach(subcategoria => {
        selector.add(new Option(subcategoria.texto, subcategoria.valor));
    });

    if (subcategoriaSeleccionada && !subcategorias.some(subcategoria => (
        subcategoria.valor === subcategoriaSeleccionada
    ))) {
        selector.add(new Option(subcategoriaSeleccionada, subcategoriaSeleccionada));
    }

    selector.value = subcategoriaSeleccionada;
}

[
    ["categoria", "subcategoria"],
    ["categoria_edit", "subcategoria_edit"]
].forEach(([categoriaId, subcategoriaId]) => {
    const categoriaSelect = document.getElementById(categoriaId);
    const subcategoriaSelect = document.getElementById(subcategoriaId);

    if (categoriaSelect && subcategoriaSelect) {
        categoriaSelect.addEventListener("change", function () {
            actualizarSubcategorias(this.value, subcategoriaSelect);
        });
    }
});


// --------------------------------------- SECCIÓN: VALIDAR FORMULARIOS DE PRODUCTOS ---------------------------------------

// Evento para la validación al enviar el formulario de alta y modificación.
const formAlta = document.getElementById("form-alta-producto");
const formModificar = document.getElementById("form-modificar-producto");

if (formAlta) {
    formAlta.addEventListener("submit", function(e) {
        if (!validarFormProductos(this)) {
            e.preventDefault();
        }
    });
}

if (formModificar) {
    formModificar.addEventListener("submit", function(e) {
        if (!validarFormProductos(this)) {
            e.preventDefault();
        }
    });
}

// Función con la lógica en común para validar los formularios de alta y modificación de productos. Devuelve true si está todo bien, o false si hay errores.
function validarFormProductos(formularioActual) {

    const regexNombre = /^[a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ()-]+$/;
    const nombre = formularioActual.querySelector('[name="nombre"]');
    const descripcion = formularioActual.querySelector('[name="descripcion"]');
    const stock = formularioActual.querySelector('[name="stock"]');
    const precio = formularioActual.querySelector('[name="precio_unitario"]');
    const imagen = formularioActual.querySelector('[name="imagen"]');

    let errores = [];

    // Validaciones básicas.
    if (descripcion && descripcion.value.trim().length < 10) 
        errores.push("La descripción debe tener al menos 10 caracteres.");
    if (stock && parseFloat(stock.value) <= 0) 
        errores.push("El stock debe ser mayor a 0.");
    if (precio && parseFloat(precio.value) <= 0) 
        errores.push("El precio debe ser mayor a 0.");

    // Validaciones intermedias.
    if (nombre && !regexNombre.test(nombre.value)) {
        errores.push("El nombre contiene caracteres no permitidos.");
    }

    if (descripcion && !isNaN(descripcion.value.trim())) {
        errores.push("La descripción no puede ser solo números.");
    }

    if (imagen && imagen.files && imagen.files.length > 0) {
        const archivo = imagen.files[0];
        const extensionesValidas = ["image/jpeg", "image/png", "image/webp"];

        if (!extensionesValidas.includes(archivo.type)) {
            errores.push("La imagen debe ser JPG, PNG o WEBP.");
        }

        if (archivo.size > 2 * 1024 * 1024) {
            errores.push("La imagen no debe superar los 2 MB.");
        }
    }

    // Mostrar errores.
    if (errores.length > 0) {
        alert("Errores:\n\n" + errores.join("\n"));
        return false; // Retorna falso porque falló.
    }

    return true; // Retorna verdadero si pasó todo.
};





// --------------------------------------- SECCIÓN: MODIFICAR PRODUCTOS ---------------------------------------

// Función que muestra el formulario de modificar un producto (botón "Modificar").
function mostrarFormularioEdicion(boton) {
    const form = document.getElementById("form-modificar-producto");

    if (form) {
        const producto = boton.dataset;
        form.action = producto.editarUrl;
        form.querySelector('[name="producto_id"]').value = producto.productoId;
        form.querySelector('[name="nombre"]').value = producto.productoNombre;
        form.querySelector('[name="descripcion"]').value = producto.productoDescripcion;
        form.querySelector('[name="stock"]').value = producto.productoStock;
        form.querySelector('[name="precio_unitario"]').value = producto.productoPrecio;

        const categoria = form.querySelector('[name="categoria"]');
        const subcategoria = form.querySelector('[name="subcategoria"]');
        categoria.value = producto.productoCategoria;
        actualizarSubcategorias(
            categoria.value,
            subcategoria,
            producto.productoSubcategoria
        );

        const seccionModificar = document.getElementById("seccion-modificar");
        if (seccionModificar) {
            seccionModificar.style.display = "block";
        }
        
        form.scrollIntoView({ behavior: "smooth" });
    }
}

// Función que oculta el formulario de modificar un producto (botón "Cancelar").
function cancelarFormularioEdicion() {
    const seccionModificar = document.getElementById("seccion-modificar");
    
    if (seccionModificar) {
        seccionModificar.style.display = "none"; 
    }
}

// --------------------------------------- SECCIÓN: ELIMINAR PRODUCTOS ---------------------------------------

// Capturar el ID dinámicamente cuando se abre el modal y asignar la URL del formulario de eliminación.
const modalEliminar = document.getElementById('modalEliminar');

if (modalEliminar) {
    modalEliminar.addEventListener('show.bs.modal', function (event) {
        const botonPresionado = event.relatedTarget;
        
        if (botonPresionado) {
            const idProducto = botonPresionado.getAttribute('data-producto-id');
            const formEliminar = modalEliminar.querySelector('#form-eliminar-producto');
            
            if (formEliminar) {
                formEliminar.action = `/eliminar/${idProducto}/`;
            }
        }
    });
}