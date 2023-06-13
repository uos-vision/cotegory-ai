import pickle
from . import ModelEnum
from .ease import EASE
from .auto_encoder import AutoEncoder
import config as cf
import utils
import torch
from scipy import sparse
import os

class MyCoustomUnpickler(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str):
        if __module_name == '__main__':
            __module_name = __name__ # __module_name을 현재 실행되는 파일의 __name__으로 변경
        return super().find_class(__module_name, __global_name)

def get_model_dir_file(model_name):
    # 경로는 유동적으로 변경해서 사용
    # 모델 파일 이름은 모델 이름을 소문자로 변경한 뒤 뒤에 _model을 붙인 파일로 고정
    # ex) EASE => ease_model
    model_dir = os.path.join(cf.model_root_dir, model_name.lower())
    model_file_name = f'{model_name.lower()}_model'
    return model_dir, model_file_name

def get_model(model_name, model_src_file_name):
    # 모델 불러오기
    model_dir, model_file_name = get_model_dir_file(model_name)
    model_path = utils.call_pre_path(model_dir, model_file_name)

    if (model_path is None) or (not os.path.exists(model_path)):
        print(f"{model_name} - 기본 모델 경로로 설정")
        model_path = utils.call_pre_path(model_dir, model_file_name, model_src_file_name)

    print(f"{model_name} 모델 경로 : " + model_path)

    try:
        if model_name == ModelEnum.EASE:
            rec_model = EASE(300, cf.num_problem)
            rec_model.B = sparse.load_npz(model_path).toarray()
            rec_model.nz = rec_model.B.sum(0).nonzero()[0]
        elif model_name == ModelEnum.AUTO_ENCODER:
            # 모델 불러오기
            device = (
                "cuda" if torch.cuda.is_available()
                else "cpu"
            )
            print(f"{model_name} - device : {device}")
            rec_model = AutoEncoder(cf.num_problem, K=1024, device=device)
            rec_model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
            rec_model.eval()
    except Exception as e:
        print(e)
        print_load_err(model_name)
    return rec_model

def print_load_err(model_name):
    print(f"{model_name} : 가중치 로드 실패 - 초기 가중치로 설정")
