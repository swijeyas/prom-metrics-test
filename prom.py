import prometheus_client

from prometheus_client import Gauge

class Metric:
    def __init__(self, name, reg):
        self.g = Gauge(name, 'This is my gauge', multiprocess_mode="livemostrecent", registry=reg)

    def update(self, val):
        self.g.set(val)
