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
    home_form = HomeSearchForm()
    query = request.GET.get('search')
    find_info = Treatment()
    selection = find_info.get_choice_selection(query)

    if selection:
        #convert products or categories name into slug type
        for product in selection["elements"]:
            product["slug_name"] = product["name"].replace(" ", "-")
        
        context = {
            'element_number': selection["number"],
            'element_type': selection["type"],
            'list' : selection["elements"],
            'header_form' : header_form,
            'home_form' : home_form
        }

    else:
        context = {
            'element_number': 0,
            'header_form' : header_form,
            'home_form' : home_form
        }
    return render(request, 'choice.html', context)

# Search List
def substitute(request, element_type, info_id):

    header_form = HeaderSearchForm()
    home_form = HomeSearchForm()
    find_info = Treatment()
    selection = find_info.get_substitute_selection(element_type, info_id)
    if selection:
        context = {
            'element_number': selection["number"],
            'element_type': selection["type"],
            'list' : selection["elements"],
            'header_form' : header_form,
            'home_form' : home_form
        }
    else:
        context = {
            'element_number': 0,
            'header_form' : header_form,
            'home_form' : home_form
        }
    return render(request, 'list.html', context)    

# Product

# Log-in

# Sign-in

# Sign-out

# Personal account