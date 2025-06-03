from tkinter import Tk, Frame, Label, Entry, Button, Text, Scrollbar, messagebox, Toplevel
from fractions import Fraction
import numpy as np

class GaussSeidelSolver:
    def __init__(self):
        self.n = 0
        self.coeff_entries = []
        self.b_entries = []
        self.root = Tk()
        self.root.title("Resolución de Sistema de Ecuaciones por Gauss-Seidel")
        self.root.geometry("500x300")  # Tamaño específico de la ventana principal
        self.coeff_frame = Frame(self.root)
        self.coeff_frame.pack(fill="both", expand=True)

        self.eq_label = Label(self.coeff_frame, text="Número de ecuaciones:")
        self.eq_label.grid(row=0, column=0, padx=5, pady=5)

        self.eq_entry = Entry(self.coeff_frame, width=6)
        self.eq_entry.grid(row=0, column=1, padx=5, pady=5)

        self.create_button = Button(self.coeff_frame, text="Crear casillas", command=self.crear_casillas)
        self.create_button.grid(row=0, column=2, padx=5, pady=5)

        self.solve_button = Button(self.coeff_frame, text="Resolver", command=self.resolver_sistema)
        self.solve_button.grid(row=0, column=3, padx=5, pady=5)

        self.centrar_ventana()  # Centrar la ventana en la pantalla

    def crear_casillas(self):
        try:
            self.n = int(self.eq_entry.get())
            if self.n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero positivo.")
            return

        # Eliminar las casillas existentes, si las hay
        for entry_row in self.coeff_entries:
            for entry in entry_row:
                entry.destroy()

        # Eliminar las casillas del vector b existentes, si las hay
        for entry in self.b_entries:
            entry.destroy()

        # Crear las nuevas casillas de entrada
        self.coeff_entries.clear()
        for i in range(self.n):
            row_entries = []
            for j in range(self.n):
                entry = Entry(self.coeff_frame, width=10)
                entry.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")
                row_entries.append(entry)
            self.coeff_entries.append(row_entries)

        self.b_entries.clear()
        for i in range(self.n):
            entry = Entry(self.coeff_frame, width=10)
            entry.grid(row=i + 1, column=self.n, padx=5, pady=5, sticky="nsew")
            self.b_entries.append(entry)

        # Actualizar la geometría de la ventana para ajustarse a las nuevas casillas
        self.root.update()

    def resolver_sistema(self):
        # Obtener los coeficientes de las ecuaciones de las casillas de entrada
        coeficientes = []
        for row_entries in self.coeff_entries:
            fila = []
            for entry in row_entries:
                try:
                    valor = Fraction(entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.")
                    return
                fila.append(valor)
            coeficientes.append(fila)

        # Obtener los valores del vector b
        b_values = []
        for entry in self.b_entries:
            try:
                valor = Fraction(entry.get())
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido para el vector b.")
                return
            b_values.append(valor)

        try:
            A, b = self.reacomodar_matriz(coeficientes, b_values)
            self.mostrar_ventana_matriz_reacomodada(A)
            steps, solution = self.gauss_seidel(A, b)
            self.mostrar_resultados(steps, solution)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def reacomodar_matriz(self, A, b):
        n = len(A)

        # Verificar si la matriz ya tiene una diagonal dominante
        diagonal_dominante = True
        for i in range(n):
            row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
            if abs(A[i][i]) <= row_sum:
                diagonal_dominante = False
                break

        # Reacomodar las filas para obtener una matriz con diagonal dominante
        if not diagonal_dominante:
            # Crear una lista de índices para reordenar las filas
            indices = list(range(n))

            for i in range(n):
                # Encontrar el índice de la fila con el máximo elemento en la columna actual
                max_index = max(range(i, n), key=lambda x: abs(A[indices[x]][i]))

                # Intercambiar las filas
                indices[i], indices[max_index] = indices[max_index], indices[i]

                # Verificar si la matriz reordenada tiene una diagonal dominante
                diagonal_dominante = True
                for i in range(n):
                    row_sum = sum(abs(A[indices[i]][j]) for j in range(n) if j != i)
                    if abs(A[indices[i]][i]) <= row_sum:
                        diagonal_dominante = False
                        break

                if diagonal_dominante:
                    break

            # Reordenar las filas de la matriz y el vector b
            A = [A[i] for i in indices]
            b = [b[i] for i in indices]

        return A, b

    def gauss_seidel(self, A, b, x0=None, epsilon=1e-10, max_iterations=100):
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        n = A.shape[0]

        if x0 is None:
            x0 = np.zeros(n)

        steps = []
        solution = None
        x = x0.copy()

        for iteration in range(max_iterations):
            x_prev = x.copy()

            for i in range(n):
                sigma = 0.0

                for j in range(n):
                    if j != i:
                        sigma += A[i, j] * x[j]

                x[i] = (b[i] - sigma) / A[i, i]

            residual = np.linalg.norm(A @ x - b)

            step = f"Paso {iteration + 1}:\n\n"
            step += f"Solución: {x}\n\n"
            step += f"Residual: {residual}\n\n"

            steps.append(step)

            if np.linalg.norm(x - x_prev) < epsilon:
                solution = x
                break

        if solution is None:
            raise ValueError("El método de Gauss-Seidel no converge.")

        return steps, solution

    def mostrar_ventana_matriz_reacomodada(self, A):
        matrix_window = Toplevel(self.root)
        matrix_window.title("Matriz Reacomodada")
        matrix_window.geometry("400x300")
        matrix_window.pack_propagate(False)  # Evitar que la ventana cambie de tamaño automáticamente

        matrix_text = Text(matrix_window, width=40, height=10)
        matrix_text.pack(fill="both", expand=True)  # Hacer que el widget de texto ocupe todo el espacio disponible

        matrix_text.insert("end", "Matriz Reacomodada:\n\n")

        for row in A:
            for element in row:
                matrix_text.insert("end", str(element) + "\t")
            matrix_text.insert("end", "\n")

        matrix_text.configure(state="disabled")  # Deshabilitar la edición del texto

    def mostrar_resultados(self, steps, solution):
        results_window = Toplevel(self.root)
        results_window.title("Resultados")
        results_window.geometry("400x300")
        results_window.pack_propagate(False)  # Evitar que la ventana cambie de tamaño automáticamente

        results_text = Text(results_window, width=40, height=10)
        results_text.pack(fill="both", expand=True)  # Hacer que el widget de texto ocupe todo el espacio disponible

        results_text.insert("end", "Pasos:\n\n")

        for step in steps:
            results_text.insert("end", step + "\n")

        results_text.insert("end", "\nSolución Final:\n\n")
        results_text.insert("end", str(solution))

        results_text.configure(state="disabled")  # Deshabilitar la edición del texto

    def centrar_ventana(self, ventana=None):
        if not ventana:
            ventana = self.root
        ventana.update_idletasks()
        ventana_width = ventana.winfo_width()
        ventana_height = ventana.winfo_height()
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        x = (screen_width // 2) - (ventana_width // 2)
        y = (screen_height // 2) - (ventana_height // 2)
        ventana.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

    def run(self):
        self.root.mainloop()

solver = GaussSeidelSolver()
solver.run()