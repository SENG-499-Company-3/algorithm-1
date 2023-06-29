import numpy as np
from matplotlib import pyplot as plt
import sys



MAX_TEACHERS_PER_COURSE = 1
MAX_TIMES_PER_COURSE = 1
MAX_REQUIRED_COURSES_PER_TIME = 1



class HyperGraph:
    def __init__(self, dims, prefs, loads, required_course_pivots, max_iter=1000, P=np.arange(7, dtype=np.uint8), p_tgt=3):
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
        self.set_pivots(required_course_pivots)

    def set_pivots(self, pivots):
        _, card_ti, _ = self.shape
        sorted_pivots = np.sort(pivots)
        start = 0
        for pivot in sorted_pivots:
            stop = pivot + 1
            
            if stop - start > card_ti:
                return False

            start = stop

        self.pivots = sorted_pivots
        return True

    def reset(self, tensor=None):
        if tensor is None:
            tensor = self.tensor
        tensor[:, :, :] = 0

    def random_search(self, tensor=None):
        if tensor is None:
            tensor = self.tensor
        
        teacher_loads = self.loads.copy()
        card_c, card_ti, _ = tensor.shape
        start = 0

        for pivot in self.pivots:
            stop = pivot + 1 
            candidate_times = [i for i in range(card_ti)]
            preferred = self.get_preferred(start, stop).items()
            
            for course, pref_teachers in preferred:
                candidate_teachers = [teacher for teacher in pref_teachers if teacher_loads[teacher] > 0]
                teacher = np.random.choice(candidate_teachers, size=1)
                time = np.random.choice(candidate_times, size=1, replace=False)
                tensor[course, time, teacher] = self.prefs[teacher, course] 
                teacher_loads[teacher] -= 1
                candidate_times.remove(time)
            
            start = stop 

    def get_preferred(self, start, stop):
        candidate_teachers, candidate_courses = np.where(self.prefs[:, start : stop] >= self.p_tgt)
        candidate_assignment_dict = {}
        
        for idx in range(candidate_teachers.size):
            course = candidate_courses[idx]
            teacher = candidate_teachers[idx]
            
            if course not in candidate_assignment_dict:
                candidate_assignment_dict[course] = [teacher]
                
            else:
                candidate_assignment_dict[course].append(teacher)
                
        return candidate_assignment_dict

    def set_sufficient_reward(self):
        card_c, _, _ = self.shape
        self.sufficient_reward = card_c * np.tanh(self.p_tgt - np.median(self.P))

    def solve(self):
        reward, max_reward = 0, 0
        random_tensor = np.zeros(self.shape, dtype=self.dtype)
        self.random_search()
        return
        for self.iter in range(self.max_iter):
            self.random_search(random_tensor)
            
            if self.is_valid_schedule():
                self.tensor[:, :, :] = random_tensor[:, :, :]
            
    def done(self, reward):
        if self.is_valid_schedule() and reward > self.sufficient_reward:
            return True
        return False

    def sparse(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        courses, times, teachers = tensor.nonzero()
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

        no_course_time_conflicts = self.check_course_time_constraint(tensor) 
        no_course_teacher_conflicts = self.check_course_teacher_constraint(tensor)

        if no_course_time_conflicts and no_course_teacher_conflicts:
            return True

        return False

    def check_course_time_constraint(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        proj = self.proj_2d(("courses", "times"), tensor)
        num_times_per_course = np.count_nonzero(proj, axis=1)
        num_courses_per_time = np.count_nonzero(proj, axis=0)

        if num_times_per_course[num_times_per_course > MAX_TIMES_PER_COURSE].size > 0:
            return False
        
        start = 0
        for pivot in self.pivots:
            stop = pivot + 1
            required_courses = num_courses_per_time[start : stop] 
            
            if required_courses[required_courses > MAX_REQUIRED_COURSES_PER_TIME].size > 0:
                return False
            
            start = stop

        return True

    def check_course_teacher_constraint(self, tensor=None):
        if tensor is None:
            tensor = self.tensor

        proj = self.proj_2d(("teachers", "courses"), tensor)
        num_courses_per_teacher = np.count_nonzero(proj, axis=1)
        num_teachers_per_course = np.count_nonzero(proj, axis=0)

        if num_teachers_per_course[num_teachers_per_course > MAX_TEACHERS_PER_COURSE].size > 0:
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
