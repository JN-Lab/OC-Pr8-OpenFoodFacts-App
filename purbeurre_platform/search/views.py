from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import HeaderSearchForm, HomeSearchForm, RegisterForm, ConnexionForm
from .utils.treatment import Treatment
from .models import Product, Category, Profile

# Create your views here.

# Home page
def index(request):
    """
    This view manages the home page
    """
    header_form =  HeaderSearchForm()
    home_form = HomeSearchForm()
    return render(request, 'index.html', locals())

# Search Selection
def choice(request):
    """
    This view manages the selection page with products or categories
    to substitute
    """
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
            'button_go_to' : "substitute_page",
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
    """
    This view manages the page showing a list of products for substitution
    """
    header_form = HeaderSearchForm()
    home_form = HomeSearchForm()
    find_info = Treatment()
    selection = find_info.get_substitute_selection(element_type, info_id)
    if selection:
        context = {
            'button_go_to' : "product_page",
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
    return render(request, 'substitute.html', context)    

# Product
def product(request, code):
    """
    this view manages the product page showing all the elements linked
    to a product
    """
    header_form = HeaderSearchForm()
    home_form = HomeSearchForm()
    find_info = Treatment()
    selection = find_info.get_selected_product(code)
    if selection:
        context = {
            'header_form' : header_form,
            'home_form' : home_form,
            'product' : selection,
        }
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
        if user.profile.products.all().exists():
            if context["product"]["ref"] in user.profile.products.all():
                context["product_registered"] = True                
        else:
            context["product_registered"] = False   

    return render(request, 'product.html', context)

# Register
def register(request):
    """
    This view manages the register page to create an account
    """
    header_form = HeaderSearchForm()

    if request.method == "POST":
        register_form = RegisterForm(request.POST) 
        if register_form.is_valid():
            username = register_form.cleaned_data["username"]
            mail = register_form.cleaned_data["mail"]
            password = register_form.cleaned_data["password"]
            password_check = register_form.cleaned_data["password_check"]

            username_already_exist = User.objects.filter(username=username).exists()
            if not username_already_exist and password == password_check:
                user = User.objects.create_user(username, mail, password)
                user_profile = Profile(user=user)
                user_profile.save()
                return redirect(reverse('search:log_in'), locals())
            else:
                error = True
                if username_already_exist:
                    user_exist = True
                if password != password_check:
                    password_problem = True
                return render(request, 'register.html', locals())
    else:
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

# Log-in
def log_in(request):
    """
    This view manages the log-in page
    """
    header_form = HeaderSearchForm()
    error = False
    if request.method == "POST":
        login_form = ConnexionForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect(reverse('search:personal'), locals)
            else:
                error = True
                return render(request, 'log_in.html', locals())
    else:
        login_form = ConnexionForm()
        return render(request, 'log_in.html', locals())

# Log-out
def log_out(request):
    """
    This view manages the log-out page
    """
    logout(request)
    return redirect(reverse('search:log_in'), locals())

# Personal account
@login_required(login_url='/search/login')
def personal(request):
    """
    This view manages the personal account page where the user
    can find all his personal informations
    """
    header_form = HeaderSearchForm()
    return render(request, 'personal.html', locals())

# Product registered
@login_required(login_url='/search/login')
def product_registered(request):
    """
    This view manages the product-registered page where the user
    can find all the products he registered
    """
    header_form = HeaderSearchForm()
    return render(request, 'product_registered.html', locals())