import numpy as np
import copy
from matplotlib import pyplot as plt
from typing import List, Tuple


MAX_TEACHERS_PER_COURSE = 1
MAX_TIMES_PER_COURSE = 1
MAX_REQUIRED_COURSES_PER_TIME = 1


class HyperGraph:
    def __init__(
        self, 
        dims: dict, 
        prefs: np.ndarray, 
        loads: np.ndarray,
        required_course_pivots: List[int],
        max_iter: int = 1000, 
        P: np.arange = np.arange(7, dtype=np.uint8), 
        p_tgt: int = 3
    ):
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
        self.pivots = np.sort(required_course_pivots) 
        self.sufficient_reward = self.shape[0] * np.tanh(self.p_tgt - np.median(self.P)) 
        self.sparse_tensor = {}
 
    def calc_reward(self, sparse_tensor: dict = None) -> float:
        if sparse_tensor is None:
            sparse_tensor = self.sparse_tensor

        p_hat = np.array(list(sparse_tensor.values()), dtype=self.dtype)
        R = np.sum(np.tanh(p_hat - np.median(self.P)), dtype=np.float32)

        return R

    def random_search(self, sparse_tensor: dict) -> None:
        teacher_loads = self.loads.copy()
        _, card_ti, card_te = self.shape
        start = 0

        for pivot in self.pivots:
            stop = pivot 
            candidate_times = [i for i in range(card_ti)]
             
            for course in range(start, stop):
                candidate_teachers = [
                    teacher for teacher in range(card_te) 
                    if teacher_loads[teacher] > 0 and 
                    self.prefs[teacher, course] >= self.p_tgt
                ]
                if not candidate_teachers: 
                    continue
                teacher = int(np.random.choice(candidate_teachers, size=1))
                time = int(np.random.choice(candidate_times, size=1, replace=False))
                sparse_tensor[(course, time, teacher)] = self.prefs[teacher, course] 
                teacher_loads[teacher] -= 1
                candidate_times.remove(time)
            
            start = stop 

    def solve(self) -> None:
        reward, max_reward = 0, 0
        random_tensor = {}

        for i in range(self.max_iter):
            self.random_search(random_tensor)
            reward = self.calc_reward(random_tensor)
            
            if reward > max_reward:
                self.iter = i 
                max_reward = reward
                self.sparse_tensor = copy.deepcopy(random_tensor)

            random_tensor.clear()

    def is_complete(self, sparse_tensor: dict) -> bool:
        card_c, _, _ = self.shape

        if len(self.sparse_tensor.items()) < card_c:
            return False
        
        return True

    def is_valid_schedule(self, sparse_tensor: dict = None) -> bool:
        if sparse_tensor is None:
            sparse_tensor = self.sparse_tensor

        no_course_time_conflicts = self.check_course_time_constraint(sparse_tensor) 
        no_course_teacher_conflicts = self.check_course_teacher_constraint(sparse_tensor)

        if no_course_time_conflicts and no_course_teacher_conflicts:
            return True

        return False

    def check_course_time_constraint(self, sparse_tensor: dict) -> bool:
        proj = self.proj_2d(("courses", "times"), sparse_tensor)
        num_times_per_course = np.count_nonzero(proj, axis=1)

        if num_times_per_course[num_times_per_course > MAX_TIMES_PER_COURSE].size > 0:
            return False
         
        start = 0
        for pivot in self.pivots:
            stop = pivot
            required_courses = num_times_per_course[start : stop] 
            
            if required_courses[required_courses > MAX_REQUIRED_COURSES_PER_TIME].size > 0:
                return False
            
            start = stop

        return True

    def check_course_teacher_constraint(self, sparse_tensor: dict) -> bool:
        proj = self.proj_2d(("teachers", "courses"), sparse_tensor)
        num_courses_per_teacher = np.count_nonzero(proj, axis=1)
        num_teachers_per_course = np.count_nonzero(proj, axis=0)

        if num_teachers_per_course[num_teachers_per_course > MAX_TEACHERS_PER_COURSE].size > 0:
            return False

        if num_courses_per_teacher[num_courses_per_teacher > self.loads].size > 0:
            return False

        return True

    def proj_2d(self, dim_keys: Tuple[str, str], sparse_tensor: dict) -> np.ndarray:
        k1, k2 = dim_keys
        idx1, idx2 = self.dim_idx_map[k1], self.dim_idx_map[k2]
        n, m = self.shape[idx1], self.shape[idx2]
        proj = np.zeros(shape=(n, m), dtype=self.dtype)

        for assignment in sparse_tensor:
            i, j = assignment[idx1], assignment[idx2]
            proj[i, j] = 1

        return proj

    def plot(self, sparse_tensor: dict = None) -> None:
        if sparse_tensor is None:
            sparse_tensor = self.sparse_tensor
        
        plt.rcParams["figure.figsize"] = [10.00, 5.00]
        plt.rcParams["figure.autolayout"] = True
        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.set_xlabel("$Courses$")
        ax.set_ylabel("$Times$")
        ax.set_zlabel("$Teachers$")
        courses = np.asarray([assignment[0] for assignment in sparse_tensor])
        times = np.asarray([assignment[1] for assignment in sparse_tensor])
        teachers = np.asarray([assignment[2] for assignment in sparse_tensor])
        ax.scatter(courses, times, teachers, c=teachers, alpha=1)
        plt.show()
