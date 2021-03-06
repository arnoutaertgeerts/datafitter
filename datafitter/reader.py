__author__ = 'Arnout Aertgeerts'

import pandas
import numpy as np
import os


class Reader:
    def __init__(self, path, names):
        """
        A Reader which reads data from an excel file and builds a space that can be used to fit a curve.
        :param names: List of names in the order they appear in the excel file/dataframe, including the name of the
        output variable as last element in the list. Names are structured in the following way in the excel file:

        ****************** 3 *****
        *     *  2  *            *
        *  1  *******  Output(4) *
        *     *  2  *            *
        **************************

        :param path: Path to the excel file.
        """
        self.path = path
        self.names = names
        self.extension = os.path.splitext(path)[1]
        self.space = self.construct_space()

        print self.dataframe
        print '---------------------------------------------------------------------------'
        print pandas.DataFrame.from_dict(self.space)

    @property
    def dataframe(self):
        """
        Create the pandas dataframe.
        :return: The pandas dataframe.
        """
        return pandas.io.excel.read_excel(self.path)

    @property
    def length(self):
        return len(self.space[self.names[0]])

    def construct_space(self):
        """
        Build the point space where each combination of input points is unique and points to one output value.
        :return: A (n+1 x m*p*q) matrix with n the number of different inputs and mxpxq the product of the input
        vector dimensions.
        """
        space_dict = {}

        space = self.get_input_space()
        space.append(self.output)
        for i in range(0, len(space)):
            space_dict[self.names[i]] = space[i]

        return space_dict

    def exclude(self, value, original=True):
        """
        Exclude a value from the current or original space
        :param original: Use the original space if true, otherwise use the current space
        :param value: The value to exclude
        """
        if original:
            self.space = self.construct_space()

        remove_indexes = []
        for i in range(0, len(self.space[self.names[-1]])-1):
            if self.space[self.names[-1]][i] == value:
                remove_indexes.append(i)

        #Remove this data point
        for name in self.names:
            self.space[name] = np.delete(self.space[name], np.s_[remove_indexes])

        if len(remove_indexes) == 1:
            print str(len(remove_indexes)) + ' data point was removed from the result space'
        elif len(remove_indexes) == 0:
            print str(value) + ' was not found in the result space. No points were removed'
        else:
            print str(len(remove_indexes)) + ' data points where removed from the result space'

    def query(self, query):
        """
        Find a result value in the space matrix
        :param query: A query dictionary containing values of all the input parameters
        :return: A result value
        """
        ordered_query = self.inputsdict_to_array(query)

        if len(ordered_query) > 3:
            return self.dataframe.loc[int(ordered_query[0])].loc[int(ordered_query[1]), int(ordered_query[2])]
        else:
            return self.dataframe.loc[float(ordered_query[0]), float(ordered_query[1])]

    def get_input_space(self):
        """
        Create the input space which is the left side of the space matrix containing unique combinations of input points
        :return: The input space
        """
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
        Create the output vector which gives the results for each combination of unique input combinations
        :return: The output vector
        """
        input_space = self.get_input_space()

        length = len(input_space)
        output = np.array([])

        #Loop over all input combinations
        for i in range(0, len(input_space[0])):
            #Construct a query using these input combinations
            query = []
            for j in range(0, length):
                query.append(input_space[j][i])

            if length > 2:
                #TODO: Allow for query of non-integer parameters
                output = np.append(output, self.dataframe.loc[int(query[0])].loc[int(query[1]), int(query[2])])
            else:
                output = np.append(output, self.dataframe.loc[query[0], query[1]])

        return output

    @property
    def inputs(self):
        """
        Create the input vectors of the space.
        :return: A matrix containing the input vectors with rows equal to the number of input points.
        """
        inputs = []

        try:
            for level in self.dataframe.index.levels:
                inputs.append(level)
        except AttributeError:
            inputs.append(self.dataframe.index)
        inputs.append(self.dataframe.columns.values)

        return inputs

    def inputs_dict(self):
        """
        The input vector as a dictionary that can be called using the names of the variables
        :return: A dictionary
        """
        dictionary = {}
        for i in range(0, len(self.inputs)):
            dictionary[self.names[i]] = self.inputs[i]

        return dictionary

    def inputsdict_to_array(self, dictionary):
        """
        Convert an inputs dictionary to an array in the right order which is the order the names are stored in the
        names array.
        :param dictionary: A dictionary containing data about inputs
        """
        array = [0] * len(self.space)

        for key, value in dictionary.iteritems():
            array[self.names.index(key)] = value

        return array