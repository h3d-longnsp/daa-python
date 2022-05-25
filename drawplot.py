import time
import random
import string
import pandas as pd
import matplotlib.pyplot as plt

from csv import DictWriter
from textwrap import wrap

plt.rcParams["figure.figsize"] = [8.5, 4.5]
plt.rcParams["figure.autolayout"] = True

headers1 = ['Int length', 'Execution time (common)']
headers2 = ['Int length', 'Execution time (karatsuba)']

df1 = pd.read_csv('output_one.csv', names=headers1)
ax = df1.set_index('Int length').plot(marker="*", color="orange")

df2 = pd.read_csv('output_two.csv', names=headers2)
df2.set_index('Int length').plot(ax=ax, marker="*", color="blue")

plt.title('\n'.join(wrap('Compare')))
plt.savefig("Execution time compare between common and Karatsuba.png")
plt.show()