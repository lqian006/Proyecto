from test_graph import*
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def Grafo3():
    CreateGraph_2()

def Grafo2():
    CreateGraph_1()

def show_Grafo3():
    Grafo3()

def show_Grafo2():
    Grafo2()

def show_text():
    messagebox.showinfo("Texto introducido: ")

root=tk.Tk()
root.geometry("800x400")
root.title("Ejemplo de formulario")

root.columnconfigure(0,weight=1)
root.columnconfigure(1, weight=10)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

button_graph_frame = tk.LabelFrame(root, text="Gráficos")
button_graph_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

button_graph_frame.rowconfigure(0, weight=1)
button_graph_frame.rowconfigure(1, weight=1)
button_graph_frame.columnconfigure(0, weight=1)

button1 = tk.Button(button_graph_frame, text="Mostrar grafo del step 3",command = show_Grafo3)
button1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

button2=tk.Button(button_graph_frame, text="Mostrar nuestro grafo del step 3",command = show_Grafo2)
button2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S))


