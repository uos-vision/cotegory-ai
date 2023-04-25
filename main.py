from fastapi import FastAPI
import numpy as np
import bottleneck as bn
from pydantic import BaseModel
import config as cf
import crawling as cr
import os
import pandas as pd
from model import model
from train.train import train_model

# uvicorn main:app --reload

app = FastAPI()

#####################################
################ API ################
#####################################

###### 태그 기반 추천 ######
class Item(BaseModel):
    handle: str = None
    tag: str

@app.post("/recommand")
async def recommand(item : Item):
    assert item.tag in cf.selected_tags, '리스트에 없는 태그입니다.'

    if item.handle is not None:
        # 아이디로 추천
        user_problem = np.zeros([1, cf.num_problem])

        cr.add_to_user_problem_mat(0, item.handle, user_problem)

        result = cf.ease.forward(user_problem)

        # 유저가 푼 문제와 비슷한 유형 추천
        result[user_problem.nonzero()] = -np.inf
        result = np.expand_dims(result[0][cf.selected_probs_by_tags[item.tag]], axis=0)
        top_idx_by_user = bn.argpartition(-result, cf.NUM_TOP_PROBLEMS, axis=1)[:, :cf.NUM_TOP_PROBLEMS][0]  # 값이 큰 10개 문제 고름
        problems = np.array([cf.idx_to_num[item.tag][idx] for idx in top_idx_by_user])
    else:
        # 랜덤 추천
        problems = np.array(cf.selected_probs_by_tags[item.tag])

    problems += 1000
    rand_idx = np.random.randint(len(problems))
    recommand_num = problems.tolist()[rand_idx]

    return recommand_num

###### 추천 모델 다시 불러오기 ######
@app.post("/model")
def reload_model():
    # 모델
    cf.ease = model.get_model(cf.model_path)

    # 데이터
    cf.tag_problem_mat = pd.read_csv(cf.dataset_path, index_col=0)
    cf.tag_problem_mat = cf.tag_problem_mat.T[cf.selected_tags].T
    cf.selected_probs_by_tags, cf.idx_to_num = cf.set_tag_problem(cf.tag_problem_mat)

    return '모델 세팅'

###### 추천 모델 재 훈련 ######
class TrainItem(BaseModel):
    model_name : str
    cfg : dict

@app.post("/train")
def train(item : TrainItem):
    train_model(item.model_name, item.cfg)
    return '훈련 발생'