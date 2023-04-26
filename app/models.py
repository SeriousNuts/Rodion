from typing import Iterable
import math

time_values = {'секунда': 31536000, 'минута': 526000, 'час': 8766, 'неделя': 52, 'день': 365, 'месяц': 12, 'год': 1}


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

        self.alfa = float(value['alfa']) / time_values[value['alfa_time']]
        self.beta = float(value['beta']) / time_values[value['beta_time']]
        self.t_between = float(value['t_between']) / time_values[value['t_between_time']]
        self.t_diag = float(value['t_diag']) / time_values[value['t_diag_time']]
        self.t_const = float(value['t_const']) / time_values[value['t_const_time']]
        if value['ib_checked'] == 1:
            self.number_IB = True

    def construct_from_json(self):
        pass

    def b_1(self):  # формула для N, всегда округляется вниз
        return int(1 / (self.t_between + self.t_diag))

    def p_impact(self):  # формула P(1) воздействия
        if self.alfa == self.beta:
            return (math.exp(-self.alfa * self.t_const)) * (1 - self.alfa * self.t_const)
        else:
            return ((self.alfa - 1 / self.beta) ** -1) * (self.alfa * math.exp(self.t_const / self.beta) -
                                                          (self.beta ** -1 * (math.exp(-1 * self.alfa * self.t_const)))
                                                          )

    def t_ost(self):  # T остаточное
        n = self.b_1()
        return self.t_const - n * (self.t_between + self.t_diag)

    def p_middle(self):  # формула P среднее
        n = self.b_1()
        beta_inv = 1 / self.beta
        exp_term = self.alfa * math.exp(-(self.t_between + self.t_diag) / self.beta) - \
                   beta_inv * math.exp(-self.alfa * (self.t_between + self.t_diag))
        numerator = 1 / (self.alfa - beta_inv)
        denominator = numerator * exp_term
        result = denominator ** n
        return result

    def p_end(self):  # P конечное
        t_ost = self.t_ost()
        return (self.alfa - math.pow(self.beta, -1)) ** -1 * (
                self.alfa * math.exp(-t_ost / self.beta) - math.pow(self.beta, -1) * math.exp(-self.alfa * t_ost))

    def p_impact2(self):  # P(2) воздействия
        return self.p_middle() * self.p_end()

    def r_nadezh(self):
        return 1 - self.p_impact2()

    def t_diag_iter(self):  # формула для более точного t_diag
        t_diag_iter = self.t_diag
        r_nad = self.r_nadezh()
        for i in range(4):
            t_diag_iter = t_diag_iter ** i * (1 - r_nad ** i) + r_nad ** i * self.t_recharge
        return t_diag_iter

    def r_integral(self):  # формула для R интегральное
        return 1 - (1 - self.r_nadezh()) * (1 - self.r_nadezh())
