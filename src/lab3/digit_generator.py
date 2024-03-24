import numpy as np
from random import randint
import matplotlib.pyplot as plt
import math
from collections import Counter
import argparse
import sys

# Число испытаний
_N = 1000

# Размерность корзины
_n = 30

# Task
# Из урны, в которой 20 белых и 10 черных шаров, наудачу вынимают 4 шара
# Хi — вероятность того что попадется Xi белых шаров

theory_rep_selection = Counter()


def plot_data(x_t, y_t, x_pi, y_pi, title):
    plt.bar(x_t, y_t, width=0.3, align='edge', color = '#FA8072', label="Theoretical", alpha=0.7)
    plt.bar(x_pi, y_pi, width=0.3, color = '#7B68EE', label="Gen Result", alpha=0.7)
    plt.title(title)
    plt.legend()
    plt.show()


# Вычисление теоретической выборки
def calc_theory_selection(mode, pi):
    global theory_rep_selection
    
    # Для выборки с повторениями
    tselect = {}
    for i in range(0, len(pi)):
        tselect[i] = int(_N * pi[i])
    
    # Приведение к объекту Counter
    theory_rep_selection = Counter(tselect)
    print(theory_rep_selection)


# m - размер выборки для алгоритма "без возвратов"
def get_selection(mode, pi, m=5):
    selection = []

    match mode:
        case 0:        
        # Массив, хранящий суммы вероятностей (вектор накопленных вероятностей до каждой категории)
            sum_pi = np.cumsum(pi)
            print(sum_pi)

            for i in range(_N):
                # Генерация случайного числа от 0 до 1
                rand_value = np.random.rand()
                # Нахождение индекса категории. Чем больше вероятность, тем больше интервал
                category = np.searchsorted(sum_pi, rand_value)
                # Добавление категории в выборку
                selection.append(category)
            
            return Counter(selection)
        case 1:
            # Статистика по белым шарам (0, 1, 2, 3, или 4 были в выборке)

            # Инициализация корзины с шарами (индексация шаров)
            basket = [None] * _n

            # Проводим N экспериментов
            for i in range(0, _N):
                white_count = 0
                
                local_selection = []
                # Индексы шаров
                for i in range(1, _n + 1):
                    basket[i - 1] = i
                
                # [n, n-1, n-2, n-3]
                # Произвести выборку
                for s in range(_n, _n - m, -1):
                    index = randint(0, s - 1)
                    print(f's: {s}, index: {index}')
                    # Добавить шар с индексом в выборку
                    local_selection.append(basket[index])
                    # Исключение из выборки выбранного значения
                    basket[index] = basket[s - 1]

                for index in local_selection:
                    if index <= 20:
                        white_count += 1

                print(white_count)
                selection.append(white_count)
            return Counter(selection)


def main():
    parser = argparse.ArgumentParser(description="Command line arguments parser")

    parser.add_argument('--mode', type=int, default=1, help='Режим 0 - выборка с повторениями, 1 - без повторений')
    
    args = parser.parse_args()

    # Вероятности, расчитанные по формуле Бернулли и формуле гипергеометрической вероятности соответственно
    pi = [0.01265, 0.09876, 0.296, 0.39506, 0.19753] if not args.mode else [0.00766, 0.08757, 0.311995, 0.415982, 0.176793]
    print(pi)
    calc_theory_selection(args.mode, pi)

    # Генерация выборки с повторениями с заданными вероятностями
    selection_count = get_selection(args.mode, pi, len(pi) - 1)
    print(selection_count)


    plot_data(theory_rep_selection.keys(), theory_rep_selection.values(), selection_count.keys(), selection_count.values(), "Гистограмма для выборки с повторениями" if not args.mode else "Гистограмма для выборки без повторений")


if __name__ == '__main__':
    main()
