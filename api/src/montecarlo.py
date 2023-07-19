import numpy as np
import matplotlib.pyplot as plt

def generate_prefs():
    prefs = np.loadtxt('./data/formatted_prefs.csv', delimiter=',')
    p_counts, bins = np.histogram(prefs, bins=np.arange(0,8))
    pref_probs = p_counts/p_counts.sum()
    P = np.arange(0, 7)
    generated_prefs = np.random.choice(P, size=(29, 33), p=pref_probs)
    return generated_prefs

def generate_teacher_loads(teachers=29):
    loads = np.loadtxt('./data/formatted_loads.csv', delimiter=',')
    generated_loads = []
    p_counts, bins = np.histogram(loads, bins=np.arange(0,8))
    loads_probs = p_counts/p_counts.sum()
    P = np.arange(0,7)
    for i in range(teachers):
        generated_loads.append(np.random.choice(P, p=loads_probs))
    return generated_loads

def main(num_simulations: int = 5, show_plot: bool = False):
    all_prefs = []
    all_loads = []
    num_simulations = 5

    prefs = np.loadtxt('./data/formatted_prefs.csv', delimiter=',')
    # loads = np.loadtxt('./data/formatted_loads.csv', delimiter=',')
    p_counts, bins = np.histogram(prefs, bins=np.arange(0,8))
    # pref_probs = p_counts/p_counts.sum()

    for i in range(num_simulations):
        all_prefs.append(generate_prefs())
        all_loads.append(generate_teacher_loads(29))
    array = np.asarray(all_prefs)

    # Plot last generated preferences
    if show_plot:
        plt.hist(all_prefs[-1][-1], bins)
        plt.show()

    # Save generated preferences to csv
    # Each case is a 29x33 matrix divided by a newline with "Case i" as the header
    with open('./data/generated_prefs.csv', 'w') as f:
        for i in range(array.shape[0]):
            f.write("Case " + str(i+1) + "\n")
            np.savetxt(f, array[i], delimiter=',', fmt='%d')
    f.close()

    return all_prefs, all_loads

if __name__ == '__main__':
    main()