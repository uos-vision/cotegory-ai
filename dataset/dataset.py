import utils
import pandas as pd
import config as cf
import os
from scipy import sparse
import numpy as np

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
        dataset_path = utils.call_pre_path(dataset_dir, dataset_file_name, cf.dataset_src_file_name)

    exp = dataset_path.split(sep='.')[-1]
    if exp == "csv":
        tag_problem_mat = pd.read_csv(dataset_path, index_col=0).T
    elif exp == "npz":
        tp_mat = sparse.load_npz(dataset_path).toarray()
        tag_list_all = np.load(f'{dataset_dir}/tag_list_all.npy', allow_pickle=True)
        tag_problem_mat = pd.DataFrame({tag:mat for (tag,mat) in zip(tag_list_all,tp_mat)})

    tag_problem_mat = tag_problem_mat[selected_tags].T
    print("문제데이터셋 경로 : " + dataset_path)
    print(f"태그-문제 매트릭 shape : {tag_problem_mat.shape}")

    # 태그별 문제 저장
    selected_probs_by_tags, idx_to_num = set_tag_problem(tag_problem_mat, selected_tags)

    return tag_problem_mat, selected_probs_by_tags, idx_to_num

def get_num_problems(dataset_dir, data_file):
    data_path = os.path.join(dataset_dir, data_file)
    try:
        exp = data_path.split(sep='.')[-1]
        if exp == "csv":
            s_mat = pd.read_csv(data_path, index_col=0)
        elif exp == "npz":
            s_mat = sparse.load_npz(data_path).toarray()
        num_problem = s_mat.shape[1]  # 1000 ~ 27981 -> 26982
    except:
        print("훈련 데이터 불러오기 실패 - 초기 문제 개수로 설정")
        num_problem = 26982
    print(f"가장 큰 문제 번호 : {999+num_problem}")
    return num_problem