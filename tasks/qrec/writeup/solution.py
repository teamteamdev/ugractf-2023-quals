def f(n):
    if n == 1:
        return 1
    s = 0
    for i in range(1, n):
        if n % i == 0:
            s += f(i)
    s += n
    return s
