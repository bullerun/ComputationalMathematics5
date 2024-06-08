def finite_differences(x, y):
    n = len(x)
    diff_table = [[0] * n for _ in range(n)]
    for i in range(n):
        diff_table[i][0] = y[i]
    for j in range(1, n):
        for i in range(n - j):
            diff_table[i][j] = (diff_table[i + 1][j - 1] - diff_table[i][j - 1]) / (x[i + j] - x[i])
    return diff_table


def finite_forward_differences(y):
    n = len(y)
    forward_diff = [[0] * n for _ in range(n)]
    for i in range(n):
        forward_diff[i][0] = y[i]
    for j in range(1, n):
        for i in range(n - j):
            forward_diff[i][j] = forward_diff[i + 1][j - 1] - forward_diff[i][j - 1]
    return forward_diff


def finite_backward_differences(y):
    n = len(y)
    backward_diff = [[0] * n for _ in range(n)]
    for i in range(n):
        backward_diff[i][0] = y[i]
    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            backward_diff[i][j] = backward_diff[i][j - 1] - backward_diff[i - 1][j - 1]
    return backward_diff


def interpolate_newton_divided_diff(x, y, x_interp):
    n = len(x)
    diff_table = finite_differences(x, y)
    y_interp = diff_table[0][0]
    product = 1.0
    for i in range(1, n):
        product *= (x_interp - x[i - 1])
        y_interp += diff_table[0][i] * product
    return y_interp


def interpolate_newton_forward_diff(x, y, x_interp):
    n = len(x)
    h = x[1] - x[0]
    t = (x_interp - x[0]) / h
    forward_diff = finite_forward_differences(y)
    y_interp = y[0]
    product = 1.0
    for i in range(1, n):
        product *= (t - (i - 1)) / i
        y_interp += forward_diff[0][i] * product
    return y_interp


def interpolate_newton_backward_diff(x, y, x_interp):
    n = len(x)
    h = x[1] - x[0]
    t = (x_interp - x[-1]) / h
    backward_diff = finite_backward_differences(y)
    y_interp = y[-1]
    product = 1.0
    for i in range(1, n):
        product *= (t + (i - 1)) / i
        y_interp += backward_diff[-1][i] * product
    return y_interp


def interpolate_lagrange(x, y, x_interp):
    n = len(x)
    result = 0
    for i in range(n):
        term = y[i]
        for j in range(n):
            if j != i:
                term *= (x_interp - x[j]) / (x[i] - x[j])
        result += term
    return result

