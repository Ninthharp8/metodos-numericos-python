import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sympy import symbols, lambdify

x = symbols('x')  # Declarar variable simbólica global

class Splines:
    def __init__(self, x_vals, y_vals, a_eval):
        self.x_vals = x_vals
        self.y_vals = y_vals
        self.a = a_eval  # punto a evaluar

    def PolSplines(self):
        xi = self.x_vals
        yi = self.y_vals
        n = len(xi)
        h = [xi[i+1] - xi[i] for i in range(n - 1)]

        # Matriz del sistema
        A = np.zeros((n - 2, n - 2))
        b = np.zeros(n - 2)

        for i in range(n - 2):
            A[i][i] = 2 * (h[i] + h[i+1])
            if i > 0:
                A[i][i - 1] = h[i]
                A[i - 1][i] = h[i]

        for i in range(2, n):
            b[i - 2] = 6 * (
                (yi[i] - yi[i - 1]) / (xi[i] - xi[i - 1])
                - (yi[i - 1] - yi[i - 2]) / (xi[i - 1] - xi[i - 2])
            )

        # Resolver sistema
        M = np.linalg.solve(A, b).tolist()
        M.insert(0, 0)
        M.append(0)

        splines = []
        dominios = []

        for i in range(n - 1):
            hi = h[i]
            a = (M[i+1] - M[i]) / (6 * hi)
            b = M[i] / 2
            c = (yi[i+1] - yi[i]) / hi - hi * (2*M[i] + M[i+1]) / 6
            d = yi[i]
            Si = a*(x - xi[i])**3 + b*(x - xi[i])**2 + c*(x - xi[i]) + d
            splines.append(Si)
            dominios.append([xi[i], xi[i+1]])

        # Gráfica con Plotly
        fig = go.Figure()
        s_dict = {}
        for i, Si in enumerate(splines):
            f_lambda = lambdify(x, Si, modules='numpy')
            x_range = np.linspace(*dominios[i], 100)
            fig.add_trace(go.Scatter(x=x_range, y=f_lambda(x_range), mode='lines', name=f"Spline {i}"))
            s_dict[i] = (dominios[i], f_lambda)

        # Evaluar el punto `a`
        for i in s_dict:
            x_dom, f_spline = s_dict[i]
            if x_dom[0] <= self.a <= x_dom[1]:
                y_eval = f_spline(self.a)
                fig.add_trace(go.Scatter(x=[self.a], y=[y_eval], mode='markers',
                                         marker=dict(size=10, color='red'),
                                         name="Punto evaluado"))
                break

        fig.update_layout(title="Interpolación por Splines cúbicos",
                          xaxis_title="x", yaxis_title="y")
        fig.show()

        print(f"La aproximación en x = {self.a} es: {y_eval}")
        print("Los polinomios son:")
        for spline, intervalo in zip(splines, dominios):
            print(spline.expand(), "en", intervalo)


if __name__ == "__main__":
    xi = [0.1,0.2,0.3,0.4]
    yi = [1.45,1.8,1.7,2]
    a = 0.25  # punto a evaluar

    metodo = Splines(xi, yi, a)
    splines, dominios = metodo.PolSplines()

    # Mostrar splines simbólicos
    for i, (Si, dom) in enumerate(zip(splines, dominios)):
        print(f"Spline {i}: {Si.expand()} en intervalo {dom}")
