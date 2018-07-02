from django.shortcuts import render
from django.http import HttpResponse
from .forms import HeaderSearchForm, HomeSearchForm

# Create your views here.

# Home page
def index(request):
    header_form =  HeaderSearchForm()
    home_form = HomeSearchForm()
    return render(request, 'index.html', locals())

# Search Selection
def choice(request):
    query = request.GET.get('search')
    pass
    # juste pour tester
    # pour le contexte :
    #   - si c'est cat ou produit
    #   - nom de la cat ou produit
    #   -  
    # return render(request, 'choice.html', context)

# Search List

# Product

# Log-in

# Sign-in

# Sign-out

# Personal account