import numpy as np
from matplotlib import pyplot as plt

MIN_TEACHERS_PER_COURSE = 0
MAX_TEACHERS_PER_COURSE = 1


class HyperGraph:
    def __init__(self, dims, prefs, loads, max_iter=1000, P=np.arange(7, dtype=np.uint8), p_tgt=3):
        assert "courses" in dims and "times" in dims and "teachers" in dims
        self.dtype = np.uint8
        self.dims = dims
        self.dim_idx_map = {"courses": 0, "times": 1, "teachers": 2}
        self.shape = (dims["courses"], dims["times"], dims["teachers"])
        self.prefs = prefs
        self.loads = loads
        self.iter = 0
        self.max_iter = max_iter
        self.P = P
        self.p_tgt = p_tgt
        self.set_sufficient_reward()
        self.tensor = np.zeros(shape=self.shape, dtype=self.dtype)
        self.reset()

    def reset(self, tensor=None):
        if tensor is None:
            tensor = self.tensor
        tensor[:, :, :] = 0
        self.random_search(tensor)

    def random_search(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        card_c, card_ti, _ = tensor.shape

        for course in range(card_c):
            time = np.random.randint(low=0, high=card_ti, size=1)
            ideal_tc_matches = np.where(self.prefs[:, course] >= self.p_tgt)[0]
            if ideal_tc_matches.size > 0:
                teacher = np.random.choice(ideal_tc_matches, size=1)
                tensor[course, time, teacher] = 1

    def set_sufficient_reward(self):
        card_c, _, _ = self.shape
        self.sufficient_reward = card_c * np.tanh(self.p_tgt - np.median(self.P))

    def solve(self):
        reward, max_reward = 0, 0
        random_tensor = np.zeros(self.shape, dtype=self.dtype)

        for self.iter in range(self.max_iter):
            if self.done(max_reward):
                break

            self.reset(random_tensor)
            reward = self.calc_reward(random_tensor)

            if reward > max_reward:
                max_reward = reward
                self.tensor[:, :, :] = random_tensor[:, :, :]

    def done(self, reward):
        if self.is_valid_schedule() and reward >= self.sufficient_reward:
            return True
        return False

    def sparse(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        courses, times, teachers = tensor.nonzero()
        assert courses.size == times.size == teachers.size
        sparse_tensor = {
            (courses[i], times[i], teachers[i]): self.prefs[teachers[i], courses[i]]
            for i in range(courses.size)
        }
        return sparse_tensor

    def plot(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        plt.rcParams["figure.figsize"] = [10.00, 5.00]
        plt.rcParams["figure.autolayout"] = True
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.set_xlabel("$Courses$")
        ax.set_ylabel("$Times$")
        ax.set_zlabel("$Teachers$")
        courses, times, teachers = tensor.nonzero()
        ax.scatter(courses, times, teachers, c=teachers, alpha=1)
        plt.show()

    def calc_reward(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        courses, times, teachers = tensor.nonzero()
        assert courses.size == teachers.size
        tc_pairs = [(teachers[i], courses[i]) for i in range(courses.size)]
        p_hat = np.array(
            [self.prefs[tc_pair] for tc_pair in tc_pairs], 
            dtype=self.dtype
        )

        R = np.sum(np.tanh(p_hat - np.median(self.P)), dtype=np.float32)

        return R

    def is_complete(self, tensor=None):
        if tensor is None:
            tensor = self.tensor
        
        card_c, _, _ = tensor.shape

        if len(self.sparse().items()) < card_c:
            return False
        
        return True

    def is_valid_schedule(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        no_imbalanced_loads = self.check_course_loads(tensor)
        no_time_conflicts = self.check_time_conflicts(tensor)

        if no_imbalanced_loads and no_time_conflicts:
            return True

        return False

    def check_time_conflicts(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        proj = self.proj_2d(("teachers", "times"), tensor)
        teachers, times = proj.shape

        for teacher in range(teachers):
            window = 2
            time = 2
            while time < times - 1:
                time_window = proj[teacher, time - window : time + window + 1]
                assignments_in_window = np.count_nonzero(time_window)

                if assignments_in_window > 1:
                    return False

                if time == 22:
                    time = 25
                    window = 1

                time += 1

        return True

    def check_course_loads(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        proj = self.proj_2d(("teachers", "courses"), tensor)
        num_courses_per_teacher = np.count_nonzero(proj, axis=1)
        num_teachers_per_course = np.count_nonzero(proj, axis=0)

        if (num_teachers_per_course[num_teachers_per_course < MIN_TEACHERS_PER_COURSE].size > 0):
            return False

        if (num_teachers_per_course[num_teachers_per_course > MAX_TEACHERS_PER_COURSE].size > 0):
            return False

        if num_courses_per_teacher[num_courses_per_teacher > self.loads].size > 0:
            return False

        return True

    def proj_2d(self, dim_keys, tensor=None):
        assert len(dim_keys) == 2

        if tensor is None:
            tensor = self.tensor

        k1, k2 = dim_keys
        idx1, idx2 = self.dim_idx_map[k1], self.dim_idx_map[k2]
        n, m = self.shape[idx1], self.shape[idx2]
        proj = np.zeros(shape=(n, m), dtype=self.dtype)
        sparse_tensor = self.sparse(tensor)

        for loc in sparse_tensor:
            i, j = loc[idx1], loc[idx2]
            proj[i, j] = 1

        return proj
