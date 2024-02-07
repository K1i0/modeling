import numpy as np
import matplotlib.pyplot as plt
import math

# Количество генерируемых точек
N = 10000
# Уровень значимости
ALPHA = 0.01
# Число степеней свободы
R = 2
# Взял значения таблицы распределения X^2 для ALPHA == 0.01 (стр. 78 пособия)
X2 = [6.635, 9.210, 11.345, 13.237, 15.086, 16.812, 18.475, 20.090, 21.666, 23.209, 24.795, 24.217, 27.688, 29.141, 30.578, 32.000, 32.409, 34.805, 36.191, 37.566, 38.932, 40.289, 41.638, 42.980, 42.314, 45.642, 46.963, 48.278, 49.588, 50.892]

def in_gap_filter(num, left, right, is_last):
    if num >= left:
        if is_last:
            if num <= right:
                return True
        else:
            if num < right:
                return True
    return False

# Рассчет середин отрезков
def calc_mids(gaps, k):
    mids = []
    for i in range(1, k + 1):
        mids.append((gaps[i - 1] + gaps[i]) / 2)
    return mids
# Вычисление мат. ожидания
def calc_math_expect(mids, freqs, n) -> float:
    math_expect = 0.0
    for i in range(0, len(mids)):
        math_expect += (mids[i] * freqs[i])
    math_expect /= n
    return math_expect
# Вычисление дисперсии
def calc_variance(mids, freqs, math_expect, n):
    variance = 0.0
    for i in range(0, len(mids)):
        variance += (pow(mids[i], 2) * freqs[i])
    variance = (variance / n) - pow(math_expect, 2)
    return variance

# Среднеквадратичное отклонение
def calc_diviation(variance):
    return math.sqrt(variance)

# Вычисление несмещённой оценки дисперсии случайной величины
def calc_s2(variance, n):
    s2 = (n / (n - 1)) * variance
    return s2

# Вероятность попадания в интервал  (Pi)
def fall_into_interval_chance(gaps, a_star, b_star):
    fall_chance = []
    for i in range(1, len(gaps)):
        fall_chance.append((gaps[i] - gaps[i-1]) / (b_star - a_star))
    return fall_chance

# Вычисление теоретических частот
def calc_theory_freqs(fall_chance, n):
    theory_freqs = []
    for i in range(0, len(fall_chance)):
        theory_freqs.append(n * fall_chance[i])
    return theory_freqs

# Рассчет статистики наблюдений
def calc_stats(freqs, theory_freqs):
    x_stat = 0.0
    for i in range (0, len(freqs)):
        x_stat += pow((freqs[i] - theory_freqs[i]), 2) / theory_freqs[i]
    return  x_stat

def check_hypotesis(x_stat, x2):
    if x2 <= x_stat:
        print("Гипотеза отвергается. Xstat = {} >= Xcrit = {}".format(x_stat, x2))
    else:
        print("Гипотеза не отвергается. Xstat = {} < Xcrit = {}".format(x_stat, x2))

# Вычисление коэффициента автокорреляции, tao (τ) - смещение
# Верхняя граница n - tao должна включаться? [] или [)?
def calc_autocor(numbers, math_expect, s2, n, tao = 1):
    autocor = 0.0
    for i in range(1, n - tao):
        autocor += (numbers[i] - math_expect) * (numbers[i - tao] - math_expect)
    autocor /= (s2 * (n - tao))
    return autocor

def check_dependency(autocor):
    if abs(autocor) < 1:
        print("Нет зависимости при генерации: |r(τ)| < 1 (|r(τ)| = {})".format(abs(autocor)))
    else:
        print("Есть зависимость при генерации: |r(τ)| >= 1 (|r(τ)| = {})".format(abs(autocor)))

# если диапазон от 0 до 1 - надо сгенерировать 100 чифек и сложить в массив
numbers = np.random.uniform(low=0.0, high=1.0, size=(N,))

min = (min(numbers))
max = (max(numbers))

print("MIN: {}".format(min))
print("MAX: {}".format(max))

# кол-во гистограмм
k = math.ceil(1 + math.log(N, 2))
h = ((max - min) / k)

print("k: {}".format(k))
print("h: {}".format(h))

gaps = [min]
for i in range(1, k + 1):
    gaps.append((gaps[i - 1] + h))

print("GAPS: ", gaps)

freqs = [0] * k
for num in numbers:
    for j in range(1, k + 1):
        if in_gap_filter(num, gaps[j - 1], gaps[j], True if (j == k) else False):
            freqs[j - 1] += 1
            break
print(freqs)

rel_freqs = [0.0] * k
for i in range(0, len(freqs)):
    rel_freqs[i] = freqs[i] / N
print(rel_freqs)

mids = calc_mids(gaps, k)
print("Middles: ", mids)

math_expect = calc_math_expect(mids, freqs, N)
print("Math expectation: ", math_expect)

variance = calc_variance(mids, freqs, math_expect, N)
print("Variance: ", variance)

deviation = calc_diviation(variance)
print("Diviation: ", deviation)

s2 = calc_s2(variance, N)
s = math.sqrt(s2)
print("S2: ", s2, ", S: ", s)

# a*, b* - с конспекта практики
a_star = math_expect - s * math.sqrt(3)
b_star = math_expect + s * math.sqrt(3)
print("a*: ", a_star, ", b*: ", b_star)

# Используя критерии‌ Пирсона, при уровне значимости 0,01 проверить, согласуется ли гипотеза о равномерном распределении генеральнои‌ совокупности
# Плотность распределения
dencity = 1.0 / (b_star - a_star)
print("Dencity: ", dencity)

# Оценка вероятности попадания в интервал
fall_chance = fall_into_interval_chance(gaps, a_star, b_star)
print("Fall into intervals chances: ", fall_chance)

# Вычисление n`
theory_freqs = calc_theory_freqs(fall_chance, N)
print("Theoretical frequencies: ", theory_freqs)

# Статистика X^2
x_stat = calc_stats(freqs, theory_freqs)
print("X^2: ", x_stat)

# По критерию Пирсона при уровне значимости alpha == 0,01 требуется проверить, значимо или нет различие в частотах ni и ni'
# Дополнительный -1 для отображения данных из таблицы на логику массива
x2 = X2[k - R - 1 - 1]
check_hypotesis(x_stat, x2)

# Используя коэффициент автокореляции, проверить касисьво генеральной совокупности на независимость
autocor = calc_autocor(numbers, math_expect, s2, N)
check_dependency(autocor)

#create graphic
ax = plt.gca()
plt.plot(mids, rel_freqs, marker='o', linestyle='-')
plt.xticks(gaps)
plt.ylim(0.0, np.max(rel_freqs))
plt.title('График относительных частот')
plt.xlabel('Интервалы значений выборки')
plt.ylabel('Относительные частоты')
plt.show()