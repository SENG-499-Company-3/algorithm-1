import ray
from ray import serve
from fastapi import FastAPI


app = FastAPI()

@serve.deployment(route_prefix="/")
@serve.ingress(app)
class Algorithm1:
    @app.get("/{name}")
    async def say_hello(self, name: str) -> str:
        return f"Hello {name}!" 

deployment_graph = Algorithm1.bind()
