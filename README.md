# cotegory-ai
cotegory ai 추천 서버

+ api 문서 : localhost:8000/docs

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
<summary><b>[POST] /model</b> - 모델 다시 불러오기</summary>

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
모델 추천 완료
```
</details>

---
+ requirements
```
fastapi[all]
bottleneck
pandas
beautifulsoup4
requests
numpy
tqdm
```

+ categories
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
