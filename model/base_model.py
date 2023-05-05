import torch
class BaseModel(torch.nn.Module):
    def __init__(self):
        super(BaseModel, self).__init__()

    def getUsersRating(self, user_row):
        raise NotImplementedError