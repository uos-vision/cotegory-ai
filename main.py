from fastapi import FastAPI
import numpy as np
import bottleneck as bn
from pydantic import BaseModel
import config as cf
import crawling as cr
import os
from model import model

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

@app.post("/model")
async def reload_model():
    cf.ease = cf.model_setting()
    cf.tag_problem_mat = cf.dataset_setting()
    return '모델 세팅 완료'
@app.post("/train")
async def train():

    return '훈련 완료'