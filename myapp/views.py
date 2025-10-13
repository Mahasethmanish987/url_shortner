from django.shortcuts import render
from shortner.services.analytics_service import AnalyticsService 
# Create your views here.

def index(request): 
    stats = AnalyticsService.get_all_urls_detail()

    context = {
        'total_urls': stats.get('total_urls', 0),
        'total_clicks': stats.get('total_clicks', 0),
    }
    return render(request, 'myapp/index.html',context)