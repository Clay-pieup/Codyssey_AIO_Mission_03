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

### 9. 라벨 정규화는 표(딕셔너리) 하나로
- 맥락: `+`, `x`, `cross`처럼 같은 뜻의 표기가 섞여 있다.
- 결정: 공백 제거·소문자로 바꾼 뒤 `LABEL_MAP`에서 찾는다.
- 결과: 얻은 것: 대소문자·공백이 달라도 통일되고, 새 표기는 표에 한 줄만 더하면 된다. / 포기한 것: 표에 없는 표기는 자동으로 알아내지 못하고 FAIL로 남긴다(의도한 동작).

### 10. 오류는 케이스 단위 FAIL, 파일 오류는 안내 후 종료
- 맥락: 데이터 하나가 틀렸다고 전체가 멈추면 나머지 결과를 볼 수 없다.
- 결정: 패턴 문제는 그 케이스만 FAIL + 이유로 남기고 계속 진행한다. 파일 없음·JSON 깨짐은 안내 한 줄 후 모드 2를 끝낸다.
- 결과: 얻은 것: 프로그램이 비정상 종료하지 않는다. / 포기한 것: 검사 코드가 길어졌다.

### 11. data.json 위치를 main.py 기준으로
- 맥락: 평가자가 다른 폴더에서 실행할 수 있다.
- 결정: `__file__`로 main.py가 있는 폴더를 찾아 그 옆의 data.json을 읽는다.
- 결과: 얻은 것: 실행 위치와 상관없이 동작한다. / 포기한 것: 다른 위치의 데이터 파일은 지정할 수 없다.

### 12. PASS/FAIL 이유를 나눠 기록 (`grade`)
- 맥락: 실패가 '점수가 거의 같아서'인지 '반대로 판정해서'인지 알아야 원인을 고칠 수 있다.
- 결정: `grade()`가 판정과 expected를 비교하고, 실패 이유를 '동점(UNDECIDED)'과 '판정 ≠ expected' 두 가지로 돌려준다. 검증 단계 FAIL(U5)도 같은 실패 목록에 넣는다.
- 결과: 얻은 것: 결과 요약만 보고 수치 비교 문제인지, 로직·데이터 문제인지 구분할 수 있다. / 포기한 것: 없음.

### 13. 성능 표는 같은 조건(모두 1.0인 표)으로 측정
- 맥락: data.json에는 3×3이 없고, 시간은 값이 아니라 칸 수에 따라 달라진다.
- 결정: `PERF_SIZES = [3, 5, 13, 25]`마다 `make_matrix(n, 1.0)` 두 개로 잰다.
- 결과: 얻은 것: 네 크기를 공정하게 비교한다. / 포기한 것: 실제 data.json 패턴으로 잰 시간은 아니다.

### 14. 오류 시험은 별도 파일 + 실행 인자
- 맥락: 원본 data.json에는 오류 케이스가 없다. 오류 처리를 보여 주려고 원본을 고치면 안 된다.
- 결정: `tests/`에 오류 데이터 파일을 두고 `python main.py tests/data_error.json`처럼 실행할 때 파일을 고른다. 인자가 없으면 기본 data.json을 읽는다.
- 결과: 얻은 것: 원본은 그대로 두고, 누구나 명령 한 줄로 같은 시험을 재현한다. / 포기한 것: main.py에 `sys.argv` 몇 줄이 늘었다.

### 15. 실패 3개는 고치지 않고 분석한다
- 맥락: data.json 6개 중 3개가 동점(UNDECIDED)으로 FAIL이다. epsilon을 키우거나 줄이면 PASS로 바꿀 수도 있다.
- 결정: 데이터와 epsilon을 그대로 두고, 원인을 데이터 / 로직 / 수치 비교 순서로 진단해 README에 적는다.
- 결과: 얻은 것: 판정 기준이 정답에 맞춰 흔들리지 않고, 오차가 판정을 뒤집는 상황을 정직하게 보여 준다. / 포기한 것: 통과 수가 3/6에 머문다.

### 16. 패턴 생성기는 메뉴 3번, 공통 출력은 함수로
- 맥락: 생성한 패턴을 모드 1과 성능 분석에 다시 써야 하는데, 모드 1·2의 명세 흐름은 바꾸고 싶지 않다.
- 결정: 메뉴 3번으로 따로 둔다. 모드 1의 결과 출력은 `print_mac_result()`로 떼어 내 함께 쓰고, 성능 표는 `print_performance_table()`을 그대로 부른다. 크기는 3~51 사이 홀수만 받는다(가운데 줄이 하나여야 대칭).
- 결과: 얻은 것: 모드 1·2는 그대로이고, 새 기능은 같은 계산·출력·측정을 그대로 쓴다. / 포기한 것: 짝수 크기는 만들 수 없다. 모드 1 안에서 바로 고르는 방식은 아니다.

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

<details><summary>main.py · U5 data.json 로드·검증·라벨 정규화</summary>

**① 준비물과 라벨·키 처리**
```python
import json                                    # JSON 파일을 파이썬 사전·리스트로 바꿔 주는 표준 도구
import os                                      # 파일 경로를 다루는 표준 도구 (os.path만 사용)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
#   __file__ = 지금 실행 중인 main.py의 위치 → 그 폴더(dirname) → 거기에 "data.json"을 붙인 경로
LABEL_MAP = {"+": "Cross", "cross": "Cross", "x": "X"}   # 여러 표기 → 표준 라벨

def normalize_label(raw):
    key = str(raw).strip().lower()             # 글자로 바꾸고, 앞뒤 공백 지우고, 소문자로 ("X " → "x")
    return LABEL_MAP.get(key)                  # 표에서 찾는다. 없으면 None(= 모르는 라벨)

def size_from_key(key):
    parts = str(key).split("_")                # "size_13_2" → ["size", "13", "2"]
    if len(parts) >= 2 and parts[0] == "size" and parts[1].isdigit():   # 모양이 맞고 두 번째가 숫자면
        return int(parts[1])                   #   13을 숫자로 돌려준다
    return None                                # 아니면 None(= 키 형식 오류)
```

**② n×n 검사와 파일 읽기**
```python
def check_matrix(matrix, n):                   # n×n 숫자 표인지 검사, 문제 없으면 None
    if not isinstance(matrix, list) or len(matrix) != n:      # 리스트가 아니거나 행이 n개가 아니면
        return f"행이 {n}개가 아님"
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:        # 어느 줄이든 칸이 n개가 아니면
            return f"열이 {n}개가 아닌 줄이 있음"
        for value in row:
            if not isinstance(value, (int, float)):           # 숫자가 아닌 값이 섞였으면
                return f"숫자가 아닌 값이 있음 ({value!r})"
    return None

def load_data(path):
    try:
        with open(path, encoding="utf-8") as file:   # 읽기 전용으로 열고, 다 쓰면 자동으로 닫는다
            data = json.load(file)                     # JSON → 파이썬 사전
    except FileNotFoundError:                          # 파일이 없으면
        print("✗ data.json을 찾을 수 없습니다 …"); return None
    except json.JSONDecodeError as error:              # JSON 문법이 깨졌으면
        print(f"✗ data.json 형식 오류: {error}"); return None
    … filters·patterns가 사전(dict)으로 들어 있는지 확인 …
    return data
```

**③ 필터 정리와 케이스 검사**
- `load_filters()`: `size_5`에서 5를 꺼낸 뒤, 그 안의 `cross`·`x`를 정규화해 Cross·X로 저장한다. 둘 다 있어야 그 크기를 쓴다. 결과는 `{5: {"Cross": 표, "X": 표}, 13: …, 25: …}`.
- `prepare_case(key, entry, filters)`: 키 형식 → 그 크기 필터가 있는지 → `input`·`expected`가 있는지 → n×n 숫자 표인지 → 라벨을 바꿀 수 있는지 순서로 검사한다. 실패하면 그 자리에서 이유를 돌려주고, 통과하면 `{"n", "pattern", "expected"(표준 라벨), "raw_expected"(원래 표기)}`를 돌려준다.
- `run_mode2()`: [1] 필터 로드 → [2] 패턴마다 검사 결과 출력. (점수·PASS/FAIL·성능 표·요약은 U6)
- 파일은 읽기만 한다(`open`에 `'w'`가 없음). 그래서 시험 차단 목록에 걸리지 않는다.

</details>

<details><summary>main.py · U6 판정·PASS/FAIL·성능 표·결과 요약</summary>

**① PASS/FAIL 판단**
```python
def grade(result, expected):
    if result == expected:                         # 판정이 정답과 같으면
        return True, ""                            #   통과, 이유 없음
    if result == UNDECIDED:                        # 동점이라 판정을 못 했으면
        return False, "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
    return False, f"판정 {result} ≠ expected {expected}"   # 반대로 판정했으면
```
- 비교하는 두 값은 모두 표준 라벨이다: `judge()` 결과(Cross/X/UNDECIDED)와 정규화된 expected(Cross/X).

**② `run_mode2()` [2] 패턴 분석**
```python
total = 0; passed = 0; failures = []               # 셀 통 3개: 전체 수, 통과 수, 실패 목록
for key, entry in data["patterns"].items():        # 케이스마다
    total += 1
    case, reason = prepare_case(key, entry, filters)   # U5 검사
    if case is None:                               # 검사에서 떨어지면
        print(f"FAIL ({reason})"); failures.append((key, reason)); continue
    pair = filters[case["n"]]                      # 크기에 맞는 Cross·X 필터 한 쌍
    cross_score = mac(case["pattern"], pair["Cross"])   # Cross 필터 점수
    x_score = mac(case["pattern"], pair["X"])           # X 필터 점수
    result = judge(cross_score, x_score, "Cross", "X")  # U2 판정 (epsilon)
    ok, reason = grade(result, case["expected"])        # 정답과 비교
    … 점수 2줄, "판정 | expected | PASS 또는 FAIL(이유)" 출력 …
    통과면 passed += 1, 아니면 failures에 (이름, 이유) 추가
```

**③ [3] 성능 분석과 [4] 결과 요약**
- [3]: `PERF_SIZES`(3·5·13·25)마다 `make_matrix(n, 1.0)` 두 개를 만들어 U4의 `print_performance_table()`에 넘긴다.
- [4]: 총·통과·실패 수를 출력하고, 실패 목록을 `- 이름: 이유`로 한 줄씩 출력한다.

</details>

<details><summary>main.py · U7 실행 인자로 파일 고르기</summary>

```python
import sys                                     # 실행할 때 붙인 글자(인자)를 읽는 표준 도구

def get_data_path():
    if len(sys.argv) > 1:                      # sys.argv = ["main.py", "tests/data_error.json"] 처럼 들어온다
        return sys.argv[1], sys.argv[1]        #   파일 이름을 붙였으면 그 파일 (경로, 화면 이름)
    return DATA_FILE, "data.json"              # 안 붙였으면 기본 data.json

def run_mode2():
    path, name = get_data_path()               # 읽을 파일 정하기
    print_header(f"[1] 필터 로드 ({name})")    # 어느 파일인지 제목에 표시
    data = load_data(path, name)               # 오류 문구에 실제 파일 이름(name)을 넣는다
```
- `sys`는 시험 차단 목록에 없다. 사용하는 도구는 `json`·`os`·`sys`·`time` 4개로, 모두 파이썬 표준 라이브러리다.

**시험 파일 구성 (`tests/data_error.json`, 원본의 size_5 필터 사용)**
| 케이스 | 넣은 오류 | 결과 |
|---|---|---|
| size_5_ok | 없음 (정상 십자가) | PASS |
| size_5_label | expected `' CROSS '` (대문자·공백) | 정규화돼 PASS |
| size_5_row | 행 4개 | FAIL: 행이 5개가 아님 |
| size_5_col | 마지막 줄 4칸 | FAIL: 열이 5개가 아닌 줄이 있음 |
| size_5_text | 숫자 자리에 `"a"` | FAIL: 숫자가 아닌 값 |
| size_5_big | 5×5 키에 13×13 패턴 (크기 불일치) | FAIL: 행이 5개가 아님 |
| size_5_badlabel | expected `"o"` | FAIL: 라벨 오류 |
| size_5_noexp | expected 없음 | FAIL: 스키마 오류 |
| size_7_1 | 7×7 필터 없음 | FAIL: size_7 필터가 없음 |
| pattern_5_1 | 키가 size_로 시작하지 않음 | FAIL: 키 형식 오류 |
| (필터) size_9 | cross만 있고 x 없음 | 필터 로드에서 건너뜀 |

`tests/data_broken.json`은 JSON 문법이 중간에 끊긴 파일이다.

</details>

<details><summary>main.py · U9 패턴 생성기</summary>

**① 모양 만들기**
```python
def make_cross_pattern(n):
    pattern = make_matrix(n)                 # U2 함수: 0.0으로 채운 N×N 표
    mid = n // 2                             # 가운데 번호 (5면 2, 0부터 셈)
    for row in range(n):
        for col in range(n):
            if row == mid or col == mid:     # 가운데 행이거나 가운데 열이면
                set_value(pattern, row, col, 1.0)   # 1.0으로 칠한다
    return pattern

def make_x_pattern(n):
    pattern = make_matrix(n)
    for row in range(n):
        for col in range(n):
            if row == col or row + col == n - 1:    # ↘ 대각선(행=열) 또는 ↙ 대각선(행+열=N−1)
                set_value(pattern, row, col, 1.0)
    return pattern
```
- `//`는 나눈 몫만 남기는 나눗셈이다(5 // 2 = 2).
- ↙ 대각선 예(5×5): (0,4), (1,3), (2,2), (3,1), (4,0) → 모두 행+열 = 4 = N−1.
- 생성된 3×3 Cross·X는 명세 1장의 예시 그림과 같다.

**② 크기 입력과 모드 3 흐름**
```python
def read_size():                             # 크기 N 입력 (틀리면 다시 묻기, U3 read_row와 같은 방식)
    text = input(…).strip()
    if not text.isdigit(): → "숫자만 입력하세요"
    n = int(text)
    if n < 3 or n > 51 or n % 2 == 0: → "3~51 사이의 홀수를 입력하세요"   # % 2 == 0 은 '짝수'

def run_mode3():
    n = read_size()                          # [1] 크기 입력
    cross = make_cross_pattern(n); x = make_x_pattern(n)   # [2] 생성 (25×25까지만 그림 출력)
    for name, pattern in (("Cross 패턴", cross), ("X 패턴", x)):   # [3] 두 모양을 하나씩 입력으로
        score_a = mac(pattern, cross)        #   필터 A = 생성한 Cross
        score_b = mac(pattern, x)            #   필터 B = 생성한 X
        result = judge(score_a, score_b, "A", "B")
        print_mac_result(…)                  #   모드 1과 같은 출력 함수
    print_performance_table([3×3 생성 패턴, N×N 생성 패턴])   # [4] 성능 분석
```
- 결과는 항상 Cross 입력이 A(2N−1점 대 1점), X 입력이 B(1점 대 2N−1점)다. 두 모양이 가운데 칸 하나만 공유하기 때문이다.
- `print_mac_result()`: 모드 1에 있던 점수·시간·판정 출력을 함수로 떼어 낸 것(리팩터링). 모드 1 화면은 그대로다.

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

### U5 · data.json 로드·검증·라벨 정규화
```
PS> python main.py
선택: 2
# [1] 필터 로드
✓ size_5 필터 로드 완료 (Cross, X)
✓ size_13 필터 로드 완료 (Cross, X)
✓ size_25 필터 로드 완료 (Cross, X)
# [2] 패턴 검증 (라벨 정규화 적용)
--- size_5_1 --- 5×5 · 필터 size_5 선택 · expected 'x' → X · 검증 OK
--- size_5_2 --- 5×5 · 필터 size_5 선택 · expected '+' → Cross · 검증 OK
--- size_13_1 --- 13×13 · 필터 size_13 선택 · expected 'x' → X · 검증 OK
--- size_13_2 --- 13×13 · 필터 size_13 선택 · expected '+' → Cross · 검증 OK
--- size_25_1 --- 25×25 · 필터 size_25 선택 · expected 'x' → X · 검증 OK
--- size_25_2 --- 25×25 · 필터 size_25 선택 · expected '+' → Cross · 검증 OK
```
의도적 오류 시험 (AI가 data.json **사본**으로 시험, 원본은 그대로. Clay 재현은 U7)

| 넣은 오류 | 출력 |
|---|---|
| 5×5 키에 13×13 패턴 | `검증 FAIL: 패턴 형식 오류: 행이 5개가 아님 (필터는 5×5)` |
| 한 줄만 4칸 | `검증 FAIL: 패턴 형식 오류: 열이 5개가 아닌 줄이 있음` |
| 숫자 자리에 `'a'` | `검증 FAIL: 패턴 형식 오류: 숫자가 아닌 값이 있음 ('a')` |
| expected `'circle'` | `검증 FAIL: 라벨 오류: 표준 라벨로 바꿀 수 없는 expected 값 'circle'` |
| 키 `big_5_1` | `검증 FAIL: 키 형식 오류 (size_N_번호 형식이 아님)` |
| expected 없음 | `검증 FAIL: 스키마 오류 (input 또는 expected 없음)` |
| `size_7_1` (7×7 필터 없음) | `검증 FAIL: size_7 필터가 없음` |
| expected `' Cross '` | `→ Cross · 검증 OK` (정규화 성공) |
| 필터 size_9에 cross만 있음 | `✗ size_9: Cross·X 필터가 모두 있어야 해서 이 크기는 쓰지 않음` |
| 파일 없음 / JSON 깨짐 / filters 키 없음 | 각각 안내 한 줄 후 모드 2 종료 (Traceback 없음) |

### U6 · 판정·PASS/FAIL·성능 표·결과 요약
```
PS> python main.py
선택: 2
# [1] 필터 로드
✓ size_5 필터 로드 완료 (Cross, X)
✓ size_13 필터 로드 완료 (Cross, X)
✓ size_25 필터 로드 완료 (Cross, X)
# [2] 패턴 분석 (라벨 정규화 적용)
--- size_5_1 ---
Cross 점수: 0.9
X 점수: 0.8999999999999999
판정: UNDECIDED | expected: X | FAIL (동점(UNDECIDED) 처리 규칙에 따라 FAIL)
--- size_5_2 ---
Cross 점수: 8.9
X 점수: 0.1
판정: Cross | expected: Cross | PASS
--- size_13_1 ---
Cross 점수: 0.3
X 점수: 14.700000000000008
판정: X | expected: X | PASS
--- size_13_2 ---
Cross 점수: 7.499999999999997
X 점수: 7.5
판정: UNDECIDED | expected: Cross | FAIL (동점(UNDECIDED) 처리 규칙에 따라 FAIL)
--- size_25_1 ---
Cross 점수: 4.9
X 점수: 4.899999999999999
판정: UNDECIDED | expected: X | FAIL (동점(UNDECIDED) 처리 규칙에 따라 FAIL)
--- size_25_2 ---
Cross 점수: 52.9
X 점수: 0.1
판정: Cross | expected: Cross | PASS
# [3] 성능 분석 (평균/10회)
크기       평균 시간(ms)    연산 횟수(N²)
----------------------------------------
3×3             0.0014             9
5×5             0.0022            25
13×13           0.0101           169
25×25           0.0253           625
# [4] 결과 요약
총 테스트: 6개
통과: 3개
실패: 3개
실패 케이스:
- size_5_1: 동점(UNDECIDED) 처리 규칙에 따라 FAIL
- size_13_2: 동점(UNDECIDED) 처리 규칙에 따라 FAIL
- size_25_1: 동점(UNDECIDED) 처리 규칙에 따라 FAIL
```
- VS Code 터미널을 스크롤하면 같은 블록이 겹쳐 보일 수 있다(화면 표시 문제). 실제 출력은 위와 같이 케이스마다 한 번씩이다.
- 칸 수는 9 → 625로 약 69배, 시간은 0.0014 → 0.0253 ms로 약 18배 늘었다.

### U7 · 재현성 검증
| # | 명령 (입력) | 결과 | 확인 |
|---|---|---|---|
| ① | `python main.py` (`1` + 명세 예시 9줄) | A 1.0 / B 5.0 / 연산 시간 0.0007 ms / 판정 B / 3×3 표 0.0008 ms·9 | 모드 1 정상 |
| ② | `python main.py` (`2`) | 케이스 6개 중 PASS 3·FAIL 3, 요약 총 6 / 통과 3 / 실패 3 | 합계 일치 |
| ③ | `python main.py tests/data_error.json` (`2`) | 아래 출력 | 오류 케이스만 FAIL, 끝까지 진행 |
| ④ | `python main.py tests/data_broken.json` (`2`) | `✗ tests/data_broken.json 형식 오류: Expecting value: line 4 column 1 (char 39)` | 안내 후 종료 |
| ⑤ | `python main.py tests/none.json` (`2`) | `✗ tests/none.json을(를) 찾을 수 없습니다. 파일 위치를 확인하세요.` | 안내 후 종료 |
| ⑥ | `Select-String -Path main.py -Pattern "^import"` | `import json` / `import os` / `import sys` / `import time` | 표준 라이브러리만 |

③ 출력 (주요 부분)
```
# [1] 필터 로드 (tests/data_error.json)
✓ size_5 필터 로드 완료 (Cross, X)
✗ size_9: Cross·X 필터가 모두 있어야 해서 이 크기는 쓰지 않음
# [2] 패턴 분석 (라벨 정규화 적용)
--- size_5_ok ---        … 판정: Cross | expected: Cross | PASS
--- size_5_label ---     … 판정: Cross | expected: Cross | PASS
--- size_5_row ---       FAIL (패턴 형식 오류: 행이 5개가 아님 (필터는 5×5))
--- size_5_col ---       FAIL (패턴 형식 오류: 열이 5개가 아닌 줄이 있음 (필터는 5×5))
--- size_5_text ---      FAIL (패턴 형식 오류: 숫자가 아닌 값이 있음 ('a') (필터는 5×5))
--- size_5_big ---       FAIL (패턴 형식 오류: 행이 5개가 아님 (필터는 5×5))
--- size_5_badlabel ---  FAIL (라벨 오류: 표준 라벨로 바꿀 수 없는 expected 값 'o')
--- size_5_noexp ---     FAIL (스키마 오류 (input 또는 expected 없음))
--- size_7_1 ---         FAIL (size_7 필터가 없음)
--- pattern_5_1 ---      FAIL (키 형식 오류 (size_N_번호 형식이 아님))
# [4] 결과 요약
총 테스트: 10개
통과: 2개
실패: 8개
```
- 모드 1 오류 입력(열 수·숫자 오류 → 재입력, Ctrl+C 안전 종료)은 U3 수행 로그에 있다.
- Python 3.8 문법 검사: 코드를 3.8 문법 기준으로 해석해 통과 (AI 확인). 실행 환경은 Python 3.14.7.
- ②의 성능 표에서 3×3(0.0026 ms)이 5×5(0.0021 ms)보다 느리게 나왔다. 아주 짧은 계산은 측정 오차가 크다는 예다.

### U8 · 결과 리포트와 보안 점검
- 결과 리포트: README `## 결과 리포트`에 실패 원인 분석 + 시간 복잡도 분석 작성 (빈 줄 빼고 21줄). README 전체는 99줄.

| 점검 항목 | 결과 |
|---|---|
| 저장소에 올라가는 파일 | `.gitignore`, `LEARNING.md`, `README.md`, `data.json`, `main.py`, `tests/data_broken.json`, `tests/data_error.json` 7개 |
| 이메일·토큰·비밀번호·API 키·전화번호·내 PC 경로 | 없음 (`.gitignore`의 설명 주석 한 줄만 검색됨) |
| 명세 PDF·md | 저장소 안에 없음 |
| 커밋 9개에 CLAUDE.md·명세가 들어간 적 | 없음 |
| 커밋 작성자 이메일 | GitHub noreply 주소만 사용 |

### U9 · 패턴 생성기
| # | 실행 (입력) | 결과 |
|---|---|---|
| ① | `python main.py` (`3` → `4` → `1` → `abc` → `5`) | `4`·`1` → "3~51 사이의 홀수", `abc` → "숫자만" 안내 후 재입력 / 5×5 Cross·X 그림 / Cross 입력 A 9.0·B 1.0·판정 A, X 입력 A 1.0·B 9.0·판정 B / 성능 표 3×3 0.0011 ms·9, 5×5 0.0028 ms·25 |
| ② | `python main.py` (`3` → `51`) | 그림 생략 안내 / Cross 입력 A 101.0·B 1.0·판정 A, X 입력 A 1.0·B 101.0·판정 B / 성능 표 3×3 0.0006 ms·9, 51×51 0.0880 ms·2601 |
| ③ | `python main.py` (`4` → `1` → 명세 예시) | "1, 2, 3 중에서 입력하세요" 후 모드 1 결과 그대로 (A 1.0 / B 5.0 / 판정 B) |
- 3×3 → 51×51: 연산 289배, 시간 약 147배. 크기가 클수록 시간 증가가 N²에 가까워진다.

## 시행착오
### 1. push 실패 `remote: Repository not found`
- 문제: 첫 push가 "저장소를 찾을 수 없음"으로 실패했다.
- 원인: GitHub에 저장소를 만들기 전에 push했다. 주소 등록(`remote add`)은 됐지만 받을 곳이 없었다.
- 해결: GitHub에 Public 빈 저장소(체크 항목 비움)를 만든 뒤 `git push -u origin main`만 다시 실행했다. commit과 remote add는 이미 끝났으므로 다시 하지 않았다.

### 2. U2 커밋 전에 U3 코드가 덮어써짐
- 문제: U2를 커밋하기 전에 다음 단위 코드가 `main.py`에 들어가, U2 커밋에 U3 코드가 섞일 뻔했다.
- 원인: 다음 단위 파일을 이전 단위 커밋보다 먼저 썼다.
- 해결: 파일 지문(md5 해시)이 Clay가 실행한 U2 버전과 같은지 확인하며 되돌리고, U2를 커밋한 뒤 U3를 넣었다. 교훈: 단위마다 커밋을 먼저 끝낸다.

### 3. U4 문서가 커밋에서 빠짐
- 문제: U4 커밋 `8ea9eba`에 main.py만 들어가고 README·LEARNING이 빠졌다.
- 원인: 판정 메시지에 커밋 명령을 같이 보여 줘서, 문서를 반영하기 전에 `git add`가 실행됐다.
- 해결: 두 문서를 따로 커밋했다(`9a5f416`). 이후 커밋 명령은 문서 반영이 끝난 뒤에만 안내한다.

### 4. PC에 다듬기 전 파일이 들어감
- 문제: U5 코드를 넣은 뒤 오류 문구를 다듬었는데, Clay PC에는 다듬기 전 파일이 들어가 있었다.
- 원인: 파일을 옮긴 뒤 PC 쪽 파일이 같은지 확인하지 않았다.
- 해결: U5 커밋 전에 해시를 비교해 차이를 찾고, 다듬은 버전으로 다시 넣은 뒤 해시가 같은 것을 확인했다. 이후에는 파일을 넣을 때마다 해시를 확인한다.
- 재발(U9): 다듬기 직전 파일이 또 들어갔지만, 넣은 직후 해시 비교로 바로 찾아 다시 넣었다. 확인 절차가 실제로 효과가 있었다.

## 배운 점
- U1: 커밋은 내 PC 장부에 적는 것이고 push는 GitHub로 복사하는 것이다. 그래서 push가 실패해도 커밋은 남는다. `.gitignore`에 적은 파일은 `git add .`를 해도 올라가지 않는다.
- U2: 반복문 두 개가 겹치면 안쪽 줄이 n×n번 돈다. 0.1+0.2가 0.3이 아니어서 소수는 ==로 비교하면 안 된다.
- U3: 입력은 믿지 말고 검사한다. try/except로 오류를 잡으면 프로그램이 멈추지 않고 다시 물을 수 있다.
- U4: 시간은 잴 때마다 달라서 여러 번 재서 평균을 낸다. 사람 입력처럼 계산과 상관없는 구간은 빼고 잰다.
- U5: 데이터는 약속(스키마)대로 왔는지 먼저 검사한다. 같은 뜻의 다른 표기는 한 표로 모아 통일하면 관리가 쉽다.
- U6: 실패 이유를 종류별로 나눠 적으면 원인 진단이 쉬워진다. 칸 수가 69배 늘 때 시간은 약 18배 늘었다. 작은 표에서는 고정 비용이 섞이기 때문이다.
- U7: 재현성은 다른 사람이 같은 명령으로 같은 결과를 얻는 것이다. 시험용 데이터를 따로 두면 원본을 건드리지 않고 오류 처리를 보여 줄 수 있다. 아주 짧은 계산은 측정 오차가 커서 작은 크기가 더 느리게 나오기도 한다.
- U8: 실패를 없애는 것보다 왜 실패했는지 설명하는 것이 더 중요할 때가 있다. 원인은 가능성을 하나씩 지워 가며 찾는다.
- U9: 공통 부분을 함수로 떼어 내면 새 기능도 같은 출력과 측정을 그대로 쓸 수 있다. 크기가 클수록 시간 증가가 N²에 가까워진다(3→51: 연산 289배, 시간 약 147배).

### 과제 목표, 내 말로
1. **MAC 연산이 무엇이고 왜 중요한가**: 같은 자리 숫자끼리 곱해서 모두 더하는 계산이다. AI가 그림을 알아볼 때 이 계산을 수억 번 하기 때문에, 이걸 빨리 하는 칩(NPU)이 따로 생겼다.
2. **곱하고 더해 유사도를 계산하는 원리**: 모양이 겹치는 칸만 점수가 쌓이므로 점수는 '얼마나 겹치는가'를 숫자로 나타낸 것이다. 십자가 입력은 십자가 필터와 5칸, X 필터와 1칸 겹쳐 5점 대 1점이 된다.
3. **키·라벨 규칙과 정규화가 필요한 이유**: 키 size_13_2에서 가운데 13이 크기라서 size_13 필터를 쓴다. 정답 표기가 +, x, cross처럼 섞여 있어 Cross·X 두 이름으로 통일해야 비교가 틀리지 않는다.
4. **부동소수점 오차와 epsilon**: 컴퓨터는 0.1을 정확히 저장 못 해서 0.9가 0.8999…가 된다. ==로 비교하면 이 작은 오차로 승패가 갈리니, 차이가 1e-9보다 작으면 동점으로 본다.
5. **O(N²)의 근거**: 한 변이 2배가 되면 칸 수가 4배라 계산도 4배가 된다. 표의 연산 횟수(9→625)와 시간이 함께 커지는 것으로 확인했다.
6. **실패 원인 진단**: 데이터 검증 통과 → 데이터 문제 아님, 같은 코드로 다른 케이스는 PASS → 로직 문제 아님, 두 점수 차이가 거의 0 → 수치 비교 문제. 이렇게 하나씩 지워 나갔다.

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
| JSON | 사람도 컴퓨터도 읽기 쉬운 데이터 기록 형식. `{"이름": 값}` 모양 |
| 딕셔너리 (dict) | "이름표 → 값"으로 짝지어 저장하는 상자. `LABEL_MAP["+"]`는 `"Cross"` |
| None | "아무것도 없음"을 뜻하는 값. 여기서는 "찾지 못함·문제없음" 신호로 쓴다 |
| isinstance | "이 값이 리스트(또는 숫자)가 맞니?" 하고 종류를 확인하는 함수 |
| with open(...) | 파일을 열고, 쓰임이 끝나면 자동으로 닫아 주는 안전한 방식 |
| 스키마 검증 | 데이터가 약속한 모양(키 이름, 칸 수, 값 종류)을 지키는지 확인하는 일 |
| PASS / FAIL | 프로그램의 판정이 정답(expected)과 같으면 통과, 다르면 실패 |
| 집계 | 여러 결과를 세어 합계를 내는 일 (총·통과·실패 수) |
| 튜플 | 값 여러 개를 괄호로 묶은 한 묶음. 실패 목록에 `(이름, 이유)`를 함께 넣을 때 쓴다 |
| 실행 인자 (sys.argv) | 프로그램 이름 뒤에 붙여 주는 추가 정보. `python main.py tests/data_error.json`에서 `tests/data_error.json` |
| 재현성 | 다른 사람이 같은 명령을 실행해도 같은 결과가 나오는 성질 |
| Select-String | PowerShell에서 파일 안의 특정 글자가 있는 줄을 찾아 주는 명령 |
| 고정 비용 (오버헤드) | 계산 크기와 상관없이 매번 드는 기본 비용(함수 호출, 시간 재기 등). 작은 계산일수록 비중이 커진다 |
| `//` (몫 나눗셈) | 나눈 결과에서 소수점 아래를 버리고 몫만 남긴다. 7 // 2 = 3 |
| `%` (나머지) | 나누고 남은 수. `n % 2 == 0`이면 짝수 |
| 대각선 | 표의 한 모서리에서 반대쪽 모서리로 이어지는 비스듬한 줄 |
| 리팩터링 | 결과는 그대로 두고 코드 구조만 정리하는 일 |
