from main_task import finite_forward_differences


def print_difference_table(x, y):
    n = len(x)
    forward_diff = finite_forward_differences(y)
    res = ''
    res += "Таблица конечных разностей:\n"
    header = "№\txi\t\t\tyi"
    for j in range(1, n):
        header += f"\t\tΔ{j}yi"
    res += (header+"\n")

    for i in range(n):
        row = f"{i}\t{x[i]:.2f}\t\t{y[i]:.2f}"
        for j in range(1, n - i):
            row += f"\t\t{forward_diff[i][j]:.2f}"
        res += (row + "\n")
    res += "\n"
    return res
