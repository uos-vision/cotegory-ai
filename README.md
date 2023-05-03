# cotegory-ai
cotegory ai 추천 서버

---
## api 

/recommand
- 문제 추천
{
    "handle": string,
    "tag" : string,
    "cnt" : int, 
    "model" : string
}
- 예시
{
    "handle": "sem1308",
    "tag" : "그리디 알고리즘",
    "cnt" : 20, 
    "model" : "EASE"
}
- handle 
 -- 백준 아이디
 -- non essential
 -- default : None
 -- handle이 없으면 랜덤 추천

- tag 
 + 문제 유형
 + essential
 
- cnt
 + 반환 문제 개수 
 + non essential
 + default : 20

- model
 + 추천 모델 이름
 + non essential
 + default : "EASE"

/model
- 모델 다시 불러오기
{
    "model" : string
}
- 예시
{
    "model" : "EASE"
}
- model
 + 추천 모델 이름
 + non essential
 + default : "EASE"
 
 ---
 + requirements
fastapi[all]
bottleneck
pandas
beautifulsoup4
requests
numpy
tqdm

+ categories
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
