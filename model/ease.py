import numpy as np
class EASE:
    """
    Embarrassingly Shallow Autoencoders model class
    """

    def __init__(self, lambda_):
        self.B = None
        self.lambda_ = lambda_

    def train(self, interaction_matrix):
        """
        train pass
        :param interaction_matrix: interaction_matrix
        """
        G = interaction_matrix.T @ interaction_matrix
        diag = list(range(G.shape[0]))
        G[diag, diag] += self.lambda_
        P = np.linalg.inv(G)

        # B = P * (X^T * X − diagMat(γ))
        self.B = P / -np.diag(P)
        min_dim = min(*self.B.shape)
        self.B[range(min_dim), range(min_dim)] = 0

    def forward(self, user_row):
        """
        forward pass
        """
        return user_row @ self.B

    def getUsersRating(self, user_row):
        return self.forward(user_row)