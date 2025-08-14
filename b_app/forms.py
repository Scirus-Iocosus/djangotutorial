from django import forms
from .models import Iscritto, file

class files(forms.ModelForm):
    class Meta:
        model = file
        fields = '__all__'
        widgets = {
            'Documento': forms.ClearableFileInput(attrs={
                'class': 'file-input',
                'id': 'file-input',
            }),
        }

class AnimatoForm(forms.ModelForm):
    class Meta:
        model = Iscritto
        fields = '__all__'
        widgets = {
            'cucina': forms.CheckboxSelectMultiple(),
        }
