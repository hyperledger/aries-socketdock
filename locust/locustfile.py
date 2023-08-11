from locust import SequentialTaskSet, task, User, between
from locustClient import CustomClient
import os

class CustomLocust(User):
    abstract = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.client = CustomClient(self.host)

class UserBehaviour(SequentialTaskSet):
    def on_start(self):
        self.client.startup()

    def on_stop(self):
        self.client.shutdown()

    @task
    def msg_client(self):
        self.client.msg_client()

class SocketDock(CustomLocust):
    tasks = [UserBehaviour]
    wait_time = between(float(os.getenv('LOCUST_MIN_WAIT',0.1)), float(os.getenv('LOCUST_MAX_WAIT',1)))
