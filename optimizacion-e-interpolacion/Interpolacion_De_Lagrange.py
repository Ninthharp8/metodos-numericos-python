import sympy as sy
import numpy as np
import matplotlib.pyplot as plt

def arg_prod(i, j, x_sym, x_vals):
    """Producto base de Lagrange (L_k)."""
    return (x_sym - x_vals[i]) / (x_vals[j] - x_vals[i]) if i != j else 1

def interpolacion_lagrange(x_vals, y_vals, num_puntos=100, graficar=False, point_to_evaluate=None):
    """
    Calcula el polinomio de interpolación de Lagrange. Opcionalmente grafica 
    y evalua en un punto dado .

    Parámetros:
    - x_vals: lista o array de valores de x
    - y_vals: lista o array de valores de y
    - num_puntos: número de puntos para evaluar y graficar el polinomio
    - graficar: bool, si True muestra el gráfico
    - point_to_evaluate: int, si ingresa un número este sera evaluado en la función resultante

    Retorna:
    - lagrange_poly: polinomio simbólico de Lagrange
    - x_test: valores de x evaluados (para graficar)
    - y_test: valores de y correspondientes al polinomio evaluado
    """
    x_sym = sy.symbols('x')
    points = len(x_vals)

    # Bases Lagrange
    lj = []
    for k in range(points):
        lk = np.prod([arg_prod(i, k, x_sym, x_vals) for i in range(points)])
        lj.append(lk)

    lagrange_poly = sum(np.array(y_vals) * np.array(lj))
    print(f"El polinomio resultante es: {lagrange_poly}")

    # Convertimos a función numérica para evaluación rápida
    lagrange_func = sy.lambdify(x_sym, lagrange_poly, modules=['numpy'])

    x_test = np.linspace(min(x_vals), max(x_vals), num_puntos)
    y_test = lagrange_func(x_test)

    # Evaluación puntual
    if point_to_evaluate is not None:
        y_eval = lagrange_func(point_to_evaluate)
        print(f"\nEvaluación puntual: f({point_to_evaluate}) = {y_eval}")
    else:
        y_eval = None

    # Graficar
    if graficar:
        plt.figure(figsize=(8, 5))
        plt.plot(x_test, y_test, label='Polinomio de Lagrange', color='blue')
        plt.scatter(x_vals, y_vals, color='red', label='Puntos originales')

        if point_to_evaluate is not None:
            plt.scatter(point_to_evaluate, y_eval, color='green', marker='x', s=100, label=f'f({point_to_evaluate}) = {y_eval:.2f}')
            plt.annotate(f'{y_eval:.2f}', (point_to_evaluate, y_eval), textcoords="offset points", xytext=(0,10), ha='center')

        plt.title("Interpolación con Polinomio de Lagrange")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    

if __name__ == "__main__":
    x = np.array([1, 3, 5, 7, 13])
    y = np.array([800,2310,3090,3940,4755])

    # Puntos generados por el polinomio de Lagrange
    interpolacion_lagrange(x, y,graficar=True,point_to_evaluate=10)