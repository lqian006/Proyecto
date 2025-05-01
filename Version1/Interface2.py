from test_graph import*
import tkinter as tk
from tkinter import messagebox
import matplotlib as plt
import numpy as np




def Grafo1():
    CreateGraph_1()


def Grafo2():
    CreateGraph_2()

def Grafo_Datos():
    CreateGraph_3()

def Show_Neighbours():
    messagebox.showinfo("Texto introducido: ")



root=tk.Tk()
root.geometry("800x400")
root.title("Interfaz")

root.columnconfigure(0,weight=1)
root.columnconfigure(1, weight=10)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)

button_graph_frame = tk.LabelFrame(root, text="Graphic")
button_graph_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

button_graph_frame.rowconfigure(0, weight=1)
button_graph_frame.rowconfigure(1, weight=1)
button_graph_frame.columnconfigure(0, weight=1)

button1 = tk.Button(button_graph_frame, text="Mostrar grafo del step 3",command =Grafo1)
button1.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

button2=tk.Button(button_graph_frame, text="Mostrar nuestro grafo del step 3",command =Grafo2)
button2.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)



button_graph_frame = tk.LabelFrame(root, text="Gráficos desde un fichero")
button_graph_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

button_graph_frame.rowconfigure(0, weight=1)
button_graph_frame.rowconfigure(1, weight=1)
button_graph_frame.columnconfigure(0, weight=1)

button3 = tk.Button(button_graph_frame, text="Fichero Datos",command = Grafo_Datos)
button3.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)




button_graph_frame = tk.LabelFrame(root, text="Gráficos desde un fichero")
button_graph_frame.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)

button_graph_frame.rowconfigure(0, weight=1)
button_graph_frame.rowconfigure(1, weight=1)
button_graph_frame.columnconfigure(0, weight=1)

button3 = tk.Button(button_graph_frame, text="Fichero Datos",command = Grafo_Datos)
button3.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N +tk.E +tk.W +tk.S)


