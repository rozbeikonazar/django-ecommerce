from django.shortcuts import  render, redirect
from .forms import AuthenticationForm, NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UpdateUserForm, UpdateProfileForm



def register_request(request):
	title = "Registration"
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("products:product_list")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="register.html", context={"register_form":form, 'title': title})


def login_request(request):
	title = "Login"
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=email, password=password)
			if user is not None:
				login(request, user)
				return redirect("products:product_list")
			else: 
				messages.error(request, "products:product_list")
		else:
			messages.error(request, 'Invalid username or password')
	form = AuthenticationForm()
	return render(request=request, template_name='login.html', context={'login_form': form, 'title': title})

@login_required
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfull loged out")
	return redirect("products:product_list")

@login_required
def profile_request(request):
	title = "Profile"
	return render(request=request, template_name='profile.html', context={'title': title})

@login_required
def edit_profile(request):
	title = "Edit Profile"
	if request.method == 'POST':
		user_form = UpdateUserForm(request.POST, instance=request.user)
		profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile is updated successfully')
	else:
		user_form = UpdateUserForm(instance=request.user)
		profile_form = UpdateProfileForm(instance=request.user.profile)

	return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form' : profile_form, 'title': title})

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('accounts:edit_profile')
    

class PasswordResetView(SuccessMessageMixin, PasswordResetView):
	template_name = 'reset_password.html'
	email_template_name = 'reset_password_email.html'
	success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
	success_url = reverse_lazy('products:product_list')