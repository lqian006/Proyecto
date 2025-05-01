import tkinter as tk
from tkinter import ttk, messagebox
from test_graph import *
from graph import *
from node import *
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent

grafo1 = CreateGraph_1()
grafo2 = CreateGraph_2()
grafo3 = CreateGraph_3()
grafo4 = Graph()


grafos = {"Grafo 1 (Step 3)": grafo1, "Grafo 2 (Inventado)": grafo2, "Grafo 3 (Desde fichero)": grafo3, "Grafo 4 (Personal)": grafo4}
grafo_actual = grafo1  # grafo por defecto

def on_click(event):
    if event.inaxes:
        x, y= event.xdata, event.ydata
        messagebox.showinfo("Coordenadas del clic", f"Has clicado en:({x:.2f}, {y:.2f})")



def seleccionar_grafo(event):
    global grafo_actual
    seleccion = combo_grafos.get()
    grafo_actual = grafos[seleccion]


def mostrar_vecinos():
    nodo = entry_vecino.get().strip()
    if nodo:
        PlotNode(grafo_actual, nodo)


def añadir_nodo():
    nombre = entry_nombre.get().strip()
    try:
        x = float(entry_x.get().strip())
        y = float(entry_y.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Coordenadas inválidas")
        return

    if nombre:
        AddNode(grafo_actual, Node(nombre, x, y))


def añadir_segmento():
    origen = entry_origen.get().strip()
    destino = entry_destino.get().strip()
    if origen and destino:
        AddSegment(grafo_actual, origen + destino, origen, destino)


def eliminar_nodo():
    nombre = entry_borrar.get().strip()
    if nombre:
        DeleteNode(grafo_actual, nombre)


def mostrar_grafo():
    Plot(grafo_actual)


def guardar_grafo():
    nombre_archivo = entry_guardar.get().strip()
    if not nombre_archivo:
        nombre_archivo = "grafo_guardado.txt"
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"
    SaveGraphToFile(grafo_actual, nombre_archivo)
    messagebox.showinfo("Guardado", f"Grafo guardado en {nombre_archivo}")

def CambioColor():
    plt.figure()

    if not grafo_actual.nodes:
        return

    # Calcular el centro horizontal del grafo

    min_x = min(node.x for node in grafo_actual.nodes)
    max_x = max(node.x for node in grafo_actual.nodes)
    centro = (min_x + max_x) / 2


    for segment in grafo_actual.segments:
        if segment.origin.x < centro:
            color = "red"
        else:
            color = "black"

        x_values = [segment.origin.x, segment.destination.x]
        y_values = [segment.origin.y, segment.destination.y]
        plt.plot(x_values, y_values, color)

        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        plt.text(mid_x, mid_y, f"{segment.cost:.1f}", fontsize=8, ha="center")


    for node in grafo_actual.nodes:
        plt.plot(node.x, node.y, "ko")
        plt.text(node.x, node.y, node.name, fontsize=9, ha="right", va="bottom")

    plt.title("Segmentos con origen a la izquierda están en rojo")
    plt.axis("equal")
    plt.grid(True)
    plt.show()



# --------- INTERFAZ ---------
root = tk.Tk()
root.title("Editor de Grafos")
root.geometry("600x700")

# Selector de grafo
tk.Label(root, text="Selecciona un grafo:").pack()
combo_grafos = ttk.Combobox(root, values=list(grafos.keys()))
combo_grafos.set("Grafo 1 (Step 3)")
combo_grafos.pack(pady=5)
combo_grafos.bind("<<ComboboxSelected>>", seleccionar_grafo)

# Mostrar grafo
tk.Button(root, text="Mostrar grafo", command=mostrar_grafo).pack(pady=5)

# Vecinos
tk.Label(root, text="Ver vecinos de nodo:").pack()
entry_vecino = tk.Entry(root)
entry_vecino.pack()
tk.Button(root, text="Ver vecinos", command=mostrar_vecinos).pack(pady=5)

# Añadir nodo
tk.Label(root, text="Añadir nodo (Nombre, X, Y):").pack()
entry_nombre = tk.Entry(root)
entry_nombre.pack()
entry_x = tk.Entry(root)
entry_x.pack()
entry_y = tk.Entry(root)
entry_y.pack()
tk.Button(root, text="Añadir nodo", command=añadir_nodo).pack(pady=5)

# Añadir segmento
tk.Label(root, text="Añadir segmento (Origen, Destino):").pack()
entry_origen = tk.Entry(root)
entry_origen.pack()
entry_destino = tk.Entry(root)
entry_destino.pack()
tk.Button(root, text="Añadir segmento", command=añadir_segmento).pack(pady=5)

# Eliminar nodo
tk.Label(root, text="Eliminar nodo:").pack()
entry_borrar = tk.Entry(root)
entry_borrar.pack()
tk.Button(root, text="Eliminar nodo", command=eliminar_nodo).pack(pady=5)

# Guardar grafo
tk.Label(root, text="Guardar grafo como (.txt):").pack()
entry_guardar = tk.Entry(root)
entry_guardar.insert(0, "grafo_guardado")
entry_guardar.pack()
tk.Button(root, text="Guardar grafo", command=guardar_grafo).pack(pady=10)

# Cambiar color
tk.Button(root, text="Cambiar color de segmentos izquierdos", command=CambioColor).pack(pady=5)

root.mainloop()
