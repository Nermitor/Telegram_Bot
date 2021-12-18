import matplotlib.pyplot as plt
from numpy import linspace
from math import *


def save_picture(start, stop, n, func, title):
    x = linspace(start, stop, n)
    fig = plt.subplots()
    plt.title(title)
    plt.plot(x, list(map(func, x)))
    ax = plt.gca()
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('center')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.set_xlabel("X", fontsize=15, color='blue', labelpad=120)  # +
    ax.set_ylabel("Y", fontsize=15, color='orange', labelpad=140)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.savefig("to_send.png")


