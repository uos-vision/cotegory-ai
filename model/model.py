import pickle
from . import ModelEnum
from .ease import EASE
from .auto_encoder import AutoEncoder
import config as cf
import torch
import pandas as pd

class MyCoustomUnpickler(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str):
        if __module_name == '__main__':
            __module_name = __name__ # __module_name을 현재 실행되는 파일의 __name__으로 변경
        return super().find_class(__module_name, __global_name)

def get_model_dir_file(model_name):
    model_dir = f'{cf.model_root_dir}/{model_name.lower()}'
    model_file_name = f'{model_name.lower()}_model'
    return model_dir, model_file_name

def get_model(model_name, model_src_file_name):
    # 모델 불러오기
    model_dir, model_file_name = get_model_dir_file(model_name)
    try:
        model_path = cf.call_pre_path(model_dir, model_file_name)
    except:
        print(f"{model_name} - 기본 모델로 설정")
        model_path = cf.call_pre_path(model_dir, model_file_name, model_src_file_name)

    print(f"{model_name} 모델 경로 : " + model_path)

    if model_name == ModelEnum.EASE:
        with open(model_path, 'rb') as file:
            model = MyCoustomUnpickler(file)
            model = model.load()
    elif model_name == ModelEnum.AUTO_ENCODER:
        # 모델 불러오기
        cfg = {
            "data_dir" : "./dataset/saved",
            "data_file" : "user_problem_mat.csv",
            "K" : 1024,
            "device" : "cuda"
        }
        train_data_path = f'{cfg["data_dir"]}/train_{cfg["data_file"]}'
        train_s_mat = pd.read_csv(train_data_path, index_col=0)
        model = AutoEncoder(train_s_mat, cfg)
        model.load_state_dict(torch.load(model_path))
        model.eval()

    return model