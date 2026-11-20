from locust import HttpUser, task, between


class ApplicationUser(HttpUser):

    wait_time = between(0.1, 0.5)

    @task(3)
    def home(self):
        self.client.get("/")

    @task(2)
    def information(self):
        self.client.get("/info")

    @task(5)
    def cpu_work(self):
        self.client.get("/work?ms=200")

    @task(1)
    def health(self):
        self.client.get("/health/live")
