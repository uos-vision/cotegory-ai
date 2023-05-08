import numpy as np
from .base_model import BaseModel
class EASE(BaseModel):
    """
    Embarrassingly Shallow Autoencoders model class
    """

    def __init__(self, lambda_, item_n):
        self.B = np.random.rand(item_n,item_n)
        self.lambda_ = lambda_

    def forward(self, user_row):
        """
        forward pass
        """
        return user_row @ self.B

    def getUsersRating(self, user_row):
        return self.forward(user_row)