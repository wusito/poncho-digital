from django import forms
from .models import PostulanteArtesano

RUBROS_CHOICES = [
    ('textil_telar', 'Tejido en Telar (Criollo / Pedal)'),
    ('textil_hilanderia', 'Hilandería Tradicional'),
    ('textil_randa', 'Randa y Bordado Tradicional'),
    ('ceramica', 'Cerámica / Alfarería'),
    ('cuero', 'Cuero y Talabartería'),
    ('madera', 'Madera y Luthería (Instrumentos)'),
    ('metal', 'Platería, Cincelado y Metales'),
    ('piedra', 'Piedra y Rodocrosita'),
    ('cesteria', 'Fibras Vegetales / Cestería'),
    ('vidrio', 'Vidrio Artesanal / Vitral'),
    ('jugueteria', 'Juguetería Artesanal'),
    ('papel', 'Papel Artesanal / Cartapesta'),
    ('otro', 'Otro rubro no listado'),
]

DEPARTAMENTOS_CHOICES = [
    ('Ambato', 'Ambato'),
    ('Ancasti', 'Ancasti'),
    ('Andalgala', 'Andalgalá'),
    ('Antofagasta de la Sierra', 'Antofagasta de la Sierra'),
    ('Belen', 'Belén'),
    ('Capayan', 'Capayán'),
    ('Capital', 'Capital'),
    ('El Alto', 'El Alto'),
    ('Fray Mamerto Esquiu', 'Fray Mamerto Esquiú'),
    ('La Paz', 'La Paz'),
    ('Paclin', 'Paclín'),
    ('Poman', 'Pomán'),
    ('Santa Maria', 'Santa María'),
    ('Santa Rosa', 'Santa Rosa'),
    ('Tinogasta', 'Tinogasta'),
    ('Valle Viejo', 'Valle Viejo'),
]

class PostulanteArtesanoForm(forms.ModelForm):
    rubro_principal = forms.ChoiceField(choices=RUBROS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    departamento = forms.ChoiceField(choices=DEPARTAMENTOS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = PostulanteArtesano
        exclude = ['estado_solicitud', 'usuario']

        widgets = {
            'datos_personales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nombre_emprendimiento': forms.TextInput(attrs={'class': 'form-control'}),
        }