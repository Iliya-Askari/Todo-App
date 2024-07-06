# import pytest
# from rest_framework.test import APIClient
# from django.urls import reverse , resolve
# from datetime import datetime

# from accounts.models import Users
# from todo.models import Task
# from todo.api.v1.views import TaskViewSet

# @pytest.fixture
# def api_client():
#     client = APIClient()
#     return client

# @pytest.fixture
# def user_api():
#     user = Users.objects.create_user(email='user@example.com',password='a/@123456')
#     return user

# @pytest.fixture
# def task_api(user_api):
#     task = Task.objects.create(title = "Task" , user = user_api)
#     return task

# @pytest.mark.django_db
# class TestTodoApiView:

#     def test_get_task_response_200(self,api_client,user_api):
#         api_client.force_authenticate(user=user_api)
#         response = api_client.get(reverse('todo:api-v1:tasklist-list'))
#         assert response.status_code == 200

#     def test_post_task_response_201(self, api_client, user_api):
#         api_client.force_authenticate(user=user_api)
#         data = {
#             'title': 'Test Task',
#         }
#         response = api_client.post(reverse('todo:api-v1:tasklist-list'), data=data)
#         assert response.status_code == 201
    
#     def test_put_task_response_200(self, api_client, user_api , task_api):
#         api_client.force_authenticate(user=user_api)
#         task = task_api
#         data = {
#             'title': 'Updated Test Task',
#         }
#         response = api_client.put(reverse('todo:api-v1:tasklist-detail', kwargs={'pk': task.pk}), data=data)
#         assert response.status_code == 200
    
#     def test_patch_task_response_200(self, api_client, user_api , task_api):
#         api_client.force_authenticate(user=user_api)
#         task = task_api
#         data = {
#             'title': 'Updated Test Task',
#         }
#         response = api_client.patch(reverse('todo:api-v1:tasklist-detail', kwargs={'pk': task.pk}), data=data)
#         assert response.status_code == 200

#     def test_delete_task_response_204(self, api_client, user_api, task_api):
#         api_client.force_authenticate(user=user_api)
#         task = task_api
#         response = api_client.delete(reverse('todo:api-v1:tasklist-detail', kwargs={'pk': task.pk}))
#         assert response.status_code == 204
    
#     def test_get_task_unauthorized_response_401(self, api_client):
#         response = api_client.get(reverse('todo:api-v1:tasklist-list'))
#         assert response.status_code == 401

#     def test_get_task_not_found_response_404(self, api_client, user_api):
#         api_client.force_authenticate(user=user_api)
#         response = api_client.get(reverse('todo:api-v1:tasklist-detail', kwargs={'pk': 999}))
#         assert response.status_code == 404

#     def test_post_task_bad_request_response_400(self, api_client, user_api):
#         api_client.force_authenticate(user=user_api)
#         data = {'title': ''}  
#         response = api_client.post(reverse('todo:api-v1:tasklist-list'), data=data)
#         assert response.status_code == 400

# @pytest.mark.django_db
# class TestTodoApiUrl:
    
#     def test_tasklist_list_url(self, api_client):
#         url = reverse('todo:api-v1:tasklist-list')
#         assert resolve(url).func.cls == TaskViewSet
#         response = api_client.get(url)
#         assert response.status_code in [200, 401]  # 401 اگر احراز هویت نیاز باشد

#     def test_tasklist_detail_url(self, api_client, task_api):
#         url = reverse('todo:api-v1:tasklist-detail', kwargs={'pk': task_api.pk})
#         assert resolve(url).func.cls == TaskViewSet
#         response = api_client.get(url)
#         assert response.status_code in [200, 401, 404]  # 401 اگر احراز هویت نیاز باشد و 404 اگر مورد وجود نداشته باشد

#     def test_tasklist_create_url(self, api_client, user_api):
#         api_client.force_authenticate(user=user_api)
#         url = reverse('todo:api-v1:tasklist-list')
#         data = {'title': 'Test Task'}
#         response = api_client.post(url, data=data)
#         assert response.status_code == 201

#     def test_tasklist_update_url(self, api_client, user_api, task_api):
#         api_client.force_authenticate(user=user_api)
#         url = reverse('todo:api-v1:tasklist-detail', kwargs={'pk': task_api.pk})
#         data = {'title': 'Updated Test Task'}
#         response = api_client.put(url, data=data)
#         assert response.status_code == 200

#     def test_tasklist_delete_url(self, api_client, user_api, task_api):
#         api_client.force_authenticate(user=user_api)
#         url = reverse('todo:api-v1:tasklist-detail', kwargs={'pk': task_api.pk})
#         response = api_client.delete(url)
#         assert response.status_code == 204