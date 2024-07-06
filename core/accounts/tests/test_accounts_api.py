import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import datetime
from rest_framework.authtoken.models import Token


from accounts.models import Users , Profile

@pytest.fixture
def api_client():
    client = APIClient()
    return client

@pytest.fixture
def user_api():
    user = Users.objects.create_user(email='testuser@example.com', password='a/@123456')
    user.is_verified = True
    user.save()
    return user

@pytest.fixture
def profile_api(user_api):
    profile = Profile.objects.create(user=user_api , 
                                     first_name = 'testuser',
                                     last_name = 'testuserrr' ,
                                     description = 'Test description'
                                     )
    return profile


@pytest.mark.django_db
class TestAccountApiView:

    def test_registration_user_valid_response_200(self, api_client):
        data = {
            'email': 'newuser@example.com',
            'password': 'a/@123456',
            'password_2': 'a/@123456'
        }
        response = api_client.post(reverse('accounts:accounts-urls:registrations'), data=data, format='json')
        assert response.status_code == 200
    
    def test_registration_user_invalid_response_400(self, api_client):
        data = {
            'email': 'newuser@examp',
            'password': 'a/@123456',
        }
        response = api_client.post(reverse('accounts:accounts-urls:registrations'), data=data, format='json')
        assert response.status_code == 400

    def test_create_token_user_valid_response_200(self, api_client , user_api):
            token, created = Token.objects.get_or_create(user=user_api)
            api_client.force_authenticate(user=user_api)
            response = api_client.post(reverse('accounts:accounts-urls:discard-token'), format='json')
            assert response.status_code == 204

    def test_create_token_user_invalid_response_400(self, api_client):
        response = api_client.post(reverse('accounts:accounts-urls:create-token'), format='json')
        assert response.status_code == 400

    def test_dicard_token_user_invalid_response_401(self, api_client , user_api):
        token, created = Token.objects.get_or_create(user=user_api)
        response = api_client.post(reverse('accounts:accounts-urls:discard-token'), format='json')
        assert response.status_code == 401

    def test_create_token_jwt_user_valid_response_200(self, api_client, user_api):
        user_api.is_verified = True
        user_api.save()
        data = {'email': user_api.email, 'password': 'a/@123456'}
        api_client.force_authenticate(user=user_api)
        response = api_client.post(reverse('accounts:accounts-urls:create-jwt-token'), data, format='json')
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_create_token_jwt_user_valid_response_400(self, api_client, user_api):
        user_api.is_verified = True
        user_api.save()

        api_client.force_authenticate(user=user_api)
        response = api_client.post(reverse('accounts:accounts-urls:create-jwt-token'),  format='json')
        assert response.status_code == 400

    def test_create_token_jwt_user_valid_response_401(self, api_client, user_api):
        user_api.is_verified = True
        user_api.save()
        data = {'email': user_api.email, 'password': user_api.password}
        api_client.force_authenticate(user=user_api)
        response = api_client.post(reverse('accounts:accounts-urls:create-jwt-token'), data, format='json')
        assert response.status_code == 401
  
    def test_refresh_token_jwt_user_valid_response_200(self, api_client, user_api):
        user_api.is_verified = True
        user_api.save()
        data = {'email': user_api.email, 'password': 'a/@123456'}
        response = api_client.post(reverse('accounts:accounts-urls:create-jwt-token'), data, format='json')
        assert response.status_code == 200
        refresh_token = response.data['refresh']
        refresh_data = {'refresh': refresh_token}
        refresh_response = api_client.post(reverse('accounts:accounts-urls:refresh-jwt-token'), refresh_data, format='json')
        assert refresh_response.status_code == 200

    def test_create_token_jwt_user_invalid_credentials_401(self, api_client, user_api):
        # اطمینان از احراز هویت کاربر
        user_api.is_verified = True
        user_api.save()
        
        # احراز هویت کاربر و ایجاد توکن JWT با اطلاعات احراز هویت نامعتبر
        invalid_data = {'email': user_api.email, 'password': 'invalid_password'}
        response = api_client.post(reverse('accounts:accounts-urls:create-jwt-token'), invalid_data, format='json')
        
        # بررسی کد وضعیت پاسخ
        assert response.status_code == 401
        assert 'detail' in response.data
        assert response.data['detail'] == 'No active account found with the given credentials'

    def test_verify_jwt_token_valid_response_200(self , api_client, user_api):
        data = {'email': user_api.email, 'password': 'a/@123456'}
        response = api_client.post(reverse('accounts:accounts-urls:create-jwt-token'), data, format='json')
        assert response.status_code == 200

        access_token = response.data['access']
        verify_data = {'token': access_token}
        verify_response = api_client.post(reverse('accounts:accounts-urls:verify-jwt-token'), verify_data, format='json')
        assert verify_response.status_code == 200

    def test_verify_jwt_token_invalid_response_401(self , api_client, user_api):
        data = {'email': user_api.email, 'password': 'a/@123456'}
        response = api_client.post(reverse('accounts:accounts-urls:create-jwt-token'), data, format='json')
        assert response.status_code == 200

        access_token = response.data.get('access')
        assert access_token is not None
        verify_data = {'token': 'invalid-token'}
        verify_response = api_client.post(reverse('accounts:accounts-urls:verify-jwt-token'), verify_data, format='json')
        assert verify_response.status_code == 401

    def test_get_profile_response200(self, api_client, profile_api):
        Profile.objects.filter(user=profile_api.user).exclude(id=profile_api.id).delete()
        api_client.force_authenticate(user=profile_api.user)
        url = reverse('accounts:profiles-urls:profile-detail')
        response = api_client.get(url, format='json')
        assert response.status_code == 200

    def test_update_profile_put(self, api_client, profile_api):
        api_client.force_authenticate(user=profile_api.user)
        Profile.objects.filter(user=profile_api.user).exclude(id=profile_api.id).delete()
        url = reverse('accounts:profiles-urls:profile-detail')
        update_data = {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'description': 'Updated bio',
        }
        response = api_client.put(url, update_data, format='json')
        assert response.status_code == 200

    def test_update_profile_patch(self, api_client, profile_api):
        api_client.force_authenticate(user=profile_api.user)
        Profile.objects.filter(user=profile_api.user).exclude(id=profile_api.id).delete()
        url = reverse('accounts:profiles-urls:profile-detail')
        update_data = {
            'description': 'Updated bio with PATCH',
        }
        response = api_client.patch(url, update_data, format='json')

        assert response.status_code == 200
