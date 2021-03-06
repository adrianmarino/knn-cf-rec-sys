import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class RatingsMatrix:
    def __init__(self, data):
        self.data = pd.DataFrame(data)

    @staticmethod
    def from_df(df, rows, columns, value):
        n_rows = len(np.unique(df[rows].values))
        n_columns = len(np.unique(df[columns].values))
        matrix = np.zeros((n_rows, n_columns))

        for _, row in df.iterrows():
            matrix[int(row[rows]-1), int(row[columns]-1)] = row[value]

        return RatingsMatrix(matrix)

    def T(self):
        return RatingsMatrix(self.data.T)

    def row(self, row_id):
        return self.data.iloc[row_id-1, :].values.reshape(1, -1)

    def mean_row(self, row_id):
        return self.row(row_id).mean()
    
    def cell(self, row_id, col_id):
        return self.data.iloc[row_id-1, col_id-1]

    def row_deviation(self, row_id, col_id):
        return self.cell(row_id, col_id) - self.mean_row(row_id)
    
    @property
    def n_rows(self): return self.data.shape[0]
    
    @property
    def n_columns(self): return self.data.shape[1]

    def __repr__(self):
        display(self.data)
        return ""

    @property
    def cells(self):
        for user_idx in range(self.n_rows):
            user_id = user_idx + 1
            for item_idx in range(self.n_columns):
                item_id = item_idx + 1
                value = self.cell(user_id, item_id)
                yield (value, user_id, item_id)

    def plot(self, figsize = (5, 5)):
        plt.figure(figsize = figsize)
        plt.imshow(self.data, cmap='hot')
        plt.colorbar()
        plt.show()

    @property
    def shape(self):
        return self.data.shape

    def to_batch(self, condition_fn=lambda value: True):
        batch = []
        for _, user_id, item_id in self.cells:
            value = self.cell(user_id, item_id)
            if condition_fn:
                batch.append((user_id, item_id, value))
        return batch