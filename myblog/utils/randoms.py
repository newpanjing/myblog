import random


def getRandomArray(count, size):
    arr = []
    for i in range(0, size):
        val = random.randint(0, count-1)
        arr.append(val)
    return arr
