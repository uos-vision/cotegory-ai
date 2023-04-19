import requests
from bs4 import BeautifulSoup
import numpy as np

#####################################
############# CROWLING ##############
#####################################

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

def add_to_user_problem_mat(idx, id, user_problem_mat: np.array):
    data = requests.get(f'https://www.acmicpc.net/user/{id}', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('div.problem-list')

    for tr in trs:
        problem_nums = tr.select('a')

        for problem_num in problem_nums:

            problem_num = int(problem_num.text) - 1000
            # print(problem_num)
            try:
                user_problem_mat[idx, problem_num] = 1
            except:
                print("문제 번호 : " + str(problem_num))