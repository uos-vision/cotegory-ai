import pandas as pd
import os
import model
from model import ModelEnum
import dataset

####################################
############# CONFIGS ##############
####################################

def call_pre_path(dir,file_name, src = None):
    link_path = os.path.join(dir,file_name)

    if src is not None:
        if os.path.islink(link_path):
            os.unlink(link_path)
        path = os.path.join(dir,src)
        os.symlink(path, link_path)

    return os.readlink(link_path)

# 태그 설정
selected_tags = ['그리디 알고리즘', '다이나믹 프로그래밍', '브루트포스 알고리즘', '이분 탐색',
                 '너비 우선 탐색', '깊이 우선 탐색', '데이크스트라', '플로이드–워셜', '비트마스킹', '분리 집합']

# 모델 불러오기
model_root_dir = './model/saved'
models = {}
for m in ModelEnum:
    models[m] = model.get_model(m)
print("모델 불러오기 완료")

# 데이터 셋 불러오기 - 추천할 문제에 쓰임
tag_problem_mat, selected_probs_by_tags,idx_to_num = dataset.get_dataset()
# tag_problem_mat.shape : (10, 26188)

# 훈련한 문제 개수 설정
st_pb_num = 1000
ed_pb_num = 27981
num_problem = ed_pb_num - st_pb_num + 1  # 1000 ~ 27981

# 추천될 문제 개수
NUM_TOP_PROBLEMS = 20
