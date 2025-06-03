import tkinter as tk
from fractions import Fraction

def gaussian_elimination(matrix, vector):
    n = len(matrix)
    steps = []  # Lista para almacenar las operaciones de la matriz paso a paso

    for i in range(n):
        # Buscar un 1 en la columna i
        for j in range(i, n):
            if matrix[j][i] == 1:
                matrix[i], matrix[j] = matrix[j], matrix[i]
                vector[i], vector[j] = vector[j], vector[i]
                break

        # Agregar operación de reestructuración a los pasos
        steps.append(f"Reestructuración (fila {i+1} <-> fila {j+1})")
        steps.append(f"Matriz:\n{format_matrix(matrix, vector)}")
        steps.append(f"Vector:\n{format_vector(vector)}")

        # Eliminación gaussiana
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            vector[j] -= factor * vector[i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]

            # Agregar operación de eliminación gaussiana a los pasos
            steps.append(f"Eliminación gaussiana (fila {j+1})")
            steps.append(f"Matriz:\n{format_matrix(matrix, vector)}")
            steps.append(f"Vector:\n{format_vector(vector)}")

    # Sustitución hacia atrás
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = vector[i]
        for j in range(i + 1, n):
            solution[i] -= matrix[i][j] * solution[j]
        solution[i] /= matrix[i][i]

    # Agregar la solución final a los pasos
    steps.append("Solución final:")
    steps.append(f"Matriz:\n{format_matrix(matrix, vector)}")
    steps.append(f"Vector:\n{format_vector(vector)}")
    steps.append(f"Solución: {format_solution(solution)}")

    return solution, steps

# funciones para la interfaz 
def format_matrix(matrix, vector):
    return "\n".join([" ".join([format_fraction(x) for x in row[:-1]]) + f" | {format_fraction(vector[i])}" for i, row in enumerate(matrix)])

def format_vector(vector):
    return " ".join([format_fraction(x) for x in vector])

def format_solution(solution):
    return " ".join([f"x{i+1}={format_fraction(x)}" for i, x in enumerate(solution)])

def format_fraction(num):
    frac = Fraction(num).limit_denominator()
    if frac.denominator == 1:
        return str(frac.numerator)
    else:
        return f"{frac.numerator}/{frac.denominator}"

def create_entries():
    global entries, n, entry_frame, window

    # Eliminar entradas existentes
    if entries:
        entry_frame.destroy()

    n = int(size_entry.get())

    # Crear un nuevo marco para las entradas
    entry_frame = tk.Frame(window)
    entry_frame.grid(row=1, column=0, columnspan=n+2, padx=10, pady=10, sticky="w")

    # Crear nuevas entradas
    entries = []
    for i in range(n):
        row = []
        for j in range(n):
            entry = tk.Entry(entry_frame, width=10)
            entry.grid(row=i, column=j, padx=5, pady=5)
            row.append(entry)
        label = tk.Label(entry_frame, text=" = ")
        label.grid(row=i, column=n, padx=5, pady=5)
        entry = tk.Entry(entry_frame, width=10)
        entry.grid(row=i, column=n+1, padx=5, pady=5)
        row.append(entry)
        entries.append(row)

    # Actualizar el tamaño de la ventana en función del tamaño de la matriz
    window_width = 250 + n * 120
    window_height = 200 + n * 50
    window.geometry(f"{window_width}x{window_height}")

def solve_equations():
    # Obtener los valores de entrada
    matrix = [[float(entries[i][j].get()) for j in range(len(entries[i]))] for i in range(len(entries))]
    vector = [float(entries[i][-1].get()) for i in range(len(entries))]

    # Resolver el sistema de ecuaciones
    solution, steps = gaussian_elimination(matrix, vector)

    # Crear la ventana de resultados
    result_window = tk.Toplevel(window)
    result_window.title("Resultados")

    # Crear un marco con scroll para los resultados
    scroll_frame = tk.Frame(result_window)
    scroll_frame.pack(fill=tk.BOTH, expand=True)

    # Configurar el scroll
    scrollbar = tk.Scrollbar(scroll_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Crear el área de texto para mostrar los resultados
    results_text = tk.Text(scroll_frame, yscrollcommand=scrollbar.set)
    results_text.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=results_text.yview)

    # Mostrar las operaciones paso a paso en el área de texto
    for step in steps:
        results_text.insert(tk.END, step + "\n\n")

    # Desactivar la edición del área de texto
    results_text.config(state=tk.DISABLED)

def solve_window():
    # Crear la ventana principal
    window = tk.Tk()
    window.title("Eliminación de Gauss")

    # Etiqueta y campo de entrada para el tamaño de la matriz
    size_label = tk.Label(window, text="Tamaño de la matriz:")
    size_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    size_entry = tk.Entry(window, width=5)
    size_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # Crear el botón de crear
    create_button = tk.Button(window, text="Crear", command=create_entries)
    create_button.grid(row=0, column=2, padx=10, pady=10, sticky="e")

    # Crear el botón de resolver
    solve_button = tk.Button(window, text="Resolver", command=solve_equations)
    solve_button.grid(row=0, column=3, padx=10, pady=10, sticky="e")

    # Variables globales
    entries = []
    n = 0
    entry_frame = tk.Frame(window)

    # Obtener el tamaño de la pantalla
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calcular la posición de la ventana
    window_width = 500
    window_height = 300
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2

    # Configurar la geometría de la ventana
    window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # Iniciar el bucle principal de la ventana
    window.mainloop()

solve_window()