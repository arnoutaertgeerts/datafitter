__author__ = 'Arnout Aertgeerts'

from scipy.optimize import curve_fit
from multipolyfit import multipolyfit
import numpy as np


class Fitter:
    def __init__(self, reader):
        self.reader = reader
        self.function = None
        self.powers = None
        self.beta = None

    def fit(self, degree):
        x = []
        y = self.reader.space[self.reader.names[-1]]

        for i in range(0, len(self.reader.names)-1):
            x.append(self.reader.space[self.reader.names[i]])

        self.function = multipolyfit(np.array(x).T, y, degree, model_out=True)
        (beta, powers) = multipolyfit(np.array(x).T, y, degree, powers_out=True)
        self.beta = beta
        self.powers = powers

    def print_function(self):
        string = []
        for b in range(0, len(self.beta)):
            string.append(str(self.beta[b]))
            string.append('*(')
            for p in range(0, len(self.powers[b])):
                if p == 1:
                    string.append('1 + ')
                else:
                    if self.powers[b][p] != 0:
                        string.append(self.reader.names[p])
                    else:
                        string.append('1 + ')
                    if self.powers[b][p] != 1:
                        string.append('^')
                        string.append(str(self.powers[b][p]))
                        string.append(' + ')
            string.append(')')
        print ''.join(string)


