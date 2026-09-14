// --------------------------------------- SECCIÓN: CATEGORÍAS Y SUBCATEGORÍAS ---------------------------------------

// Definición de eventos y datos globales.
const categoriaSelect = document.getElementById("categoria");
const subcategoriaSelect = document.getElementById("subcategoria");

const subcategoriasPorCategoria = {
    "textiles-tradicionales": [
        "Prendas de Vicuña",
        "Fajas",
        "Mantas",
        "Chalinas"
    ],
    "artesanias-articulos-hogar": [
        "Cerámica",
        "Accesorios",
        "Madera tallada",
        "Cestería",
        "Decoración"
    ],
    "productos-regionales-delicatessen": [
        "Dulces",
        "Miel",
        "Frutos secos",
        "Vinos regionales"
    ],
    "sector-comercial": [
        "Souvenirs",
        "Accesorios",
        "Regalos",
        "Merchandising"
    ]
};



// Evento que detecta el cambio por categoría seleccionada y actualiza las subcategorías.
categoriaSelect.addEventListener("change", function () {
    const categoriaSeleccionada = this.value;

    // Limpiar subcategorías anteriores.
    subcategoriaSelect.innerHTML = "";

    // Si la categoría existe en el objeto.
    if (subcategoriasPorCategoria[categoriaSeleccionada]) {

        // Habilitar el selector.
        subcategoriaSelect.disabled = false;

        // Agregar las nuevas subcategorías.
        subcategoriasPorCategoria[categoriaSeleccionada].forEach(sub => {
            const opcion = document.createElement("option");
            opcion.value = sub.toLowerCase().replace(/\s+/g, "-");
            opcion.textContent = sub;
            subcategoriaSelect.appendChild(opcion);
        });

    } else {
        // Si no hay categoría válida, deshabilitar y mostrar mensaje.
        subcategoriaSelect.disabled = true;

        const opcion = document.createElement("option");
        opcion.value = "";
        opcion.textContent = "Selecciona primero una categoría.";
        subcategoriaSelect.appendChild(opcion);
    }
});





// --------------------------------------- SECCIÓN: VALIDAR FORMULARIOS DE PRODUCTOS ---------------------------------------

// Evento para la validación al enviar el formulario de alta y modificación.
document.getElementById("form-alta-producto").addEventListener("submit", validarFormProductos);
document.getElementById("form-modificar-producto").addEventListener("submit", validarFormProductos);


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
    if (descripcion.value.trim().length < 10) 
        errores.push("La descripción debe tener al menos 10 caracteres.");
    if (stock.value <= 0) 
        errores.push("El stock debe ser mayor a 0.");
    if (precio.value <= 0) 
        errores.push("El precio debe ser mayor a 0.");


    // Validaciones intermedias.
    if (!regexNombre.test(nombre.value)) {
        errores.push("El nombre contiene caracteres no permitidos.");
    }

    if (!isNaN(descripcion.value.trim())) {
        errores.push("La descripción no puede ser solo números.");
    }

    if (imagen.files.length > 0) {
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
    // Enviar el formulario pasadas las instancias de verificación.
    formularioActual.submit();
};





// --------------------------------------- SECCIÓN: AGREGAR PRODUCTOS ---------------------------------------
document.getElementById("form-alta-producto").addEventListener("submit", function(e) {
    e.preventDefault();

    // Validar el formulario usando la función que ya arreglamos.
    if (!validarFormProductos(this)) {
        return; // Si hay errores, se corta la ejecución.
    }

    // Capturar los valores de los inputs.
    const nombre = this.querySelector('[name="nombre"]').value;
    const descripcion = this.querySelector('[name="descripcion"]').value;
    const stock = parseInt(this.querySelector('[name="stock"]').value);
    const precio = parseFloat(this.querySelector('[name="precio_unitario"]').value);
    const categoria = this.querySelector('[name="categoria"]').value;
    const subcategoria = this.querySelector('[name="subcategoria"]').value;
    
    // Simulación de imagen y generación de ID automático.
    const imagenUrl = "https://via.placeholder.com/150"; // Imagen de relleno por ahora.
    const nuevoId = artesano1.productos.length > 0 ? Math.max(...artesano1.productos.map(p => p.ID)) + 1 : 1;

    // Crear el nuevo objeto Producto.
    const nuevoProducto = new Producto(
        nuevoId, 
        imagenUrl, 
        nombre, 
        descripcion, 
        stock, 
        precio, 
        categoria, 
        subcategoria, 
        "Activo"
    );

    // Agregarlo a la lista del artesano y actualizar la tabla.
    artesano1.agregarProducto(nuevoProducto);
    mostrarProductosPublicados(artesano1);

    // Limpiar el formulario y avisar al usuario.
    this.reset();
    alert("Producto agregado exitosamente.");
});




// --------------------------------------- SECCIÓN: MODIFICAR PRODUCTOS ---------------------------------------

// Función que muestra el formulario de modificar un producto (botón "Modificar").
function mostrarFormularioEdicion(idProducto) {

    const producto = artesano1.productos.find(p => p.ID === idProducto);

    const form = document.getElementById("form-modificar-producto");

    form.querySelector('[name="producto_id"]').value = producto.ID;
    form.querySelector('[name="nombre"]').value = producto.nombre;
    form.querySelector('[name="descripcion"]').value = producto.descripcion;
    form.querySelector('[name="stock"]').value = producto.stock;
    form.querySelector('[name="precio_unitario"]').value = producto.precio_unitario;

    // Cambia el estilo para que el contenedor sea visible.
    document.getElementById("seccion-modificar").style.display = "block";
    
    // Hace scroll suavemente hacia el formulario.
    form.scrollIntoView({ behavior: "smooth" });
}


// Función que oculta el formulario de modificar un producto (botón "Cancelar").
function cancelarFormularioEdicion() {
    const seccionModificar = document.getElementById("seccion-modificar");
    
    // Cambia el estilo para que el contenedor no vuelva a ser visible.
    seccionModificar.style.display = "none"; 
}


// Evento para guardar las modificaciones.
document.getElementById("form-modificar-producto").addEventListener("submit", function(e) {
    e.preventDefault(); // Evita que la página se recargue.

    // Llamamos a la validación. Si devuelve false, cortamos la ejecución.
    if (!validarFormProductos(this)) {
        return; 
    }

    const id = this.querySelector('[name="producto_id"]').value;
    const producto = artesano1.productos.find(p => p.ID == id);

    if(producto) {
        producto.nombre = this.querySelector('[name="nombre"]').value;
        producto.descripcion = this.querySelector('[name="descripcion"]').value;
        producto.stock = this.querySelector('[name="stock"]').value;
        producto.precio_unitario = this.querySelector('[name="precio_unitario"]').value;
    
        // Actualizamos la tabla visualmente.
        mostrarProductosPublicados(artesano1);
        
        // Ocultamos el formulario y avisamos
        cancelarFormularioEdicion();
        alert("Producto modificado correctamente.");
    }
});





// --------------------------------------- SECCIÓN: ELIMINAR PRODUCTOS ---------------------------------------

// Función que elimina el producto del array y actualiza la vista.
function ejecutarEliminacion() {
    const idProducto = document.getElementById("producto_id_eliminar").value;

    // Filtra el producto en el array para sacarlo.
    artesano1.productos = artesano1.productos.filter(p => p.ID != idProducto);
    mostrarProductosPublicados(artesano1); // Actualiza la vista.
    
    // Cierra el modal.
    const modalElement = document.getElementById('modalEliminar');
    const modalInstance = bootstrap.Modal.getOrCreateInstance(modalElement);
    
    if (modalInstance) {
        alert("Producto eliminado correctamente.");
        modalInstance.hide();
    }
}


// Capturar el ID dinámicamente cuando se abre el modal.
const modalEliminar = document.getElementById('modalEliminar');

modalEliminar.addEventListener('show.bs.modal', function (event) {
    // 1. event.relatedTarget es el botón exacto que el usuario hizo clic.
    const botonPresionado = event.relatedTarget;
    
    // 2. Extraemos el ID del atributo data-producto-id que le pusimos.
    const idProducto = botonPresionado.getAttribute('data-producto-id');
    
    // 3. Seleccionamos el input oculto dentro del modal y le pasamos el valor.
    const inputOculto = modalEliminar.querySelector('#producto_id_eliminar');
    inputOculto.value = idProducto;
});





// --------------------------------------- SECCIÓN: ESTRUCTURA DE LAS TABLAS DE LOS PRODUCTOS PUBLICADOS ---------------------------------------

// Productos.
class Producto {

    constructor(ID, imagen, nombre, descripcion, stock, precio_unitario, categoria, subcategoria, estado) {
        this.ID = ID;
        this.imagen = imagen;
        this.nombre = nombre;
        this.descripcion = descripcion;
        this.stock = stock;
        this.precio_unitario = precio_unitario;
        this.categoria = categoria;
        this.subcategoria = subcategoria;
        this.estado = estado;
    }
}

// Conjunto de productos publicados por artesano.
class ProductosPublicadosArtesano {

    constructor() {
        this.productos = []; // Lista donde se guardan los productos.
    }

    // Método para recibir un objeto Producto y agregarlo a la lista.
    agregarProducto(producto) {
        this.productos.push(producto);
        console.log(`Producto agregado: ${producto.nombre}`);
    }
}


// Dos ejmeplos.
const producto1 = new Producto(1, "https://upload.wikimedia.org/wikipedia/commons/5/5f/Poncho.jpg?utm_source=es.wikipedia.org&utm_campaign=index&utm_content=original", "Poncho", "Abrigo tradicional confeccionado en tela gruesa.", 6, 850000, "Textiles Tradicionales", "Prendas de Vicuña",  "Activo");
const producto2 = new Producto(2, "https://matesibarra.com/wp-content/uploads/2023/02/MayoPubli-11-scaled.jpg", "Mate", "Recipiente tradicional utilizado para beber la infusión de yerba mate.", 7, 50.000, "Artesanías y Artículos para el Hogar", "Accesorios", "Activo");


// Instanciamos la clase de ProductosPublicadosArtesano.
const artesano1 = new ProductosPublicadosArtesano();


// Agrega los productos al artesano.
artesano1.agregarProducto(producto1);
artesano1.agregarProducto(producto2);


// Función que muestra en tabla los productos publicados.
function mostrarProductosPublicados(artesano) {
    const cuerpoTabla = document.getElementById("cuerpo-tabla-productos-publicados");
    cuerpoTabla.innerHTML = ""; //Limpia la tabla.

    // Recorre el array.
    artesano.productos.forEach(producto => {
        
        // Crea la fila y los componentes dinámicamente.
        cuerpoTabla.innerHTML += `
            <tr>
                <td>${producto.ID}</td>
                <td><img src="${producto.imagen}" alt="${producto.nombre}" width="120"></td>
                <td>${producto.nombre}</td>
                <td>${producto.descripcion}</td>
                <td>${producto.stock}</td>
                <td>$${producto.precio_unitario.toLocaleString('es-AR')}</td>
                <td>${producto.categoria}</td>
                <td>${producto.subcategoria}</td>
                <td>${producto.estado}</td>
                <td>
                    <button
                        class="btn btn-warning w-100 mb-2"
                        type="button"
                        onclick="mostrarFormularioEdicion(${producto.ID})">
                        Modificar
                    </button>

                    <button
                        class="btn btn-danger w-100 mb-2"
                        type="button"
                        data-bs-toggle="modal"
                        data-bs-target="#modalEliminar"
                        data-producto-id="${producto.ID}">
                        Eliminar
                    </button>
                </td>
            </tr>
        `;
    });
}

// Llama a la función y pasa la instancia para que se rellene la tabla.
mostrarProductosPublicados(artesano1);
