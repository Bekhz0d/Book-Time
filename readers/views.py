from django.shortcuts import render, redirect
from django.views import View
from readers.forms import ReaderCreateForm, ProfileUpdateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout
from django.contrib import messages
from readers.models import Readers


class RegisterView(View):
    def get(self, request):
        create_form = ReaderCreateForm()
        context = {
            "form": create_form,
        }
        return render(request, 'readers/register.html', context)
    
    def post(self, request):
        create_form = ReaderCreateForm(data=request.POST)

        if create_form.is_valid():
            create_form.save()
            return redirect('readers:login')
        else:
            context = {
            "form": create_form,
            }
            return render(request, 'readers/register.html', context)


class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        return render(request, 'readers/login.html', {"login_form": login_form})
    
    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)

            messages.success(request, "You have succesfully logged in.")
            
            return redirect("main:list")
        else:
            return render(request, "readers/login.html", {"login_form": login_form})
        

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        reader = Readers.objects.get(username=request.user.username)
        if not request.user.is_authenticated:
            return redirect("readers:login")
        return render(request, "readers/profile.html", {"user": reader})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have succesfully logged out.")
        return redirect("landing_page")
    

class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = ProfileUpdateForm(instance=request.user)

        return render(request, "readers/profile_edit.html", {"form": user_update_form})
    
    def post(self, request):
        user_update_form = ProfileUpdateForm(instance=request.user,
                                          data=request.POST,
                                          files=request.FILES
                                          )
        
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            
            return redirect("readers:profile")

        return render(request, 'readers/profile_edit.html', {'form': user_update_form})
    