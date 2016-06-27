import pandas as pd
import numpy as np
from pandas import DataFrame
from src.base.model.fuzzyset import Term
from src.base.model.fuzzyset import LingVariable

fisher = pd.read_csv('../data/Fisher.csv')
names = fisher.columns.values
ling_vars = [LingVariable(name=name, universum=(fisher[name].min(), fisher[name].max())) for name in names]
for ling in ling_vars:
    print("{0} : {1}".format(ling, ling.universum))
inputs = ling_vars[1::]
output = ling_vars[0]

decart = lambda x, y: sum([(a - b) ** 2 for a, b in zip(x, y)])

# normalization
for ling in inputs:
    fisher[ling.name] = (fisher[ling.name] - ling.universum[0]) / (ling.universum[1] - ling.universum[0])
    ling.universum = (0, 1)
print(fisher)


# need to complete
H = 10
max_epoch = 5
eps = 0.0001
alfa_w = 0.5
alfa_r = 0.2
epoch_number = 0

while (True):
    epoch_number += 1
    n = [1 for i in range(0, H)]
    for ling in inputs:
        x_t = fisher[ling.name]

