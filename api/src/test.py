from search_drivers import batch_driver, sequential_driver


hg = sequential_driver()
print(f"valid: {hg.is_valid_schedule()}\nsufficient reward: {hg.sufficient_reward}\nreward: {hg.calc_reward()}\nassignments: {hg.sparse()}")
