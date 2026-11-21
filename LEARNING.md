# Mission 03 학습 기록

[README로 돌아가기](README.md)

## 목차
- [설계 결정](#설계-결정)
- [핵심 코드 해설](#핵심-코드-해설)
- [수행 로그](#수행-로그)
- [시행착오](#시행착오)
- [배운 점](#배운-점)
- [용어 사전](#용어-사전)

## 설계 결정

### 1. 브랜치는 main 하나만 쓴다
- 맥락: 명세에 브랜치 규칙이 없다. 혼자 하는 작은 프로그램이다.
- 결정: 작업 브랜치 없이 `main`에서 바로 작업하고 커밋한다.
- 결과: 얻은 것: 절차가 단순하고 평가 요청 때 브랜치를 헷갈리지 않는다. / 포기한 것: 실험하다 망가뜨려도 되는 별도 공간.

### 2. data.json을 저장소에 넣는다
- 맥락: 프로그램은 `data.json`이 있어야 모드 2를 실행할 수 있다.
- 결정: 저장소 최상위 폴더에 그대로 넣고 README에 출처(코디세이 Mission 03 제공 데이터)를 적는다. 원본은 고치지 않는다.
- 결과: 얻은 것: 누구나 내려받아 바로 실행할 수 있다. / 포기한 것: 제공 자료를 공개하는 데 따른 부담 (공지로 금지되면 제외한다).

### 3. 보너스는 패턴 생성기 하나만 한다
- 맥락: 보너스 2개(1차원 배열 최적화, 패턴 생성기) 중 시간 안에 할 수 있는 것을 골라야 한다.
- 결정: 패턴 생성기만 한다.
- 결과: 얻은 것: 반복문 두 개로 모양을 만드는 방식이라 설명하기 쉽다. / 포기한 것: 1차원 배열 최적화 (메모리 접근 설명이 어렵고, 파이썬에서는 속도 차이가 작게 나올 수 있다).

## 핵심 코드 해설
(U2부터 파일별로 추가)

## 수행 로그

### U1 · 저장소 초기 설정
```
PS> python --version            → Python 3.14.7
PS> py --version                → Python 3.14.7
PS> git --version               → git version 2.54.0.windows.1
PS> git config --global user.name   → Clay-pieup
PS> git config --global user.email  → (GitHub noreply 주소, 공개 저장소라 가림)
PS> git init -b main
PS> git add .
PS> git status
On branch main / No commits yet
Changes to be committed:
        new file:   .gitignore
        new file:   LEARNING.md
        new file:   README.md
        new file:   data.json
→ CLAUDE.md가 목록에 없음 = .gitignore가 제대로 막고 있음
PS> git commit -m "Docs: 저장소 뼈대 추가 - README·LEARNING·.gitignore·data.json으로 작업 시작 준비"
[main (root-commit) 0a70162] … 4 files changed, 361 insertions(+)
PS> git remote add origin https://github.com/Clay-pieup/Codyssey_AIO_Mission_03.git
PS> git push -u origin main      → 1차 실패 (시행착오 1)
PS> git push -u origin main      → 2차 성공: GitHub에 커밋 0a70162·파일 4개·README 표시 확인
```

## 시행착오
### 1. push 실패 `remote: Repository not found`
- 문제: 첫 push가 "저장소를 찾을 수 없음"으로 실패했다.
- 원인: GitHub에 저장소를 만들기 전에 push했다. 주소 등록(`remote add`)은 됐지만 받을 곳이 없었다.
- 해결: GitHub에 Public 빈 저장소(체크 항목 비움)를 만든 뒤 `git push -u origin main`만 다시 실행했다. commit과 remote add는 이미 끝났으므로 다시 하지 않았다.

## 배운 점
- U1: 커밋은 내 PC 장부에 적는 것이고 push는 GitHub로 복사하는 것이다. 그래서 push가 실패해도 커밋은 남는다. `.gitignore`에 적은 파일은 `git add .`를 해도 올라가지 않는다.

## 용어 사전
| 용어 | 쉬운 풀이 |
|---|---|
| MAC 연산 | 같은 자리 숫자끼리 곱하고(Multiply) 그 결과를 계속 더해 가는(Accumulate) 계산. AI가 그림을 알아보는 기본 동작 |
| 필터 | "이런 모양이면 점수가 높게 나와라" 하고 정해 둔 기준 숫자표 |
| 패턴 | 판정하고 싶은 그림을 숫자표로 바꾼 것 |
| NPU | MAC 연산을 한꺼번에 수천 개씩 처리하는 AI 전용 칩 |
| 부동소수점 오차 | 컴퓨터가 0.1 같은 소수를 정확히 저장하지 못해 생기는 아주 작은 오차 (0.9가 0.8999…로 나옴) |
| epsilon(허용오차) | "이 정도 차이는 같은 걸로 치자" 하고 정한 아주 작은 값 (여기서는 0.000000001) |
| 라벨 정규화 | `+`, `cross`처럼 제각각인 이름을 `Cross` 하나로 통일하는 것 |
| 스키마 | 데이터 파일이 지켜야 하는 모양 규칙 (어떤 키가 있고, 값이 몇 칸인지) |
| 시간 복잡도 O(N²) | 표 한 변의 길이 N이 2배가 되면 계산량이 4배가 된다는 뜻 (N×N칸을 하나씩 곱하니까) |
| 브랜치 | 원본을 건드리지 않고 따로 작업하는 갈림길. 이번 미션은 원본 길(`main`) 하나만 쓴다 |
| noreply 이메일 | GitHub가 주는 공개용 가짜 이메일. 진짜 이메일을 공개 저장소에 남기지 않으려고 쓴다 |
| .gitignore | "이 파일들은 Git에 올리지 마"라고 적어 두는 목록 |
| PowerShell | Windows에서 글자로 명령을 입력해 컴퓨터를 움직이는 창 |
| 원격 저장소 (remote·origin) | 인터넷(GitHub)에 있는 내 코드 보관함. 관례상 이름을 `origin`으로 붙인다. 내 PC 폴더는 로컬 저장소 |
| Public 저장소 | 누구나 볼 수 있는 공개 보관함. 이메일·토큰 같은 정보를 넣으면 안 된다 |
| git init | 평범한 폴더에 변경 기록 장부(`.git` 숨김 폴더)를 만들어 Git 저장소로 바꾸는 명령 |
| 스테이징 (git add) | 사진 찍기 전에 찍을 사람들을 줄 세우는 단계. 줄에 선 파일만 다음 커밋에 담긴다 |
| 커밋 | 지금 파일 상태를 설명 한 줄과 함께 장부에 찍어 두는 기록 한 장 |
| push | 내 PC에 쌓인 커밋을 GitHub로 올려 보내는 것. 실패해도 커밋은 PC에 남는다 |
