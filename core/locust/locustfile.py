from locust import HttpUser, task, between

class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post("/accounts/api/v1/jwt/create/", data ={"email": "admin@1admin.com",
                                                        "password": "123"
                                                        }).json()
        
        self.client.headers = {"Authorization": f"Bearer {response.get('access',None)}"}

    @task
    def post_list(self):
        self.client.get("/api/v1/Tasklist/")
