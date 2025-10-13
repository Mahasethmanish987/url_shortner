from django.urls import path 
from .views import DashboardView,ShortUrlCreateView,ShortUrlEditView,DeleteShortUrlView,GetAllShortUrlsView,GetQRCode

app_name='shortner'

urlpatterns=[
    path('dashboard/',DashboardView.as_view(),name='dashboard'),
    path('create_url/',ShortUrlCreateView.as_view(),name='create_url'),
    path('edit_url/<int:short_url_id>/',ShortUrlEditView.as_view(),name='edit_url'),
    path('delete_url/<int:short_url_id>/',DeleteShortUrlView.as_view(),name='delete_url'),
    path('all_urls/',GetAllShortUrlsView.as_view(),name='all_urls'),
    path('qr/<str:short_code>/', GetQRCode.as_view(), name='generate_qr'),


]