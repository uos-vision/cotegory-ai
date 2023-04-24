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


NUM_TOP_PROBLEMS = 20

# 태그 설정
selected_tags = ['그리디 알고리즘', '다이나믹 프로그래밍', '브루트포스 알고리즘', '이분 탐색',
                 '너비 우선 탐색', '깊이 우선 탐색', '데이크스트라', '플로이드–워셜', '비트마스킹', '분리 집합']


# 모델 불러오기
def model_setting(model_dir='./model/saved',
                  model_file_name='ease_model',
                  model_file_exp='.p'):
    model_path = os.path.join(model_dir, f"{model_file_name}{model_file_exp}")
    return model.get_model(model_path)


ease = model_setting()


# 데이터 셋 불러오기
def dataset_setting(dataset_dir='./dataset',
                    dataset_file_name='tag_problem_mat_all',
                    dataset_file_exp='.csv'):
    dataset_path = os.path.join(dataset_dir, f"{dataset_file_name}{dataset_file_exp}")
    return pd.read_csv(dataset_path, index_col=0)


tag_problem_mat = dataset_setting()
tag_problem_mat = tag_problem_mat.T[selected_tags].T

# 훈련한 문제 개수 설정
st_pb_num = 1000
ed_pb_num = 27917
num_problem = ed_pb_num - st_pb_num + 1  # 1000 ~ 27917

# tag_problem_mat.shape : (10, 18745)

# 태그별 문제 저장
selected_probs_by_tags = {}
idx_to_num = {}
for tag in selected_tags:
    selected_probs_by_tags[tag] = get_problems_by_category(tag, tag_problem_mat)
    idx_to_num[tag] = dict(zip(range(len(selected_probs_by_tags[tag])), selected_probs_by_tags[tag]))
