import uvicorn
from fastapi import FastAPI
import numpy as np
import bottleneck as bn
from pydantic import BaseModel
import config as cf
import crawling as cr
import pandas as pd
import model
import random
from model import ModelEnum
# uvicorn main:app --reload

app = FastAPI()

#####################################
################ API ################
#####################################

###### 태그 기반 추천 ######
class Item(BaseModel):
    handle: str = None
    tag: str
    cnt : int = cf.NUM_TOP_PROBLEMS
    model : ModelEnum = ModelEnum.EASE

@app.post(path = "/recommand", description="문제 추천")
async def recommand(item : Item) -> list:
    # TODO : 에러 처리
    assert item.tag in cf.selected_tags, '리스트에 없는 태그입니다.'
    assert item.model in list(ModelEnum), '리스트에 없는 모델입니다.'
    assert item.cnt < cf.NUM_TOP_PROBLEMS, '반환 문제 개수가 top sampling 문제 개수를 초과합니다.'

    print(item.model, list(ModelEnum))

    if item.handle is not None:
        # 아이디로 추천
        user_problem = np.zeros([1, cf.num_problem])
        cr.add_to_user_problem_mat(0, item.handle, user_problem)

        RecModel = cf.models[item.model]

        if item.model == ModelEnum.EASE:
            result = RecModel.forward(user_problem)

        # 유저가 푼 문제와 관련이 높은 문제 추천
        result[user_problem.nonzero()] = -np.inf
        result = np.expand_dims(result[0][cf.selected_probs_by_tags[item.tag]], axis=0)
        top_idx_by_user = bn.argpartition(-result, cf.NUM_TOP_PROBLEMS, axis=1)[:, :cf.NUM_TOP_PROBLEMS][0]  # 값이 큰 10개 문제 고름
        problems = np.array([cf.idx_to_num[item.tag][idx] for idx in top_idx_by_user])
    else:
        # 랜덤 추천
        problems = np.array(cf.selected_probs_by_tags[item.tag])

    problems += 1000
    rand_idx = random.sample(range(len(problems)),item.cnt)
    recommand_num = problems[rand_idx].tolist()

    return recommand_num

###### 추천 모델 다시 불러오기 ######
class M_Item(BaseModel):
    model : ModelEnum = ModelEnum.EASE

@app.post(path = "/model", description="추천 모델 다시 불러오기")
def reload_model(item : M_Item) -> str:
    assert item.model in list(ModelEnum), '리스트에 없는 모델입니다.'

    # 모델
    if item.model == ModelEnum.EASE:
        cf.ease = model.get_model(cf.ease_model_path)

    # 데이터
    cf.tag_problem_mat = pd.read_csv(cf.dataset_path, index_col=0)
    cf.tag_problem_mat = cf.tag_problem_mat.T[cf.selected_tags].T
    cf.selected_probs_by_tags, cf.idx_to_num = cf.set_tag_problem(cf.tag_problem_mat)

    return '모델 세팅 완료'

if __name__ == "__main__" :
    uvicorn.run("main:app", port=8000, reload=True)