from .models import ShortURL
from django import forms 
from datetime import date
from shortner.services.url_shortner import UrlService

class ShortURLForm(forms.ModelForm): 
    short_code=forms.CharField(max_length=6,required=False)  
    expiration_date=forms.DateField(required=False,widget=forms.DateInput(attrs={'type':'date'}))
    

    class Meta: 
        model=ShortURL
        fields=['original_url','short_code','expiration_date']


    
    def clean_expiration_date(self): 
        expiration_date=self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date < date.today(): 
            raise forms.ValidationError("Expiration date cannot be in the past.")
        return expiration_date
    
      
    def clean_short_code(self):

        
      short_code = self.cleaned_data.get('short_code')
  
      
      if short_code:
          if len(short_code) != 6:
                raise forms.ValidationError("Short code must be exactly 6 characters long.")
            
          if UrlService.check_short_url_exists(short_code):
              raise forms.ValidationError("Short code already exists. Please choose a different one.")
      
      return short_code
    
        
    def clean_original_url(self): 

        original_url=self.cleaned_data.get('original_url')
        
        
        if not original_url.startswith(('http://','https://')): 
            
            raise forms.ValidationError("Original URL must start with http:// or https://")
        
        return original_url    



class ShortURLUpdateForm(forms.ModelForm): 
    short_code=forms.CharField(max_length=6)  
    expiration_date=forms.DateField(required=False,widget=forms.DateInput(attrs={'type':'date'}))
    

    class Meta: 
        model=ShortURL
        fields=['original_url','short_code','expiration_date','is_expired']


    def __init__(self, *args, **kwargs):
        # pop the user if passed
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_expiration_date(self): 
        expiration_date=self.cleaned_data.get('expiration_date')
        if expiration_date and expiration_date < date.today(): 
            raise forms.ValidationError("Expiration date cannot be in the past.")
        return expiration_date
    
      
    def clean_short_code(self):

        short_code=self.cleaned_data.get('short_code')
        if not short_code: 
            raise forms.ValidationError("Short code is required.")
        if len(short_code) != 6:
            raise forms.ValidationError("Short code must be exactly 6 characters long.")
        if UrlService.check_short_url_belongs_to_user(short_code,self.user.id): 
            return short_code
        if  UrlService.check_short_url_exists(short_code): 
            raise forms.ValidationError("Short code already exists. Please choose a different one.")
        return short_code 
    
        
    def clean_original_url(self): 

        original_url=self.cleaned_data.get('original_url')
       
        if not original_url.startswith(('http://','https://')): 
            
            raise forms.ValidationError("Original URL must start with http:// or https://")
        
        return original_url
    