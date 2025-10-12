from django.contrib.auth import get_user_model 
from django import forms
import re 

User=get_user_model()

class UserForm(forms.ModelForm): 
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

    class Meta: 
        model=User
        fields=['username', 'email', 'password']
    

    def clean_email(self): 
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self): 
        username = self.cleaned_data.get('username')

        # Check allowed characters: letters, numbers, underscores
        if not re.match(r'^\w+$', username):
            raise forms.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )

        
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")

        #  max length 
        if len(username) > 50:
            raise forms.ValidationError("Username cannot exceed 150 characters.")

        return username
    

    def clean(self): 
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password != confirm_password: 
            raise forms.ValidationError("Passwords do not match")    
        return cleaned_data
    

class LoginForm(forms.Form): 
    username=forms.CharField(max_length=150)
    password=forms.CharField(widget=forms.PasswordInput)

    def clean_username(self): 
        username = self.cleaned_data.get('username')

        # Check allowed characters: letters, numbers, underscores
        if not re.match(r'^\w+$', username):
            raise forms.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )

        
        if len(username) < 3:
            raise forms.ValidationError("Username must be at least 3 characters long.")

        #  max length (Django enforces <=150 by default)
        if len(username) > 50:
            raise forms.ValidationError("Username cannot exceed 150 characters.")

        return username
    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required.")
        return password

    
    