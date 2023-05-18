import numpy as np
class EASE():
    """
    Embarrassingly Shallow Autoencoders model class
    """

    def __init__(self, lambda_, item_n):
        self.B = np.random.rand(item_n,item_n)
        self.lambda_ = lambda_

        self.item_n = item_n
        self.nz = None

    def forward(self, user_row):
        """
        forward pass
        """
        return user_row @ self.B

    def getUsersRating(self, user_row):
        res = user_row[:,self.nz] @ self.B[self.nz].T[self.nz]

        rating = np.zeros((user_row.shape[0],self.item_n))
        rating[:,self.nz] = res

        return rating