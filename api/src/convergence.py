import pickle
from montecarlo import generate_prefs, generate_teacher_loads
from models import InputData
from drivers import distributed_driver

def main(num_simulations: int = 1): 
    schedules = []

    for i in range(num_simulations):
        output = {}
        input_data = InputData(
            prefs = generate_prefs(),
            loads = generate_teacher_loads(),
        )
        print(input_data.loads)

        # Run distributed driver
        schedule = distributed_driver(input_data=input_data)
        output = {"sim_num": i, "prefs": input_data.preferences, "loads": input_data.loads, "schedule": schedule.sparse_tensor, "iteration": schedule.iter, "quality": schedule.quality, "reward": schedule.reward, "c_hat": schedule.c_hat}
        schedules.append(output)

        if i != 0 and i % 100 == 0:
            print(f"Dumping to file...")
            with open(f'./data/generated_schedules.pkl', 'wb') as f:
                pickle.dump(schedules, f)
            f.close()
            schedules = []
        
    with open(f'./data/generated_schedules.pkl', 'wb') as f:
        pickle.dump(schedules, f)
    f.close()
    with open(f'./data/generated_schedules.pkl', 'rb') as f:
        unpickled = pickle.load(f)
        print(unpickled)
    f.close()
    return schedules

if __name__ == '__main__':
    main()