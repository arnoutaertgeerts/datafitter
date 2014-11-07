__author__ = 'Arnout Aertgeerts'

import pylab


class Plotter:
    def __init__(self, reader):
        self.reader = reader
        self.inputs = self.reader.inputs_dict()

    def plot(self, variable, constants):
        xaxis, yaxis = self.array_for_plot(variable, constants)

        pylab.plot(xaxis, yaxis)

    def field_plot(self, variable, field, constant):
        ranger = self.inputs[field]

        for r in ranger:
            constant[field] = r
            self.plot(variable, constant)

    def array_for_plot(self, variable, constants):

        xaxis = []
        yaxis = []

        for i in self.inputs[variable]:
            xaxis.append(i)
            query = constants
            query[variable] = i

            yaxis.append(self.reader.query(query))

        return xaxis, yaxis
