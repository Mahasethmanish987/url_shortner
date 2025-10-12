from django.contrib.auth import get_user_model
import pytest 
from shortner.models import ShortURL
User=get_user_model()


@pytest.fixture 
def create_user(db): 
    """Fixture to create a test user."""
    return User.objects.create_user(username='testuser',email='test1@gmail.com', password='testpassword123')

@pytest.fixture 
def create_another_user(db): 
    """Fixture to create another test user."""
    return User.objects.create_user(username='anotheruser',email='test2@gmail.com', password='anotherpassword123')

@pytest.fixture 
def create_short_url(db,create_user): 
    """Fixture to create a test short URL."""
    
    return ShortURL.objects.create(original_url='https://www.example.com', short_code='abc123', user=create_user)


@pytest.fixture
def create_another_short_url(db,create_another_user): 
    """Fixture to create another test short URL."""
    
    return ShortURL.objects.create(original_url='https://www.anotherexample.com', short_code='def456', user=create_another_user)    
