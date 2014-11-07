__author__ = 'Arnout Aertgeerts'

import pylab


class Plotter:
    def __init__(self, reader):
        """
        This class makes plots based on the the space.
        :param reader: A reader object containing the space information.
        """
        self.reader = reader
        self.inputs = self.reader.inputs_dict()

    def plot(self, variable, constants):
        """
        Plot a single line which shows the output in function of the variable while keeping the other values constant
        :param variable: A string containing the variable name
        :param constants: A dictionary specifying the constant values
        """
        xaxis, yaxis = self.array_for_plot(variable, constants)

        pylab.plot(xaxis, yaxis)

    def field_plot(self, variable, field, constant):
        """
        Plot multiple lines which shows the output in function of the variable while varying the field parameter and
        keeping one constant
        :param variable: The variable to plot
        :param field: The varying variable
        :param constant: The constant variable
        """
        ranger = self.inputs[field]

        for r in ranger:
            constant[field] = r
            self.plot(variable, constant)

    def array_for_plot(self, variable, constants):
        """
        Create data for a simple 2D plot of the output in function of the variable while keeping some values constant
        :param variable: A string containing the variable name
        :param constants: A dictionary containing the names and values of the variables we want to keep constant
        :return: A tuple containing x and y axis data for a 2D plot
        """
        xaxis = []
        yaxis = []

        for i in self.inputs[variable]:
            xaxis.append(i)
            query = constants
            query[variable] = i

            yaxis.append(self.reader.query(query))

        return xaxis, yaxis
