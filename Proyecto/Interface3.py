import tkinter as tk
from tkinter import messagebox
from test_graph import *
from graph import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg







grafo1 = None
grafo2 = None
grafo3 = None



def mostrar_vecinos(grafo):
    nodo = simpledialog.askstring("Mostrar vecinos", "Introduce el nombre del nodo:")
    if nodo:
        PlotNode(grafo, nodo)

def mostrar_grafo1():
    global grafo1
    grafo1 = CreateGraph_1()
    Plot(grafo1)
    mostrar_vecinos(grafo1)

def añadir_nodo_g1():
    nombre = simpledialog.askstring("Añadir nodo", "Nombre del nodo:")
    x = simpledialog.askfloat("Añadir nodo", "Coordenada X:")
    y = simpledialog.askfloat("Añadir nodo", "Coordenada Y:")
    if nombre and x is not None and y is not None:
        AddNode(grafo1, Node(nombre, x, y))

def añadir_segmento_g1():
    origen = simpledialog.askstring("Segmento", "Nodo origen:")
    destino = simpledialog.askstring("Segmento", "Nodo destino:")
    if origen and destino:
        AddSegment(grafo1, origen + destino, origen, destino)

def eliminar_nodo_g1():
    nombre = simpledialog.askstring("Eliminar nodo", "Nombre del nodo:")
    if nombre:
        DeleteNode(grafo1, nombre)

# --- Funciones grafo 2 ---
def mostrar_grafo2():
    global grafo2
    grafo2 = CreateGraph_2()
    Plot(grafo2)
    mostrar_vecinos(grafo2)

def añadir_nodo_g2():
    nombre = simpledialog.askstring("Añadir nodo", "Nombre del nodo:")
    x = simpledialog.askfloat("Añadir nodo", "Coordenada X:")
    y = simpledialog.askfloat("Añadir nodo", "Coordenada Y:")
    if nombre and x is not None and y is not None:
        AddNode(grafo2, Node(nombre, x, y))

def añadir_segmento_g2():
    origen = simpledialog.askstring("Segmento", "Nodo origen:")
    destino = simpledialog.askstring("Segmento", "Nodo destino:")
    if origen and destino:
        AddSegment(grafo2, origen + destino, origen, destino)

def eliminar_nodo_g2():
    nombre = simpledialog.askstring("Eliminar nodo", "Nombre del nodo:")
    if nombre:
        DeleteNode(grafo2, nombre)

# --- Funciones grafo 3 ---
def mostrar_grafo3():
    global grafo3
    grafo3 = CreateGraph_3()
    Plot(grafo3)
    mostrar_vecinos(grafo3)

def añadir_nodo_g3():
    nombre = simpledialog.askstring("Añadir nodo", "Nombre del nodo:")
    x = simpledialog.askfloat("Añadir nodo", "Coordenada X:")
    y = simpledialog.askfloat("Añadir nodo", "Coordenada Y:")
    if nombre and x is not None and y is not None:
        AddNode(grafo3, Node(nombre, x, y))

def añadir_segmento_g3():
    origen = simpledialog.askstring("Segmento", "Nodo origen:")
    destino = simpledialog.askstring("Segmento", "Nodo destino:")
    if origen and destino:
        AddSegment(grafo3, origen + destino, origen, destino)

def eliminar_nodo_g3():
    nombre = simpledialog.askstring("Eliminar nodo", "Nombre del nodo:")
    if nombre:
        DeleteNode(grafo3, nombre)

def mostrar_grafo4():
    Plot(grafo4)
    mostrar_vecinos(grafo4)

def añadir_nodo_g4():
    nombre = simpledialog.askstring("Añadir nodo", "Nombre del nodo:")
    x = simpledialog.askfloat("Añadir nodo", "Coordenada X:")
    y = simpledialog.askfloat("Añadir nodo", "Coordenada Y:")
    if nombre and x is not None and y is not None:
        AddNode(grafo4, Node(nombre, x, y))

def añadir_segmento_g4():
    origen = simpledialog.askstring("Segmento", "Nodo origen:")
    destino = simpledialog.askstring("Segmento", "Nodo destino:")
    if origen and destino:
        AddSegment(grafo4, origen + destino, origen, destino)

def eliminar_nodo_g4():
    nombre = simpledialog.askstring("Eliminar nodo", "Nombre del nodo:")
    if nombre:
        DeleteNode(grafo4, nombre)



def Grafo1():
    G = CreateGraph_1()
    Plot(G)
    mostrar_vecinos(G)

def Grafo2():
    G=CreateGraph_2()
    Plot(G)
    mostrar_vecinos(G)

def Grafo_Datos():
    G = CreateGraph_3()
    Plot(G)
    mostrar_vecinos(G)

def mostrar_vecinos(grafo):
    nodo = simpledialog.askstring("Mostrar vecinos", "Introduce el nombre del nodo al que le quieras ver sus vecinos:")
    PlotNode(grafo, nodo)

#----------INTERFAZ----------#

root = tk.Tk()
root.title("Visor de Grafos")
root.geometry("600x700")

# FRAME GRAFO 1
frame1 = tk.LabelFrame(root, text="Step 3: Grafo base")
frame1.pack(fill="both", expand=True, padx=10, pady=5)

tk.Button(frame1, text="Mostrar", command=mostrar_grafo1).pack(pady=3)
tk.Button(frame1, text="Añadir nodo", command=añadir_nodo_g1).pack(pady=3)
tk.Button(frame1, text="Añadir segmento", command=añadir_segmento_g1).pack(pady=3)
tk.Button(frame1, text="Eliminar nodo", command=eliminar_nodo_g1).pack(pady=3)

# FRAME GRAFO 2
frame2 = tk.LabelFrame(root, text="Step 3: Grafo inventado")
frame2.pack(fill="both", expand=True, padx=10, pady=5)

tk.Button(frame2, text="Mostrar", command=mostrar_grafo2).pack(pady=3)
tk.Button(frame2, text="Añadir nodo", command=añadir_nodo_g2).pack(pady=3)
tk.Button(frame2, text="Añadir segmento", command=añadir_segmento_g2).pack(pady=3)
tk.Button(frame2, text="Eliminar nodo", command=eliminar_nodo_g2).pack(pady=3)

# FRAME GRAFO 3
frame3 = tk.LabelFrame(root, text="Grafo cargado desde fichero")
frame3.pack(fill="both", expand=True, padx=10, pady=5)

tk.Button(frame3, text="Mostrar", command=mostrar_grafo3).pack(pady=3)
tk.Button(frame3, text="Añadir nodo", command=añadir_nodo_g3).pack(pady=3)
tk.Button(frame3, text="Añadir segmento", command=añadir_segmento_g3).pack(pady=3)
tk.Button(frame3, text="Eliminar nodo", command=eliminar_nodo_g3).pack(pady=3)


# FRAME GRAFO 4

grafo4 = Graph()
frame4 = tk.LabelFrame(root, text="Crear tu propio grafo")
frame4.pack(fill="both", expand=True, padx=10, pady=5)

# Mostrar grafo
tk.Button(frame4, text="Mostrar", command=lambda: [Plot(grafo4), mostrar_vecinos_entrada()]).pack(pady=3)


# Añadir nodo
tk.Label(frame4, text="Añadir nodo (Nombre, X, Y):").pack()
entry_nombre_4 = tk.Entry(frame4)
entry_nombre_4.pack()
entry_x_4 = tk.Entry(frame4)
entry_x_4.pack()
entry_y_4 = tk.Entry(frame4)
entry_y_4.pack()

def añadir_nodo_entrada():
    nombre = entry_nombre_4.get().strip()
    try:
        x = float(entry_x_4.get().strip())
        y = float(entry_y_4.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Coordenadas inválidas")
        return
    if nombre:
        AddNode(grafo4, Node(nombre, x, y))

tk.Button(frame4, text="Añadir nodo", command=añadir_nodo_entrada).pack(pady=3)

# Añadir segmento
tk.Label(frame4, text="Añadir segmento (Origen, Destino):").pack()
entry_origen_4 = tk.Entry(frame4)
entry_origen_4.pack()
entry_destino_4 = tk.Entry(frame4)
entry_destino_4.pack()

def añadir_segmento_entrada():
    origen = entry_origen_4.get().strip()
    destino = entry_destino_4.get().strip()
    if origen and destino:
        AddSegment(grafo4, origen + destino, origen, destino)

tk.Button(frame4, text="Añadir segmento", command=añadir_segmento_entrada).pack(pady=3)

# Eliminar nodo
tk.Label(frame4, text="Eliminar nodo:").pack()
entry_eliminar_4 = tk.Entry(frame4)
entry_eliminar_4.pack()

def eliminar_nodo_entrada():
    nombre = entry_eliminar_4.get().strip()
    if nombre:
        DeleteNode(grafo4, nombre)

tk.Button(frame4, text="Eliminar nodo", command=eliminar_nodo_entrada).pack(pady=3)

root.mainloop()