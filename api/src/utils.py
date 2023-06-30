import numpy as np
from typing import List
from models import InputData
from hypergraph import HyperGraph


def preprocess(fname: str = "prefs.csv") -> np.ndarray:
    val_map = {0: 0, 20: 1, 39: 2, 40: 3, 78: 4, 100: 5, 195: 6}
    prefs = np.loadtxt(fname, delimiter=",", dtype=np.uint64)
    rows, cols = prefs.shape
    
    for i in range(rows):
        for j in range(cols):
            prefs[i, j] = val_map[prefs[i, j]]
    
    return prefs


def numpy_to_fastapi_type_conversion(hg: HyperGraph) -> List[List[int]]:
    items = hg.sparse().items()

    fastapi_type_compatible_assignments = [
        [num.item() for num in key]
        for key, _ in items
    ]
    
    return fastapi_type_compatible_assignments 
