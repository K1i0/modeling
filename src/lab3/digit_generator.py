import numpy as np
import random
import matplotlib.pyplot as plt
import math
from collections import Counter
import argparse
import sys

_N = 10000

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


def get_selection(mode, pi):

    if not mode:
        selection = []

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
    else:
        # Выборка без возврата...
        return


def main():
    parser = argparse.ArgumentParser(description="Command line arguments parser")

    parser.add_argument('--mode', type=int, default=1, help='Режим 0 - выборка с повторениями, 1 - без повторений')
    
    args = parser.parse_args()

    # Вероятности, расчитанные по формуле Бернулли и формуле гипергеометрической вероятности соответственно
    pi = [0.01265, 0.09876, 0.296, 0.39506, 0.19753] if not args.mode else [0.00766, 0.08757, 0.311995, 0.415982, 0.176793]
    print(pi)
    calc_theory_selection(args.mode, pi)

    # Генерация выборки с повторениями с заданными вероятностями
    selection_count = get_selection(args.mode, pi)
    print(selection_count)


    plot_data(theory_rep_selection.keys(), theory_rep_selection.values(), selection_count.keys(), selection_count.values(), "Гистограмма для выборки с повторениями" if not args.mode else "Гистограмма для выборки без повторений")


if __name__ == '__main__':
    main()
