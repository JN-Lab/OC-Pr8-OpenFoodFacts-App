from django.shortcuts import render
from django.http import HttpResponse
from .forms import HeaderSearchForm, HomeSearchForm
from .utils.treatment import Treatment

# Create your views here.

# Home page
def index(request):
    header_form =  HeaderSearchForm()
    home_form = HomeSearchForm()
    return render(request, 'index.html', locals())

# Search Selection
def choice(request):
    header_form = HeaderSearchForm()
    query = request.GET.get('search')
    find_info = Treatment()
    selection = find_info.get_choice_selection(query)

    if selection:
        context = {
            'element_type': selection["type"],
            'list' : selection["elements"],
            'header_form' : header_form
        }
        return render(request, 'choice.html', context)
    else:
        # Find the best scenario
        pass

# Search List

# Product

# Log-in

# Sign-in

# Sign-out

# Personal account