import tkinter as tk
from tkinter import ttk, messagebox

from test_graph import *
from graph import *
from node import *
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

modo_click = None
segmento_click = []


grafo1 = CreateGraph_1()
grafo2 = CreateGraph_2()
grafo3 = CreateGraph_3()
grafo4 = Graph()


grafos = {"Grafo 1 (Step 3)": grafo1, "Grafo 2 (Inventado)": grafo2, "Grafo 3 (Desde fichero)": grafo3, "Grafo 4 (Personal)": grafo4}
g = grafo1  # grafo por defecto


def seleccionar_grafo(event):
    global g
    seleccion = combo_grafos.get()
    g = grafos[seleccion]



def mostrar_vecinos():
    nodo = entry_vecino.get().strip()
    if nodo:
        fig, ax = plt.subplots()
        PlotNode(g, nodo)
        canvas_actual = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas_widget = canvas_actual.get_tk_widget()
        canvas_widget.config(width=700, height=600)
        canvas_widget.grid(row=0, column=1)

        canvas_actual.draw()


def añadir_nodo():
    nombre = entry_nombre.get().strip()
    try:
        x = float(entry_x.get().strip())
        y = float(entry_y.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Coordenadas inválidas")
        return

    if nombre:
        AddNode(g, Node(nombre, x, y))
        mostrar_grafo()


def añadir_nodo_manualmente():
    global modo_click
    modo_click = "nodo"
    messagebox.showinfo("Modo activado", "Haz clic en el gráfico para añadir un nodo")


def añadir_segmento_manualmente():
    global modo_click, segmento_click
    modo_click = "segmento"
    segmento_click.clear()
    messagebox.showinfo("Modo activado", "Haz clic en dos nodos para crear un segmento")


def añadir_segmento():
    origen = entry_origen.get().strip()
    destino = entry_destino.get().strip()
    if origen and destino:
        AddSegment(g, origen + destino, origen, destino)
        mostrar_grafo()


def eliminar_nodo():
    nombre = entry_borrar.get().strip()
    if nombre:
        DeleteNode(g, nombre)
        mostrar_grafo()

def on_click(event):
    global modo_click, segmento_click

    if not event.inaxes:
        return

    x = event.xdata
    y = event.ydata

    if modo_click == "nodo":
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Nombre requerido", "Por favor, escribe un nombre para el nodo antes de hacer clic.")
            return
        AddNode(g, Node(nombre, x, y))
        entry_nombre.delete(0, tk.END)
        mostrar_grafo()

    elif modo_click == "segmento":
        nodo_clicado = GetClosest(g, x, y)
        if nodo_clicado:
            segmento_click.append(nodo_clicado.name)
            if len(segmento_click) == 2:
                origen, destino = segmento_click
                AddSegment(g, origen + destino, origen, destino)
                segmento_click.clear()
                mostrar_grafo()


def mostrar_grafo():
    fig, ax = plt.subplots()
    Plot(g)
    canvas_actual=FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas_actual.get_tk_widget()
    canvas_widget.config(width=700, height=600)
    canvas_widget.grid(row=0, column=1)

    canvas_actual.mpl_connect("button_press_event", on_click)

    canvas_actual.draw()


def cargar_grafo_desde_fichero():
    global g
    nombre_archivo = entry_guardar.get().strip()

    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"

    grafo_cargado = LoadGraphFromFile(nombre_archivo)

    if grafo_cargado:
        g = grafo_cargado
        grafos["Grafo 4 (Personal)"] = g
        mostrar_grafo()
    else:
        messagebox.showerror("Error", f"No se pudo cargar el archivo {nombre_archivo}")


def guardar_grafo():
    nombre_archivo = entry_guardar.get().strip()
    if not nombre_archivo:
        nombre_archivo = "grafo_guardado.txt"
    if not nombre_archivo.endswith(".txt"):
        nombre_archivo += ".txt"
    SaveGraphToFile(g, nombre_archivo)
    messagebox.showinfo("Guardado", f"Grafo guardado en {nombre_archivo}")



# --------- INTERFAZ ---------
root = tk.Tk()
root.title("Editor de Grafos")
root.geometry("1150x780")

root.columnconfigure(0,weight=1)
root.columnconfigure(1, weight=10)

button_graph_frame = tk.LabelFrame(root, text="Opciones")
button_graph_frame.grid(row=0, column=0, padx=20, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

for i in range(100):
    button_graph_frame.rowconfigure(i, weight=1)

button_graph_frame.columnconfigure(0, weight=1)


# Selector de grafo
tk.Label(button_graph_frame, text="Selecciona un grafo").grid(row=0, column=0, padx=5, pady=2, sticky=tk.N +tk.E +tk.W +tk.S)
combo_grafos = ttk.Combobox(button_graph_frame, values=list(grafos.keys()))
combo_grafos.set("Grafo 1 (Step 3)")
combo_grafos.grid(row=1, column=0, padx=50, pady=2, sticky=tk.N +tk.E +tk.W +tk.S)
combo_grafos.bind("<<ComboboxSelected>>", seleccionar_grafo)

# Mostrar grafo
tk.Button(button_graph_frame, text="Mostrar grafo", command=mostrar_grafo).grid(row=2, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

# Vecinos
tk.Label(button_graph_frame, text="Ver vecinos de nodo:").grid(row=3, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_vecino = tk.Entry(button_graph_frame)
entry_vecino.grid(row=4, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
tk.Button(button_graph_frame, text="Ver vecinos", command=mostrar_vecinos).grid(row=5, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

# Añadir nodo
tk.Label(button_graph_frame, text="Añadir nodo (Nombre, X, Y):").grid(row=6, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_nombre = tk.Entry(button_graph_frame)
entry_nombre.grid(row=7, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_x = tk.Entry(button_graph_frame)
entry_x.grid(row=8, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_y = tk.Entry(button_graph_frame)
entry_y.grid(row=9, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
tk.Button(button_graph_frame, text="Añadir nodo", command=añadir_nodo).grid(row=10, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

tk.Button(button_graph_frame, text="Añadir nodo manualmente", command=añadir_nodo_manualmente).grid(row=11, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)



# Añadir segmento
tk.Label(button_graph_frame, text="Añadir segmento (Origen, Destino):").grid(row=12, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_origen = tk.Entry(button_graph_frame)
entry_origen.grid(row=13, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_destino = tk.Entry(button_graph_frame)
entry_destino.grid(row=14, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
tk.Button(button_graph_frame, text="Añadir segmento", command=añadir_segmento).grid(row=15, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

tk.Button(button_graph_frame, text="Añadir segmento manualmente", command=añadir_segmento_manualmente).grid(row=16, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)



# Eliminar nodo
tk.Label(button_graph_frame, text="Eliminar nodo:").grid(row=17, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_borrar = tk.Entry(button_graph_frame)
entry_borrar.grid(row=18, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
tk.Button(button_graph_frame, text="Eliminar nodo", command=eliminar_nodo).grid(row=19, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

# Guardar grafo
tk.Label(button_graph_frame, text="Escribe el nombre del fichero:").grid(row=20, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
entry_guardar = tk.Entry(button_graph_frame)
entry_guardar.grid(row=21, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)
tk.Button(button_graph_frame, text="Guardar grafo", command=guardar_grafo).grid(row=22, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

tk.Button(button_graph_frame, text="Cargar grafo desde fichero", command=cargar_grafo_desde_fichero).grid(row=23, column=0, padx=50, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)



# --- PARTE DERECHA DE LA INTERFAZ ---

graph_frame = tk.LabelFrame(root, text="Grafo")
graph_frame.grid(row=0, column=1, rowspan=1, padx=20, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

graph_frame.rowconfigure(0, weight=1)
graph_frame.rowconfigure(1, weight=1)
graph_frame.columnconfigure(0, weight=1)



root.mainloop()



