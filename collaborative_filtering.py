import numpy as np
import pandas as pd
from pandas.core.algorithms import isin
from pandas.core.frame import DataFrame

class CollaborativeFiltering(object):

    def __init__(self, k):
        """Class constructor for KMeans
        Arguments:
            k {int} -- number of similar items to consider
        """
        self.k = k
    
    def get_row_mean(self, data):
        """Returns the mean of each row in the DataFrame or the mean of the
        Series. If the parameter data is a DataFrame, the function will
        return a Series containing the mean of each row in the DataFrame. If
        the parameter data is a Series, the function will return a np.float64
        which is the mean of the Series. This function should not consider
        blank ratings represented as NaN.

        Arguments:
            data {DataFrame or Series} -- dataset
        Returns:
            Series or np.float64 -- row mean
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Check if the parameter data is a Series or a DataFrame

        # TODO: return the mean of each row if the parameter data is a
        # DataFrame. Return the mean of the Series if the parameter data is a
        # Series.
        # Hint: Use pandas.DataFrame.mean() or pandas.Series.mean() functions.
        
        if isinstance(data, pd.DataFrame):
            row_mean = data.mean(1)
        else:
            row_mean = data.mean()

        # print(row_mean)

        return row_mean

    def normalize_data(self, data, row_mean):
        """Returns the data normalized by subtracting the row mean.

        For the arguments point1 and point2, you can only pass these
        combinations of data types:
        - DataFrame and Series -- returns DataFrame
        - Series and np.float64 -- returns Series

        For a DataFrame and a Series, if the shape of the DataFrame is
        (3, 2), the shape of the Series should be (3,) to enable broadcasting.
        This operation will result to a DataFrame of shape (3, 2)

        Arguments:
            data {DataFrame or Series} -- dataset
            row_mean {Series or np.float64} -- mean of each row
        Returns:
            DataFrame or Series -- normalized data
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Check if the combination of parameters is correct
        # Normalize the parameter data by parameter row_mean.
        # HINT: Use pandas.DataFrame.subtract() or pandas.Series.subtract()
        # functions.

        # print(row_mean)
        # print(data)

        if (isinstance(data, pd.DataFrame) and isinstance(row_mean, pd.Series)) or (isinstance(data, pd.Series) and isinstance(row_mean, np.float64)):
            data = data.subtract(row_mean, axis = 0)
        else:
            print('Invalid Combination')

        return data

    def get_cosine_similarity(self, vector1, vector2):
        """Returns the cosine similarity between two vectors. These vectors can
        be represented as 2 Series objects. This function can also compute the
        cosine similarity between a list of vectors (represented as a
        DataFrame) and a single vector (represented as a Series), using
        broadcasting.

        For the arguments vector1 and vector2, you can only pass these
        combinations of data types:
        - Series and Series -- returns np.float64
        - DataFrame and Series -- returns pd.Series

        For a DataFrame and a Series, if the shape of the DataFrame is
        (3, 2), the shape of the Series should be (2,) to enable broadcasting.
        This operation will result to a Series of shape (3,)

        Arguments:
            vector1 {Series or DataFrame} - vector
            vector2 {Series or DataFrame} - vector
        Returns:
            np.float64 or pd.Series -- contains the cosine similarity between
            two vectors
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Check if the parameter data is a Series or a DataFrame

        # TODO: Compute the cosine similarity between the two parameters.
        # HINT: Use np.sqrt() and pandas.DataFrame.sum() and/or
        # pandas.Series.sum() functions.

        # print(vector1)
        # print(vector2)

        if isinstance(vector1, pd.Series) and isinstance(vector2, pd.Series):
            upper = (vector1 * vector2).sum()
            lower = np.sqrt((vector1**2).sum()) * np.sqrt((vector2**2).sum())
            cosine_similarity =  upper / lower
        elif isinstance(vector1, pd.Series) and isinstance(vector2, pd.DataFrame):

            cosine_similarity = pd.Series()
            idx = []

            for index, row in vector2.iterrows():
                upper = (vector1 * row).sum()
                lower = np.sqrt((vector1**2).sum()) * np.sqrt((row**2).sum())

                # print(upper)
                # print(lower)

                temp = pd.Series([np.divide(upper, lower)])
                
                idx.append(index)

                cosine_similarity = cosine_similarity.append(temp)

            cosine_similarity.index = idx

        elif isinstance(vector1, pd.DataFrame) and isinstance(vector2, pd.Series):
            cosine_similarity = pd.Series()
            idx = []

            for index, row in vector1.iterrows():
                upper = (vector2 * row).sum()
                lower = np.sqrt((vector2**2).sum()) * np.sqrt((row**2).sum())

                # print(upper)
                # print(lower)

                temp = pd.Series([np.divide(upper, lower)])
                
                idx.append(index)

                cosine_similarity = cosine_similarity.append(temp)

            cosine_similarity.index = idx
        else:
            print('Invalid Combination')
            cosine_similarity = 0

        return cosine_similarity

    def get_k_similar(self, data, vector):
        """Returns two values - the indices of the top k similar items to the
        vector from the dataset, and a Series representing their similarity
        values to the vector. We find the top k items from the data which
        are highly similar to the vector.

        Arguments:
            data {DataFrame} -- dataset
            vector {Series} -- vector
        Returns:
            Index -- indices of the top k similar items to the vector
            Series -- computed similarity of the top k similar items to the
            vector
        """

        # TODO: Implement this function based on the documentation.

        # TODO: Normalize parameters data and vector
        # HINT: Use the normalize_data() function that we have defined in this
        # class

        # TODO: Get the cosine similarity between the normalized data and
        # vector
        # HINT: Use the get_cosine_similarity() function that we have defined
        # in this class

        # TODO: Get the INDICES of the top k most similar items based on
        # the cosine similarity values
        # HINT: Use pandas.Series.nlargest() function.

        # TODO: Return 2 values. See function comment

        # print(data)
        # print(vector)

        data_mean = self.get_row_mean(data)
        vector_mean = self.get_row_mean(vector)

        # print(data_mean)
        # print(vector_mean)

        data = self.normalize_data(data, data_mean)
        vector = self.normalize_data(vector, vector_mean)

        cosine_similarity = self.get_cosine_similarity(data, vector)

        # print(cosine_similarity)

        # print(cosine_similarity.nlargest(self.k))

        top = cosine_similarity.nlargest(self.k)

        return top

    def get_rating(self, data, index, column):
        """Returns the extrapolated rating for the item in row index from the
        user in column column based on similar items.

        The algorithm for this function is as follows:
        1. Get k similar items.
        2. Compute for the rating using the similarity values and the raw
        ratings for the k similar items.

        Arguments:
            data {DataFrame} -- dataset
            index {int} -- row of the item
            column {int} -- column of the user
        Returns:
            np.float64 -- extrapolated rating based on similar ratings
        """

        # TODO: Complete this function.

        before_df = data.iloc[:index, :]
        after_df = data.iloc[index + 1:, :]
        new_data = pd.concat([before_df, after_df])
        vector = data.iloc[index, :]

        # print(data)
        # print(index, column)

        # print(before_df)
        # print(after_df)
        # print(new_data)
        # print(vector)
        
        # TODO: Get top k items that are similar to the parameter vector
        # HINT: Use the get_k_similar() function that we have defined in this
        # class

        k_similar = self.get_k_similar(new_data, vector)

        # print(k_similar)

        # TODO: Compute for the rating using the similarity values and the raw
        # ratings for the k similar items.

        # print(k_similar.index)

        # print(new_data)

        upper = new_data.loc[k_similar.index].mul(k_similar, axis=0)
        upper = upper.iloc[:, column].sum()

        lower = k_similar.sum()

        # print(upper)
        # print(lower)

        rating = upper / lower

        return rating
