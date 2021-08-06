from config.constants import SystemModelEnums
from algorithmes.fitness.task_offloading_opt import GiniFunctions as gf
import numpy as np
import math


class GiniCoefficientBasedAlg:
    @classmethod
    def gini_mue_association_alg(cls, set_of_mues_in_each_fn, request_set_of_mues,
                                 set_of_mues, distances_of_fog, list_of_d__n_of_tasks):
        conflict = 1
        fn_sum_gamma = []
        gamma_fn = []
        # sorted_mues_of_fn = []
        for m in range(SystemModelEnums.M.value):
            sum_of_gamma = 0
            gamma_i_m_n = []
            # sorted_mues = []
            for i in range(len(set_of_mues_in_each_fn[m])):
                R_i = request_set_of_mues[set_of_mues_in_each_fn[m][i]]
                for n in range(R_i):
                    gamma_i_m_n.append([gf.income_function(R_i, R_i[n], distances_of_fog, set_of_mues_in_each_fn[m][i], m), i, set_of_mues_in_each_fn[m][i]])
                    # sorted_mues.append([gf.income_function(R_i, R_i[n], distances_of_fog, set_of_mues_in_each_fn[m][i], m), i, set_of_mues_in_each_fn[m][i]])

                gamma_i_m_n.sort()
                # sorted_mues.sort()
                # sorted_mues.reverse()

                sum_of_gamma += gamma_i_m_n[i][0]
            fn_sum_gamma[m] = sum_of_gamma
            gamma_fn.append(gamma_i_m_n)
            # sorted_mues_of_fn.append(sorted_mues)

        gini_m = []
        kappa_star_m = []
        # b_i
        for m in range(SystemModelEnums.M.value):
            # sum_of_gamma_j_m = []
            b_i = []
            # for i in np.array(gamma_fn[m]).T[1]:
            for i in range(len(gamma_fn[m])): # i is based on sort
                sum_of_gamma_j = 0
                for j in range(i):
                    sum_of_gamma_j += gamma_fn[m][j][0]

                b_i.append(sum_of_gamma_j/fn_sum_gamma[m])
            sum_b_i = 0
            for i in range(len(set_of_mues_in_each_fn[m]) - 1):
                sum_b_i += b_i[i]

            gini = 1 - ((1/len(set_of_mues_in_each_fn[m]))*(1 + 2 * sum_b_i))
            gini_m.append(gini)

            gamma_i = min(SystemModelEnums.f__0.value/np.argmax(list_of_d__n_of_tasks), len(set_of_mues_in_each_fn[m]),
                          SystemModelEnums.K__max.value)

            k_star_m = min((1/gini)+gamma_i*(len(set_of_mues_in_each_fn[m]) - math.ceil(1/gini)),
                           len(set_of_mues_in_each_fn[m]))

            kappa_star = []
            for i in range(len(set_of_mues_in_each_fn[m]), len(set_of_mues_in_each_fn[m]) + 1 - k_star_m, -1):
                kappa_star.append(gamma_fn[m][i][2])
            kappa_star_m.append(kappa_star)
        while conflict:
            for i in set_of_mues:
                count_mue_in_fogs = 0
                for m in range(len(kappa_star_m)):
                    if kappa_star_m[m].count(i) > 0:
                        count_mue_in_fogs += 1

                if count_mue_in_fogs > 1:
                    conflict = 1


