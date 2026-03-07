from django import forms
from example.models import Formulario

class FormularioForm(forms.ModelForm):
    class Meta:
        model = Formulario
        fields = ['descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows':4, 'cols':40}),
        }