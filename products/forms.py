from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Products', max_length=100)