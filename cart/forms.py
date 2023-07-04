from django import forms

class DeliveryInformationForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email', max_length=100)
    address = forms.CharField(label='Address', max_length=200)
    city = forms.CharField(label='City', max_length=100)
    country = forms.CharField(label='Country', max_length=100)
    zipcode = forms.CharField(label='Zip Code', max_length=20)
