from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario para la creación y edición de productos, integrando validaciones 
    de modelo y widgets compatibles con Bootstrap.
    """
    
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'categoria',
            'subcategoria',
            'stock',
            'precio_unitario',
            'imagen',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Poncho',
                'required': True,
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Detalla las características del producto...',
                'required': True,
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select',
                'id': 'categoria',
            }),
            'subcategoria': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'subcategoria',
                'placeholder': 'Escribe o selecciona la subcategoría',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Ej: 5',
                'required': True,
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': 'Ej: 850000',
                'required': True,
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
        }
        labels = {
            'nombre': 'Nombre del producto',
            'descripcion': 'Descripción del producto',
            'categoria': 'Selecciona la categoría del producto',
            'subcategoria': 'Selecciona la subcategoría del producto',
            'stock': 'Stock (cantidad) del producto',
            'precio_unitario': 'Precio del producto (por unidad)',
            'imagen': 'Imagen del producto',
        }



    # VALIDACIONES PERSONALIZADAS

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        import re
        regex_nombre = r'^[a-zA-Z0-9 áéíóúÁÉÍÓÚñÑ()-]+$'
        if not re.match(regex_nombre, nombre):
            raise forms.ValidationError("El nombre contiene caracteres no permitidos.")
        return nombre

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if len(descripcion) < 10:
            raise forms.ValidationError("La descripción debe tener al menos 10 caracteres.")
        if descripcion.isdigit():
            raise forms.ValidationError("La descripción no puede contener solo números.")
        return descripcion

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock <= 0:
            raise forms.ValidationError("El stock debe ser mayor a 0.")
        return stock

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Validación de formato de imagen (JPG, PNG, WEBP).
            extensiones_validas = ['image/jpeg', 'image/png', 'image/webp']
            if hasattr(imagen, 'content_type') and imagen.content_type not in extensiones_validas:
                raise forms.ValidationError("La imagen debe ser JPG, PNG o WEBP.")

            # Validación de tamaño máximo (2 MB = 2 * 1024 * 1024 bytes).
            max_bytes = 2 * 1024 * 1024
            if hasattr(imagen, 'size') and imagen.size > max_bytes:
                raise forms.ValidationError("La imagen no debe superar los 2 MB.")
        return imagen