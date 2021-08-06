from config.data_generator import Distributions
from config.constants import SystemModelEnums, SystemModelRanges


class MUE:
    def __init__(self, x_, y_):
        self.x_ = x_
        self.y_ = y_

    def create_mue(self):
        return {"x": self.x_, "y": self.y_}


class ListOfMUEs(MUE):

    def __init__(self, x_, y_, number_of_mues):
        super().__init__(x_, y_)
        self.number_of_mues = number_of_mues

    def create_location_of_mues(self):
        return [Distributions.homogenous_poisson_point_process_distribution
                (SystemModelRanges.x_Min_FNs, SystemModelRanges.x_Max_FNs,
                 SystemModelRanges.y_Min_FNs, SystemModelRanges.y_Max_FNs,
                 SystemModelEnums.lambda_)
                for i in range(self.number_of_mues)]

    def create_list_of_mues(self):
        mues = []
        xx, yy = self.create_location_of_mues()
        for i in range(self.number_of_mues):
            mues.append(MUE.create_mue(MUE(xx[i], yy[i])))

        return mues
