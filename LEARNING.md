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

### 4. 2차원 리스트 + 기능별 함수
- 맥락: 크기가 3~25로 다양하고, 모드 1·2가 같은 계산을 쓴다.
- 결정: 파이썬 기본 리스트로 표를 만들고, 표 만들기·MAC·판정을 함수로 나눈다.
- 결과: 얻은 것: 외부 라이브러리 없이 어떤 크기든 같은 코드로 처리하고, 함수를 재사용한다. / 포기한 것: NumPy 같은 빠른 계산 도구.

### 5. epsilon 비교 정책
- 맥락: 컴퓨터는 소수를 정확히 저장하지 못해 0.9와 0.8999…를 다른 수로 본다.
- 결정: `==` 대신 `abs(A−B) < 1e-9`면 동점(UNDECIDED)으로 본다. 기준값은 맨 위 `EPSILON` 한 곳에 둔다.
- 결과: 얻은 것: 계산 오차 때문에 한쪽이 억지로 이기는 판정을 막는다. / 포기한 것: 차이가 아주 작은 진짜 승부도 동점이 된다.

### 6. 틀린 줄만 다시 받기
- 맥락: 3줄 중 한 줄만 틀려도 처음부터 다시 치게 하면 불편하다.
- 결정: 한 줄씩 검사해서 틀린 줄만 다시 받는다. 줄 수는 프로그램이 n줄만 물어서 보장한다.
- 결과: 얻은 것: 입력이 편하고, 행 수 불일치가 아예 생기지 않는다. / 포기한 것: 형식은 맞지만 숫자를 잘못 친 줄은 되돌릴 수 없다(다시 실행해야 함).

### 7. Ctrl+C·입력 끊김 안전 종료
- 맥락: 입력 중 Ctrl+C를 누르면 파이썬이 빨간 오류(Traceback)를 띄운다.
- 결정: `main()` 전체를 `try/except (KeyboardInterrupt, EOFError)`로 감싸 안내 문구만 띄우고 끝낸다.
- 결과: 얻은 것: 평가자에게 깔끔한 종료 화면을 보여 준다. / 포기한 것: 없음(정상 흐름에는 영향 없음).

### 8. 시간 측정 방식
- 맥락: 3×3 계산은 1000분의 1초보다 짧고, 잴 때마다 값이 흔들린다.
- 결정: 가장 정밀한 `time.perf_counter()`로 MAC 호출만 10번 재서 평균을 낸다. 반복 횟수는 맨 위 `REPEAT` 한 곳에 둔다.
- 결과: 얻은 것: 입출력에 영향받지 않는 계산 시간. / 포기한 것: 실행할 때마다 값이 조금씩 다르고, 아주 작은 표에서는 함수를 부르는 기본 비용이 섞인다.

## 핵심 코드 해설
<details><summary>main.py · U2 데이터 구조·MAC·판정</summary>

**① 표 만들기·읽기·쓰기**
```python
def make_matrix(n, fill=0.0):        # n×n 표를 만드는 함수. 칸을 채울 값을 안 주면 0.0
    matrix = []                      # 빈 큰 상자(표 전체)
    for _ in range(n):               # n번 반복해 줄(행)을 만든다
        row = []                     # 빈 작은 상자(한 줄)
        for _ in range(n):           # 한 줄에 칸을 n개
            row.append(fill)         # 칸 하나를 채워 줄 끝에 붙인다
        matrix.append(row)           # 다 만든 줄을 표에 붙인다
    return matrix                    # 완성된 표를 돌려준다

def set_value(matrix, row, col, value):
    matrix[row][col] = value         # row번째 줄, col번째 칸에 값 저장 (0부터 센다)

def get_value(matrix, row, col):
    return matrix[row][col]          # 같은 위치의 값을 읽어 돌려준다
```
- n에 아무 숫자나 넣을 수 있으니 3·5·13·25 크기를 모두 같은 코드로 처리한다.
- `_`는 "반복 횟수만 필요하고 번호는 안 쓴다"는 표시다.

**② MAC 연산**
```python
def mac(pattern, filter_matrix):
    n = len(pattern)                 # 표가 몇 줄인지 센다 (3×3이면 3)
    score = 0.0                      # 점수 통, 소수로 시작 → 결과도 소수(float)
    for row in range(n):             # 줄을 위에서 아래로
        for col in range(n):         # 칸을 왼쪽에서 오른쪽으로
            score += pattern[row][col] * filter_matrix[row][col]   # 같은 칸끼리 곱해서 통에 더한다
    return score                     # 다 더한 점수를 돌려준다
```
- 반복문 두 개가 겹쳐 있어 안쪽 줄(`score += …`)은 정확히 n×n번 실행된다 (3×3이면 9번, 25×25면 625번). 이것이 O(N²)의 근거다.

**③ epsilon 판정**
```python
def judge(score_a, score_b, label_a="A", label_b="B"):
    if abs(score_a - score_b) < EPSILON:   # 두 점수 차이(절댓값)가 0.000000001보다 작으면
        return UNDECIDED                   #   동점 → 판정 불가
    if score_a > score_b:                  # A가 더 크면
        return label_a                     #   A의 이름 (모드 2에서는 "Cross")
    return label_b                         # 아니면 B의 이름 (모드 2에서는 "X")
```
- `==`로 비교하지 않는 이유: 컴퓨터는 0.9와 0.8999999999999999를 다른 수로 본다. 사람이 보기엔 같은 점수인데 한쪽이 이기는 것을 막으려고 "이 정도 차이는 같다"는 기준을 둔다.

</details>

<details><summary>main.py · U3 메뉴·모드 1 입력</summary>

**① 한 줄 입력과 검증**
```python
def read_row(n):
    while True:                          # 올바른 줄이 들어올 때까지 반복
        parts = input().split()          # 한 줄을 받아 공백 기준으로 자른다 ("0 1 0" → ["0","1","0"])
        if len(parts) != n:              # 조각이 n개가 아니면 (열 수 불일치)
            print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
            continue                     #   안내하고 이 줄을 다시 받는다
        values = []
        try:                             # "시도해 보고, 오류가 나면 except로 간다"
            for part in parts:
                values.append(float(part))   # 글자 "1"을 숫자 1.0으로 바꾼다. "a"면 ValueError 발생
        except ValueError:               # 숫자로 못 바꿨으면
            print("입력 형식 오류: 숫자만 입력하세요. (예: 0 1 0)")
            continue                     #   이 줄을 다시 받는다
        return values                    # 통과한 줄을 돌려준다
```

**② n줄을 받아 표에 저장**
```python
def read_matrix(title, n=3):
    print(f"{title} ({n}줄 입력, 공백 구분)")
    matrix = make_matrix(n)              # U2 함수로 빈 3×3 표를 만든다
    for row in range(n):                 # 1~3번째 줄을 차례로
        values = read_row(n)             #   검사를 통과한 한 줄을 받아
        for col in range(n):
            set_value(matrix, row, col, values[col])   # 칸마다 저장
    return matrix
```
- 정확히 n줄만 물으므로 행 수 불일치는 생길 수 없다. 검사할 것은 열 수와 숫자 여부 두 가지다.

**③ 모드 선택**
```python
def choose_mode():
    while True:
        … 메뉴 출력 …
        choice = input("선택: ").strip()   # 앞뒤 공백을 지운다 (" 1 " → "1")
        if choice == "1" or choice == "2":
            return choice
        print("입력 오류: 1 또는 2를 입력하세요.")   # 그 밖의 값이면 다시 묻는다
```

**④ 실행 순서와 안전 종료**
- `run_mode1()`: 필터 A 입력 → 필터 B 입력 → 저장된 필터 출력(저장 확인) → 패턴 입력 → `mac()`으로 A·B 점수 → `judge()`로 판정 → `UNDECIDED`면 "판정 불가"로 바꿔 출력
- 맨 아래 `try: main() except (KeyboardInterrupt, EOFError):` → Ctrl+C나 입력 끊김에도 오류 대신 안내 문구를 띄우고 끝낸다.

</details>

<details><summary>main.py · U4 시간 측정·성능 표</summary>

```python
import time                                   # 파이썬 표준 시계 도구 (외부 라이브러리 아님, 시험 차단 목록에도 없음)
REPEAT = 10                                   # 반복 횟수

def measure_mac_ms(pattern, filter_matrix, repeat=REPEAT):
    start = time.perf_counter()               # 출발 시각 기록 (초 단위)
    for _ in range(repeat):                   # 10번
        mac(pattern, filter_matrix)           #   MAC 연산만 돌린다 (입출력 없음)
    end = time.perf_counter()                 # 도착 시각 기록
    return (end - start) * 1000 / repeat      # 걸린 초 × 1000 = 밀리초(ms), ÷ 10 = 1회 평균

def print_performance_table(pairs):
    print("크기       평균 시간(ms)    연산 횟수(N²)")   # 표 머리
    for pattern, filter_matrix in pairs:      # (패턴, 필터) 쌍마다
        n = len(pattern)                      #   한 변의 길이
        avg_ms = measure_mac_ms(pattern, filter_matrix)
        size_text = f"{n}×{n}"                #   "3×3" 같은 글자
        print(f"{size_text:<10}{avg_ms:>12.4f}{n * n:>14}")
        # :<10 = 왼쪽 맞춤 10칸, :>12.4f = 오른쪽 맞춤 12칸에 소수 넷째 자리까지, n*n = 연산 횟수
```
- `run_mode1()`에는 [3] MAC 결과의 `연산 시간(평균/10회)` 한 줄과, 맨 끝 `[4] 성능 분석` 표가 추가됐다.
- 표 함수는 (패턴, 필터) 쌍 목록만 받으면 크기와 상관없이 쓸 수 있어서 모드 2(U6)에서 다시 쓴다.

</details>

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

### U2 · 데이터 구조·MAC·판정
```
PS> python main.py
make_matrix(3) 후 (1, 2) 칸에 7.5 저장: [[0.0, 0.0, 0.0], [0.0, 0.0, 7.5], [0.0, 0.0, 0.0]]
(1, 2) 칸 읽기: 7.5
십자가 입력 × 십자가 필터 = 5.0
십자가 입력 × X 필터 = 1.0
판정: Cross
0.1 + 0.2 = 0.30000000000000004
0.9 == 0.8999999999999999 ? False
0.9 vs 0.8999999999999999 판정: UNDECIDED
```
- 5.0·1.0은 명세 1장 Case 1·2 점수와 같다.
- 시험 차단 명령 점검(main.py): 해당 없음

### U3 · 모드 선택·모드 1 입력
① 정상 입력 (명세 예시)
```
PS> python main.py
=== Mini NPU Simulator ===
[모드 선택] … 선택: 1
# [1] 필터 입력
필터 A (3줄 입력, 공백 구분)   0 1 0 / 1 1 1 / 0 1 0
필터 B (3줄 입력, 공백 구분)   1 0 1 / 0 1 0 / 1 0 1
저장된 필터 A:
  0.0 1.0 0.0
  1.0 1.0 1.0
  0.0 1.0 0.0
저장된 필터 B:
  1.0 0.0 1.0
  0.0 1.0 0.0
  1.0 0.0 1.0
# [2] 패턴 입력
패턴 (3줄 입력, 공백 구분)   1 0 1 / 0 1 0 / 1 0 1
# [3] MAC 결과
A 점수: 1.0
B 점수: 5.0
판정: B
```
② 오류 입력 + ③ Ctrl+C
```
선택: 3
입력 오류: 1 또는 2를 입력하세요.
선택: 1
필터 A (3줄 입력, 공백 구분)
010
입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.
0 1 0
0 1
입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.
1 a 1
입력 형식 오류: 숫자만 입력하세요. (예: 0 1 0)
1 1 1
(Ctrl+C)
입력이 중단되어 프로그램을 종료합니다.
```

### U4 · 시간 측정과 성능 표
```
PS> python main.py   (입력은 U3 ①과 같음)
# [3] MAC 결과
A 점수: 1.0
B 점수: 5.0
연산 시간(평균/10회): 0.0025 ms
판정: B
# [4] 성능 분석 (평균/10회)
크기       평균 시간(ms)    연산 횟수(N²)
----------------------------------------
3×3             0.0021             9
```
- 시간 값은 컴퓨터와 실행 순간에 따라 조금씩 달라진다.

## 시행착오
### 1. push 실패 `remote: Repository not found`
- 문제: 첫 push가 "저장소를 찾을 수 없음"으로 실패했다.
- 원인: GitHub에 저장소를 만들기 전에 push했다. 주소 등록(`remote add`)은 됐지만 받을 곳이 없었다.
- 해결: GitHub에 Public 빈 저장소(체크 항목 비움)를 만든 뒤 `git push -u origin main`만 다시 실행했다. commit과 remote add는 이미 끝났으므로 다시 하지 않았다.

### 2. U2 커밋 전에 U3 코드가 덮어써짐
- 문제: U2를 커밋하기 전에 다음 단위 코드가 `main.py`에 들어가, U2 커밋에 U3 코드가 섞일 뻔했다.
- 원인: 다음 단위 파일을 이전 단위 커밋보다 먼저 썼다.
- 해결: 파일 지문(md5 해시)이 Clay가 실행한 U2 버전과 같은지 확인하며 되돌리고, U2를 커밋한 뒤 U3를 넣었다. 교훈: 단위마다 커밋을 먼저 끝낸다.

## 배운 점
- U1: 커밋은 내 PC 장부에 적는 것이고 push는 GitHub로 복사하는 것이다. 그래서 push가 실패해도 커밋은 남는다. `.gitignore`에 적은 파일은 `git add .`를 해도 올라가지 않는다.
- U2: 반복문 두 개가 겹치면 안쪽 줄이 n×n번 돈다. 0.1+0.2가 0.3이 아니어서 소수는 ==로 비교하면 안 된다.
- U3: 입력은 믿지 말고 검사한다. try/except로 오류를 잡으면 프로그램이 멈추지 않고 다시 물을 수 있다.
- U4: 시간은 잴 때마다 달라서 여러 번 재서 평균을 낸다. 사람 입력처럼 계산과 상관없는 구간은 빼고 잰다.

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
| 함수 (def) | 자주 하는 일을 이름 붙여 묶어 둔 것. 이름을 부르면 일을 하고 결과를 돌려준다(`return`) |
| 2차원 리스트 | 리스트 안에 리스트가 들어 있는 것. 바깥은 줄, 안쪽은 칸 |
| 인덱스 | 칸의 번호. 파이썬은 0부터 센다. `[1][2]`는 두 번째 줄의 세 번째 칸 |
| 절댓값 (abs) | 마이너스를 뗀 크기. `abs(-3)`은 3. 어느 쪽이 큰지와 상관없이 차이만 볼 때 쓴다 |
| float | 소수점이 있는 숫자 |
| while True | 멈추라고 할 때까지(`return`) 계속 도는 반복 |
| continue | 반복의 나머지를 건너뛰고 처음으로 돌아가는 명령 |
| try / except | 오류가 날 수 있는 일을 먼저 시도해 보고, 오류가 나면 멈추는 대신 except 쪽 처리를 한다 |
| split() | 글자 한 줄을 공백 기준으로 잘라 조각 리스트로 만든다 |
| strip() | 글자 앞뒤의 공백을 지운다 |
| Ctrl+C (KeyboardInterrupt) | 실행 중인 프로그램을 멈추라는 키. 파이썬에서는 KeyboardInterrupt라는 오류로 전달된다 |
| import | 파이썬에 기본으로 들어 있는 도구 상자(모듈)를 꺼내 쓰겠다는 선언 |
| ms (밀리초) | 1000분의 1초 |
| perf_counter | 아주 짧은 시간을 정밀하게 재는 파이썬의 스톱워치 |
| f-string 서식 (`:.4f`, `:<10`) | 숫자를 소수 몇째 자리까지, 몇 칸에 맞춰 보여 줄지 정하는 표시법 |
