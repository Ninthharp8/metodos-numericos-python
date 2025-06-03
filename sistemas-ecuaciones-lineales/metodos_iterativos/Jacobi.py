import numpy as np
from tkinter import Tk, Frame, Label, Entry, Button, messagebox, Toplevel, Text, Scrollbar
from fractions import Fraction

class JacobiSolver:
    def __init__(self):
        self.n = 0
        self.coeff_entries = []
        self.b_entries = []
        self.root = Tk()
        self.root.title("Resolución de Sistema de Ecuaciones por Método de Jacobi")
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
        coefficients = []
        for row_entries in self.coeff_entries:
            row = []
            for entry in row_entries:
                try:
                    value = float(entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.")
                    return
                row.append(value)
            coefficients.append(row)

        # Obtener los valores del vector b
        b_values = []
        for entry in self.b_entries:
            try:
                value = float(entry.get())
            except ValueError:
                messagebox.showerror("Error", "Ingrese un número válido para el vector b.")
                return
            b_values.append(value)

        try:
            solution, operations = self.jacobi_solver(coefficients, b_values)
            self.mostrar_resultados(solution, operations)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def jacobi_solver(self, coefficients, b, initial_solution=None, tolerance=1e-6, max_iterations=100):
        A = np.array(coefficients)
        n = len(A)

        if initial_solution is None:
            initial_solution = np.zeros(n)

        x = initial_solution.copy()
        x_new = np.zeros_like(x)

        operations = []

        for iteration in range(max_iterations):
            operations.append(f"Iteración {iteration + 1}:")

            for i in range(n):
                sigma = np.dot(A[i, :], x) - A[i, i] * x[i]
                x_new[i] = (b[i] - sigma) / A[i, i]

                row_operation = f"x{i + 1} = ({Fraction(b[i]).limit_denominator()}"
                for j in range(n):
                    if j != i:
                        row_operation += f" - ({Fraction(A[i, j]).limit_denominator()} * {Fraction(x[j]).limit_denominator()})"
                row_operation += f") / {Fraction(A[i, i]).limit_denominator()}"
                operations.append(row_operation)

            operations.append("")

            if np.linalg.norm(x_new - x) < tolerance:
                break

            x = x_new.copy()

        return x, operations

    def mostrar_resultados(self, solution, operations):
        results_window = Toplevel(self.root)
        results_window.title("Resultados")
        results_window.geometry("600x400")

        self.centrar_ventana(results_window)

        results_frame = Frame(results_window)
        results_frame.pack(fill="both", expand=True)

        scrollbar = Scrollbar(results_frame)
        scrollbar.pack(side="right", fill="y")

        output_text = Text(results_frame, yscrollcommand=scrollbar.set)
        output_text.pack(fill="both", expand=True)

        for operation in operations:
            output_text.insert("end", operation + "\n")

        output_text.insert("end", "\nSolución:\n")
        for i, sol in enumerate(solution):
            output_text.insert("end", f"x{i + 1} = {Fraction(sol).limit_denominator()}\n")

        scrollbar.config(command=output_text.yview)

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

solver = JacobiSolver()
solver.root.mainloop()