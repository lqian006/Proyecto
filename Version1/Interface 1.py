import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
from node import *
from segment import*
from test_graph import *
from graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def Grafo1():
    G = CreateGraph_1()
    Plot(G)

def Grafo2():
    G=CreateGraph_2()
    Plot(G)

def Grafo_Datos():
    G = CreateGraph_3()
    Plot(G)




root = tk.Tk()
root.title("Visor de Grafos")
root.geometry("400x400")
root.grid()

# Configurar una sola columna para toda la ventana
root.columnconfigure(0, weight=1)

# Crear un solo frame para todos los botones
button_frame = tk.LabelFrame(root, text="Opciones de gráficos")
button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Configurar la columna del frame
button_frame.columnconfigure(0, weight=1)

# Botón 1
button1 = tk.Button(button_frame, text="(1) Mostrar grafo del Step 3", command=Grafo1)
button1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Botón 2
button2 = tk.Button(button_frame, text="(2) Mostrar nuestro grafo del Step 3", command=Grafo2)
button2.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

# Botón 3
button3 = tk.Button(button_frame, text="(3) Fichero Datos", command=Grafo_Datos)
button3.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

# Botón 4
button4 = tk.Button(button_frame, text="Fichero Datos", command=Grafo_Datos)
button4.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

# Botón 5
button5 = tk.Button(button_frame, text="Fichero Datos", command=Grafo_Datos)
button5.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

# Botón 6
button6 = tk.Button(button_frame, text="Fichero Datos", command=Grafo_Datos)
button6.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

# Botón 7
button7 = tk.Button(button_frame, text="Fichero Datos", command=Grafo_Datos)
button7.grid(row=6, column=0, padx=5, pady=5, sticky="nsew")

# Botón 8
button8 = tk.Button(button_frame, text="Fichero Datos", command=Grafo_Datos)
button8.grid(row=7, column=0, padx=5, pady=5, sticky="nsew")

# Botón 9
button9 = tk.Button(button_frame, text="Fichero Datos", command=Grafo_Datos)
button9.grid(row=8, column=0, padx=5, pady=5, sticky="nsew")

# Configurar filas para que los botones se expandan

for i in range(9):
    button_frame.rowconfigure(i, weight=1)


# Mostrar la ventana
root.mainloop()