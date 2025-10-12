import pytest 
from datetime import date ,timedelta
from  shortner.forms import ShortURLForm


def test_valid_form_data(db): 
    form_data={
        'original_url': 'https://www.validurl.com',
        'short_code': 'abc123',
        'expiration_date': date.today() + timedelta(days=10)
    }
    form=ShortURLForm(data=form_data)
    assert form.is_valid()
    

def test_invalid_form_data_short_code_uniqueness(db,create_short_url):
    form_data={
        'original_url': 'https://www.anotherurl.com',
        'short_code': create_short_url.short_code,  
        'expiration_date': date.today() 
    }
    form=ShortURLForm(data=form_data)
    assert not  form.is_valid()
    assert 'short_code' in form.errors
    assert form.errors['short_code'][0]=="Short code already exists. Please choose a different one."


def test_invalid_form_data_expiration_date(db):
    form_data={
        'original_url': 'https://www.anotherurl.com',
        'short_code': 'unique1',  
        'expiration_date': date.today() - timedelta(days=1) 
    }
    form=ShortURLForm(data=form_data)
    assert not  form.is_valid()
    assert 'expiration_date' in form.errors
    assert form.errors['expiration_date'][0]=="Expiration date cannot be in the past."

