import numpy as np
import itertools
import copy
from matplotlib import pyplot as plt
from typing import List, Tuple, Union


MAX_TEACHERS_PER_COURSE = 1
MAX_TIMES_PER_COURSE = 1
MAX_REQUIRED_COURSES_PER_TIME = 1
MAX_TIME_PER_TEACHER = 1


class HyperGraph:
    def __init__(
        self, 
        dims: dict, 
        prefs: np.ndarray, 
        loads: np.ndarray,
        required_course_pivots: np.ndarray,
        max_iter: int = 1000, 
        P: np.arange = np.arange(7, dtype=np.uint8), 
        p_tgt: int = 4,
    ):
        self.dims = dims 
        self.prefs = prefs
        self.loads = loads
        self.pivots = np.sort(required_course_pivots) 
        self.max_iter = max_iter
        self.P = P
        self.p_tgt = p_tgt
        self.dtype = np.uint8
        self.sparse_tensor = {}
        self.candidates = {}
        self.iter = 0
        self.c_hat = 0.0
        self.reward = 0.0
        self.quality = 0.0
        self.dim_idx_map = {"courses": 0, "times": 1, "teachers": 2} 
        self.shape = (dims["courses"], dims["times"], dims["teachers"])
        self.max_reward = self.shape[0] * (1 + np.tanh(P.max() - np.median(P)))
 
    def calc_reward(self, sparse_tensor: dict = None) -> Tuple[float, float]:
        if sparse_tensor is None:
            sparse_tensor = self.sparse_tensor
       
        card_psi, _, _ = self.shape
        c_hat = float(len(sparse_tensor) / card_psi)
        p_hat = np.array(list(sparse_tensor.values()), dtype=self.dtype)
        R = (c_hat * card_psi) + np.sum(np.tanh(p_hat - np.median(self.P)), dtype=np.float32)
        return (R, c_hat)

    def random_search(self, sparse_tensor: dict) -> None:
        _, card_gamma, card_delta = self.shape
        assigned_teachers_times = np.zeros(shape=(card_delta, card_gamma), dtype=self.dtype)
        teacher_loads = self.loads.copy()
        start = 0

        for pivot in self.pivots:
            stop = pivot 
            candidate_times = {ti for ti in range(card_gamma)}

            for course in range(start, stop):
                time = int(np.random.choice(list(candidate_times), size=1, replace=False))

                candidate_teachers = {
                    teacher for teacher in range(card_delta) if
                    teacher_loads[teacher] > 0 and 
                    self.prefs[teacher, course] >= self.p_tgt and 
                    not assigned_teachers_times[teacher, time]
                }

                self.candidates[course] = (candidate_times, candidate_teachers)
                if not candidate_teachers: continue
                teacher = int(np.random.choice(list(candidate_teachers), size=1))
                sparse_tensor[(course, time, teacher)] = self.prefs[teacher, course]
                assigned_teachers_times[teacher, time] = 1
                teacher_loads[teacher] -= 1
                candidate_times.remove(time)
            
            start = stop 

    def solve(self) -> None:
        curr_reward = 0
        random_tensor = {}

        for i in range(self.max_iter):
            self.random_search(random_tensor)
            curr_reward, c_hat = self.calc_reward(random_tensor)
            
            if curr_reward > self.reward:
                self.iter = i 
                self.reward = curr_reward
                self.c_hat = c_hat
                self.quality = curr_reward / self.max_reward
                self.sparse_tensor = copy.deepcopy(random_tensor)

            random_tensor.clear()

    def is_complete(self, sparse_tensor: dict = None) -> bool:
        if sparse_tensor is None:
            sparse_tensor = self.sparse_tensor

        card_psi, _, _ = self.shape

        if len(sparse_tensor) < card_psi:
            return False
        
        return True

    def is_valid_schedule(self, sparse_tensor: dict = None) -> bool:
        if sparse_tensor is None:
            sparse_tensor = self.sparse_tensor
        
        no_course_time_conflicts = self.check_course_time_constraint(sparse_tensor) 
        no_course_teacher_conflicts = self.check_course_teacher_constraint(sparse_tensor)
        no_teacher_time_conflicts = self.check_teacher_time_constraint(sparse_tensor)

        if no_course_time_conflicts and no_course_teacher_conflicts and no_teacher_time_conflicts:
            return True

        return False

    def check_teacher_time_constraint(self, sparse_tensor: dict) -> bool:
        _, card_gamma, card_delta = self.shape 
        teacher_time_collisions = np.zeros((card_delta, card_gamma), dtype=self.dtype)
        
        for course, time, teacher in sparse_tensor:
            teacher_time_collisions[teacher, time] += 1
        
        if teacher_time_collisions.any(where=teacher_time_collisions > MAX_TIME_PER_TEACHER):
            return False

        return True

    def check_course_time_constraint(self, sparse_tensor: dict) -> bool:
        proj = self.proj_2d(("courses", "times"), sparse_tensor)
        num_times_per_course = np.count_nonzero(proj, axis=1)

        if num_times_per_course.any(where=num_times_per_course > MAX_TIMES_PER_COURSE):
            return False
         
        start = 0
        
        for pivot in self.pivots:
            stop = pivot
            required_courses = num_times_per_course[start : stop] 
            
            if required_courses.any(where=required_courses > MAX_REQUIRED_COURSES_PER_TIME):
                return False
            
            start = stop

        return True

    def check_course_teacher_constraint(self, sparse_tensor: dict) -> bool:
        proj = self.proj_2d(("teachers", "courses"), sparse_tensor)
        num_courses_per_teacher = np.count_nonzero(proj, axis=1)
        num_teachers_per_course = np.count_nonzero(proj, axis=0)

        if num_teachers_per_course.any(where=num_teachers_per_course > MAX_TEACHERS_PER_COURSE):
            return False

        if num_courses_per_teacher.any(where=num_courses_per_teacher > self.loads):
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

    def scatter(self, sparse_tensor: dict = None) -> None:
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

    def voxel(self, stop_psi_index: Union[int, None] = None) -> None:
        card_psi, card_gamma, card_delta = self.shape
        
        if stop_psi_index is None or stop_psi_index > card_psi:
            stop_psi_index = card_psi

        candidates = self.candidates.copy()
        assignments = list(self.sparse_tensor.copy())
        assignemnts = assignments.reverse()
        tensor = np.zeros(shape=self.shape, dtype=self.dtype)
        colors = np.zeros(shape=[card_psi, card_gamma, card_delta, 4], dtype=np.float32)
       
        for psi_n in range(stop_psi_index):
            tensor[psi_n, :, :] = 1
            candidate_gamma, candidate_delta = candidates.pop(psi_n)
            candidate_indices = itertools.product(candidate_gamma, candidate_delta)
            
            for gamma, delta in candidate_indices:
                tensor[psi_n, gamma, delta] = 2
            
            if candidate_delta:
                psi, gamma, delta = assignments.pop()
                tensor[psi, gamma, delta] = 3

            colors[tensor == 1] = [1, 0, 0, 0.9]
            colors[tensor == 2] = [0, 0, 1, 0.9]
            colors[tensor == 3] = [0, 1, 0, 0.9]
            ax = plt.figure().add_subplot(projection='3d')
            ax.voxels(tensor, facecolors=colors, edgecolor='k')
            plt.show()
