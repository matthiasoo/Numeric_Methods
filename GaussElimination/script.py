import numpy as np

# funkcja do samodzielnego wprowadzania macierzy
def enter_from_keyboard() :
    R = int(input("Podaj ilość równań: "))

    if R < 1 :
        print("Zbyt mała liczba równań")
        exit()

    matrixA = np.zeros((R, R), dtype=float)
    matrixB = np.zeros((R, 1), dtype=float)

    print("Macierz A:")
    for i in range(R) :
        for j in range(R) :
            matrixA[i, j] = float(input(f"Podaj element[{i}][{j}]: "))

    print("Macierz B:")
    for i in range(R) :
        matrixB[i] = float(input(f"Podaj prawą stronę równania {i+1}: "))

    return matrixA, matrixB

# funkcja do wczytywania macierzy z pliku
def load_from_file() :
    filename = input("Podaj nazwę pliku: ")

    try:
        data = np.loadtxt(f"matrixes/{filename}")

        print(f"Wczytano dane z pliku {filename}")

        R, C = data.shape

        if C != R + 1:
            print("Nieprawidłowe wymiary macierzy")
            exit()

        matrixA = np.zeros((R, R), dtype=float)
        matrixB = np.zeros((R, 1), dtype=float)

        matrixA = data[:, :-1]
        matrixB = data[:, -1].reshape(R, 1)

        return matrixA, matrixB

    except FileNotFoundError:
        print("Nie znaleziono pliku.")
        exit()
    except ValueError:
        print("Niepoprawne dane")
        exit()
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        exit()

# funkcja obliczajaca rząd macierzy
def rank(matrix) :
    R = matrix.shape[0]
    rank = 0
    reducedMatrix = gauss(matrix)
    # print(reducedMatrix)

    for i in range(R):
        if not np.all(reducedMatrix[i] == 0):
            rank += 1

    return rank

# funkcja sprowadzająca macierz do postaci trójkątnej / zredukowanej
def gauss(matrix) :
    R = matrix.shape[0]
    p = 0 # pivot, element główny

    while p < R :
        # if matrix[p, p] == 0 :
        #     for i in range(p+1, R) :
        #         if matrix[i, p] != 0 :
        #             matrix[[p, i]] = matrix[[i, p]]
        #             i = R

        # częściowy wybór elementu głównego
        for i in range(p+1, R) :
            if abs(matrix[p][p]) < abs(matrix[i][p]) :
                matrix[[i, p]] = matrix[[p, i]]

        for i in range(p+1, R) :
            multiplier = matrix[i, p] / matrix[p, p]
            matrix[i] -= (multiplier * matrix[p])
            # print(matrix)

        p += 1

    return matrix

# funkcja obliczająca rozwiązania URL metodą podstawiania wstecz
def solve(matrixX) :
    R = matrixX.shape[0]
    x = np.zeros(R)
    matrix = gauss(matrixX)

    x[R-1] = matrix[R-1, R] / matrix[R-1, R-1]

    for i in range(R-2, -1, -1) :
        x[i] = matrix[i, R]

        for j in range(i + 1, R) :
            x[i] -= matrix[i, j] * x[j]

        x[i] /= matrix[i, i]

    return x

def main() :
    choices = {
        "1": enter_from_keyboard,
        "2": load_from_file
    }

    print("Sposoby wprowadzania URL:")
    print("1 - z klawiatury")
    print("2 - z pliku")
    choice = input("Wybierz sposób: ")

    if choice not in choices:
        print("Niepoprawny wybór sposobu")
        exit()

    matrixA, matrixB = choices[choice]()

    matrixAB = np.concatenate((matrixA, matrixB), axis=1)
    count = matrixA.shape[0] # liczba niewiadomych

    rankA = rank(matrixA)
    rankAB = rank(matrixAB)
    # rankA = np.linalg.matrix_rank(matrixA)
    # rankAB = np.linalg.matrix_rank(matrixAB)

    if rankA != rankAB :
        print("Układ równań liniowych jest sprzeczny")
        exit()
    elif rankAB < count :
        print(f"Układ równań liniowych jest nieoznaczony (rozwiązania układu zależą od liczby parametrów równej {count - rankA})")
        exit()
    else :
        xs = solve(matrixAB)
        print("Rozwiązania:")
        for i in range(count):
            print(f"x{i} = {xs[i]}")

main()