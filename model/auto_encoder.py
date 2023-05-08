from .base_model import BaseModel
from torch import nn
import torch
import numpy as np

class AutoEncoder(BaseModel):

    def __init__(self, item_n, K, device):
        """
        Arguments
        - item_n : number of item dimensions
        - K (int): number of latent dimensions
        - device : using device
        """
        super(AutoEncoder, self).__init__()
        # convert ndArray
        self.item_n = item_n
        self.K = K
        self.device = device

        # Initialize user and item latent feature matrice
        self.I_1 = nn.Linear(self.item_n, self.K, bias=True, device=self.device)
        self.I_2 = nn.Linear(self.K, self.item_n, bias=True, device=self.device)

        nn.init.normal_(self.I_1.weight, std=1. / self.K)
        nn.init.normal_(self.I_2.weight, std=1. / self.K)

    def forward(self, x):
        user_emb = self.I_1(x)
        rating = self.I_2(user_emb)

        return rating

    def getUsersRating(self, user_row: np.array):
        return self.forward(torch.Tensor(user_row).to(self.device)).cpu().detach().numpy()