from models import InputData
from models import *
from drivers import distributed_driver
from hypergraph import HyperGraph
from rooms import add_rooms


def generate_schedule(input_data: InputData = None):
    hypergraph = distributed_driver(input_data)
    if hypergraph is None:
        print("hypergraph is none")

    # check hypergraph not none
    rooms_list = add_rooms(hypergraph)

    assignments_list = []

    # generate schedule

    # this needs to be schedule

    return hypergraph
