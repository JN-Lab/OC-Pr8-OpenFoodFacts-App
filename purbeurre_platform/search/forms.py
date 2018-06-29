from django import forms

class HeaderSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2', 'placeholder': 'chercher'})
        )


class HomeSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Produit'})
        )