import requests
import ray
from ray import serve
from fastapi import FastAPI



app = FastAPI()
@serve.deployment(route_prefix="/")
@serve.ingress(app)
class Algorithm1:
    @app.get("/hello")
    def say_hello(self, name: str):
        return f"Hello {name}!" 

ray.init(address='auto', namespace="serve-example", ignore_reinit_error=True)
serve.start(detached=True)
Algorithm1.deploy()
