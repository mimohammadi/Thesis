from config.constants import SystemModelEnums
import math


class GiniFunctions:
    @classmethod
    def income_function(cls, task_library, n, distances_of_fog, i, m):
        t_l_i_n = task_library[n].D__n / SystemModelEnums.w.value
        e_l_i_n = SystemModelEnums.kappa.value * task_library[n].D__n * SystemModelEnums.w.value ** 2
        t_u_i_m_n = task_library[n].S__n / cls.transmit_rate(distances_of_fog, i, m)
        e_u_i_m_n = SystemModelEnums.p__u.value * t_u_i_m_n
        t_d_m_i_n = task_library[n].S__n * task_library[n].Theta__n / cls.downlink_rate(distances_of_fog, i, m)
        e_d_m_i_n = SystemModelEnums.p__m.value * t_d_m_i_n
        t_T_i_m_n = t_u_i_m_n + t_d_m_i_n
        e_T_i_m_n = e_u_i_m_n + e_d_m_i_n
        t__i_m_n_f_0 = task_library[n].D__n / SystemModelEnums.f__0.value  #** f_i_m
        e__cpt_i_m_n_f_0 = SystemModelEnums.kappa_server * task_library[n].D__n * (SystemModelEnums.f__0.value ** 2)

        return ((SystemModelEnums.rho_t.value * t_l_i_n)/(t_T_i_m_n + t__i_m_n_f_0)) + ((SystemModelEnums.rho_e.value * e_l_i_n)/(e_T_i_m_n + e__cpt_i_m_n_f_0))

    @classmethod
    def transmit_rate(cls, distances_of_fog, i, m):
        # m = fog
        # i = MUE
        sum_ = 0
        for o in range(SystemModelEnums.M.value):
            if o != m:
                for j in range(SystemModelEnums.K.value):
                    if j != i:
                        sum_ += SystemModelEnums.p__u.value*(distances_of_fog[j][m]**-SystemModelEnums.a.value)* SystemModelEnums.g_u_i_m.value

        return SystemModelEnums.B.value * math.log(1 + ((SystemModelEnums.p__u*(distances_of_fog[i][m]** -SystemModelEnums.a.value) * SystemModelEnums.g_u_i_m.value)
                                                        /(SystemModelEnums.sigma_2.value + sum_)),2)

    @classmethod
    def downlink_rate(cls, distances_of_fog, i, m):
        # m = fog
        # i = MUE
        sum_ = 0
        for o in range(SystemModelEnums.M.value):
            if o != m:
                for j in range(SystemModelEnums.K.value):
                    if j != i:
                        sum_ += SystemModelEnums.p__m.value * (distances_of_fog[j][m] ** -SystemModelEnums.a.value) * SystemModelEnums.g_d_i_m.value

        return SystemModelEnums.B.value * math.log(1 + ((SystemModelEnums.p__m * (
                    distances_of_fog[i][m] ** -SystemModelEnums.a.value) * SystemModelEnums.g_d_i_m.value)
                                                        / (SystemModelEnums.sigma_2.value + sum_)), 2)
