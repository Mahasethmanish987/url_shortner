from django.contrib.auth import get_user_model

User=get_user_model()

def user_context_processor(request):
    """Context processor to add user information to the context."""
    return {
        'current_user': request.user if request.user.is_authenticated else None
    }
