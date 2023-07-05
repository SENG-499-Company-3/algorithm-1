import numpy as np
import matplotlib.pyplot as plt

def generate_prefs(P, pref_probs):
    generated_prefs = np.random.choice(P, size=(29, 33), p=pref_probs)
    return generated_prefs

def generate_teacher_loads(teachers):
    generated_loads = []
    for i in range(teachers):
        generated_loads.append(np.random.randint(1, 4))
    return generated_loads

all_prefs = []
all_loads = []
num_simulations = 5

P = np.arange(0, 7)
prefs = np.loadtxt('./formatted_prefs.csv', delimiter=',')
# print(generate_teacher_loads(29))
p_counts, bins = np.histogram(prefs, bins=np.arange(0,8))
pref_probs = p_counts/p_counts.sum()

for i in range(num_simulations):
    all_prefs.append(generate_prefs(P, pref_probs))
    all_loads.append(generate_teacher_loads(29))
array = np.asarray(all_prefs)

# Plot last generated preferences
plt.hist(all_prefs[-1][-1], bins)
plt.show()

# Save generated preferences to csv
# Each case is a 29x33 matrix divided by a newline with "Case i" as the header
with open('./generated_prefs.csv', 'w') as f:
    for i in range(array.shape[0]):
        f.write("Case " + str(i+1) + "\n")
        np.savetxt(f, array[i], delimiter=',', fmt='%d')
f.close()