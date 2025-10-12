from django.shortcuts import render,redirect
from django.views import View
from .models import ShortURL
from .forms import ShortURLForm,ShortURLUpdateForm
from django.contrib import messages 
from shortner.services.url_shortner import UrlWriteService,UrlService
from django.utils import timezone
from django.http import HttpResponse

class AuthRequiredMixin: 
    """Mixin to ensure the user is authenticated before accessing the view."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, 'You are not authorized to perform the action')
            return redirect('myapp:index')
        return super().dispatch(request, *args, **kwargs)

class DashboardView(AuthRequiredMixin,View): 
    
    template_name='shortner/dashboard.html'
    
    

    def get(self,request): 
        short_urls=ShortURL.objects.filter(user=request.user)
        return render(request,self.template_name,{'short_urls':short_urls})
    

class ShortUrlCreateView(AuthRequiredMixin,View): 
    template_name='shortner/create_url.html'
    

    
    def get(self,request): 
        form=ShortURLForm()
        return render(request,self.template_name,{'form':form})

    def post(self,request): 
        
        form=ShortURLForm(request.POST)
        if form.is_valid(): 
            short_code=form.cleaned_data.get('short_code')
            expiration_date=form.cleaned_data.get('expiration_date')
            original_url=form.cleaned_data.get('original_url')
            user_id=request.user.id 
            try: 
                if not short_code: 
                    short_code=UrlService.get_short_code()
                
    
                   
                UrlWriteService.create_short_url(user_id,original_url,short_code,expiration_date=expiration_date)   
                messages.info(request,'Short Url created')
                return redirect('shortner:dashboard')  
            except ValueError as e: 
               messages.error(request,"creation failed. Please try again.")
            except Exception as e: 
               messages.error(request,"An error occurred. Please try again.")

        return render(request,self.template_name,{'form':form})


class RedirectUrlView(View): 

    def get(self,request,short_code):

        try: 
            short_url=UrlService.get_original_url(short_code)
            if short_url.get('is_expired') :
               return HttpResponse("This short URL has expired.",status=410)
            UrlWriteService.increment_clicks(short_url.get('id'))
            return redirect(short_url.get('original_url'))
        except ShortURL.DoesNotExist: 
           return HttpResponse("Short URL does not exist.",status=404) 


class ShortUrlEditView(AuthRequiredMixin,View): 
    template_name='shortner/edit_url.html'

    def get(self,request,short_url_id): 
        try: 
            short_url=UrlWriteService.get_short_url_by_id(short_url_id)
            if short_url.user != request.user: 
                messages.error(request,"You are not authorized to edit this URL.")
                return redirect('shortner:dashboard')
            form=ShortURLUpdateForm(instance=short_url)
            return render(request,self.template_name,{'form':form,'short_url':short_url})
        except ShortURL.DoesNotExist: 
            messages.error(request,"Short URL does not exist.")
            return redirect('shortner:dashboard')

    def post(self,request,short_url_id):    
        try: 
            short_url=UrlWriteService.get_short_url_by_id(short_url_id)
            if short_url.user != request.user: 
                messages.error(request,"You are not authorized to edit this URL.")
                return redirect('shortner:dashboard')
            form=ShortURLUpdateForm(request.POST,instance=short_url,user=request.user)
            if form.is_valid(): 
                validate_data=form.cleaned_data
                print(validate_data,"validated data")
                UrlWriteService.edit_short_url(short_url_id,request.user.id,validate_data)
                messages.success(request,"Short URL updated successfully.")
                return redirect('shortner:dashboard')
            return render(request,self.template_name,{'form':form,'short_url':short_url})
        except ShortURL.DoesNotExist: 
            messages.error(request,"Short URL does not exist.")
            return redirect('shortner:dashboard')


class DeleteShortUrlView(AuthRequiredMixin,View): 
    
    def post(self,request,short_url_id): 
        try: 
            
           UrlWriteService.delete_short_url(short_url_id,request.user.id)
           messages.success(request,"Short URL deleted successfully.")
           return redirect('shortner:dashboard')
           
        except ShortURL.DoesNotExist: 
            messages.error(request,"Short URL does not exist.")
            return redirect('shortner:dashboard')
        except PermissionError:
            messages.error(request,"You are not authorized to delete this URL.")
            return redirect('shortner:dashboard')