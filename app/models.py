from typing import Iterable
import math

time_values = {'Секунда': 31536000, 'Минута': 526000, 'Час': 8766, 'Неделя': 52, 'День': 365, 'Месяц': 12, 'Год': 1}


class ModelTreat:
    alfa = 0.0
    alfa_time = ''
    beta = 0.0
    beta_time = ''
    t_between = 0.0
    t_between_time = ''
    t_diag = 0.0
    t_diag_time = ''
    t_recharge = 0.0
    t_recharge_time = ''
    t_const = 0.0
    t_const_time = ''
    number_IB = False
    operand = ''

    def consruct_from_dir(self, value):
        self.alfa = float(int(value['alfa']))
        # self.alfa = float(value['alfa']) / time_values[value['alfa_time']]
        self.beta = float(int(value['beta'])) / time_values[value['beta_time']]
        self.t_between = float(int(value['t_between'])) / time_values[value['t_between_time']]
        self.t_diag = float(int(value['t_diag'])) / time_values[value['t_diag_time']]
        self.t_const = float(int(value['t_const'])) / time_values[value['t_const_time']]

    def construct_from_json(self):
        pass

    def b_1(self):  # формула для N, всегда округляется вниз
        return int(self.t_const / (self.t_between + self.t_diag))

    def p_impact(self, t_const):  # формула P(1) воздействия
        if self.alfa == self.beta ** -1:
            return (math.exp(-self.alfa * t_const)) * (1 + self.alfa * t_const)
        else:
            return ((self.alfa - 1 / self.beta) ** -1) * (self.alfa * math.exp(-t_const / self.beta) -
                                                          (self.beta ** -1 * (math.exp(-1 * self.alfa * t_const)))
                                                          )

    def t_ost(self):  # T остаточное
        n = self.b_1()
        return self.t_const - n * (self.t_between + self.t_diag)

    def r_nadezh(self):
        if self.t_const >= (self.t_between + self.t_diag):
            p_middle = math.pow(self.p_impact(self.t_between+self.t_diag), self.b_1())
            p_end = self.p_impact(self.t_ost())
            return 1 - p_middle * p_end
        else:
            return 1 - self.p_impact(self.t_const)

    def r_integral(self):  # формула для R интегральное
        return 1 - (1 - self.r_nadezh()) * (1 - self.r_nadezh())
