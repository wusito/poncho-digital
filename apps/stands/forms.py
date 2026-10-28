import re
from decimal import Decimal, InvalidOperation

from django import forms

from .models import Stand


class StandForm(forms.ModelForm):
    class Meta:
        model = Stand
        fields = ['numero_stand', 'estado', 'ubicacion_mapa']
        widgets = {
            'numero_stand': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion_mapa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '25,60',
            }),
        }
        labels = {
            'numero_stand': 'Número de stand',
            'estado': 'Estado inicial',
            'ubicacion_mapa': 'Ubicación en el mapa (X,Y)',
        }
        help_texts = {
            'ubicacion_mapa': 'Coordenadas porcentuales X,Y entre 0 y 100, separadas por coma. Ejemplo: 25,60.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estado_invalido = (
            Stand.EstadoStand.DISPONIBLE
            if self.instance.artesano_id
            else Stand.EstadoStand.ASIGNADO
        )
        self.fields['estado'].choices = [
            choice for choice in self.fields['estado'].choices
            if choice[0] != estado_invalido
        ]

    def clean_ubicacion_mapa(self):
        ubicacion = self.cleaned_data['ubicacion_mapa'].strip()
        coordenadas = ubicacion.split(',')
        if len(coordenadas) != 2:
            raise forms.ValidationError(
                'Ingresá dos coordenadas porcentuales separadas por coma, por ejemplo 25,60.'
            )

        if any(not re.fullmatch(r'\d{1,3}(?:\.\d{1,4})?', coordenada.strip()) for coordenada in coordenadas):
            raise forms.ValidationError(
                'Las coordenadas deben ser números entre 0 y 100, por ejemplo 25,60.'
            )

        try:
            x, y = (Decimal(coordenada.strip()) for coordenada in coordenadas)
        except InvalidOperation as exc:
            raise forms.ValidationError(
                'Las coordenadas deben ser números entre 0 y 100, por ejemplo 25,60.'
            ) from exc

        if not all(coordenada.is_finite() and 0 <= coordenada <= 100 for coordenada in (x, y)):
            raise forms.ValidationError('Cada coordenada debe estar entre 0 y 100.')

        return ','.join(format(coordenada.normalize(), 'f') for coordenada in (x, y))
