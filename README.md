# cotegory-ai
cotegory ai 추천 서버

+ api 문서 : localhost:8000/docs
+ server 실행 명령어
  ```commandline
  # window 
  (관리자로 실행후)
  uvicorn main:app --reload --host=0.0.0.0 --port=8000
  
  # Linux
  sudo uvicorn main:app --reload --host=0.0.0.0 --port=8000
  ```
## api 

<details>
<summary><b>[POST] /recommand</b> - 문제 추천</summary>

#### < 입력 json >
```
{
    "handle": "string",
    "tag" : "string",
    "cnt" : int, 
    "model" : "string"
}
```
+ 예시
```
{
    "handle": "sem1308",
    "tag" : "그리디 알고리즘",
    "cnt" : 20, 
    "model" : "EASE"
}
```
<details>
<summary>설명</summary>
    
+ handle
  - 백준 아이디
  - non essential
  - default : None
  - handle이 없으면 랜덤 추천

  + tag 
    - 문제 유형
    - essential
 
  + cnt
    - 반환 문제 개수 
    - non essential
    - default : 20

  + model
    - 추천 모델 이름
    - non essential
    - default : "EASE"
</details>

#### < 반환 >
```
[
  int, ...
]
```
+ 예시
```
[
    2839, 1946, 1105, 10775, 2812, 1083, 1461, 2217, 1931, 2212,
    1339, 1744, 1715, 16953, 1343, 2720, 1049, 11399, 1080, 2012
]
```
</details>

<details>
<summary><b>[POST] /reload/model</b> - 모델 다시 불러오기</summary>

#### < 입력 json >
```
{
    "model" : "string"
}
```
+ 예시
```
{
    "model" : "EASE"
}
```

#### < 반환 >
```
string
```
+ 예시
```
모델 로드 완료
```
</details>

<details>
<summary><b>[POST] /reload/data</b> - 데이터 다시 불러오기</summary>

#### < 입력 json >
#### < 반환 >
```
string
```
+ 예시
```
데이터 로드 완료
```
</details>

<br>
    
## requirements
###### SOFTWARE
```commandline
pip install -r requirements.txt
```
```
fastapi[all]
bottleneck
pandas
beautifulsoup4
requests
numpy
tqdm
chardet
scipy
```
+ python 3.10
+ torch 2.0, cuda 11.x (11.7)
    + pip
  ```
  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
  ```
  + conda
  ```
  conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
  ```
###### HARDWARE
+ GPU
  + 최소 1GB 이상
  + 권장 2GB 이상
  + 없어도 무관 단, cpu 성능이 좋아야함 
###### REQUIRED FILES
```commandline
필요한 파일 구조
│ 
├─dataset
│  └─saved
│        tag_problem_mat_all.csv
│           - 태그별 문제 매트릭스
│           - 추천할 문제는 이 매트릭스에서 선정
│           - 아래 카테고리가 전부 포함되어야함
│        tag_problem_mat_all.npz
│           - 태그별 문제 매트릭스 (row, culumn에 이름이 명시되어있지 않음)
│           - prob_num_list_all.npy, tag_list_all.npy파일 필요
│        prob_num_list_all.npy
│           - 전체 문제 번호 리스트
│           - 태그별 문제 매트릭스의 column 이름
│        tag_list_all.npy) 
│           - 전체 태그 리스트
│           - 태그별 문제 매트릭스의 row 이름
│        user_problem_mat.npz
│           - 훈련에 쓰인 유저-문제 매트릭스
│           - 훈련에 쓰인 문제 개수 불러오는 데에 쓰임
│
└─model
   └─saved
     ├─auto_encoder
     │      auto_encoder_model.pt
     │         - AUTO_ENCODER 모델 가중치 파일
     │      
     └─ease
            ease_model.npz
     │         - EASE 모델 가중치 파일
            
- 서버 실행시 모델 파일을 가리키는 심볼릭 링크 파일(.symlink) 자동 생성
- 모델 가중치 파일 없어도 실행 가능 (단, tag_problem_mat_all 파일 필요)
  └─ 훈련된 모델이 아니므로 이상한 문제를 추천함
```

## **Recommand Models**
+ k=10

| Model              | Precision@10  | Recall@10  | nDCG@10    |
|--------------------|:--------------|:-----------|:-----------|
| EASE               | 0.9614        | 0.1255     | 0.9691     |
| AUTO_ENCODER       | 0.9595        | 0.1252     | 0.9670     | 
| AUTO_ENCODER_CONST | **0.9647**    | **0.1259** | **0.9712** |

+ k=20

| Model              | Precision@20  | Recall@20  | nDCG@20    | 
|--------------------|:--------------|:-----------|:-----------|
| EASE               | 0.9259        | 0.2404     | 0.9418     | 
| AUTO_ENCODER       | 0.9259        | 0.2403     | 0.9410     | 
| AUTO_ENCODER_CONST | **0.9292**    | **0.2413** | **0.9443** | 

## **categories**
```
그리디 알고리즘
다이나믹 프로그래밍
브루트포스 알고리즘
이분 탐색
너비 우선 탐색
깊이 우선 탐색
데이크스트라
플로이드–워셜
비트마스킹
분리 집합
```
