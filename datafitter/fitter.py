__author__ = 'Arnout Aertgeerts'

from multipolyfit import multipolyfit
import numpy as np
import math


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

    def parameter_based_func(self, inputs):
        """
        A function which calculates the output based on the beta and powers parameters.
        :param inputs: The input dictionary
        """
        y = 0
        x = self.reader.inputsdict_to_array(inputs)
        x.insert(0, 1)

        for i in range(0, len(self.beta)):
            term = self.beta[i]
            for j in range(0, len(self.powers[i])):
                term *= math.pow(x[j], self.powers[i][j])
            y = y + term

        return y

    def modelica_output(self):
        """
        Print an output for beta and powers that can easily be copied for use in the Modelica model
        """
        string = []
        beta_string = []
        powers_string = []

        beta_string.append('{')
        for i in self.beta[0:-1]:
            beta_string.append(str(i))
            beta_string.append(',')
        beta_string.append(str(self.beta[-1]))
        beta_string.append('}')

        powers_string.append('{')
        for i in self.powers:
            powers_string.append('{')
            for j in i[0:-1]:
                powers_string.append(str(j))
                powers_string.append(',')
            powers_string.append(str(i[-1]))
            powers_string.append('}')
            powers_string.append(',')
        del powers_string[-1]
        powers_string.append('}')

        string.append('BETA:-------------------------------------')
        string.append('\n')
        string.append(''.join(beta_string))
        string.append('\n')
        string.append('POWERS:-----------------------------------')
        string.append('\n')
        string.append(''.join(powers_string))

        return ''.join(string)


    def print_function(self):
        """
        WIP: Print a pretty representation of the fitted function
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


