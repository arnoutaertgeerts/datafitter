__author__ = 'Arnout Aertgeerts'

import pandas
import numpy as np
import os


class Reader:
    def __init__(self, path, names):
        """
        A Reader which reads data from an excel file and builds a space that can be used to fit a curve.
        :param names: List of names in the order they appear in the excel file/dataframe
        :param path: The path to the excel file.
        """
        self.path = path
        self.names = names
        self.extension = os.path.splitext(path)[1]
        self.space = self.space()

        print self.dataframe

    @property
    def dataframe(self):
        """
        Create the pandas dataframe.
        :return: The pandas dataframe.
        """
        return pandas.io.excel.read_excel(self.path)

    def space(self):
        """
        Build the point space where each combination of input points is unique and points to one output value.
        :return: A (n+1 x mxpxq) matrix with n the number of different inputs and mxpxq the product of the input
        vector dimensions.
        """
        space_dict = {}

        space = self.get_input_space()
        space.append(self.output)
        for i in range(0, len(space)):
            space_dict[self.names[i]] = space[i]

        return space_dict

    def query(self, query):
        ordered_query = [0] * len(self.space)

        for key, value in query.iteritems():
            ordered_query[self.names.index(key)] = value

        return self.dataframe.loc[int(ordered_query[0])].loc[int(ordered_query[1]), int(ordered_query[2])]

    def get_input_space(self):
        inputs = self.inputs
        dimension = 1
        repetition = []
        input_space = []

        for i in range(0, len(inputs)):
            dimension *= len(inputs[i])
            length = 1

            for j in range(i + 1, len(inputs)):
                length *= len(inputs[j])

            repetition.append(length)
        repetition.insert(0, dimension)

        for i in range(0, len(inputs)):
            column = np.array([])
            subcolumn = np.array([])

            frequency = repetition[i]/repetition[i+1]
            length = repetition[i+1]

            for j in range(0, frequency):
                subcolumn = np.append(subcolumn, np.ones(length)*inputs[i][j])

            for k in range(0, repetition[0]/len(subcolumn)):
                column = np.append(column, subcolumn)

            input_space.append(column)

        return input_space

    @property
    def output(self):
        """
        Create the output vector
        :return: The output vector
        """
        input_space = self.get_input_space()

        length = len(input_space)
        output = np.array([])
        for i in range(0, len(input_space[0])):
            query = []
            for j in range(0, length):
                query.append(input_space[j][i])

            output = np.append(output, self.dataframe.loc[int(query[0])].loc[int(query[1]), int(query[2])])

        return output

    @property
    def inputs(self):
        """
        Create the input vectors of the space.
        :return: A matrix containing the input vectors with rows equal to the number of input points.
        """
        inputs = []

        for level in self.dataframe.index.levels:
            inputs.append(level)
        inputs.append(self.dataframe.columns.values)

        return inputs

    def inputs_dict(self):
        dictionary = {}
        for i in range(0, len(self.inputs)):
            dictionary[self.names[i]] = self.inputs[i]

        return dictionary