def expma(n, arr):
    arr = arr[:n]
    x = arr[0]
    for a in arr[1:]:
        x = ((2 * a) + (n - 1) * x) / (n + 1)
    return x


def macd(arr):
    return (224 / 51 * expma(9, arr))\
           - (16 / 3 * expma(12, arr))\
           + (16 / 17 * expma(26, arr))
