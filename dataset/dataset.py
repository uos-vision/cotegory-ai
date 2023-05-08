import utils
import pandas as pd
import os

def get_problems_by_category(tag_name, tag_problem_mat):
    selected_probs_by_tag = []
    for tag_pro_row in tag_problem_mat:
        if tag_problem_mat[tag_pro_row][tag_name]:
            selected_probs_by_tag.append(int(tag_pro_row) - 1000)
    return selected_probs_by_tag

def set_tag_problem(tag_problem_mat, selected_tags):
    selected_probs_by_tags = {}
    idx_to_num = {}

    for tag in selected_tags:
        selected_probs_by_tags[tag] = get_problems_by_category(tag, tag_problem_mat)
        idx_to_num[tag] = dict(zip(range(len(selected_probs_by_tags[tag])), selected_probs_by_tags[tag]))

    return selected_probs_by_tags,idx_to_num

def get_dataset(dataset_dir, dataset_file_name, selected_tags):
    # 데이터 셋 불러오기
    dataset_path = utils.call_pre_path(dataset_dir, dataset_file_name)

    if (dataset_path is None) or (not os.path.exists(dataset_path)):
        print("기본 데이터로 설정")
        dataset_src_file_name = 'tag_problem_mat_all.csv'
        dataset_path = utils.call_pre_path(dataset_dir, dataset_file_name, dataset_src_file_name)

    tag_problem_mat = pd.read_csv(dataset_path, index_col=0)
    tag_problem_mat = tag_problem_mat.T[selected_tags].T

    print("문제데이터셋 경로 : " + dataset_path)

    # 태그별 문제 저장
    selected_probs_by_tags, idx_to_num = set_tag_problem(tag_problem_mat, selected_tags)

    return tag_problem_mat, selected_probs_by_tags, idx_to_num

def get_num_problems(dataset_dir, data_file):
    train_data_path = os.path.join(dataset_dir, data_file)
    train_s_mat = pd.read_csv(train_data_path, index_col=0)
    num_problem = train_s_mat.shape[1]  # 1000 ~ 27981 -> 26982
    return num_problem