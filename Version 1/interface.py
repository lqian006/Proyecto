import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from node import *
from test_graph import *

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