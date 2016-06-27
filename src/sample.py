import pandas as pd
import numpy as np
from pandas import DataFrame
from src.base.model.fuzzyset import Term
from src.base.model.fuzzyset import LingVariable

decart = lambda x, y: sum([(a - b) ** 2 for a, b in zip(x, y)])


def clear_clusters(clusters):
    result = []
    for cluster in clusters:
        if min(cluster) >= 0 and max(cluster) <= 1:
            result.append(cluster)
    return result


fisher = pd.read_csv('../data/Fisher.csv')
names = fisher.columns.values
ling_vars = [LingVariable(name=name, universum=(fisher[name].min(), fisher[name].max())) for name in names]

print("initialized ling_vars: ")
for ling in ling_vars:
    print("{0} : {1}\n".format(ling, ling.universum))

inputs = ling_vars[1::]
output = ling_vars[0]

# normalization
for ling in inputs:
    fisher[ling.name] = (fisher[ling.name] - ling.universum[0]) / (ling.universum[1] - ling.universum[0])
    ling.universum = (0, 1)

H = 10

max_epoch = 5
eps = 0.0001
alfa_w = 0.06
alfa_r = 0.02
n = [1 for i in range(0, H)]

# clusters's centers initialization
c = [np.random.sample(len(inputs)) for k in range(0, H)]

epoch_number = 0
c_old = c
stop_flag = False
while not stop_flag:
    epoch_number += 1
    for index, row in fisher.iterrows():
        results = np.asarray([decart(row[1::], c[k]) * n[k] / sum(n) for k in range(0, H)])
        winner = results.argmin()
        results[winner] = results.max()
        reebok = results.argmin()
        n[winner] += 1
        c[winner] = [b + alfa_w * (a - b) for a, b in zip(row[1::], c[winner])]
        print(c[winner])
        c[reebok] = [b - alfa_r * (a - b) for a, b in zip(row[1::], c[reebok])]
        alfa_w *= (1 - epoch_number / max_epoch)
        alfa_r *= (1 - epoch_number / max_epoch)
    if sum([decart(new, old) for new, old in zip(c, c_old)]) / H < eps:
        stop_flag = True
    else:
        c_old = c
# remove all clusters which center not in [0,1]^n
clusters = clear_clusters(c)
