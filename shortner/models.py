from django.db import models
from django.contrib.auth import get_user_model



User=get_user_model()
class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True)
    total_clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)
    expiration_date = models.DateField(null=True, blank=True)



    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
        models.Index(fields=['short_code']),    
       
    ]
    
    def expire(self):
        self.is_expired = True
        self.save()
