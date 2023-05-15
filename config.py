import model
from model import ModelEnum
import dataset

####################################
############# CONFIGS ##############
####################################

# 태그 설정
selected_tags = ['그리디 알고리즘', '다이나믹 프로그래밍', '브루트포스 알고리즘', '이분 탐색',
                 '너비 우선 탐색', '깊이 우선 탐색', '데이크스트라', '플로이드–워셜', '비트마스킹', '분리 집합']

# 데이터 셋 불러오기 - 추천할 문제에 쓰임
dataset_dir = './dataset/saved'
dataset_file_name = 'tag_problem_mat'
dataset_src_file_name = 'tag_problem_mat_all.npz'
tag_problem_mat, selected_probs_by_tags,idx_to_num = dataset.get_dataset(dataset_dir, dataset_file_name, selected_tags)
# tag_problem_mat.shape : (10, 26188)

# 훈련한 문제 개수 설정
data_file = "train_user_problem_mat.npz"
num_problem = dataset.get_num_problems(dataset_dir,data_file)

# 모델 불러오기
model_root_dir = './model/saved'
models = {}
model_srcs = {
    ModelEnum.EASE : 'ease_model.npz',
    ModelEnum.AUTO_ENCODER : 'auto_encoder_model.pt',
}
for m, src in model_srcs.items():
    models[m] = model.get_model(m, src)
print("모델 불러오기 완료")

# 추천될 문제 개수
NUM_TOP_PROBLEMS = 20
