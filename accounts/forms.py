from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Profile


class NewUserForm(UserCreationForm):

	class Meta:
		model = get_user_model()
		fields = ("email", "name",  "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.name = self.cleaned_data['name']
		if commit:
			user.save()
		return user
	
class UpdateUserForm(forms.ModelForm):
	name = forms.CharField(max_length=100, required=True)
	email = forms.EmailField(required=True)
	class Meta:
		model = get_user_model()
		fields = ['name', 'email']

class UpdateProfileForm(forms.ModelForm):
    profile_image = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['profile_image']
