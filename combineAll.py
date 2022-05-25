import time
import random
import string
import pandas as pd
import matplotlib.pyplot as plt

from csv import DictWriter
from textwrap import wrap

# Execution parameters
RUN_TIMES = 12
REPEAT_TIMES = 5
INTEGER_LENGTH1 = 10
INTEGER_LENGTH2 = 10
STEP = 90

def drawPlot1():
    plt.rcParams["figure.figsize"] = [8.5, 4.5]
    plt.rcParams["figure.autolayout"] = True

    headers = ['Int length', 'Execution time (nanosecond)']

    df = pd.read_csv('output_one.csv', names=headers)
    df.set_index('Int length').plot(marker="*", color="orange")

    plt.title('\n'.join(wrap('Execution time of common method')))
    plt.savefig("Execution time of common method.png")
    # plt.show()


def drawPlot2():
    plt.rcParams["figure.figsize"] = [8.5, 4.5]
    plt.rcParams["figure.autolayout"] = True

    headers = ['Int length', 'Execution time (nanosecond)']

    df = pd.read_csv('output_two.csv', names=headers)
    df.set_index('Int length').plot(marker="*", color="blue")

    plt.title('\n'.join(wrap('Execution time of Karatsuba method')))
    plt.savefig("Execution time of Karatsuba method.png")
    plt.show()


def genRandStr(chars=string.digits, N=10):
    """
    Helper function to generate random integer string
    """
    return ''.join(random.choice(chars) for _ in range(N))


def zeroPad(numberString, zeros, left=True):
    """
    Helper function that return the string with zeros 
    added to the left or right
    """
    for _ in range(zeros):
        if left:
            numberString = '0' + numberString
        else:
            numberString = numberString + '0'
    return numberString


def commonMultiplication(x, y) -> int:
    """
    Function that multiply two integers using common method.

    Parameters
    ----------
        `x` : int
            first input integer
        `y` : int
            second input integer

    Return
    ------
        `partialSum` : int
            product of `a` and `b`
    """
    # convert to strings for easy access to digits
    x = str(x)
    y = str(y)

    # keep track of number of zeros required to pad partial multiplications
    zeroPadding = 0

    # sum of the partial multiplications
    partialSum = 0

    # loop over each digit in the second number
    for i in range(len(y) - 1, -1, -1):
        # keep track of carry for multiplications resulting in answers > 9
        carry = 0

        # partial multiplication answer as a string for easier manipulation
        partial = ''

        # pad with zeros on the right
        partial = zeroPad(partial, zeroPadding, False)

        # loop over each digit in the first number
        for j in range(len(x) - 1, -1, -1):
            z = int(y[i])*int(x[j])
            z += carry
            # convert to string for easier manipulation
            z = str(z)

            # keep track of carry when answer > 9
            if len(z) > 1:
                carry = int(z[0])
            else:
                carry = 0

            # concatenate final answer to the left of partial string
            partial = z[len(z) - 1] + partial

        # if there's any carry left at the end concatenate to partial string
        if carry > 0:
            partial = str(carry) + partial

        # sum the partials as you go
        partialSum += int(partial)

        # for the next digit of the second number we need another zero to the right
        zeroPadding += 1
    return partialSum


def karatsubaMultiplication(x, y):
    """Multiply two integers using Karatsuba's algorithm."""
    # convert to strings for easy access to digits
    x = str(x)
    y = str(y)
    # base case for recursion
    if len(x) == 1 and len(y) == 1:
        return int(x) * int(y)

    if len(x) < len(y):
        x = zeroPad(x, len(y) - len(x))
    elif len(y) < len(x):
        y = zeroPad(y, len(x) - len(y))

    n = len(x)
    j = n//2

    # for odd digit integers
    if (n % 2) != 0:
        j += 1

    BZeroPadding = n - j
    AZeroPadding = BZeroPadding * 2
    a = int(x[:j])
    b = int(x[j:])
    c = int(y[:j])
    d = int(y[j:])

    # recursively calculate
    ac = karatsubaMultiplication(a, c)
    bd = karatsubaMultiplication(b, d)
    k = karatsubaMultiplication(a + b, c + d)
    A = int(zeroPad(str(ac), AZeroPadding, False))
    B = int(zeroPad(str(k - ac - bd), BZeroPadding, False))
    return A + B + bd


if __name__ == "__main__":
    """
    abc
    """
    headers1 = ["Int length", "Execution time"]
    file = open("output_one.csv", "a", newline="")
    for i in range(RUN_TIMES):
        total_exec_time = 0
        for _ in range(REPEAT_TIMES):
            a = genRandStr(N=INTEGER_LENGTH1)
            b = genRandStr(N=INTEGER_LENGTH1)

            clk_start = time.perf_counter_ns()

            product = commonMultiplication(a, b)

            clk_end = time.perf_counter_ns()
            total_exec_time += clk_end - clk_start

        dict = {"Int length": INTEGER_LENGTH1,
                "Execution time": total_exec_time // RUN_TIMES}
        dictwriter_object = DictWriter(file, fieldnames=headers1)
        print("NORMAL: write int length: ", INTEGER_LENGTH1)
        dictwriter_object.writerow(dict)
        INTEGER_LENGTH1 = INTEGER_LENGTH1 + STEP
    file.close()

    drawPlot1()
# ---------------------
    headers2 = ["Int length", "Execution time"]
    file = open("output_two.csv", "a", newline="")
    for i in range(RUN_TIMES):
        total_exec_time = 0
        for _ in range(REPEAT_TIMES):
            a = genRandStr(N=INTEGER_LENGTH2)
            b = genRandStr(N=INTEGER_LENGTH2)

            clk_start = time.perf_counter_ns()

            product = karatsubaMultiplication(a, b)

            clk_end = time.perf_counter_ns()
            total_exec_time += clk_end - clk_start
            
        dict = {"Int length": INTEGER_LENGTH2,
                "Execution time": total_exec_time // RUN_TIMES}
        dictwriter_object = DictWriter(file, fieldnames=headers2)
        print("KARATSUBA: write int length: ", INTEGER_LENGTH2)
        dictwriter_object.writerow(dict)
        INTEGER_LENGTH2 = INTEGER_LENGTH2 + STEP
    file.close()

    drawPlot2()
