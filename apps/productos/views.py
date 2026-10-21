from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm
from apps.artesanos.models import Artesano  # Importamos el modelo Artesano

# Create your views here.
def gestion_productos(view_context_request):
    """
    Vista principal que centraliza la administración del catálogo (HU-04 y HU-05):
    - Listar los productos en la tabla.
    - Procesar el formulario de Alta (creación).
    - Renderizar la plantilla 'gestion_productos.html'.
    """
    # 1. Consulta de productos (Consulta/Listado HU-05)
    productos = Producto.objects.all()

    # 2. Instancia del formulario para alta de nuevo producto
    if view_context_request.method == 'POST':
        form_alta = ProductoForm(view_context_request.POST, view_context_request.FILES)
        if form_alta.is_valid():
            nuevo_producto = form_alta.save(commit=False)
            
            # NOTA: En un entorno con autenticación, el artesano se asocia desde el usuario logueado.
            # Se asigna o verifica la relación según la estructura activa.
            if hasattr(view_context_request.user, 'artesano'):
                # Si existe un usuario logueado con perfil de artesano vinculado
                nuevo_producto.artesano = view_context_request.user.artesano
            else:
                # Toma el artesano creado de prueba desde la shell (para ello crear un artesano de prueba)
                artesano_default = Artesano.objects.first()
                if artesano_default:
                    nuevo_producto.artesano = artesano_default
                else:
                    messages.error(
                        view_context_request, 
                        "No existe ningún Artesano registrado en la base de datos para asociar al producto."
                    )
                    return redirect('gestion_productos')
            
            nuevo_producto.save()
            messages.success(view_context_request, "¡Producto publicado con éxito!")
            return redirect('gestion_productos')
        else:
            messages.error(view_context_request, "Ocurrió un error al intentar publicar el producto. Revisa el formulario.")
    else:
        form_alta = ProductoForm()

    context = {
        'productos': productos,
        'form_alta': form_alta,
    }
    return render(view_context_request, 'productos/gestion_productos.html', context)


def editar_producto(request, pk):
    """
    Procesa la edición/modificación de un producto existente.
    """
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form_edicion = ProductoForm(
            request.POST, 
            request.FILES, 
            instance=producto
        )
        if form_edicion.is_valid():
            form_edicion.save()
            messages.success(request, f"El producto '{producto.nombre}' ha sido actualizado correctamente.")
        else:
            messages.error(request, "Error al actualizar el producto. Verifica los campos.")

    return redirect('gestion_productos')


def eliminar_producto(request, pk):
    """
    Elimina físicamente el producto seleccionado confirmando desde el modal de Bootstrap (HU-05).
    """
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=pk)
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f"El producto '{nombre_producto}' se ha eliminado del sistema.")
    
    return redirect('gestion_productos')