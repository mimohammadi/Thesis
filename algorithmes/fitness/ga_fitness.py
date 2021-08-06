# average utility of task caching bring by d2d sharing
from config.data_generator import Distributions
from config.constants import SystemModelEnums, SystemModelRanges
import math
from scipy import integrate as integrate


class GAFitness:
    @classmethod
    def ga_fitness(cls, popularity_of_tasks, caching_probability, task_library, distance_of_mues):
        return - sum(cls.avg_utility_of_local_task_caching(popularity_of_tasks, caching_probability, task_library) +
                     cls.avg_utility_of_d2d_task_caching(popularity_of_tasks, caching_probability, task_library, distance_of_mues))

    @classmethod
    def popularity_of_tasks(cls, number_of_tasks, betta):
        return [Distributions.zipf_distribution(n, number_of_tasks, betta) for n in number_of_tasks]

    @classmethod
    def avg_utility_of_local_task_caching(cls, popularity_of_tasks, caching_probability, task_library):
        # p = cls.popularity_of_tasks(SystemModelEnums.N.value, SystemModelEnums.betta.value)
        # q =
        sum_ = 0
        for i in range(SystemModelEnums.K.value):
            for n in range(SystemModelEnums.N.value):
                t_l_i_n = task_library[n].D__n / SystemModelEnums.w.value
                e_l_i_n = SystemModelEnums.kappa.value * task_library[n].D__n * SystemModelEnums.w.value ** 2
                sum_ += popularity_of_tasks[n] * caching_probability[n] * ((SystemModelEnums.rho_t.value * t_l_i_n)
                                                                           + (SystemModelEnums.rho_e.value * e_l_i_n))
        return sum_ / SystemModelEnums.K.value

    @classmethod
    def avg_utility_of_d2d_task_caching(cls, popularity_of_tasks, caching_probability, task_library, distance_of_mues):
        sum_ = 0
        r = (SystemModelEnums.p__u.value / SystemModelEnums.D2D_establish_threshold.value)** (1/SystemModelEnums.a.value)
        for i in range(SystemModelEnums.K.value):
            for n in range(SystemModelEnums.N.value):
                t_l_i_n = task_library[n].D__n / SystemModelEnums.w.value
                e_l_i_n = SystemModelEnums.kappa.value * task_library[n].D__n * SystemModelEnums.w.value ** 2
                t_D_i_n = (SystemModelEnums.theta.value * task_library[n].S__n) / cls.avg_transmit_rate(r, distance_of_mues, i, j)
                e_D_i_n = SystemModelEnums.p__u.value * t_D_i_n
                sum_ += popularity_of_tasks[n] * (1 - caching_probability[n]) * ((SystemModelEnums.rho_t.value * (t_l_i_n - t_D_i_n))
                                                                                 + (SystemModelEnums.rho_e.value * (e_l_i_n - e_D_i_n)))
        return sum_ / SystemModelEnums.K.value

    @classmethod
    def transmit_rate(cls, distance_of_mues, i, j):  ### not complete
        sum_ = 0
        for z in range(SystemModelEnums.K.value):   # len distribution mues transmitting n
            if z != i:
                for k in range(SystemModelEnums.K.value):
                    sum_ += distance_of_mues[i][j] ** SystemModelEnums.a.value

        return SystemModelEnums.B.value * math.log(1 +
                ((SystemModelEnums.p__u.value * distance_of_mues[i][j] ** (- SystemModelEnums.a.value) * SystemModelEnums.g_d2d_i_j.value)
                / (SystemModelEnums.sigma_2.value + sum_)), 2)

    @classmethod
    def association_distance(cls, x_n, q_n):
        return 2 * math.pi * x_n * SystemModelEnums.lambda_.value * q_n * math.exp(- SystemModelEnums.lambda_.value * q_n * math.pi * x_n ** 2)

    @classmethod
    def f(cls, q_n, distance_of_mues, i, j):
        return cls.transmit_rate(distance_of_mues, i, j)*cls.association_distance(q_n, distance_of_mues[i][j])

    @classmethod
    def avg_transmit_rate(cls, r, distance_of_mues, i, j):
        res = integrate.quad(cls.f, 0, r, args=(distance_of_mues, i, j))
        return res
