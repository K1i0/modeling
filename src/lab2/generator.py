import numpy as np
import matplotlib.pyplot as plt
import math

# Количество генерируемых точек
N = 100000

# Вычисленный коэффициент
_k = 1.5566


def calc_x1(ksi):
    return (np.arccos(1 - (3 * ksi)) - 0.2)

def calc_x2(ksi):
    disc = ((9 * (_k ** _k)) - (4 * _k * ((26 * _k / 25) + ((2 * np.cos(3/5) - 2)/3) + (2 * ksi))))
    return (((3 * _k) - np.sqrt(disc)) / (2 * _k)) - 0.22


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

ksis = np.array(np.random.uniform(low=0.0, high=1.0, size=(N,)))


data = []
for ksi in ksis:
    if 0.0 <= ksi < ((1.0 - np.cos(3/5))/3):
        data.append(calc_x1(ksi))
    # else:
    if not (0.0 <= ksi < ((1.0 - 0.82533561491)/3)):
        data.append(calc_x2(ksi))

    
min = (min(data))
max = (max(data))

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
for num in data:
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

#create graphic
ax = plt.gca()
plt.plot(mids, rel_freqs, marker='o', linestyle='-')
plt.ylim(0.0, np.max(rel_freqs))
plt.title('График относительных частот')
plt.xlabel('Интервалы значений выборки')
plt.ylabel('Относительные частоты')
plt.show()