from django.shortcuts import render
from django.http import HttpResponse
from .forms import HeaderSearchForm, HomeSearchForm

# Create your views here.

# Home page
def index(request):
    header_form = HeaderSearchForm(request.POST or None)
    home_form = HomeSearchForm(request.POST or None)
    if header_form.is_valid():
        pass
    if home_form.is_valid():
        pass
    return render(request, 'index.html', locals())

# Search List

# Product

# Log-in

# Sign-in

# Sign-out

# Personal account