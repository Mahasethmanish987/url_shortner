import random 
from shortner.models import ShortURL
from django.contrib.auth import get_user_model
from datetime import date 
from django.db import transaction
from django.db.models import F

User=get_user_model()

class UrlService:
    """Service class for URL operations."""

    @staticmethod
    def generate_code():
        str="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        return ''.join(random.choices(str, k=6))
        
    @staticmethod
    def get_short_code(): 
        MAX_RETRIES=5
        for _ in range(MAX_RETRIES): 
            code=UrlService.generate_code()
            if not UrlService.check_short_url_exists(code): 
                return code
        raise Exception("Failed to generate unique short code after multiple attempts.")    



    @staticmethod
    def check_short_url_exists(short_code:str)->bool: 
        return ShortURL.objects.filter(short_code=short_code).exists()
        

    @staticmethod
    def get_original_url(short_code:str)->str:
        try: 
            short_url=ShortURL.objects.get(short_code=short_code)
            return {
                     'is_expired':UrlService.check_url_expired(short_url),
                     'original_url':short_url.original_url,
                        'id':short_url.id
            }
        except ShortURL.DoesNotExist: 
            raise

    @staticmethod    
    def check_url_expired(short_url:ShortURL)->bool: 
        if short_url.is_expired: 
            return True 
        if short_url.expiration_date and short_url.expiration_date < date.today(): 
            return True 
        return False
    @staticmethod
    def check_short_url_belongs_to_user(short_code:str,user_id:int)->bool: 
        return ShortURL.objects.filter(short_code=short_code,user_id=user_id).exists()  

class UrlWriteService: 

    @staticmethod
    def get_user(user_id:int): 
        try: 
            user=User.objects.get(id=user_id)
            return user
        except User.DoesNotExist: 
            raise

    @staticmethod 
    def get_short_url_by_id(url_id:id): 
        try: 
            short_url=ShortURL.objects.get(id=url_id)
            return short_url
        except ShortURL.DoesNotExist: 
            raise

     

        
    @transaction.atomic
    @staticmethod
    def create_short_url(user_id:int, original_url:str,short_code:str,**data)->dict:
        """Create and save a new ShortURL instance."""

        if not original_url:
            raise ValueError("Original URL is required")
        if not user_id: 
            raise ValueError("User ID is required")
        
        if not short_code: 
            short_code=UrlService.get_short_code()
        try:             
            short_url=ShortURL.objects.create(user_id=user_id, original_url=original_url, short_code=short_code,**data)
        except User.DoesNotExist: 
            raise
        except Exception as e: 
            raise e    
        return {'user_id':short_url.user.id,"short_code": short_url.short_code, "original_url": short_url.original_url}


    @staticmethod 
    def increment_clicks(url_id:id)->None: 
         """Increment the total_clicks of a ShortURL instance. """
         if not url_id: 
            raise ValueError("User ID is required")
         

         ShortURL.objects.filter(id=url_id).update(total_clicks=F('total_clicks') + 1)

        
    @staticmethod 
    def expire_short_url(url_id:int)->None:
        """Mark a ShortURL instance as expired."""
        if not url_id: 
            raise ValueError("URL ID is required")

        ShortURL.objects.filter(id=url_id).update(is_expired=True)
    
    @staticmethod
    def edit_short_url(url_id:id,user_id:id,validated_data:dict)->str: 
        """Update fields of a ShortURL instance."""
        if not url_id: 
            raise ValueError("URL ID is required")
        if not user_id: 
            raise ValueError("User ID is required")
        if 'short_code' in validated_data: 
            short_code=validated_data['short_code']
            if not  UrlService.check_short_url_belongs_to_user(short_code,user_id) and UrlService.check_short_url_exists(short_code):
                raise ValueError("Short code already exists.")

        short_url=UrlWriteService.get_short_url_by_id(url_id)
        allowed_fields={'original_url','short_code','expiration_date','is_expired'}
        if short_url.user_id != user_id: 
            raise PermissionError("You do not have permission to edit this URL.")
        for key, value in validated_data.items(): 
            if hasattr(short_url, key)  and key in allowed_fields : 
                setattr(short_url, key, value)
        short_url.save()      
                 
    
    @staticmethod 
    def delete_short_url(url_id:id,user_id:id)->None:
        """Delete a ShortURL instance."""
        if not url_id: 
            raise ValueError("URL ID is required")
        if not user_id: 
            raise ValueError("User ID is required")
        
        short_url=UrlWriteService.get_short_url_by_id(url_id)
        if short_url.user_id != user_id: 
            raise PermissionError("You do not have permission to delete this URL.")
        short_url.delete()


