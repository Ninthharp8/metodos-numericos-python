
#! Librerias 
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import pandas as pd
import math 
   
#! Funcion que grafica 3 tipos de ecuaciones
def allplot(FX, raiz=None, GX=None,a=None,b=None): #fx y gx son funciones a graficar. raiz es la raiz de fx o gx. a y b son el rango para calcular los pts.
    
    if a is not None and b is not None:
        xpts = np.linspace(a, b, 1000)
    else:
        xpts = np.linspace(-10, 10, 1000)
    
    if isinstance(FX, str): # si es FX un string
        
        fx_expr = sp.sympify(FX)
        f = sp.lambdify('x', fx_expr, modules=['numpy'])
    elif callable(FX): # si es FX == lambda x: x**3 #+ 3*x**2 + 12*x + 8
        f = FX
    else:# si es FX = x**3 + 3*x**2 + 12*x + 8
        f = sp.lambdify('x', FX, 'numpy')
    y = f(xpts)
    plt.figure(figsize=(8, 6))
    plt.plot(xpts, y, label="F(x)")
    plt.axvline(0, 0, color='black', linewidth=2, linestyle='--')
    plt.axhline(0, 0, color='black', linewidth=2, linestyle='--')
    
    #* esto es si tenemos una funcion extra y una raiz
    if GX is not None:
        if isinstance(GX, str):
            #y2 = eval(GX, {'x': xpts,**vars(np)})
            gx_expr = sp.sympify(GX)
            g = sp.lambdify('x', gx_expr, modules=['numpy']) 
        elif callable(GX):
            g = GX
        else:
            g = sp.lambdify('x', GX, 'numpy')
        y2 = g(xpts)
        plt.plot(xpts, y2, label="G(x)")
    #* si tenemos raiz 
    if raiz is not None:
        plt.scatter(raiz, 0, color='red', zorder=5, label='Raíz')
        plt.annotate(round(raiz, 9), xy=(raiz, 0.5), color='red')
    #* imprimimos labels, cuadriculas,titulos, y la grafica
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend(loc=2)
    plt.grid(True)
    plt.ylim(-15, 15)  # Ajusta los límites del eje y según los valores de la función
    plt.title('Gráfico de la función y la raíz encontrada')
    plt.show()

def biseccion(funcion, bajo, alto, epsilon,IteracionesMAX):
    #* comparamos en que lado del rango proceder
    if funcion(bajo) * funcion(alto) >= 0: #f(a)*f(b)<0
        return None,[]
    #* definimos un array para alacenar las operaciones
    valores = []
    contador = 1
    while abs(alto - bajo) >= epsilon and contador < IteracionesMAX:
        #*partimos el rango
        medio = (alto + bajo) / 2
        #* evaluamos f(c)=0
        if funcion(medio) == 0:
            return medio, valores
        #* como no estamos en la raiz vemos para que lado del rango nos vamos
        elif funcion(medio) * funcion(bajo) < 0:
            alto = medio
        else:
            bajo = medio
        #* calculamos la raiz
        R = (alto + bajo) / 2
        #* agregamos al array de valores las raices y las mismas.
        valores.append((contador,bajo,alto, R))
        #* revisamos si debemos detenernos
        contador +=1
        #if contador>=IteracionesMAX:print("\nSe detuvo por iteraciones"); break

    if R == None: print(f"\nLa raiz no esta en el intervalo\n") 
    else: print(f"\n la raiz esta en {R}")

    #se grafica los resultados
    print("\nGraficando función")
    allplot(funcion,R)

def punto_fijo(funcion,a,epsilon,MaxIter,FX):
    #* iniciamos un array para almacenar los valores
    valores = []
    #* asignamos valores de g(x) y b = g(a)
    g = funcion
    b = g(a)
    #* los agregamos al array
    valores = [((0,a,b,epsilon))]
    #* inicializamos valores de paro.
    iteraciones = 1
    error = epsilon
    #* iniciamos el metodo de punto fijo
    while (error >= epsilon) and (iteraciones < MaxIter):
        a = b
        b = g(a) 
        valores.append((iteraciones,a,b,error))
        error = abs(b-a)
        iteraciones += 1

    #  imprimimos la raiz
    print(f"\nla raiz es :{b}")
    #  llamamos a mi funcion para graficar FX y GX y el punto raiz
    allplot(FX,b,funcion,0,100)

def newton_raphson(funcion, x0, epsilon, max_iter):
    #* definimos el simbolo de la funcion
    x = sp.Symbol('x') 
    #* definimos que f sera la funcion a usar por sympy osea quitamos las comillas
    f = sp.sympify(funcion)
    #* usamos la funcion de sympy para calcular la derivada respecto a x
    df = f.diff(x) 
    #* inicializamos las iteraciones
    iteraciones = 0
    #* asignamo x_{n-1}=X0
    x_prev = x0
    #* definimos un array donde almacenaremos los resultados las operaciones e inicializamos el error.
    resultado = [(iteraciones, x_prev, f.subs(x, x_prev))]
    error = epsilon
    #* implementamos newton raphson que se ejecutara hasta que se excedan las iteraciones o el error.
   
    for iteraciones in range(1,max_iter+1):
        x_next = x_prev - f.subs(x, x_prev) / df.subs(x, x_prev)  #f.sub(x, x_next) significa evaluar la funcion f respecto de x con el valor de x_next
        #* aumentamos las iteraciones y calculamos el error 
        error = abs(x_next - x_prev)
        #* agregamos los resultados al array
        resultado.append((iteraciones, x_next, f.subs(x, x_next)))
        #* asignamos la nueva x0
        x_prev = x_next
        #* calculamos el error
        if error < epsilon:break
    # imprimimos en terminal la raiz y la derivada
    print(f"\nla raiz esta en :{x_next}\n")
    derivada = str(df)
    print(f" y su derivada es : {derivada}") 
    # graficamos la funcion, la raiz y la derivada
    allplot(funcion,x_next,derivada)

def secante(f, x0, x1, epsilon, max_iter):
    error = epsilon
    iteraciones = 1
    x_prev = x0
    x_n = x1
    valores = [(iteraciones, x_prev, x_n)]

    while error >= epsilon and iteraciones < max_iter:
        x_next = x_n - (f(x_n) * (x_n - x_prev)) / (f(x_n) - f(x_prev))
        valores.append((iteraciones, x_n, x_next))
        error = abs(f(x_n) - f(x_prev))
        iteraciones += 1
        x_prev = x_n
        x_n = x_next

    print(f"\n la raiz es =  {x_next}")
    #todo Graficamos la funcion y el resultado
    allplot(f,x_next)

if __name__ == "__main__":
    print("Modulos compilados")

    