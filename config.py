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
model_dir = './model/saved'
model_file_name = 'ease_model'
model_file_exp = 'p'
model_link_path = os.path.join(model_dir,model_file_name)
#model_path = os.path.join(model_dir,f'ease_model_20230401.p')
#os.symlink(model_path, model_link_path)
model_path = os.readlink(model_link_path)
print("모델 경로 : " + model_path)
ease = model.get_model(model_path)

# 데이터 셋 불러오기
dataset_dir = './dataset'
dataset_file_name = 'tag_problem_mat_all'
dataset_file_exp = 'csv'
dataset_link_path = os.path.join(dataset_dir,dataset_file_name)
#dataset_path = os.path.join(dataset_dir, "tag_problem_mat_all_20230401.csv")
#os.symlink(dataset_path, dataset_link_path)
dataset_path = os.readlink(dataset_link_path)
print("데이터셋 경로 : " + dataset_path)

tag_problem_mat = pd.read_csv(dataset_path, index_col=0)
tag_problem_mat = tag_problem_mat.T[selected_tags].T

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