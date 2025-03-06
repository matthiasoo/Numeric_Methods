import math
import matplotlib.pyplot as plt
import numpy as np

def wielomian(x) :
    return x**3 + x**2 - 2*x

def trygonometryczna(x) :
    return math.sin(x)

def wykladnicza(x) :
    return 0.5**x - 1

def zlozenie_wiel_tryg(x) :
    return wielomian(trygonometryczna(x))

def wyliczanie_x(a, b, funkcja, metoda) :
    if metoda == 0 :
        return (a + b) / 2
    else :
        return a - funkcja(a) * (b - a) / (funkcja(b) - funkcja(a))

def zlozenie_wykl_wiel(x) :
    return wykladnicza(wielomian(x))

def szkielet_metody(a, b, funkcja, ex, iter, metoda, wybor_k) :
    x0 = a

    if b < a:
        print("b jest mniejsze od a")

    fa = funkcja(a)
    fb = funkcja(b)

    if fa * fb >= 0:
        print("Funkcja musi mieć różne znaki na końcach przedziału [a, b]")
    else:
        x0 = wyliczanie_x(a, b, funkcja, metoda)

        while abs(a - x0) > ex if wybor_k == "1" else iter > 0:
            fx = funkcja(x0)
            fa = funkcja(a)
            fb = funkcja(b)

            if fx == 0:
                break

            if fx * fb < 0:
                a = x0

            if fx * fa < 0:
                b = x0

            x0 = wyliczanie_x(a, b, funkcja, metoda)

            if wybor_k == "2":
                iter -= 1

        print(f"x0 = {x0}")
    return x0

def metoda_bisekcji(a, b, funkcja, ex, iter, wybor_k) :
    return szkielet_metody(a, b, funkcja, ex, iter, 0, wybor_k)

def metoda_regula_falsi(a, b, funkcja, ex, iter, wybor_k) :
    return szkielet_metody(a, b, funkcja, ex, iter, 1, wybor_k)

def rysowanie_wykresu(a, b, funkcja, x0) :
    x = np.linspace(a, b, 1000)
    y = funkcja(x)
    plt.plot(x, y)
    plt.scatter(x0, funkcja(x0), color='red')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title("Wykres funkcji")
    plt.grid(True)
    plt.show()

def main() :
    ex = 1e-8
    iter = 0

    funkcje = {
        "1": wielomian,
        "2": trygonometryczna,
        "3": wykladnicza,
        "4": zlozenie_wiel_tryg,
        "5": zlozenie_wykl_wiel
    }

    print("Funkcje:")
    print("1 - wielomian")
    print("2 - f. trygonometryczna")
    print("3 - f. wykładnicza")
    print("4 - zlozenie: wielomian od f. wykładniczej")
    print("5 - zlozenie: f. wykładnicza od wielomianu")
    wybor_f = input("Wybierz funkcję: ")

    if wybor_f not in funkcje:
        print("Niepoprawny wybór funkcji")
        exit()

    funkcja = funkcje[wybor_f]

    print("Kryteria stopu:")
    print("1 - |x - x_prev| < epsilon")
    print("2 - liczba iteracji")
    wybor_k = input("Wybierz kryterium stopu: ")

    if wybor_k not in ["1", "2"] :
        print("Niepoprawny wybór kryterium stopu")
        exit()

    if wybor_k == "1" :
        ex = float(input("Podaj epsilon: "))
    else :
        iter = int(input("Podaj liczbę iteracji: "))

    a = float(input("Podaj a: "))
    b = float(input("Podaj b: "))

    metoda_bisekcji(a, b, funkcja, ex, iter, wybor_k)
    x0 = metoda_regula_falsi(a, b, funkcja, ex, iter, wybor_k)
    rysowanie_wykresu(a, b, funkcja, x0)

main()