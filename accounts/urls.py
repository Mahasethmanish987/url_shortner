from django.urls import path
from .views import RegisterUserView,LoginUserView,LogoutView
app_name='accounts'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='user_register'),
    path('login/', LoginUserView.as_view(), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
]
