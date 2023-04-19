import numpy as np
import pickle

class MyCoustomUnpickler(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str):
        if __module_name == '__main__':
            __module_name = __name__ # __module_name을 현재 실행되는 파일의 __name__으로 변경
        return super().find_class(__module_name, __global_name)

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


def get_model(model_path) -> EASE:
    # 모델 불러오기
    with open(model_path, 'rb') as file:
        ease = MyCoustomUnpickler(file)
        ease = ease.load()
    return ease