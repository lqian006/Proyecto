


import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from node import *
from test_graph import *
from graph import *

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Viewer")
        self.graph = None
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.root)
        self.canvas.get_tk_widget().pack()
        self.node_var = tk.StringVar()
        self.node_dropdown = None

def create_widgets(app):
    btn_frame = tk.Frame(app.root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Show Graph 1", command=lambda: load_graph1(app)).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Show Graph 2", command=lambda: load_graph2(app)).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Load from File", command=lambda: load_from_file(app)).grid(row=0, column=2, padx=5)

    app.node_dropdown = ttk.Combobox(app.root, textvariable=app.node_var, state='readonly')
    app.node_dropdown.pack(pady=5)
    app.node_dropdown.bind("<<ComboboxSelected>>", lambda e: show_neighbors(app))


def update_dropdown(app):
    if app.graph:
        names = [node.name for node in app.graph.nodes]
        app.node_dropdown['values'] = names
        if names:
            app.node_dropdown.current(0)


def draw_graph(app, draw_function, *args):
    app.ax.clear()
    draw_function(app.graph, *args)
    app.canvas.draw()


def load_graph1(app):
    app.graph = CreateGraph_1()
    update_dropdown(app)
    draw_graph(app, Plot)


def load_graph2(app):
    app.graph = CreateGraph_2()
    update_dropdown(app)
    draw_graph(app, Plot)


def load_from_file(app):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        app.graph = LoadGraphFromFile(file_path)
        if app.graph:
            update_dropdown(app)
            draw_graph(app, Plot)
        else:
            messagebox.showerror("Error", "Could not load graph from file.")


def show_neighbors(app):
    name = app.node_var.get()
    if app.graph and name:
        result = PlotNode(app.graph, name)
        if result:
            app.ax.clear()
            PlotNode(app.graph, name)
            app.canvas.draw()
        else:
            messagebox.showerror("Error", f"Node '{name}' not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    create_widgets(app)
    root.mainloop()

ventana = tk.Tk()
ventana.title("Editor de Grafos")

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack()

G = Graph()
modo = None
nodo_temp = None

def actualizar_grafo():
    ax.clear()
    Plot(G)
    canvas.draw()

def nuevo_grafo():
    global G
    G = Graph()
    actualizar_grafo()

def guardar_grafo():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt")
    if archivo:
        SaveGraphToFile(G, archivo)

def seleccionar_modo_agregar_nodo():
    global modo
    modo = "agregar_nodo"
    messagebox.showinfo("Modo", "Haz clic en el grafo para añadir un nodo.")

def seleccionar_modo_eliminar_nodo():
    global modo
    modo = "eliminar_nodo"
    messagebox.showinfo("Modo", "Haz clic en un nodo para eliminarlo.")

def seleccionar_modo_agregar_segmento():
    global modo, nodo_temp
    modo = "agregar_segmento"
    nodo_temp = None
    messagebox.showinfo("Modo", "Selecciona dos nodos consecutivos para conectar.")

def obtener_nodo_mas_cercano(x, y):
    return GetClosest(G, x, y)


def click_en_canvas(event):
    global nodo_temp
    if modo == "agregar_nodo":
        nombre = simpledialog.askstring("Nombre del nodo", "Introduce el nombre del nodo:")
        if nombre:
            AddNode(G, Node(nombre, event.xdata, event.ydata))
            actualizar_grafo()

    elif modo == "eliminar_nodo":
        n = GetClosest(G, event.xdata, event.ydata)
        if n:
            DeleteNode(G, n.name)
            actualizar_grafo()

    elif modo == "agregar_segmento":
        n = GetClosest(G, event.xdata, event.ydata)
        if nodo_temp is None:
            nodo_temp = n
        else:
            nombre = f"{nodo_temp.name}_{n.name}"
            AddSegment(G, nombre, nodo_temp.name, n.name)
            nodo_temp = None
            actualizar_grafo()

canvas.mpl_connect('button_press_event', click_en_canvas)


frame = tk.Frame(ventana)
frame.pack()


tk.Button(frame, text="Nuevo grafo", command=nuevo_grafo).pack(side=tk.LEFT)
tk.Button(frame, text="Guardar grafo", command=guardar_grafo).pack(side=tk.LEFT)
tk.Button(frame, text="Añadir nodo", command=seleccionar_modo_agregar_nodo).pack(side=tk.LEFT)
tk.Button(frame, text="Eliminar nodo", command=seleccionar_modo_eliminar_nodo).pack(side=tk.LEFT)
tk.Button(frame, text="Añadir segmento", command=seleccionar_modo_agregar_segmento).pack(side=tk.LEFT)


ventana.mainloop()
