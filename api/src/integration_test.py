import requests
import numpy as np

prefs = np.loadtxt('../data/formatted_prefs.csv', delimiter=',')
p_counts, bins = np.histogram(prefs, bins=np.arange(0,8)) #Look at documentation

P = np.arange(0,7, dtype=np.uint64)
PREF_PROBS = p_counts/p_counts.sum()


def generate_prefs():
    generated_prefs = np.random.choice(P, size=(29, 33), p=PREF_PROBS)
    res = generated_prefs.astype(int).tolist()
    return res

def generate_teacher_loads(teachers):
    generated_loads = []
    for i in range(teachers):
        generated_loads.append(np.random.randint(1, 4))
    return generated_loads

input_data = {
    "rooms": {
        "location": "string",
        "capacity": 0,
        "equipment": [
            "string"
        ]
    },
    "timeslots": {
        "day": [
            "string"
        ],
        "length": 0,
        "startTime": 0
    },
    "courses": 
        {"coursename": "Mathematics", "noScheduleOverlap": ["Physics", "Chemistry"], "lecturesNumber": 3, "labsNumber": 1, "tutorialsNumber": 2, "capacity": 100 },
    "professors": {
        "name": "string",
        "courses": [
            "string"
        ],
        "timePreferences": [
            "string"
        ],
        "coursePreferences": [
            "string"
        ],
        "dayPreferences": [
            "string"
        ],
        "equipmentPreferences": [
            "string"
        ]
    },
    "dimensions": 
        {
            "courses": 33,
            "times": 15,
            "teachers": 29,
            "rooms": 0
        },
    "preferences": [[]],
    "loads": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    "availabilities": [
        [
            0
        ]
    ],
    "p_tgt": 4,
    "max_iter": 999
    }
for i in range(10):
    input_data["preferences"] = generate_prefs()
    #input_data["loads"] = generate_teacher_loads(input_data[])

    #Note: this will not work on the server "http://52.39.88.189:8000/schedule/create" until the new api_schema is implemented.
    #To run on the server in the mean time, inside input_data modify the dimensions and loads to be a list of dictionaries and a list of lists, respectively (add an exterior [] to both) 
    r = requests.post("http://localhost:8000/schedule/create", json=input_data)
    print(r.status_code)
