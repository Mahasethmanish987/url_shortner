from django.contrib.auth import get_user_model
User=get_user_model()

class UserDTO: 
    def __init__(self, username:str, email:str)->None: 
        self.username=username
        self.email=email
        

class UserWriteService: 

    @staticmethod
    def create_user(username, email, password)->UserDTO: 
        
        user=User.objects.create_user(username=username, email=email,password=password)
        
        user.save()
        return UserDTO(username=user.username, email=user.email)
    
    
    @staticmethod
    def update_user(user_id,validate_data:dict)->UserDTO: 
        try: 
            user=User.objects.get(id=user_id)
            password=validate_data.pop('password', None)
            for key, value in validate_data.items(): 
                if hasattr(user, key):
                  setattr(user, key, value)
            if password: 
                user.set_password(password)    
            user.save()
            return UserDTO(username=user.username, email=user.email)
        except User.DoesNotExist: 
            raise


