def polynomial_equation(coefficients: list) -> list:
    from .Matrix import mat, eig
    p = [_ / coefficients[0] for _ in coefficients[1:]]
    return [complex(round(_.real, 12), round(_.imag, 12)) if isinstance(_, complex) else round(_, 12) for _ in eig(mat(
        [[-p[i] if j == 0 else 1 if i + 1 == j else 0 for j in range(len(p))] for i in range(len(p))]))[0].data[0]]


def multivariate_linear_equation_system(left: list, right: list) -> list:
    from .Matrix import mat
    d = mat(left).det()
    if d != 0:
        return [round(_, 12) for _ in [mat([left[_][:item] + [right[_]] + left[_][item + 1:]
                                            for _ in range(len(left))]).det() / d for item in range(len(left))]]


pe = polynomial_equation
mles = multivariate_linear_equation_system
