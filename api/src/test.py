from search_drivers import distributed_driver, sequential_driver
import time

start = time.time()
hg = distributed_driver()
end = time.time()
print(f"run-time: {end - start}\nvalid: {hg.is_valid_schedule()}\niter: {hg.iter}\nsufficient reward: {hg.sufficient_reward}\nreward: {hg.calc_reward()}\n\nassignments:\n{hg.sparse_tensor}\n\npreferences:\n{hg.prefs}")
#hg.plot()
