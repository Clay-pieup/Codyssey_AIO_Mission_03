"""Mini NPU Simulator (Mission 03)

그림을 숫자 표(2차원 리스트)로 바꾸고, 필터와 같은 칸끼리 곱해 모두 더한 점수(MAC 연산)로
십자가(Cross)인지 X인지 판정한다. 외부 라이브러리 없이 표준 기능만 쓴다.
"""

# 두 점수의 차이가 이 값보다 작으면 같은 점수(동점)로 본다.
EPSILON = 1e-9

# 동점일 때 돌려주는 판정 값
UNDECIDED = "UNDECIDED"


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
# 4. 화면 출력 도우미
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
# 5. 모드 1 입력: 한 줄씩 받고, 형식이 틀리면 그 줄만 다시 받는다
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
# 6. 모드 선택과 실행
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

    print_header("[3] MAC 결과")
    print("A 점수:", score_a)
    print("B 점수:", score_b)
    if result == UNDECIDED:
        print(f"판정: 판정 불가 (|A-B| < {EPSILON})")
    else:
        print("판정:", result)


def main():
    print("=== Mini NPU Simulator ===")
    mode = choose_mode()
    if mode == "1":
        run_mode1()
    else:
        print("data.json 분석은 U5에서 구현합니다.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")
