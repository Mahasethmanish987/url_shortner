from shortner.models import ShortURL
from django.db.models.functions import Coalesce
from django.db.models  import Count,Sum ,Value 
from django.db.models import Q 
class AnalyticsService: 

   @staticmethod 
   def get_all_urls_detail_of_user(user_id):

        return ShortURL.objects.filter(user_id=user_id).aggregate(
        total_urls=Count('id'),
        total_clicks=Coalesce(Sum('total_clicks'), Value(0)),
        active_urls=Count('id', filter=Q(is_expired=False)),
        expired_urls=Count('id', filter=Q(is_expired=True))
    )
   
   @staticmethod
   def get_all_urls_detail(): 
       return ShortURL.objects.aggregate(
           total_urls=Count('id'),
        total_clicks=Coalesce(Sum('total_clicks'), Value(0))
       )
      