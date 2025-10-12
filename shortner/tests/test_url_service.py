from shortner.services.url_shortner import UrlService, UrlWriteService
import pytest 
from datetime import date as Date
from shortner.models import ShortURL

@pytest.mark.django_db
def test_short_code_generation():
    code = UrlService.get_short_code()
    assert len(code) == 6
    assert isinstance(code, str)    

@pytest.mark.django_db
def test_short_code_uniqueness(): 
    code1 = UrlService.get_short_code()
    code2 = UrlService.get_short_code()
    assert code1 != code2

@pytest.mark.django_db
def test_check_short_code_exists(): 
    code=UrlService.get_short_code()
    assert UrlService.check_short_url_exists(code) is False


@pytest.mark.parametrize("short_code,expected_url", [
    ("abc123", "https://www.example.com"),
    ("def456", "https://www.anotherexample.com"),
])
def test_get_original_url(db,short_code, expected_url, create_short_url, create_another_short_url):
    short_url= UrlService.get_original_url(short_code)
    assert expected_url == short_url.get('original_url')


def test_short_url_creation(db,create_user): 
    long_url='https://www.editedurl.com'
    short_code=UrlService.get_short_code()
    user_id=create_user.id 
    short_url_data=UrlWriteService.create_short_url(user_id=user_id,original_url=long_url,short_code=short_code)
    returned_short_code=short_url_data.get('short_code')

    short_url=ShortURL.objects.get(short_code=short_code)

    assert short_url.short_code==short_code 
    assert short_url.original_url==long_url 
    assert short_url.expiration_date is None 
    assert short_url.user.id == user_id
    assert short_url.is_expired is False 
    assert short_url.total_clicks  ==0 

def test_short_url_creation_with_expiration_date(db,create_user):
    long_url='https://www.editedurl.com'
    short_code=UrlService.get_short_code()
    user_id=create_user.id 
    expiration_date=Date(2026,3,1)
    short_url_data=UrlWriteService.create_short_url(user_id=user_id,original_url=long_url,short_code=short_code,expiration_date=expiration_date)
    returned_short_code=short_url_data.get('short_code')

    short_url=ShortURL.objects.get(short_code=short_code)

    assert short_url.short_code==short_code 
    assert short_url.original_url==long_url 
    assert short_url.expiration_date == expiration_date
    assert short_url.user.id == user_id
    assert short_url.is_expired is False 
    assert short_url.total_clicks  ==0 



    

def test_short_url_editing(db,create_user,create_short_url): 
    test_short_code='xyz789'
    long_url='https://www.editedurl.com'
    expiration_date=Date(2024,12,31)
    validate_data={
        'short_code': test_short_code,
        'original_url': long_url,
        'expiration_date': expiration_date
    }
    UrlWriteService.edit_short_url(create_short_url.id,create_user.id,validate_data)
    create_short_url.refresh_from_db()
    assert create_short_url.short_code==test_short_code
    assert create_short_url.original_url==long_url
    assert create_short_url.expiration_date==expiration_date


def test_url_editing_unauthorized(db,create_user,create_another_user,create_short_url):
    test_short_code='xyz789'
    long_url='https://www.editedurl.com'
    expiration_date=Date(2024,12,31)
    validate_data={
        'short_code': test_short_code,
        'original_url': long_url,
        'expiration_date': expiration_date
    }
    with pytest.raises(PermissionError): 
        UrlWriteService.edit_short_url(create_short_url.id,create_another_user.id,validate_data)

def test_short_url_deletion(db,create_user,create_short_url):
    UrlWriteService.delete_short_url(create_short_url.id,create_user.id)
    
    with pytest.raises(ShortURL.DoesNotExist): 
        ShortURL.objects.get(id=create_short_url.id)




def test_short_url_deletion_unauthorized(db,create_user,create_another_user,create_short_url):


    with pytest.raises(PermissionError): 
        UrlWriteService.delete_short_url(create_short_url.id,create_another_user.id)
    
    
    assert ShortURL.objects.filter(id=create_short_url.id).exists()



def test_increment_clicks(db,create_short_url): 
    UrlWriteService.increment_clicks(create_short_url.id)

    create_short_url.refresh_from_db()
    assert create_short_url.total_clicks==1

    UrlWriteService.increment_clicks(create_short_url.id)
    create_short_url.refresh_from_db()
    assert create_short_url.total_clicks==2


def test_expire_short_url(db,create_short_url): 
    assert create_short_url.is_expired is False
    UrlWriteService.expire_short_url(create_short_url.id)
    create_short_url.refresh_from_db()
    assert create_short_url.is_expired is True


def test_short_url_deletion(db,create_short_url,create_user):

    UrlWriteService.delete_short_url(create_short_url.id,create_user.id)

    with pytest.raises(ShortURL.DoesNotExist): 
        ShortURL.objects.get(id=create_short_url.id)

def test_short_url_deletion_unauthorized(db,create_short_url,create_another_user):

    with pytest.raises(PermissionError): 
        UrlWriteService.delete_short_url(create_short_url.id,create_another_user.id)
    
    
    assert ShortURL.objects.filter(id=create_short_url.id).exists()