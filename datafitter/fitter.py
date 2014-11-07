__author__ = 'Arnout Aertgeerts'

from multipolyfit import multipolyfit
import numpy as np


class Fitter:
    def __init__(self, reader):
        """
        A class which fits a multi-variable polynomial to measurement data
        :param reader: An object of the reader class containing the data
        """
        self.reader = reader
        self.function = None
        self.powers = None
        self.beta = None

    def fit(self, degree):
        """
        Fit a multi-variable polynomial to the given reader data with a specified degree
        :param degree: The maximum degree of the polynomial function
        """
        x = []
        y = self.reader.space[self.reader.names[-1]]

        for i in range(0, len(self.reader.names)-1):
            x.append(self.reader.space[self.reader.names[i]])

        self.function = multipolyfit(np.array(x).T, y, degree, model_out=True)
        (beta, powers) = multipolyfit(np.array(x).T, y, degree, powers_out=True)
        self.beta = beta
        self.powers = powers

    def print_function(self):
        """
        Print a pretty representation of the fitted function
        """
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


