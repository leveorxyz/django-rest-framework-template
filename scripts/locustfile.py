from locust import HttpUser, task, between


class AccountUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def user_info(self):
        self.client.get("/")
