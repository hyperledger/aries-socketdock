from locust import events
from flask import Flask

import time
import inspect
import json

import fcntl
import os
import requests
import signal

from websocket import create_connection
import websocket 

import sys
import gevent

gevent.monkey.patch_all()

def stopwatch(func):
    def wrapper(*args, **kwargs):
        # get task's function name
        previous_frame = inspect.currentframe().f_back
        file_name, _, task_name, _, _ = inspect.getframeinfo(previous_frame)

        start = time.time()
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            total = int((time.time() - start) * 1000)
            events.request_failure.fire(request_type="TYPE",
                                        name=file_name + '_' + task_name,
                                        response_time=total,
                                        exception=e,
                                        response_length=0)
        else:
            total = int((time.time() - start) * 1000)
            events.request_success.fire(request_type="TYPE",
                                        name=file_name + '_' + task_name,
                                        response_time=total,
                                        response_length=0)
        return result

    return wrapper

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class InboundHTTP(metaclass=Singleton):
    _self = None

    def __init__(self):

        app = Flask(__name__)

        @app.route("/")
        def hello_world():
            return "<p>Hello, World!</p>"

        @app.route("/connect", methods=['POST'])
        def connect():
            return "<p>Hello, World!</p>"    

        @app.route("/disconnect", methods=['POST'])
        def disconnect():
            return "<p>Hello, World!</p>"

        @app.route("/message", methods=['POST'])
        def message():
            return "<p>Hello, World!</p>"

        gevent.spawn(app.run, host="0.0.0.0", port=4242)

    def track(self):
        print(f"TODO track event at {self.api_url}")

class CustomClient:
    def __init__(self, host):
        self.host = host

    _locust_environment = None

    def startup(self):
        # print("startup", file=sys.stderr)

        server = InboundHTTP()

        # Give a sec for the inbound server to start
        time.sleep(5)# Magic Number

        self.connected = False

        def on_message(wsapp, message):
            print(message)

        def on_open(wsapp):
            self.connected = True

        def on_close(wsapp):
            self.connected = False

        # Debugging stuff
        # websocket.enableTrace(True)

        self.ws = websocket.WebSocketApp("ws://websocket-gateway:8765/ws", on_message=on_message, on_open=on_open, on_close=on_close)
        gevent.spawn(self.ws.run_forever) 

        while not self.connected:
            time.sleep(1)

        
    def shutdown(self):
        self.ws.close()
        
    @stopwatch
    def msg_client(self):
        i = ''
        if self.connected == False:
            raise Exception("Not Connected!")
        self.ws.send(f"Ping! ({i})")
        pass
