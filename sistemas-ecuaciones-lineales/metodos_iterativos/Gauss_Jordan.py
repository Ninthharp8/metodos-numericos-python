from tkinter import Tk, Frame, Label, Entry, Button, Text, Scrollbar, messagebox, Toplevel
from fractions import Fraction
from tkinter import ttk


class GaussJordanSolver:
    def __init__(self):
        self.n = 0
        self.entries = []

        self.root = Tk()
        self.root.title("Resolución de sistema de ecuaciones")
        self.root.minsize(400, 300)

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

    def crear_casillas(self):
        try:
            self.n = int(self.eq_entry.get())
            if self.n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número entero positivo.")
            return

        # Eliminar las casillas existentes, si las hay
        for entry_row in self.entries:
            for entry in entry_row:
                entry.destroy()

        # Crear las nuevas casillas de entrada
        self.entries.clear()
        for i in range(self.n):
            row_entries = []
            for j in range(self.n + 1):
                entry = Entry(self.coeff_frame, width=6)
                entry.grid(row=i + 1, column=j, padx=5, pady=5, sticky="nsew")
                row_entries.append(entry)
            self.entries.append(row_entries)

        # Actualizar la geometría de la ventana para ajustarse a las nuevas casillas
        self.root.update()

    def resolver_sistema(self):
        # Obtener los coeficientes de las ecuaciones de las casillas de entrada
        coeficientes = []
        for row_entries in self.entries:
            fila = []
            for entry in row_entries:
                try:
                    valor = Fraction(entry.get())
                except ValueError:
                    messagebox.showerror("Error", "Ingrese un número válido.")
                    return
                fila.append(valor)
            coeficientes.append(fila)

        # Resolver el sistema de ecuaciones
        try:
            pasos, resultados = self.resolver_sistema_ecuaciones(coeficientes)
            self.mostrar_resultados(pasos, resultados, coeficientes)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def resolver_sistema_ecuaciones(self, coeficientes):
        n = len(coeficientes)
        pasos = []

        # Crear la matriz aumentada [A | b]
        matriz = []
        for i in range(n):
            fila = coeficientes[i]
            matriz.append(fila)

        # Aplicar el método de Gauss-Jordan
        for fila_pivote in range(n):
            pivote = matriz[fila_pivote][fila_pivote]

            # Dividir la fila por el pivote para hacerlo igual a 1
            for j in range(fila_pivote, n + 1):
                matriz[fila_pivote][j] /= pivote

            pasos.append([fila[:] for fila in matriz])

            # Eliminar los demás elementos en la columna del pivote
            for fila in range(n):
                if fila != fila_pivote:
                    factor = matriz[fila][fila_pivote]
                    for j in range(fila_pivote, n + 1):
                        matriz[fila][j] -= factor * matriz[fila_pivote][j]

            pasos.append([fila[:] for fila in matriz])

        resultados = [fila[-1] for fila in matriz]

        return pasos, resultados

    def mostrar_resultados(self, pasos, resultados, coeficientes):
        # Crear la ventana de resultados
        results_window = Toplevel(self.root)
        results_window.title("Resultados")
        results_window.geometry("600x600")

        results_frame = Frame(results_window)
        results_frame.pack(fill="both", expand=True)

        output_text = Text(results_frame, height=10)
        output_text.pack(fill="both", expand=True)

        scrollbar = Scrollbar(output_text)
        scrollbar.pack(side="right", fill="y")
        output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=output_text.yview)

        # Mostrar los pasos y la matriz original
        output_text.insert("end", "Pasos a realizar:\n")
        for i, paso in enumerate(pasos):
            output_text.insert("end", f"Paso {i+1}:\n")
            output_text.insert("end", self.matriz_a_texto(paso, coeficientes) + "\n\n")

        # Mostrar los resultados
        output_text.insert("end", "Resultados:\n")
        for i, resultado in enumerate(resultados):
            output_text.insert("end", f"x{i+1} = {resultado}\n")

    @staticmethod
    def matriz_a_texto(matriz, coeficientes):
        texto = ""
        for i, fila in enumerate(matriz):
            for j, elemento in enumerate(fila):
                if j == len(fila) - 1:
                    texto += f" | {elemento}"
                else:
                    texto += f"{elemento} "
            texto += f"\n"
        return texto


solver = GaussJordanSolver()
solver.root.mainloop()
