import pandas as pd
import os
from model import model


####################################
############# CONFIGS ##############
####################################

def get_problems_by_category(tag_name, tag_problem_mat):
    selected_probs_by_tag = []
    for tag_pro_row in tag_problem_mat:
        if tag_problem_mat[tag_pro_row][tag_name]:
            selected_probs_by_tag.append(int(tag_pro_row) - 1000)
    return selected_probs_by_tag

def call_pre_path(dir,file_name, src = None):
    link_path = os.path.join(dir,file_name)

    if src is not None:
        if os.path.islink(link_path):
            os.unlink(link_path)
        path = os.path.join(dir,src)
        os.symlink(path, link_path)

    return os.readlink(link_path), link_path

NUM_TOP_PROBLEMS = 20

# 태그 설정
selected_tags = ['그리디 알고리즘', '다이나믹 프로그래밍', '브루트포스 알고리즘', '이분 탐색',
                 '너비 우선 탐색', '깊이 우선 탐색', '데이크스트라', '플로이드–워셜', '비트마스킹', '분리 집합']

# 모델 불러오기
model_dir = './model/saved'
model_file_name = 'ease_model'

# 데이터 셋 불러오기
dataset_dir = './dataset'
dataset_file_name = 'tag_problem_mat_all'

try:
    model_path, model_link_path = call_pre_path(model_dir, model_file_name)

    dataset_path, dataset_link_path = call_pre_path(dataset_dir,dataset_file_name)
    tag_problem_mat = pd.read_csv(dataset_path, index_col=0)
    tag_problem_mat = tag_problem_mat.T[selected_tags].T
except:
    print("기본 모델로 설정")
    model_src_file_name = 'ease_model_20230401.p'
    model_path, model_link_path = call_pre_path(model_dir,model_file_name,model_src_file_name)

    print("기본 데이터로 설정")
    dataset_src_file_name = 'tag_problem_mat_all_20230401.csv'
    dataset_path, dataset_link_path = call_pre_path(dataset_dir,dataset_file_name,dataset_src_file_name)
    tag_problem_mat = pd.read_csv(dataset_path, index_col=0)
    tag_problem_mat = tag_problem_mat.T[selected_tags].T

print("데이터셋 경로 : " + dataset_path)
print("모델 경로 : " + model_path)

ease = model.get_model(model_path)

# 훈련한 문제 개수 설정
st_pb_num = 1000
ed_pb_num = 27917
num_problem = ed_pb_num - st_pb_num + 1  # 1000 ~ 27917

# tag_problem_mat.shape : (10, 18745)

# 태그별 문제 저장
def set_tag_problem(tag_problem_mat):
    selected_probs_by_tags = {}
    idx_to_num = {}

    for tag in selected_tags:
        selected_probs_by_tags[tag] = get_problems_by_category(tag, tag_problem_mat)
        idx_to_num[tag] = dict(zip(range(len(selected_probs_by_tags[tag])), selected_probs_by_tags[tag]))

    return selected_probs_by_tags,idx_to_num

selected_probs_by_tags,idx_to_num = set_tag_problem(tag_problem_mat)