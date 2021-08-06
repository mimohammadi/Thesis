from random import normalvariate

from numpy.random import randint, uniform, poisson


class Distributions:
    @classmethod
    def uniform_distribution(cls, _low, _high, _size):
        return uniform(_low, _high, _size)

    @classmethod
    def random_distribution(cls, _low, _high):
        return randint(_low, _high)

    @classmethod
    def normal_distribution(cls, _mean, _sigma):
        return normalvariate(_mean, _sigma)

    @classmethod
    def homogenous_poisson_point_process_distribution(cls, _x_min, _x_max, _y_min,
                                                      _y_max, _lambda):
        x_delta = _x_max - _x_min
        y_delta = _y_max - _y_min  # rectangle dimensions
        area_total = x_delta * y_delta

        # Simulate a Poisson point process
        numb_points = poisson(_lambda * area_total)  # Poisson number of points
        xx = x_delta * uniform(0, 1, numb_points) + _x_min  # x coordinates of Poisson points
        yy = y_delta * uniform(0, 1, numb_points) + _y_min  # y coordinates of Poisson points
        return xx, yy

    @classmethod
    def zipf_distribution(cls, _n, _number_of_tasks, _betta):
        _sum = 0
        for m in range(_number_of_tasks):
            _sum += 1/(m ** _betta)

        return (1/(_n ** _betta))/_sum
