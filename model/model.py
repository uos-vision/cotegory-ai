import pickle
from . import ModelEnum
from .ease import EASE
import config as cf

class MyCoustomUnpickler(pickle.Unpickler):
    def find_class(self, __module_name: str, __global_name: str):
        if __module_name == '__main__':
            __module_name = __name__ # __module_name을 현재 실행되는 파일의 __name__으로 변경
        return super().find_class(__module_name, __global_name)

def get_model_dir_file(model_name):
    model_dir = f'{cf.model_root_dir}/{model_name.lower()}'
    model_file_name = f'{model_name.lower()}_model'
    return model_dir, model_file_name

def get_model(model_name):
    # 모델 불러오기
    model_dir, model_file_name = get_model_dir_file(model_name)
    model_path = cf.call_pre_path(model_dir, model_file_name)

    if model_name == ModelEnum.EASE:
        try :
            with open(model_path, 'rb') as file:
                model = MyCoustomUnpickler(file)
                model = model.load()
        except:
            print("기본 모델로 설정")
            model_src_file_name = 'ease_model_1682656807.p'
            model_path = cf.call_pre_path(model_dir, model_file_name, model_src_file_name)
            with open(model_path, 'rb') as file:
                model = MyCoustomUnpickler(file)
                model = model.load()

    print(f"{model_name} 모델 경로 : " + model_path)

    return model