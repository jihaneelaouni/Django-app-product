from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image']
        # Optionnel : Ajoutez des classes CSS pour le style
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }