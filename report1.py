# 1. 행렬 입력 기능
def inputMatrix():
    # 사용자로부터 정수 n을 받아 n x n 크기의 정방행렬을 행 단뒤로 입력받을 수 있어야 함
    while True:
            n = int(input("정방행렬의 차수를 입력하세요: "))
            if n > 0:
                break
            print("양의 정수를 입력하세요.")

    # 데이터를 입력 받아 2차원 배열에 저장
    matrix = []
    for i in range(n):
        while True:
            row = list(map(int, input(f"{i + 1}행: ").split()))
            if len(row) != n:
                print(f"{n}개의 수를 입력하세요.")
                continue
            matrix.append(row)
            break
    return matrix

# 소행렬 구하는 함수
def getMinor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i] + m[i+1:])]

# 행렬식 구하는 함수
def getDeterminant(m):
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0]*m[1][1] - m[1][0]*m[0][1]

    det = 0
    for c in range(len(m)):
        det += ((-1) ** c) * m[0][c] * getDeterminant(getMinor(m, 0, c))
    return det

# 전치 행렬을 구하는 함수
def getTransposeMatrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

# ===== 2. 행렬식을 이용한 역행렬 계산 =====
def getInverseMatrixByDeterminant(matrix):
    n = len(matrix)
    det = getDeterminant(matrix)

    # 역행렬이 존재하지 않을 경우(행렬식이 0인 경우) 오류 메시지를 출력
    if abs(det) < 1e-10:
        raise ValueError("역행렬이 존재하지 않습니다.")

    if n == 1:
        return [[1/det]]

    cofactors = [[(-1) ** (i + j) * getDeterminant(getMinor(matrix, i, j)) for j in range(n)] for i in range(n)]

    inverse = getTransposeMatrix(cofactors)

    for i in range(len(inverse)):
        for j in range(len(inverse)):
            inverse[i][j] = inverse[i][j] / det

    return inverse

# ===== 3. 가우스–조던 소거법을 이용한 역행렬 계산 =====
def getInverseMatrixByGaussJordanElimination(matrix):
    n = len(matrix)
    matrix = [row[:] for row in matrix]
    inverse = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    for col in range(n):
        if abs(matrix[col][col]) < 1e-10:
            newPivot = None

            for row in range(col + 1, n):
                if abs(matrix[row][col]) >= 1e-10:
                    newPivot = row
                    break

            # 역행렬이 존재하지 않은 경우 오류 발생
            if newPivot is None:
                raise ValueError("역행렬이 존재하지 않습니다.")

            matrix[col], matrix[newPivot] = matrix[newPivot], matrix[col]
            inverse[col], inverse[newPivot] = inverse[newPivot], inverse[col]
        pivot = matrix[col][col]

        for j in range(n):
            matrix[col][j] /= pivot
            inverse[col][j] /= pivot

        for row in range(n):
            if row == col:
                continue

            elem = matrix[row][col]

            for j in range(n):
                matrix[row][j] -= elem * matrix[col][j]
                inverse[row][j] -= elem * inverse[col][j]

    return inverse

# ===== 4. 결과 출력 및 비교 =====
# 결과 출력
def printMatrix(matrix):
    for row in matrix:
        print(" ".join(f"{value:.6f}" for value in row))

# 결과 비교
def compareMatrix(m1, m2):
    if len(m1) == len(m2) and len(m1[0]) == len(m2[0]):
        for i in range(len(m1)):
            for j in range(len(m1[0])):
                if abs(m1[i][j] - m2[i][j]) > 1e-10:
                    return False
        return True
    return False

# ===== 5. 추가기능: 행렬 덧셈 및 곱셈 연산 =====
def addMatrix(m1, m2):
    matrix = []
    if len(m1) == len(m2) and len(m1[0]) == len(m2[0]):
        matrix = [[m1[i][j] + m2[i][j] for j in range(len(m1[0]))] for i in range(len(m1))]
    return matrix

def multiplyMatrix(m1, m2):
    rows = len(m1)
    cols = len(m2[0])
    mid = len(m2)
    matrix = []
    if len(m1[0]) == len(m2):
        matrix = [[sum(m1[i][k] * m2[k][j] for k in range(mid)) for j in range(cols)] for i in range(rows)]

    return matrix

# ===== 메인 함수 =====
def main():
    matrix = inputMatrix()
    print("행렬식으로 구한 역행렬: ", end='')
    printMatrix(getInverseMatrixByDeterminant(matrix))
    print("가우스-조던 소거법으로 구한 역행렬: ", end='')
    printMatrix(getInverseMatrixByGaussJordanElimination(matrix))

    if (compareMatrix(getInverseMatrixByGaussJordanElimination(matrix), getInverseMatrixByDeterminant(matrix))):
        print("두 방법의 결과가 동일합니다.")

    print("===== 추가 기능: 행렬의 덧셈과 곱셈 =====")
    matrix1 = inputMatrix()
    matrix2 = inputMatrix()
    print("1. 덧셈")
    printMatrix(addMatrix(matrix1, matrix2))
    print("2. 곱셈")
    printMatrix(multiplyMatrix(matrix1, matrix2))

if __name__ == "__main__":
    main()

