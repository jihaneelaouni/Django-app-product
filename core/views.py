from django.shortcuts import render, redirect  # On ajoute 'redirect'
from .models import Product
from .forms import ProductForm  # On importe le formulaire créé à l'étape précédente

def home(request):
    # 1. Vérifier si l'utilisateur a envoyé le formulaire (Méthode POST)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # request.FILES est obligatoire pour l'image
        if form.is_valid():
            form.save() # Enregistre le produit dans la base de données
            return redirect('home') # Recharge la page pour voir le nouveau produit
    
    # 2. Si c'est juste une visite de page (Méthode GET), on crée un formulaire vide
    else:
        form = ProductForm()

    # 3. On récupère tous les produits (optionnel: .order_by('-id') pour voir le dernier ajouté en haut)
    products = Product.objects.all().order_by('-id')

    # 4. On envoie les produits ET le formulaire ('form') au template
    return render(request, 'core/index.html', {
        'products': products, 
        'form': form
    })