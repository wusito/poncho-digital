// Definició de eventos y datos globales.
const categoriaSelect = document.getElementById("categoria");
const subcategoriaSelect = document.getElementById("subcategoria");

const subcategoriasPorCategoria = {
    "textiles-tradicionales": [
        "Ponchos",
        "Fajas",
        "Mantas",
        "Chalinas"
    ],
    "artesanias-articulos-hogar": [
        "Cerámica",
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



// Evento para la validación al enviar el formulario.
document.getElementById("alta-producto").addEventListener("submit", function(e) {
    e.preventDefault(); // evita envío si hay errores.

    const nombre = document.getElementById("nombre");
    const regexNombre = /^[a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ()-]+$/;
    const descripcion = document.getElementById("descripcion");
    const stock = document.getElementById("stock");
    const precio = document.getElementById("precio_unitario");
    const imagen = document.getElementById("imagen");


    let errores = [];


    // Validaciones básicas.
    if (descripcion.value.trim().length < 10) errores.push("La descripción debe tener al menos 10 caracteres.");
    if (stock.value <= 0) errores.push("El stock debe ser mayor a 0.");
    if (precio.value <= 0) errores.push("El precio debe ser mayor a 0.");


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
        return;
    }


    // Enviar el formulario pasadas las instancias de verificación.
    this.submit();
});