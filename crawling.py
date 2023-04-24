import requests
from bs4 import BeautifulSoup
import numpy as np
import time

#####################################
############# CROWLING ##############
#####################################

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

def add_ids(page_num, user_ids: list):
    data = requests.get(f'https://www.acmicpc.net/ranklist/{page_num}', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('tbody > tr')

    for tr in trs:
        user_ids.append(tr.select_one('td:nth-child(2) > a').text)

def add_group_ids(group_num, page_num, user_ids: list):
    data = requests.get(f'https://www.acmicpc.net/school/ranklist/{group_num}/{page_num}', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('tbody > tr')

    for tr in trs:
        user_ids.append(tr.select_one('td:nth-child(2) > a').text)

def gen_user_problem_mat(id, user_problem: dict, problem_num_set: set):
    data = requests.get(f'https://www.acmicpc.net/user/{id}', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    trs = soup.select('div.problem-list')

    time.sleep(0.1)

    user_problem[id] = []

    for tr in trs:
        problem_nums = tr.select('a')
        for problem_num in problem_nums:
            problem_num = int(problem_num.text)
            # print(problem_num)
            user_problem[id].append(problem_num)
            problem_num_set.add(problem_num)
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