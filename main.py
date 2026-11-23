"""Mini NPU Simulator (Mission 03)

그림을 숫자 표(2차원 리스트)로 바꾸고, 필터와 같은 칸끼리 곱해 모두 더한 점수(MAC 연산)로
십자가(Cross)인지 X인지 판정한다. 외부 라이브러리 없이 표준 기능만 쓴다.
"""

import json
import os
import sys
import time

# 두 점수의 차이가 이 값보다 작으면 같은 점수(동점)로 본다.
EPSILON = 1e-9

# 동점일 때 돌려주는 판정 값
UNDECIDED = "UNDECIDED"

# 시간을 잴 때 MAC 연산을 반복하는 횟수
REPEAT = 10

# data.json 위치: main.py와 같은 폴더 (어느 폴더에서 실행해도 찾을 수 있게)
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

# 성능 분석에 쓰는 크기 (명세: 3×3 포함, 5×5 / 13×13 / 25×25)
PERF_SIZES = [3, 5, 13, 25]

# 라벨 정규화 표: 여러 표기(소문자로 바꾼 뒤)를 표준 라벨 Cross / X로 통일한다
LABEL_MAP = {"+": "Cross", "cross": "Cross", "x": "X"}


# ---------------------------------------------------------------
# 1. 데이터 구조: n×n 2차원 리스트
# ---------------------------------------------------------------
def make_matrix(n, fill=0.0):
    """n×n 크기의 2차원 리스트를 만들고 모든 칸을 fill 값으로 채운다."""
    matrix = []
    for _ in range(n):
        row = []
        for _ in range(n):
            row.append(fill)
        matrix.append(row)
    return matrix


def set_value(matrix, row, col, value):
    """matrix의 (row, col) 칸에 value를 저장한다."""
    matrix[row][col] = value


def get_value(matrix, row, col):
    """matrix의 (row, col) 칸 값을 읽어 온다."""
    return matrix[row][col]


# ---------------------------------------------------------------
# 2. MAC 연산: 같은 칸끼리 곱하고(Multiply) 모두 더한다(Accumulate)
# ---------------------------------------------------------------
def mac(pattern, filter_matrix):
    """패턴과 필터의 MAC 점수를 반복문으로 직접 계산해 돌려준다."""
    n = len(pattern)
    score = 0.0
    for row in range(n):
        for col in range(n):
            score += pattern[row][col] * filter_matrix[row][col]
    return score


# ---------------------------------------------------------------
# 3. 점수 비교: 허용오차(EPSILON) 안이면 동점
# ---------------------------------------------------------------
def judge(score_a, score_b, label_a="A", label_b="B"):
    """두 점수를 비교해 더 큰 쪽의 라벨을, 차이가 EPSILON보다 작으면 UNDECIDED를 돌려준다."""
    if abs(score_a - score_b) < EPSILON:
        return UNDECIDED
    if score_a > score_b:
        return label_a
    return label_b


# ---------------------------------------------------------------
# 4. 성능 측정: MAC 연산만 REPEAT번 돌려 1회 평균 시간(ms)
# ---------------------------------------------------------------
def measure_mac_ms(pattern, filter_matrix, repeat=REPEAT):
    """입출력은 빼고 MAC 연산 호출 구간만 repeat번 재서 1회 평균(ms)을 돌려준다."""
    start = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filter_matrix)
    end = time.perf_counter()
    return (end - start) * 1000 / repeat


def print_performance_table(pairs):
    """(패턴, 필터) 쌍마다 평균 시간을 재서 크기·평균 시간·연산 횟수(N²) 표로 출력한다."""
    print("크기       평균 시간(ms)    연산 횟수(N²)")
    print("-" * 40)
    for pattern, filter_matrix in pairs:
        n = len(pattern)
        avg_ms = measure_mac_ms(pattern, filter_matrix)
        size_text = f"{n}×{n}"
        print(f"{size_text:<10}{avg_ms:>12.4f}{n * n:>14}")


# ---------------------------------------------------------------
# 5. 화면 출력 도우미
# ---------------------------------------------------------------
def print_header(title):
    """구역 제목을 줄로 감싸 출력한다."""
    print()
    print("#" + "-" * 40)
    print("# " + title)
    print("#" + "-" * 40)


def print_matrix(matrix):
    """표를 한 줄씩 공백으로 띄워 출력한다 (저장 확인용)."""
    for row in matrix:
        texts = []
        for value in row:
            texts.append(str(value))
        print("  " + " ".join(texts))


# ---------------------------------------------------------------
# 6. 모드 1 입력: 한 줄씩 받고, 형식이 틀리면 그 줄만 다시 받는다
# ---------------------------------------------------------------
def read_row(n):
    """숫자 n개가 공백으로 구분된 한 줄을 받아 소수 리스트로 돌려준다."""
    while True:
        parts = input().split()
        if len(parts) != n:
            print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
            continue
        values = []
        try:
            for part in parts:
                values.append(float(part))
        except ValueError:
            print("입력 형식 오류: 숫자만 입력하세요. (예: 0 1 0)")
            continue
        return values


def read_matrix(title, n=3):
    """n줄을 입력받아 n×n 표에 저장해 돌려준다."""
    print(f"{title} ({n}줄 입력, 공백 구분)")
    matrix = make_matrix(n)
    for row in range(n):
        values = read_row(n)
        for col in range(n):
            set_value(matrix, row, col, values[col])
    return matrix


# ---------------------------------------------------------------
# 7. 모드 2 준비: data.json 읽기, 키에서 크기 꺼내기, 검증, 라벨 정규화
# ---------------------------------------------------------------
def normalize_label(raw):
    """'+', 'cross', 'x' 같은 표기를 표준 라벨(Cross/X)로 바꾼다. 모르는 표기면 None."""
    key = str(raw).strip().lower()
    return LABEL_MAP.get(key)


def size_from_key(key):
    """'size_13' 또는 'size_13_2' 같은 키에서 크기 13을 꺼낸다. 형식이 다르면 None."""
    parts = str(key).split("_")
    if len(parts) >= 2 and parts[0] == "size" and parts[1].isdigit():
        return int(parts[1])
    return None


def check_matrix(matrix, n):
    """n×n 숫자 표인지 검사한다. 문제가 없으면 None, 있으면 이유를 글로 돌려준다."""
    if not isinstance(matrix, list) or len(matrix) != n:
        return f"행이 {n}개가 아님"
    for row in matrix:
        if not isinstance(row, list) or len(row) != n:
            return f"열이 {n}개가 아닌 줄이 있음"
        for value in row:
            if not isinstance(value, (int, float)):
                return f"숫자가 아닌 값이 있음 ({value!r})"
    return None


def load_data(path, name):
    """JSON 파일을 읽어 돌려준다. 파일이 없거나 형식이 깨졌으면 안내하고 None. name은 화면에 보일 이름."""
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"✗ {name}을(를) 찾을 수 없습니다. 파일 위치를 확인하세요.")
        return None
    except json.JSONDecodeError as error:
        print(f"✗ {name} 형식 오류: {error}")
        return None
    if not isinstance(data, dict) or not isinstance(data.get("filters"), dict) \
            or not isinstance(data.get("patterns"), dict):
        print(f"✗ {name}에 filters와 patterns가 모두 있어야 합니다.")
        return None
    return data


def load_filters(raw_filters):
    """크기별 필터를 검사해 {크기: {"Cross": 표, "X": 표}} 모양으로 정리한다."""
    filters = {}
    for size_key, group in raw_filters.items():
        n = size_from_key(size_key)
        if n is None or not isinstance(group, dict):
            print(f"✗ {size_key}: 키 형식이 size_N이 아니어서 건너뜀")
            continue
        loaded = {}
        for raw_label, matrix in group.items():
            label = normalize_label(raw_label)
            error = check_matrix(matrix, n)
            if label is None:
                print(f"✗ {size_key}.{raw_label}: 알 수 없는 필터 라벨이어서 건너뜀")
            elif error:
                print(f"✗ {size_key}.{raw_label}: {error}")
            else:
                loaded[label] = matrix
        if "Cross" in loaded and "X" in loaded:
            filters[n] = loaded
            print(f"✓ {size_key} 필터 로드 완료 (Cross, X)")
        else:
            print(f"✗ {size_key}: Cross·X 필터가 모두 있어야 해서 이 크기는 쓰지 않음")
    return filters


def prepare_case(key, entry, filters):
    """패턴 하나를 검사한다. 통과하면 (케이스 정보, None), 실패하면 (None, 실패 이유)."""
    n = size_from_key(key)
    if n is None:
        return None, "키 형식 오류 (size_N_번호 형식이 아님)"
    if n not in filters:
        return None, f"size_{n} 필터가 없음"
    if not isinstance(entry, dict) or "input" not in entry or "expected" not in entry:
        return None, "스키마 오류 (input 또는 expected 없음)"
    error = check_matrix(entry["input"], n)
    if error:
        return None, f"패턴 형식 오류: {error} (필터는 {n}×{n})"
    expected = normalize_label(entry["expected"])
    if expected is None:
        return None, f"라벨 오류: 표준 라벨로 바꿀 수 없는 expected 값 {entry['expected']!r}"
    case = {"n": n, "pattern": entry["input"], "expected": expected, "raw_expected": entry["expected"]}
    return case, None


def grade(result, expected):
    """판정과 정답(expected)을 비교해 (통과 여부, 실패 이유)를 돌려준다."""
    if result == expected:
        return True, ""
    if result == UNDECIDED:
        return False, "동점(UNDECIDED) 처리 규칙에 따라 FAIL"
    return False, f"판정 {result} ≠ expected {expected}"


def get_data_path():
    """실행할 때 파일 이름을 붙였으면 그 파일, 아니면 기본 data.json을 쓴다.
    예) python main.py tests/data_error.json  → 시험용 파일
    돌려주는 값: (읽을 경로, 화면에 보일 이름)"""
    if len(sys.argv) > 1:
        return sys.argv[1], sys.argv[1]
    return DATA_FILE, "data.json"


def run_mode2():
    """모드 2: 필터 로드 → 패턴 검증·판정·PASS/FAIL → 성능 분석 → 결과 요약."""
    path, name = get_data_path()
    print_header(f"[1] 필터 로드 ({name})")
    data = load_data(path, name)
    if data is None:
        return
    filters = load_filters(data["filters"])

    print_header("[2] 패턴 분석 (라벨 정규화 적용)")
    total = 0
    passed = 0
    failures = []                       # (케이스 이름, 실패 이유) 목록
    for key, entry in data["patterns"].items():
        total += 1
        print(f"--- {key} ---")
        case, reason = prepare_case(key, entry, filters)
        if case is None:                # 검증 단계에서 실패한 케이스
            print(f"FAIL ({reason})")
            failures.append((key, reason))
            continue
        pair = filters[case["n"]]
        cross_score = mac(case["pattern"], pair["Cross"])
        x_score = mac(case["pattern"], pair["X"])
        result = judge(cross_score, x_score, "Cross", "X")
        ok, reason = grade(result, case["expected"])
        print("Cross 점수:", cross_score)
        print("X 점수:", x_score)
        mark = "PASS" if ok else f"FAIL ({reason})"
        print(f"판정: {result} | expected: {case['expected']} | {mark}")
        if ok:
            passed += 1
        else:
            failures.append((key, reason))

    print_header(f"[3] 성능 분석 (평균/{REPEAT}회)")
    pairs = []
    for n in PERF_SIZES:                # 시간은 값이 아니라 칸 수에 달려 있으므로 같은 조건(모두 1.0)으로 비교
        pairs.append((make_matrix(n, 1.0), make_matrix(n, 1.0)))
    print_performance_table(pairs)

    print_header("[4] 결과 요약")
    print(f"총 테스트: {total}개")
    print(f"통과: {passed}개")
    print(f"실패: {len(failures)}개")
    if failures:
        print("실패 케이스:")
        for key, reason in failures:
            print(f"- {key}: {reason}")


# ---------------------------------------------------------------
# 8. 모드 선택과 실행
# ---------------------------------------------------------------
def choose_mode():
    """1 또는 2를 입력할 때까지 모드를 다시 묻는다."""
    while True:
        print()
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        choice = input("선택: ").strip()
        if choice == "1" or choice == "2":
            return choice
        print("입력 오류: 1 또는 2를 입력하세요.")


def run_mode1():
    """모드 1: 필터 A, B와 패턴을 입력받아 점수와 판정을 보여 준다."""
    print_header("[1] 필터 입력")
    filter_a = read_matrix("필터 A")
    print()
    filter_b = read_matrix("필터 B")

    print("\n저장된 필터 A:")
    print_matrix(filter_a)
    print("저장된 필터 B:")
    print_matrix(filter_b)

    print_header("[2] 패턴 입력")
    pattern = read_matrix("패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)
    result = judge(score_a, score_b, "A", "B")

    avg_ms = measure_mac_ms(pattern, filter_a)

    print_header("[3] MAC 결과")
    print("A 점수:", score_a)
    print("B 점수:", score_b)
    print(f"연산 시간(평균/{REPEAT}회): {avg_ms:.4f} ms")
    if result == UNDECIDED:
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print("판정:", result)

    print_header(f"[4] 성능 분석 (평균/{REPEAT}회)")
    print_performance_table([(pattern, filter_a)])


def main():
    print("=== Mini NPU Simulator ===")
    mode = choose_mode()
    if mode == "1":
        run_mode1()
    else:
        run_mode2()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")
