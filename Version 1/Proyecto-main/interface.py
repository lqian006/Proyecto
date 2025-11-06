import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from airport import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# --------- FUNCIONES ---------

# VERSIÓN 1

def Load_airports():

    # Aquí está para que lea los datos y los interprete
    filename=entry_filename.get().strip()
    if not filename:
        messagebox.showwarning("Advertencia", "Escriba un nombre del fichero.")
        return
    try:
        airports=LoadAirports(filename)
    except FileNotFoundError:
        messagebox.showerror("Error",f"No se encontró el archivo '{filename}'.")
        return

    # Ahora vamos a generar el plot
    fig, ax = plt.subplots()
    ax.set_title("Aeropuertos")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")

    xs = [a.lon for a in airports]
    ys = [a.lat for a in airports]
    ax.scatter(xs, ys, c='blue', marker='o')
    for a in airports:
        ax.text(a.lon, a.lat, a.code, fontsize=8)

    for widget in picture_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def Add_Airports():


# --------- INTERFAZ ---------

root = tk.Tk()
root.title("Interface")
root.geometry("900x500")

root.columnconfigure(0, weight=1) #columna 1 para los botones
root.columnconfigure(1, weight=10) #columna 2 para los gráficos
root.rowconfigure(0, weight=1) #fila 1
#Para añadir más filas es: root.rowconfigure((1,2,3, etc), weight=1)

#-----COLUMNA [0], FILA [0] (Botones)
button_frame=tk.LabelFrame(root, text= 'Botones')
button_frame.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW) #Definimos el espacio entre botones

#-----COLUMNA [1], FILA [0]
picture_frame=tk.LabelFrame(root, text='Gráfico')
picture_frame.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NSEW)
picture_frame.columnconfigure(0,weight=1)
picture_frame.rowconfigure(0, weight=1)

#Definimos que dentro de este frame tiene una columna y dos filas
label_filename = tk.Label(button_frame, text="Nombre del fichero en .txt:")
label_filename.pack(padx=5, pady=5)

entry_filename = tk.Entry(button_frame, width=30)
entry_filename.pack(padx=5, pady=5)
entry_filename.bind("<Return>", lambda event: Load_airports())  # Enter para ejecutar

# BOTONES

# Botón para cargar grafo
button1=tk.Button(button_frame, text='Load airports',command=Load_airports)
button1.pack(padx=5, pady=10, fill=tk.X)

# Botón para

button2=tk.Button(button_frame, text='Add airports',command=None)
button3=tk.Button(button_frame, text='Delete airports',command=None)
button4=tk.Button(button_frame, text='Set Schengen attribute to airports',command=None)
button5=tk.Button(button_frame, text='Show data of airports in the list',command=None)
button6=tk.Button(button_frame, text='Save Schengen airports in file',command=None)
button7=tk.Button(button_frame, text='Plot Schengen airports in a stacked bar',command=None)
button8=tk.Button(button_frame, text='Load airports',command=None)
button9=tk.Button(button_frame, text='Load airports',command=None)


root.mainloop()