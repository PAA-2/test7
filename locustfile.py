from locust import HttpUser, task, between


class PAAUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def dashboard(self):
        self.client.get("/dashboard/", name="dashboard")

    @task(5)
    def actions(self):
        self.client.get("/actions/?q=a", name="actions_list")

    @task(1)
    def search(self):
        self.client.get("/search/?q=test", name="search")
