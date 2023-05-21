import math
import logging

from flask_login import current_user

time_values = {'Секунда': 31536000, 'Минута': 526000, 'Час': 8766, 'Неделя': 52, 'День': 365, 'Месяц': 12, 'Год': 1}




def r_integral(r_nad, r_narush):  # формула для R интегральное
    r_int = 1 - (1 - float(r_nad)) * (1 - float(r_narush))
    logging.info(str(current_user.name) + " - r_int : " + str(r_int))
    return r_int


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
        self.alfa = float(value['alfa'])
        logging.info(str(current_user.name) + " - alfa : " + str(self.alfa))
        self.beta = float(value['beta']) / time_values[value['beta_time']]
        logging.info(str(current_user.name) + " - beta : " + str(self.beta))
        self.t_between = float(value['t_between']) / time_values[value['t_between_time']]
        logging.info(str(current_user.name) + " - t_between : " + str(self.t_between))
        self.t_diag = float(value['t_diag']) / time_values[value['t_diag_time']]
        logging.info(str(current_user.name) + " - t_diag : " + str(self.t_diag))
        self.t_const = float(value['t_const']) / time_values[value['t_const_time']]
        logging.info(str(current_user.name) + " - t_const : " + str(self.t_const))

    def b_1(self):  # формула для N, всегда округляется вниз
        logging.info(str(current_user.name) + " - формула для N : " + str(int(self.t_const /
                                                                              (self.t_between + self.t_diag))))
        return int(self.t_const / (self.t_between + self.t_diag))

    def p_impact(self, t_const):  # формула P(1) воздействия
        if self.alfa == self.beta ** -1:
            p_impact = (math.exp(-self.alfa * t_const)) * (1 + self.alfa * t_const)
        else:
            p_impact = ((self.alfa - 1 / self.beta) ** -1) * (self.alfa * math.exp(-t_const / self.beta) -
                                                              (self.beta ** -1 * (math.exp(-1 * self.alfa * t_const)))
                                                              )
        logging.info(str(current_user.name) + " - p_impact : " + str(p_impact))
        return p_impact

    def t_ost(self):  # T остаточное
        n = self.b_1()
        t_ost = self.t_const - n * (self.t_between + self.t_diag)
        logging.info(str(current_user.name) + " - t_ost : " + str(t_ost))
        return t_ost

    def r_nadezh(self):
        if self.t_const >= (self.t_between + self.t_diag):
            p_middle = math.pow(self.p_impact(self.t_between+self.t_diag), self.b_1())
            logging.info(str(current_user.name) + " - p_middle : " + str(p_middle))
            p_end = self.p_impact(self.t_ost())
            logging.info(str(current_user.name) + " - p_end : " + str(p_end))
            r_nad = 1 - p_middle * p_end
            logging.info(str(current_user.name) + " - r_nad : " + str(r_nad))
            return r_nad
        else:
            r_nad = 1 - self.p_impact(self.t_const)
            logging.info(str(current_user.name) + " - r_nad : " + str(r_nad))
            return r_nad
