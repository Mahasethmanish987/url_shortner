import pytest 
from django.urls import reverse 



def test_dashboard_unauthenticated(db,create_user,client):
    
    url=reverse('shortner:dashboard')
    expected_url=reverse('accounts:user_login')
    response=client.get(url)
    assert response.status_code==302 
    assert response.url== expected_url


def test_create_url_unauthenticated(db,create_user,client):

    url=reverse('shortner:create_url')
    expected_url=reverse('accounts:user_login')
    response=client.get(url)
    assert response.status_code==302 
    assert response.url== expected_url


def test_create_url_authenticated(db,create_user,client): 

    client.force_login(create_user)
    url=reverse('shortner:create_url')
    response=client.get(url)
    assert response.status_code==200 
    assert 'form' in response.context