from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.usuarios.decorators import artesano_requerido
from .models import Producto
from .forms import ProductoForm

# Create your views here.
@artesano_requerido
def gestion_productos(view_context_request):
    """
    Vista principal que centraliza la administración del catálogo (HU-04 y HU-05):
    - Listar los productos en la tabla.
    - Procesar el formulario de Alta (creación).
    - Renderizar la plantilla 'gestion_productos.html'.
    """
    # 1. Consulta de productos (Consulta/Listado HU-05).
    productos = Producto.objects.filter(artesano=view_context_request.user.artesano)

    # 2. Instancia del formulario para alta de nuevo producto.
    if view_context_request.method == 'POST':
        form_alta = ProductoForm(view_context_request.POST, view_context_request.FILES)
        if form_alta.is_valid():
            nuevo_producto = form_alta.save(commit=False)
            
            nuevo_producto.artesano = view_context_request.user.artesano
            
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


@artesano_requerido
def editar_producto(request, pk):
    """
    Procesa la edición/modificación de un producto existente.
    """
    producto = get_object_or_404(
        Producto,
        pk=pk,
        artesano=request.user.artesano,
    )

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


@artesano_requerido
def eliminar_producto(request, pk):
    """
    Elimina físicamente el producto seleccionado confirmando desde el modal de Bootstrap (HU-05).
    """
    if request.method == 'POST':
        producto = get_object_or_404(
            Producto,
            pk=pk,
            artesano=request.user.artesano,
        )
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f"El producto '{nombre_producto}' se ha eliminado del sistema.")
    
    return redirect('gestion_productos')