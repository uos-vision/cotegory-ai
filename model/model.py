import pickle
from . import ModelEnum
from .ease import EASE
import config as cf

class MyCoustomUnpickler(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str):
        if __module_name == '__main__':
            __module_name = __name__ # __module_name을 현재 실행되는 파일의 __name__으로 변경
        return super().find_class(__module_name, __global_name)

def get_model(model_path, model):
    # 모델 불러오기
    if model == ModelEnum.EASE:
        if model_path is None:
            model_src_file_name = 'ease_model_1682656807.p'
            model_path = cf.call_pre_path(ease_model_dir, ease_model_file_name, model_src_file_name)

        with open(model_path, 'rb') as file:
            model = MyCoustomUnpickler(file)
            model = model.load()
    return model