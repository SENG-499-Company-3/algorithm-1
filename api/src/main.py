import numpy as np
import ray
import json
from ray import serve
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models import Schedule
from hypergraph import HyperGraph
from lib import preprocess


app = FastAPI()

@serve.deployment(route_prefix="/")
@serve.ingress(app)
class Algorithm1:

    @app.post("/create")
    def create_schedule(self) -> JSONResponse:
        courses = 33
        times = 51
        teachers = 29
        
        dims = {"courses":courses, "times":times, "teachers":teachers}

        #prefs = np.random.randint(7, size=(teachers, times, courses), dtype=np.uint64)
        prefs = preprocess() 
        loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
        max_iter = 2500
        P = np.array([0,1,2,3,4,5,6], dtype=np.uint64)
        p_tgt = 3 
        
        hg = HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)
        hg.solve()
        schedule = {str(key): str(val) for key, val in hg.sparse().items()}
        
        return JSONResponse(content=schedule)
    
    @app.post("/validate")
    def validate_schedule(self) -> JSONResponse:
        courses = 33
        times = 51
        teachers = 29
        
        dims = {"courses":courses, "times":times, "teachers":teachers}

        #prefs = np.random.randint(7, size=(teachers, times, courses), dtype=np.uint64)
        prefs = preprocess() 
        loads = np.array([3 for i in range(teachers)], dtype=np.uint64)
        max_iter = 2500
        P = np.array([0,1,2,3,4,5,6], dtype=np.uint64)
        p_tgt = 3 
        
        hg = HyperGraph(dims, prefs, loads, max_iter, P, p_tgt)
        hg.solve()
        schedule = {str(key): str(val) for key, val in hg.sparse().items()}
        
        return JSONResponse(content=schedule)

deployment_graph = Algorithm1.bind()
