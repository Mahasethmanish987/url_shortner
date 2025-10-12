from django.shortcuts import render,redirect
from .forms import UserForm,LoginForm
from .Services.user_services import UserWriteService
from django.views import View
from django.contrib.auth import authenticate, login,logout 

from django.contrib import messages



class RegisterUserView(View):
    """
      Handle user registration
        1. Display registration form on GET request
        2. Process form data and create user on POST request
    """
    
    template_name='accounts/user_register.html'

    def get(self,request): 
        user_form=UserForm()
        return render(request, self.template_name, {'form':user_form})
    
    def post(self,request): 

       user_form=UserForm(request.POST)
       if user_form.is_valid(): 
              username=user_form.cleaned_data.get('username')
              email=user_form.cleaned_data.get('email')
              password=user_form.cleaned_data.get('password')
    
              user_dto=UserWriteService.create_user(username=username, email=email, password=password)
              
              messages.success(request, f"Account created for {user_dto.username}")
              return redirect('accounts:user_login')
       else: 
           return render(request,self.template_name, {'form':user_form})     


class LoginUserView(View):
    """
      Handle user login
        1. Display login form on GET request
        2. Authenticate and log in user on POST request
        3. Redirect to home page on successful login
        4. Show error message on failed login
      """

    template_name='accounts/user_login.html'
    def dispatch(self, request, *args, **kwargs):
        """prevent logged in users from accessing the login page """

        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect('myapp:index')
        return super().dispatch(request, *args, **kwargs)


    def get(self,request): 
        login_form=LoginForm()
        return render(request, self.template_name, {'form':login_form})
    
    def post(self,request):

        login_form=LoginForm(request.POST)
        if login_form.is_valid(): 
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')

            user=authenticate(request, username=username, password=password)
            if user is not None: 
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('myapp:index')
            else: 
                messages.error(request, "Invalid username or password.")
                return render(request, self.template_name, {'form':login_form})


class LogoutView(View): 
    """
      Handle user logout
        1. Log out user on POST request
    """
    def dispatch(self, request, *args, **kwargs):
        """prevent logged out users from accessing the logout view """
        if not request.user.is_authenticated:
            messages.info(request, "You are already logged out.")
            return redirect('myapp:index')
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request): 
        
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('myapp:index')


