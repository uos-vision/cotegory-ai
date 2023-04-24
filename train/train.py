import pandas as pd
from tqdm import tqdm
import pickle
from model import model
from config import dataset_dir,dataset_file_name, dataset_file_exp,model_dir, model_file_name, model_file_exp
from crawling import *
import os
import time

def train_model(model_name : str , cfg : dict):
    if model_name == 'EASE' :

        ## 유저-문제 크롤링 세팅 ##
        user_ids = []
        try:
            page_st = cfg['page_st']
            page_ed = cfg['page_ed']
        except:
            print('페이지 수가 설정되지 않았습니다.')
            print("dict 변수에 page_st, page_ed 값이 존재해야 합니다.")
            return

        if cfg['crawl_mode'] == 'indiv':
            ## 유저 랭킹 페이지에서 선택 ##

            for num in tqdm(range(page_st, page_ed+1)):
                add_ids(num, user_ids)
        elif cfg['crawl_mode'] == 'group':
            ## 한 그룹 내에서 선택 ##
            try:
                group_num = cfg['group_num']  # 서울시립대학교
            except:
                print('그룹 번호가 설정되지 않았습니다.')
                print("dict 변수에 group_num 값이 존재해야 합니다.")
                return

            for num in tqdm(range(page_st, page_ed + 1)):
                add_group_ids(group_num, num, user_ids)

        ## 유저-문제 크롤링 ##
        start = time.time()

        user_problem = {}
        problem_num_set = set([])

        for id in tqdm(user_ids, position=0):
            gen_user_problem_mat(id, user_problem, problem_num_set)

        end = time.time()

        print(f"유저-문제 크롤링 시간 : {end - start:.5f} sec")

        ## 유저-문제 매트릭 생성 ##
        user_problem_mat = {}
        for user, problems in user_problem.items():
            user_problem_mat[user] = {num:0 for num in problem_num_set}
            for problem in problems:
                user_problem_mat[user][problem] = 1

        ## dataframe으로 저장 ##
        df = pd.DataFrame(user_problem_mat).T
        df.to_csv(os.path.join(dataset_dir,f"{dataset_file_name}_{end}{dataset_file_exp}"))
        df = df.to_numpy()

        ## EASE 훈련 ##
        start = time.time()

        ease = model.EASE(300)
        ease.train(df)

        end = time.time()

        print(f"EASE 훈련 시간 : {end - start:.5f} sec")
        # 훈련은 약 5분 걸림 - 유저 10000명 기준
        # 훈련은 약 10초 걸림 - 유저 500명 기준 - 시립대 학생들이 푼 문제만

        # 모델 저장
        with open(os.path.join(model_dir,f'{model_file_name}{model_file_exp}_{end}'), 'wb') as file:  # 파일을 바이너리 쓰기 모드(wb)로 열기
            pickle.dump(ease, file)

