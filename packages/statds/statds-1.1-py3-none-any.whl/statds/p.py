import no_parametrics as nop
import pandas as pd
from scipy import stats 
import numpy as np
import math

df = pd.read_csv("../edu.csv")

table_results, statistic, p_value, critical_value, hypothesis = nop.friedman(df)
a,b = stats.friedmanchisquare(*[df[i].to_numpy() for i in df.columns[1:]])

print(statistic, a)

print(p_value, b)

print(p_value - b)