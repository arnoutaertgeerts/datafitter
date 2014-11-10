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

        print 'The global precision error is: ' + str(100*self.global_precision_error()) + '%.'

    def best_fit(self, start, stop):
        """
        Find the best fit varying the polynomial degree from start to stop. The function also stores the best fit
        parameters in the model.
        :param start: The start degree >=2
        :param stop: The stop degree which should be higher than the start degree
        """
        output = []

        for i in range(start, stop+1):
            self.fit(i)
            error = self.global_precision_error()
            output.append({
                'degree': i,
                'error': error
            })

        import operator
        best = sorted(output, key=operator.itemgetter('error'))

        self.fit(best[0]['degree'])
        return best

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

    def global_precision_error(self):
        """
        Calculate the quality of the function based on the global error.
        The error is equal to the weighted sum of the difference of each point divided by the true value (data value)
        """
        error = 0

        for i in range(0, self.reader.length):
            query = {}
            for name in self.reader.names:
                query[name] = self.reader.space[name][i]

            exact = self.reader.query(query)
            function = self.parameter_based_func(query)

            error += abs(exact - function) / exact

        error /= self.reader.length
        return error

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