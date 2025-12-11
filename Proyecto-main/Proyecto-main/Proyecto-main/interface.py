from LEBL import *
import tkinter as tk
from tkinter import messagebox,filedialog
import matplotlib.pyplot as plt
from airport import *
from aircraft import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import platform
import subprocess


# --------- FUNCIONES ---------

# VERSIÓN 1
def Load_airports():
    global airports  # hacemos global para reutilizarla en Add_Airports

    filename = entry_filename.get().strip()
    if not filename:
        messagebox.showwarning("Advertencia", "Escriba un nombre del fichero.")
        return

    try:
        airports = LoadAirports(filename)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo '{filename}'.")
        return

    # Crear figura
    fig, ax = plt.subplots()
    ax.set_title("Aeropuertos")
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")

    # Dibujar puntos
    xs = [a.lon for a in airports]
    ys = [a.lat for a in airports]
    colors = ['green' if a.schengen else 'red' for a in airports]
    ax.scatter(xs, ys, c=colors, marker='o')

    for a in airports:
        ax.text(a.lon, a.lat, a.code, fontsize=8)

    # Limpiar el frame de gráfico
    for widget in picture_frame.winfo_children():
        widget.destroy()

    # Crear y guardar el canvas dentro del frame
    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Guardamos la referencia del canvas
    picture_frame.canvas = canvas


def Add_Airports():
    global airports  # usamos la lista global

    # Si aún no existe la lista, inicialízala
    try:
        airports
    except NameError:
        airports = []

    # Ventana emergente para pedir datos del nuevo aeropuerto
    new_win = tk.Toplevel()
    new_win.title("Añadir aeropuerto")

    tk.Label(new_win, text="Código (ej. LEBL):").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(new_win, text="Latitud (ej. N412851):").grid(row=1, column=0, padx=5, pady=5)
    tk.Label(new_win, text="Longitud (ej. E0020500):").grid(row=2, column=0, padx=5, pady=5)

    entry_code = tk.Entry(new_win)
    entry_lat = tk.Entry(new_win)
    entry_lon = tk.Entry(new_win)
    entry_code.grid(row=0, column=1, padx=5, pady=5)
    entry_lat.grid(row=1, column=1, padx=5, pady=5)
    entry_lon.grid(row=2, column=1, padx=5, pady=5)
    entry_code.focus()  # foco inicial en código

    def confirm_add():
        code = entry_code.get().strip().upper()
        lat_str = entry_lat.get().strip().upper()
        lon_str = entry_lon.get().strip().upper()

        if not code or not lat_str or not lon_str:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        # Convertir coordenadas DMS → decimal
        try:
            lat = ConvertCoordinate(lat_str)
            lon = ConvertCoordinate(lon_str)
        except Exception:
            messagebox.showerror("Error", "Formato de coordenadas inválido. Ejemplo: N412851 o W0734640.")
            return

        # Crear el objeto aeropuerto usando Airport del módulo y SetSchengen
        new_airport = Airport(code, lat, lon)
        SetSchengen(new_airport)

        # Añadir aeropuerto usando AddAirport del módulo airport.py
        result = AddAirport(airports, new_airport)
        if result == -1:
            messagebox.showwarning("Aviso", f"El aeropuerto {code} ya existe.")
            return

        # Verificar que haya un gráfico cargado
        if not hasattr(picture_frame, 'canvas'):
            messagebox.showerror("Error", "No hay gráfico cargado aún. Use 'Load airports' primero.")
            return

        # Añadir el punto al gráfico actual
        canvas = picture_frame.canvas
        fig = canvas.figure
        ax = fig.axes[0]

        color = 'green' if new_airport.schengen else 'red'
        ax.scatter(new_airport.lon, new_airport.lat, c=color, marker='o', s=60)
        ax.text(new_airport.lon, new_airport.lat, new_airport.code, fontsize=8, color=color)

        canvas.draw()  # actualizar gráfico

        messagebox.showinfo("Éxito", f"Añadido aeropuerto {code}.")
        new_win.destroy()

    # Botón "Añadir"
    btn_add = tk.Button(new_win, text="Añadir", command=confirm_add)
    btn_add.grid(row=3, column=0, columnspan=2, pady=10)
    new_win.bind("<Return>", lambda event: confirm_add())



def Remove_Airport():
    global airports

    # Si no hay lista cargada
    try:
        airports
    except NameError:
        airports = []

    if len(airports) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados para borrar.")
        return

    # Ventana emergente para pedir el código
    new_win = tk.Toplevel()
    new_win.title("Eliminar aeropuerto")

    tk.Label(new_win, text="Código del aeropuerto (ej. LEBL):").grid(row=0, column=0, padx=5, pady=5)
    entry_code = tk.Entry(new_win)
    entry_code.grid(row=0, column=1, padx=5, pady=5)
    entry_code.focus()  # 🔹 foco inicial en código

    def confirm_remove():
        code = entry_code.get().strip().upper()
        if not code:
            messagebox.showwarning("Advertencia", "Debe introducir un código de aeropuerto.")
            return

        # Intentar eliminar el aeropuerto usando RemoveAirport del módulo
        result = RemoveAirport(airports, code)
        if result == -1:
            messagebox.showerror("Error", f"No se encontró el aeropuerto {code}.")
            return

        # Redibujar el gráfico si existe
        if hasattr(picture_frame, 'canvas'):
            canvas = picture_frame.canvas
            fig = canvas.figure
            ax = fig.axes[0]

            ax.clear()
            ax.set_title("Aeropuertos")
            ax.set_xlabel("Longitud")
            ax.set_ylabel("Latitud")

            xs = [a.lon for a in airports]
            ys = [a.lat for a in airports]
            colors = ['green' if a.schengen else 'red' for a in airports]
            ax.scatter(xs, ys, c=colors, marker='o')

            for a in airports:
                ax.text(a.lon, a.lat, a.code, fontsize=8)

            canvas.draw()

        messagebox.showinfo("Éxito", f"Aeropuerto {code} eliminado.")
        new_win.destroy()

    # Botón "Eliminar"
    btn_remove = tk.Button(new_win, text="Eliminar", command=confirm_remove)
    btn_remove.grid(row=1, column=0, columnspan=2, pady=10)

    # Permitir confirmar con Enter
    new_win.bind("<Return>", lambda event: confirm_remove())



def Print_Airport():
    global airports

    # Comprobar que haya lista cargada
    try:
        airports
    except NameError:
        airports = []

    if len(airports) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados.")
        return

    # Ventana emergente para elegir modo de visualización
    new_win = tk.Toplevel()
    new_win.title("Mostrar aeropuerto")

    tk.Label(new_win, text="Código (opcional, ej. LEBL):").grid(row=0, column=0, padx=5, pady=5)
    entry_code = tk.Entry(new_win)
    entry_code.grid(row=0, column=1, padx=5, pady=5)
    entry_code.focus()  # 🔹 foco inicial en código

    def confirm_show():
        code = entry_code.get().strip().upper()

        if not code:
            # Mostrar todos los aeropuertos usando PrintAirport del módulo
            info = ""
            for a in airports:
                PrintAirport(a)  # imprime en consola
                schengen = "Sí" if a.schengen else "No"
                info += f"{a.code}  |  Lat: {a.lat:.4f}  |  Lon: {a.lon:.4f}  |  Schengen: {schengen}\n"

            if not info:
                info = "No hay aeropuertos cargados."
            messagebox.showinfo("Lista de aeropuertos", info)
            new_win.destroy()
            return

        # Buscar aeropuerto específico
        found = None
        for a in airports:
            if a.code == code:
                found = a
                break

        if not found:
            messagebox.showerror("Error", f"No se encontró el aeropuerto {code}.")
            return

        # Mostrar usando PrintAirport del módulo (opcional)
        PrintAirport(found)

        schengen = "Sí" if found.schengen else "No"
        info = (f"--- Información del aeropuerto ---\n\n"
                f"Código: {found.code}\n"
                f"Latitud: {found.lat:.6f}\n"
                f"Longitud: {found.lon:.6f}\n"
                f"Espacio Schengen: {schengen}")

        messagebox.showinfo(f"Aeropuerto {code}", info)
        new_win.destroy()

    # Botón "Mostrar"
    btn_show = tk.Button(new_win, text="Mostrar", command=confirm_show)
    btn_show.grid(row=1, column=0, columnspan=2, pady=10)
    new_win.bind("<Return>", lambda event: confirm_show())


def Set_Schengen():
    global airports

    try:
        airports
    except NameError:
        airports = []

    if len(airports) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados.")
        return

    new_win = tk.Toplevel()
    new_win.title("Cambiar estado Schengen")

    tk.Label(new_win, text="Código del aeropuerto (ej. LEBL):").grid(row=0, column=0, padx=5, pady=5)
    entry_code = tk.Entry(new_win)
    entry_code.grid(row=0, column=1, padx=5, pady=5)

    search_btn = tk.Button(new_win, text="Buscar")
    search_btn.grid(row=1, column=0, columnspan=2, pady=10)

    def confirm_search():
        code = entry_code.get().strip().upper()
        if not code:
            messagebox.showwarning("Advertencia", "Debe introducir un código de aeropuerto.")
            return

        # Buscar aeropuerto
        found = None
        for a in airports:
            if a.code == code:
                found = a
                break

        if not found:
            messagebox.showerror("Error", f"No se encontró el aeropuerto {code}.")
            return

        # Eliminar controles anteriores
        entry_code.destroy()
        search_btn.destroy()

        # Mostrar controles nuevos
        current = tk.BooleanVar(value=found.schengen)

        tk.Label(new_win, text=f"Estado actual de {code}:").grid(row=0, column=0, padx=5, pady=5)
        cb = tk.Checkbutton(new_win, text="Schengen", variable=current)
        cb.grid(row=0, column=1, padx=5, pady=5)

        def apply_change():
            # 🔹 Actualiza según el checkbox, no llamar SetSchengen()
            found.schengen = current.get()

            # Redibujar gráfico si hay canvas
            if hasattr(picture_frame, 'canvas'):
                canvas = picture_frame.canvas
                fig = canvas.figure
                ax = fig.axes[0]
                ax.clear()

                ax.set_title("Aeropuertos")
                ax.set_xlabel("Longitud")
                ax.set_ylabel("Latitud")

                xs = [a.lon for a in airports]
                ys = [a.lat for a in airports]
                colors = ['green' if a.schengen else 'red' for a in airports]
                ax.scatter(xs, ys, c=colors, marker='o')

                for a in airports:
                    ax.text(a.lon, a.lat, a.code, fontsize=8)

                canvas.draw()

            messagebox.showinfo("Éxito", f"Estado Schengen de {code} actualizado.")
            new_win.destroy()

        btn_apply = tk.Button(new_win, text="Aplicar cambio", command=apply_change)
        btn_apply.grid(row=1, column=0, columnspan=2, pady=10)
        new_win.bind("<Return>", lambda event: apply_change())

    search_btn.config(command=confirm_search)
    new_win.bind("<Return>", lambda event: confirm_search())



def Save_SchengenAirports():
    global airports

    try:
        airports
    except NameError:
        airports = []

    if len(airports) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados.")
        return

    # Ventana emergente para pedir nombre del fichero
    new_win = tk.Toplevel()
    new_win.title("Guardar aeropuertos Schengen")

    tk.Label(new_win, text="Nombre del fichero de salida (.txt):").grid(row=0, column=0, padx=5, pady=5)
    entry_filename = tk.Entry(new_win)
    entry_filename.grid(row=0, column=1, padx=5, pady=5)

    def confirm_save():
        filename = entry_filename.get().strip()
        if not filename:
            messagebox.showwarning("Advertencia", "Debe introducir un nombre de archivo.")
            return
        if not filename.endswith(".txt"):
            filename += ".txt"

        # 🔹 Usamos directamente la función del módulo airport.py
        result = SaveSchengenAirports(airports, filename)

        if result == -1:
            messagebox.showwarning("Aviso", "No hay aeropuertos Schengen para guardar.")
        else:
            messagebox.showinfo("Éxito", f"Aeropuertos Schengen guardados en '{filename}'.")
        new_win.destroy()

    btn_save = tk.Button(new_win, text="Guardar", command=confirm_save)
    btn_save.grid(row=1, column=0, columnspan=2, pady=10)

    # 🔹 Enter también ejecuta la acción
    new_win.bind("<Return>", lambda event: confirm_save())


def Plot_Airports():
    global airports

    try:
        airports
    except NameError:
        airports = []

    if len(airports) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados.")
        return
    # Llamamos directamente a la función del módulo airport.py
    PlotAirports(airports)


def Map_Airports():
    global airports

    try:
        airports
    except NameError:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados. Use 'Load airports' primero.")
        return

    if len(airports) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos para mapear.")
        return

    original_filename = entry_filename.get().strip()
    if not original_filename:
        base_name = "airports"
    else:
        base_name = original_filename.replace('.txt', '').replace('.TXT', '')

    success, message, filename = MapAirports(airports, base_name)

    if not success:
        messagebox.showerror("Error", message)
    elif "No se pudo abrir" in message:
        messagebox.showwarning("Aviso", message)
    else:
        pass

# VERSIÓN 2


def Load_aircrafts():
    global aircrafts

    filename = entry_flights.get().strip()
    if not filename:
        messagebox.showwarning("Advertencia", "Escriba el nombre de un fichero.")
        return

    aircrafts = LoadArrivals(filename)

    if len(aircrafts) == 0:
        messagebox.showwarning("Advertencia", "No se pudieron cargar vuelos o el archivo no existe.")
    else:
        messagebox.showinfo("Éxito", f"Loaded {len(aircrafts)} arrives")

def Save_Flights():
    global aircrafts

    try:
        aircrafts
    except NameError:
        aircrafts = []

    if len(aircrafts) == 0:
        messagebox.showwarning("Aviso", "No hay vuelos cargados.")
        return

    # Ventana emergente para pedir nombre del fichero
    new_win = tk.Toplevel()
    new_win.title("Guardar vuelos")

    tk.Label(new_win, text="Nombre del fichero de salida (.txt):").grid(row=0, column=0, padx=5, pady=5)
    entry_filename = tk.Entry(new_win)
    entry_filename.grid(row=0, column=1, padx=5, pady=5)

    def confirm_save():
        filename = entry_filename.get().strip()
        if not filename:
            messagebox.showwarning("Advertencia", "Debe introducir un nombre de archivo.")
            return
        if not filename.endswith(".txt"):
            filename += ".txt"

        # 🔹 Usamos directamente la función del módulo airport.py
        result = SaveFlights(aircrafts,filename)

        if result == -1:
            messagebox.showwarning("Aviso", "No hay vuelos para guardar.")
        else:
            messagebox.showinfo("Éxito", f"vuelos guardados en '{filename}'.")
        new_win.destroy()

    btn_save = tk.Button(new_win, text="Guardar", command=confirm_save)
    btn_save.grid(row=1, column=0, columnspan=2, pady=10)

    # 🔹 Enter también ejecuta la acción
    new_win.bind("<Return>", lambda event: confirm_save())


def Plot_Arrivals_per_Hour():
    global aircrafts

    try:
        aircrafts
    except NameError:
        aircrafts = []

    if len(aircrafts) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados.")
        return

    PlotArrivals(aircrafts)

def Plot_Airlines():
    global aircrafts

    if len(aircrafts) == 0:
        messagebox.showwarning("Aviso", "No hay vuelos cargados.")
        return

    try:
        PlotAirlines(aircrafts)
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el gráfico: {str(e)}")

def Plot_FlightsType():
    global aircrafts

    if 'aircrafts' not in globals() or len(aircrafts) == 0:
        messagebox.showerror("Error", "No se ha cargado el archivo 'arrives.txt' o está vacío~")
        return

    # Llamamos a la función de aircraft.py
    PlotFlightsType(aircrafts)


def Map_Flights():

    global aircrafts

    try:
        aircrafts
    except NameError:
        messagebox.showwarning("Aviso", "No hay vuelos cargados. Use 'Load arrivals' primero.")
        return

    if len(aircrafts) == 0:
        messagebox.showwarning("Aviso", "No hay vuelos para mapear.")
        return

    from tkinter import filedialog

    airports_filename = filedialog.askopenfilename(
        title="Seleccione el archivo de aeropuertos",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not airports_filename:
        return

    airports = LoadAirports(airports_filename)

    if len(airports) == 0:
        messagebox.showerror("Error", f"No se pudieron cargar aeropuertos desde '{airports_filename}'")
        return

    MapFlights(aircrafts, airports)


def Long_Distance_Arrivals():

    global aircrafts

    try:
        aircrafts
    except NameError:
        messagebox.showwarning("Aviso", "No hay vuelos cargados. Use 'Load arrivals' primero.")
        return

    if len(aircrafts) == 0:
        messagebox.showwarning("Aviso", "No hay vuelos para procesar.")
        return

    from tkinter import filedialog

    airports_filename = filedialog.askopenfilename(
        title="Seleccione el archivo de aeropuertos", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])


    if not airports_filename:
        return

    airports = LoadAirports(airports_filename)

    if len(airports) == 0:
        messagebox.showerror("Error", f"No se pudieron cargar aeropuertos desde '{airports_filename}'")
        return

    long_distance = LongDistanceArrivals(aircrafts, airports)

    if len(long_distance) == 0:
        messagebox.showinfo("Resultado", "No hay vuelos de larga distancia (>2000 km) para mapear.")
        return

    MapFlights(long_distance, airports)


#-------- VERSION 3 ----------

bcn = None

# VERSIÓN 3 - GATE MANAGEMENT
def Set_Gates():
    global bcn
    if bcn is None:
        messagebox.showwarning("Aviso", "Primero debes cargar la estructura del aeropuerto.")
        return

    win = tk.Toplevel()
    win.title("Crear Puertas (SetGates)")

    tk.Label(win, text="Terminal:").grid(row=0, column=0)
    entry_term = tk.Entry(win)
    entry_term.grid(row=0, column=1)

    tk.Label(win, text="Área:").grid(row=1, column=0)
    entry_area = tk.Entry(win)
    entry_area.grid(row=1, column=1)

    tk.Label(win, text="Gate inicio:").grid(row=2, column=0)
    g1 = tk.Entry(win)
    g1.grid(row=2, column=1)

    tk.Label(win, text="Gate final:").grid(row=3, column=0)
    g2 = tk.Entry(win)
    g2.grid(row=3, column=1)

    tk.Label(win, text="Prefijo:").grid(row=4, column=0)
    pref = tk.Entry(win)
    pref.grid(row=4, column=1)

    def run():
        tname = entry_term.get().strip()
        aname = entry_area.get().strip()

        for t in bcn.terms:
            if t.Name == tname:
                for area in t.BoardingArea:
                    if area.name == aname:
                        r = SetGates(area, int(g1.get()), int(g2.get()), pref.get())
                        if r == 0:
                            messagebox.showinfo("Éxito", "Puertas creadas correctamente.")
                        else:
                            messagebox.showerror("Error", "No se pudieron crear las puertas.")
                        win.destroy()
                        return
        messagebox.showerror("Error", "Terminal o área no encontrada.")

    tk.Button(win, text="Crear", command=run).grid(row=5, column=0, columnspan=2, pady=10)


def Load_Airlines():
    global bcn

    win = tk.Toplevel()
    win.title("Cargar Aerolíneas")

    tk.Label(win, text="Terminal:").grid(row=0, column=0)
    entry_term = tk.Entry(win)
    entry_term.grid(row=0, column=1)

    def run():
        tname = entry_term.get().strip()

        for t in bcn.terms:
            if t.Name == tname:
                r = LoadAirlines(t, tname)
                if r == 0:
                    messagebox.showinfo("Éxito", f"Aerolíneas cargadas en {tname}.")
                else:
                    messagebox.showerror("Error", "No se pudo cargar el archivo.")
                win.destroy()
                return

        messagebox.showerror("Error", "Terminal no encontrada.")

    tk.Button(win, text="Cargar", command=run).grid(row=1, column=0, columnspan=2, pady=10)

def Load_Airport_Structure():
    '''Carga la estructura del aeropuerto LEBL desde archivo'''
    global bcn
    
    filename = filedialog.askopenfilename(
        title="Seleccione el archivo de estructura del aeropuerto (Terminals.txt)",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    if not filename:
        return
    
    bcn = LoadAirportStructure(filename)
    
    if bcn == -1:
        messagebox.showerror("Error", "No se pudo cargar la estructura del aeropuerto.")
        return
    
    # Contar puertas totales
    total_gates = 0
    for terminal in bcn.terms:
        for area in terminal.BoardingArea:
            total_gates += len(area.gate)
    
    # Contar aerolíneas cargadas
    total_airlines = sum(len(t.codes) for t in bcn.terms)
    
    message = (f"Estructura del aeropuerto {bcn.code} cargada.\n\n"
               f"Terminales: {len(bcn.terms)}\n"
               f"Total de puertas: {total_gates}\n"
               f"Aerolíneas cargadas: {total_airlines}")
    
    if total_airlines == 0:
        message += "\n\n⚠️ AVISO: No se cargaron aerolíneas.\n"
        message += "Asegúrate de tener T1_Airlines.txt y T2_Airlines.txt\n"
        message += "en la misma carpeta para asignar puertas correctamente."
    
    messagebox.showinfo("Éxito", message)

def Assign_Gates_to_Arrivals():
    '''Asigna puertas a todos los vuelos cargados'''
    global bcn, aircrafts
    
    if bcn is None:
        messagebox.showwarning("Aviso", "Primero debe cargar la estructura del aeropuerto.")
        return
    
    try:
        aircrafts
    except NameError:
        messagebox.showwarning("Aviso", "No hay vuelos cargados. Use 'Load flights' primero.")
        return
    
    if len(aircrafts) == 0:
        messagebox.showwarning("Aviso", "No hay vuelos para asignar.")
        return
    
    # Asignar puertas a cada vuelo
    assigned = 0
    failed = 0
    
    for aircraft in aircrafts:
        result = AssignGate(bcn, aircraft)
        if result == 0:
            assigned += 1
        else:
            failed += 1
    
    messagebox.showinfo("Resultado",
        f"Asignación completada:\n\n"
        f"✓ Puertas asignadas: {assigned}\n"
        f"✗ Sin puerta disponible: {failed}")


def Show_Gate_Occupancy():
    '''Muestra el estado de ocupación de todas las puertas'''
    global bcn
    
    if bcn is None:
        messagebox.showwarning("Notice", "You must load airport structure first.")
        return
    
    occupancy = GateOccupancy(bcn)
    
    # Separar puertas ocupadas y libres
    occupied = [(name, aircraft_id) for name, status, aircraft_id in occupancy if status == "Occupied"]
    free_count = len(occupancy) - len(occupied)
    
    # Crear ventana para mostrar info
    new_win = tk.Toplevel()
    new_win.title("Gate Status")
    new_win.geometry("500x400")
    
    # Frame con scrollbar
    frame = tk.Frame(new_win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    text = tk.Text(frame, yscrollcommand=scrollbar.set, wrap=tk.WORD)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=text.yview)
    
    # Escribir información
    text.insert(tk.END, f"AIRPORT: {bcn.code}\n")
    text.insert(tk.END, f"=" * 50 + "\n\n")
    text.insert(tk.END, f"Total gates: {len(occupancy)}\n")
    text.insert(tk.END, f"Occupied gates: {len(occupied)}\n")
    text.insert(tk.END, f"Free gates: {free_count}\n\n")
    text.insert(tk.END, "=" * 50 + "\n\n")
    
    if len(occupied) > 0:
        text.insert(tk.END, "OCCUPIED GATES:\n\n")
        for gate_name, aircraft_id in occupied:
            text.insert(tk.END, f"  {gate_name}: {aircraft_id}\n")
    else:
        text.insert(tk.END, "No hay puertas ocupadas.\n")
    
    text.config(state=tk.DISABLED)


def IsAirline_InTerminal():
    global bcn

    win = tk.Toplevel()
    win.title("Comprobar Aerolínea en Terminal")

    tk.Label(win, text="Terminal:").grid(row=0, column=0)
    entry_term = tk.Entry(win)
    entry_term.grid(row=0, column=1)

    tk.Label(win, text="Aerolínea (ICAO):").grid(row=1, column=0)
    entry_code = tk.Entry(win)
    entry_code.grid(row=1, column=1)

    def run():
        tname = entry_term.get().strip()
        code = entry_code.get().strip()

        for t in bcn.terms:
            if t.Name == tname:
                if IsAirlineInTerminal(t, code):
                    messagebox.showinfo("Resultado", f"La aerolínea {code} opera en {tname}.")
                else:
                    messagebox.showinfo("Resultado", f"{code} NO opera en esta terminal.")
                win.destroy()
                return

        messagebox.showerror("Error", "Terminal no encontrada.")

    tk.Button(win, text="Comprobar", command=run).grid(row=2, column=0, columnspan=2, pady=10)

def Search_Terminal():

    global bcn

    win = tk.Toplevel()
    win.title("Buscar Terminal de Aerolínea")

    tk.Label(win, text="Aerolínea (ICAO):").grid(row=0, column=0)
    entry_code = tk.Entry(win)
    entry_code.grid(row=0, column=1)

    def run():
        code = entry_code.get().strip()
        t = SearchTerminal(bcn, code)

        if t != "":
            messagebox.showinfo("Resultado", f"La aerolínea {code} opera en la terminal {t}.")
        else:
            messagebox.showerror("Error", "No se encontró ninguna terminal para esta aerolínea.")

        win.destroy()

    tk.Button(win, text="Buscar", command=run).grid(row=1, column=0, columnspan=2, pady=10)

# --------- INTERFAZ ---------

root = tk.Tk()
root.title("Interface")
root.geometry("1300x600")

root.columnconfigure(0, weight=1) #columna 1 para los botones
root.columnconfigure(1, weight=10) #columna 2 para los gráficos
root.rowconfigure(0, weight=1) #fila 1
#Para añadir más filas es: root.rowconfigure((1,2,3, etc), weight=1)

#-----COLUMNA [0], FILA [0] (Botones)
button_frame=tk.LabelFrame(root, text= 'Airports')
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
entry_filename.bind("<Return>", lambda event: Load_airports())

# ----- COLUMNA [2], FILA [0]
flights_frame = tk.LabelFrame(root, text='Flights')
flights_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

label_flights = tk.Label(flights_frame, text="Archivo de vuelos (.txt):")
label_flights.pack(padx=5, pady=5)

# COLUMNA 3 - Gates (V3)
gates_frame = tk.LabelFrame(root, text='Gates')
gates_frame.grid(row=0, column=3, padx=5, pady=5, sticky=tk.NSEW)
label_gates = tk.Label(gates_frame, text="Gestión de Puertas")
label_gates.pack(padx=5, pady=10)

# Cajita para flights
entry_flights = tk.Entry(flights_frame, width=30)
entry_flights.pack(padx=5, pady=5)
entry_flights.bind("<Return>", lambda event: Load_aircrafts())


# BOTONES COLUMNA 1

# Botón para cargar grafo
button1=tk.Button(button_frame, text='Load airports',command=Load_airports)
button1.pack(padx=5, pady=10, fill=tk.X)

# Botón para añadir aeropuertos
button2=tk.Button(button_frame, text='Add airports',command=Add_Airports)
button2.pack(padx=5, pady=10, fill=tk.X)

# Botón para borrar aeropuertos
button3=tk.Button(button_frame, text='Delete airports',command=Remove_Airport)
button3.pack(padx=5, pady=10, fill=tk.X)

# Botón para mostrar la información de los aeropuertos en la lista
button4=tk.Button(button_frame, text='Show data of airports in the list',command=Print_Airport)
button4.pack(padx=5, pady=10, fill=tk.X)

# Botón para definir Schengen attribute aeropuertos
button5=tk.Button(button_frame, text='Set Schengen attribute to airports',command=Set_Schengen)
button5.pack(padx=5, pady=10, fill=tk.X)

# Botón para guardar Schengen aeropuertos en el archivo
button6=tk.Button(button_frame, text='Save Schengen airports in file',command=Save_SchengenAirports)
button6.pack(padx=5, pady=10, fill=tk.X)

# Botón para hacer plot de los schengen aeropuertos en la barra
button7=tk.Button(button_frame, text='Plot Schengen airports in a stacked bar',command=Plot_Airports)
button7.pack(padx=5, pady=10, fill=tk.X)

button9=tk.Button(button_frame, text='Map airports',command=Map_Airports)
button9.pack(padx=5, pady=10, fill=tk.X)

# BOTONES COLUMNA 2

#boton para cargar vuelos
load_flights = tk.Button(flights_frame, text='Load flights', command=Load_aircrafts)
load_flights.pack(padx=5, pady=10, fill=tk.X)

# Botón para guardar la info de vuelos en un archivo
button3=tk.Button(flights_frame, text='Save flights',command=Save_Flights)
button3.pack(padx=5, pady=10, fill=tk.X)

# Botón para mapear vuelos por hora
button9=tk.Button(flights_frame, text='Map arrivals per hours',command=Plot_Arrivals_per_Hour)
button9.pack(padx=5, pady=10, fill=tk.X)


button4 = tk.Button(flights_frame, text='Plot arrivals per company', command=Plot_Airlines)
button4.pack(padx=5, pady=5, fill=tk.X)

#boton para plotar tipos de vuelos
button10 = tk.Button(flights_frame, text='Plot Flights', command=Plot_FlightsType)
button10.pack(padx=5, pady=10, fill=tk.X)

# Botón para Show trajectories in Google Earth
button2 = tk.Button(flights_frame, text='Map Flights to LEBL', command=Map_Flights)
button2.pack(padx=5, pady=10, fill=tk.X)

#Botón para Show only long-distance trajectories in Google Earth
button3 = tk.Button(flights_frame, text='Long Distance Arrivals (>2000km)', command=Long_Distance_Arrivals)
button3.pack(padx=5, pady=10, fill=tk.X)


# BOTONES VERSION 3 --
btn_load_structure = tk.Button(gates_frame, text='Load Airport Structure', command=Load_Airport_Structure)
btn_load_structure.pack(padx=5, pady=10, fill=tk.X)

btn_set_gates = tk.Button(gates_frame, text='Set Gates', command=Set_Gates)
btn_set_gates.pack(padx=5, pady=5, fill=tk.X)

btn_load_airlines = tk.Button(gates_frame, text='Load Airlines', command=Load_Airlines)
btn_load_airlines.pack(padx=5, pady=5, fill=tk.X)

btn_show_occupancy = tk.Button(gates_frame, text='Show Gate Occupancy', command=Show_Gate_Occupancy)
btn_show_occupancy.pack(padx=5, pady=10, fill=tk.X)

btn_is_airline_in_terminal = tk.Button(gates_frame, text='Is Airline In Terminal', command=IsAirline_InTerminal)
btn_is_airline_in_terminal.pack(padx=5, pady=5, fill=tk.X)

btn_search_terminal = tk.Button(gates_frame, text='Search Terminal', command=Search_Terminal)
btn_search_terminal.pack(padx=5, pady=5, fill=tk.X)

btn_assign_gates = tk.Button(gates_frame, text='Assign Gates to Arrivals', command=Assign_Gates_to_Arrivals)
btn_assign_gates.pack(padx=5, pady=10, fill=tk.X)

root.mainloop()

