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


if __name__ == "__main__":
    # U2 확인용 예시 (U3에서 메뉴 화면으로 바뀐다)
    cross = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
    x = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]

    grid = make_matrix(3)
    set_value(grid, 1, 2, 7.5)
    print("make_matrix(3) 후 (1, 2) 칸에 7.5 저장:", grid)
    print("(1, 2) 칸 읽기:", get_value(grid, 1, 2))

    cross_score = mac(cross, cross)
    x_score = mac(cross, x)
    print("십자가 입력 × 십자가 필터 =", cross_score)
    print("십자가 입력 × X 필터 =", x_score)
    print("판정:", judge(cross_score, x_score, "Cross", "X"))

    print("0.1 + 0.2 =", 0.1 + 0.2)
    print("0.9 == 0.8999999999999999 ?", 0.9 == 0.8999999999999999)
    print("0.9 vs 0.8999999999999999 판정:", judge(0.9, 0.8999999999999999))
