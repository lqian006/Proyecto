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

#-------- VERSION 4 ----------

bcn = BarcelonaAP("LEBL")

def Load_Departures():
    global departures

    filename = filedialog.askopenfilename(
        title="Seleccione el archivo de departures",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not filename:
        return

    try:
        departures = LoadDepartures(filename)
    except Exception:
        messagebox.showerror("Error", "No se pudo abrir el archivo de departures.")
        departures = []
        return

    messagebox.showinfo(
        "Éxito",
        f"Departures cargados correctamente.\n\nTotal: {len(departures)}"
    )


# Suponemos que `aircrafts` es tu lista global con todos los Aircraft

def Merge_Movements():
    """Merge arrivals and departures using aircraft.py function."""
    global aircrafts, departures

    try:
        aircrafts
        departures
    except NameError:
        messagebox.showerror("Error", "Debe cargar arrivals y departures primero.")
        return

    if not aircrafts or not departures:
        messagebox.showerror("Error", "Las listas de arrivals o departures están vacías.")
        return

    # Reutilizamos MergeMovements de aircraft.py
    merged = MergeMovements(aircrafts, departures)

    if merged == -1:
        messagebox.showerror("Error", "Error al fusionar: alguna lista está vacía.")
        return

    # Actualizamos la lista global
    aircrafts = merged
    messagebox.showinfo("Éxito", f"Fusión completada. Total aircrafts: {len(aircrafts)}")

def Night_Aircraft():
    global aircrafts

    try:
        aircrafts
    except NameError:
        messagebox.showerror("Error", "No se han cargado vuelos aún.")
        return

    if not aircrafts:
        messagebox.showerror("Error", "La lista de vuelos está vacía.")
        return

    night_list = NightAircraft(aircrafts)

    if night_list == -1:
        messagebox.showerror("Error", "La lista de vuelos está vacía.")
        return

    filtered_night = []

    for ac in night_list:
        if ac.TimeDeparture == "":
            continue

        hour = int(ac.TimeDeparture.split(":")[0])

        # Margen nocturno: 20:00 → 06:00
        if hour >= 20 or hour < 6:
            filtered_night.append(ac)

    if not filtered_night:
        messagebox.showinfo("Night Aircrafts", "No hay vuelos nocturnos entre 20:00 y 06:00.")
        return

    info = ""
    for ac in filtered_night:
        info += (
            f"ID: {ac.id} | Airline: {ac.AirlineCompany} | "
            f"Destination: {ac.DestinationAirport} | Departure: {ac.TimeDeparture}\n"
        )

    messagebox.showinfo("Night Aircrafts (20:00 - 06:00)", info)

def Assign_Night_Gates():
    global aircrafts, bcn

    if not aircrafts:
        messagebox.showerror("Error", "La lista de vuelos está vacía.")
        return

    assigned=AssignNightGates(bcn,aircrafts)

    if assigned==-1:
        messagebox.showerror("Error", "No hay vuelos nocturnos para asignar.")
    elif assigned==0:
        messagebox.showinfo("Asignacion nocturna", "No se pudo asignar ninguna gate nocturna.")
    else:
        messagebox.showinfo("Asignacion noctura", f"Se asignaron {assigned} gates nocturnas correctamente")

def Free_Gate():
    global aircrafts,bcn

    if not aircrafts:
        messagebox.showerror("Error", "La lista de vuelos está vacía.")
        return

    new_win = tk.Toplevel()
    new_win.title("Liberar gate")

    tk.Label(new_win, text="ID del aircraft").grid(row=0, column=0, padx=5, pady=5)
    entry_code = tk.Entry(new_win)
    entry_code.grid(row=0, column=1, padx=5, pady=5)

    def confirm_search():
        id = entry_code.get().strip().upper()
        if not id:
            messagebox.showwarning("Advertencia", "Debe introducir un el ID del aircraft")
            return

        gate=FreeGate(bcn,id)

        if gate==-1:
            messagebox.showerror("Error",f"No se encontro el aircraft {id}.")
        elif gate==0:
            messagebox.showinfo("Informacion",f"El aircraft {id} no esta asiganad a ninguna gate.")
        else:
            messagebox.showinfo("Exito",f"El aicraft {id} ha sido liberada de la gate.")

        new_win.destroy()

    tk.Button(new_win, text="Liberar gate",command=confirm_search).grid(row=1,column=0,columnspan=3,pady=10)

    new_win.bind("<Return>", lambda event: confirm_search())

def Assign_Gates_At_Time():
    global bcn, aircrafts

    if not aircrafts:
        messagebox.showerror("Error", "La lista de vuelos está vacía.")
        return

    new_win = tk.Toplevel()
    new_win.title("Hora")

    tk.Label(new_win, text="Hora exacta(XX:00): ").grid(row=0, column=0, padx=5, pady=5)
    entry_time = tk.Entry(new_win)
    entry_time.grid(row=0, column=1, padx=5, pady=5)

    def confirm_time():
        time = entry_time.get().strip()
        if not time:
            messagebox.showwarning("Advertencia", "Debe escribir una hora")
            return

        assigned = AssignGatesAtTime(bcn, aircrafts, time)

        if assigned == -1:
            messagebox.showerror("Error", "La hora no está en el formato correcto (XX:00).")
        else:
            messagebox.showinfo("Exito", f"No se ha podido asignar {assigned} aircraft(s) porque el aeropuerto está lleno.")

        new_win.destroy()

    tk.Button(new_win, text="Asignar gates", command=confirm_time).grid(row=1, column=0, columnspan=2, pady=10)
    new_win.bind("<Return>", lambda event: confirm_time())

def Plot_Day_Occupacy():
    """Plot gate occupancy and unassigned aircrafts during the day."""
    global bcn, aircrafts

    try:
        bcn
        aircrafts
    except NameError:
        messagebox.showerror(
            "Error",
            "Debe cargar el aeropuerto y los vuelos antes de hacer el plot."
        )
        return

    if not aircrafts:
        messagebox.showerror(
            "Error",
            "La lista de aircrafts está vacía. Cargue y fusione arrivals y departures."
        )
        return

    if not hasattr(bcn, "terms") or len(bcn.terms) == 0:
        messagebox.showerror(
            "Error",
            "El aeropuerto no tiene terminales cargadas."
        )
        return

    # Llamada directa a la función lógica
    PlotDayOccupancy(bcn, aircrafts)

# --------- TUTORIAL ---------

def Show_Text_Window(title, text_content):
    new_win = tk.Toplevel()
    new_win.title(title)
    new_win.geometry("600x400")

    frame = tk.Frame(new_win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar.config(command=text.yview)

    text.insert(tk.END, text_content)
    text.config(state=tk.DISABLED)

    btn_ok = tk.Button(new_win,text="Entendido",command=new_win.destroy)
    btn_ok.pack(pady=10)

def Tut_Load_Airports():
    text = ("Con este botón puedes cargar un archivo “airports.txt” que contiene el código ICAO\n\n"
            " del aeropuerto con su latitud y longitud y te lo muestra en un gráfico en la interfaz.\n\n"
            " En el gráfico aparecen los aeropuertos según su latitud y longitud, pintados de verde\n\n"
            " si son Schengen y de rojo si no son Schengen. Al darle al botón, el programa te \n\n"
            "abrirá el explorador de archivos, ahí podrás escoger el archivo que desees cargar y\n\n"
            " al darle a abrir, se te habrá cargado el archivo al programa.")

    Show_Text_Window("Tutorial - Cargar aeropuertos", text)

def Tut_Add_Airports():
    text = ("Este botón te permite añadir un aeropuerto en cualquier coordenada que desees \n\n"
            "ponerla. Para añadir un aeropuerto, debes escribir el nombre usando su código \n\n"
            "ICAO y la latitud y longitud en la que quieras que este.")

    Show_Text_Window("Tutorial - Añadir aeropuertos", text)

def Tut_Delete_Airports():
    text = ("Este botón te permite borrar cualquier aeropuerto que se encuentre en el mapa.\n\n"
            " Para ello, debes escribir el código del aeropuerto que desees borrar.")

    Show_Text_Window("Tutorial - Eliminar aeropuertos", text)

def Tut_Show_Data_of_Airports():
    text = ("Este botón te enseña los datos del aeropuerto que quieras. Escribiendo el codigo del \n\n"
            "aeropuerto del que quieres saber datos, te enseña el código ICAO del aeropuerto, su \n\n"
            "latitud, su longitud y si tiene propiedad Schengen o no.")

    Show_Text_Window("Tutorial - Ver datos aeropuertos", text)

def Tut_Set_Schengen_to_Airports():
    text = ("Este botón te permite darle el atributo Schengen a un aeropuerto que no lo tiene.\n\n"
            "Para hacerlo, escribe el código del aeropuerto al que quieras atribuir Schengen. \n\n"
            "Una vez lo hagas, te saldrá una ventana con una pequeña caja para darle tic con \n\n"
            "Schengen escrito al lado. Dándole click a la caja y luego al botón “aplicar cambios” \n\n"
            "le podrás dar atributo Schengen al aeropuerto.\n\n"
            "Observación: Este botón también te permite quitarle el atributo schengen a un aeropuerto \n\n"
            "que lo tiene. Usando el mismo procedimiento, al quitarle el tic a la caja y darle a \n\n"
            "“aplicar cambios”, se guardará ese aeropuerto como no Schengen.")

    Show_Text_Window("Tutorial - Dar atributo Schengen a aeropuertos", text)

def Tut_Save_Schengen_Airports():
    text = ("Al darle a este botón, el programa creará un archivo .txt con la información de \n\n"
            "todos los aeropuertos con el atributo Schengen. El archivo creado tendrá una estructura \n\n"
            "parecida a “airports.txt” (código, latitud, longitud). Una vez le hayas dado click al \n\n"
            "botón, se abrirá una ventana donde tendrás que escribir el nombre del archivo que quieras \n\n"
            "crear. Dándole a “Guardar” se guardará el archivo que acabas de crear en tu ordenador.")

    Show_Text_Window("Tutorial - Guardar aeropuertos Schengen", text)

def Tut_Plot_Schengen():
    text = ("Este botón te crea un gráfico de barras con el número de aeropuertos Schengen y no Schengen.")

    Show_Text_Window("Tutorial - Gráficos de aeropuertos Schengen", text)

def Tut_Map_Airports():
    text = ("Este botón te abre en el Google Earth los aeropuertos Schengen y no Schengen, \n\n"
            "te muestra la gráfica que aparece en la interfaz cuando haces Load Airports en un mapa \n\n"
            "3D de la tierra para tener una mejor visión de los aeropuertos.\n\n"
            "Nota: Es necesario tener descargado en el ordenador el Google Earth para poder usar esta función.")

    Show_Text_Window("Tutorial - Mapa de aeropuertos", text)

def Tut_Load_Flights():
    text = ("Con este botón puedes cargar un archivo “arrivals.txt” que contiene el ID del avión, \n\n"
            "su aeropuerto de origen, la hora a la que llega al aeropuerto LEBL y la aerolínea a \n\n"
            "la que pertenece. Al darle al botón, el programa te abrirá el explorador de archivos,\n\n"
            "ahí podrás escoger el archivo que desees cargar y al darle a abrir, se te habrá cargado \n\n"
            "el archivo al programa. Una vez hecho esto, aparecerá una ventana diciendo que se cargaron los\n\n"
            "505 vuelos con éxito.")

    Show_Text_Window("Tutorial - Cargar vuelos", text)

def Tut_Save_Flights():
    text = ("Al darle a este botón, el programa creará un archivo .txt con la información de todas \n\n"
            "las llegadas que tengas cargadas en ese momento. El archivo creado tendrá una estructura \n\n"
            "igual a “arrivals.txt” (ID del avión, aeropuerto de origen, hora de llegada al aeropuerto LEBL, \n\n"
            "aerolínea a la que pertenece). Una vez le hayas dado click al botón, se abrirá una ventana donde\n\n"
            " tendrás que escribir el nombre del archivo que quieras crear. Dándole a “Guardar” se guardará \n\n"
            "el archivo que acabas de crear en tu ordenador.")

    Show_Text_Window("Tutorial - Guardar vuelos", text)

def Tut_Plot_Arrivals_Hour():
    text = ("Este botón crea un gráfico mostrando el número de vuelos que aterrizan cada hora en el aeropuerto.")

    Show_Text_Window("Tutorial - Gráfico de vuelos por hora", text)

def Tut_Plot_Arrivals_Company():
    text = ("Este botón crea un gráfico mostrando el número de vuelos que pertenecen a cada compañía.")

    Show_Text_Window("Tutorial - Gráfico de vuelos por compañías", text)

def Tut_Plot_Flights():
    text = ("Este botón crea un gráfico de barras con el número de vuelos Schengen y no Schengen.")

    Show_Text_Window("Tutorial - Gráfico de vuelos", text)

def Tut_Map_Flights_LEBL():
    text = ("Este botón abre en Google Earth todos los vuelos que llegan al aeropuerto LEBL, \n\n"
            "mostrando en verde los vuelos Schengen y en rojo los vuelos no Schengen. Al darle \n\n"
            "al botón, el programa te abrirá el explorador de archivos, ahí debes de abrir el \n\n"
            "archivo “airport.txt” y se te abrira el mapa en el Google Earth.\n\n"""
            "Nota: Para poder usarlo, debes de haber cargado el archivo “arrivals.txt” usando el \n\n"
            "Load Arrivals. ")

    Show_Text_Window("Tutorial - Mapa de vuelos a LEBL", text)

def Tut_Map_Long_Distance():
    text = ("Este botón abre en Google Earth los vuelos que llegan al aeropuerto LEBL, \n\n"
            "mostrando en verde los vuelos Schengen y en rojo los vuelos no Schengen, que \n\n"
            "tengan una distancia mayor a 2000 Km . Al darle al botón, el programa te abrirá el \n\n"
            "explorador de archivos, ahí debes de abrir el archivo “airport.txt” y se te abrira el \n\n"
            "mapa en el Google Earth.\n\n"
            "Nota: Para poder usarlo, debes de haber cargado el archivo “arrivals.txt” usando el \n\n"
            "Load Arrivals.  ")

    Show_Text_Window("Tutorial - Mapa de vuelos a distancia", text)

def Tut_Load_Airport_Structure():
    text = ("Este botón carga la estructura del aeropuerto LEBL. Al darle al botón, el programa te \n\n"
            "abrirá el explorador de archivos, ahí debes de abrir el archivo “Terminal.txt” y se te \n\n"
            "cargaran todos los datos que hay en el archivo.")

    Show_Text_Window("Tutorial - Cargar estructura del aeropuerto", text)

def Tut_Set_Gate():
    text = ("Este botón genera puertas a partir de la información que tu le das. Al darle al botón, \n\n"
            "aparecerá una ventana donde te pide la terminal y el área en el que encontrarán \n\n"
            "estas puertas, el inicio y final de estas puertas y el prefijo que quieras usar para \n\n"
            "llamarlas.")

    Show_Text_Window("Tutorial - Generar puertas", text)

def Tut_Load_Airlines():
    text = ("Este botón carga las aerolíneas en la terminal que tu desees. Al darle al botón, \n\n"
            "aparecerá una ventana donde tienes que poner en el cuadro de texto en qué\n\n"
            "terminal quieres cargar las aerolíneas. ")

    Show_Text_Window("Tutorial - Cargar aerolíneas", text)

def Tut_Show_Gate_Occupancy():
    text = ("Este botón muestra una ventana con la información del número de puertas totales, \n\n"
            "el número de puertas libres y el número de puertas ocupados.")

    Show_Text_Window("Tutorial - Ver ocupación de puertas", text)

def Tut_Is_Airline_in_Terminal():
    text = ("Este botón muestra si cierta aerolínea se encuentra en esa terminal o no. Al darle al  \n\n"
            "botón, aparecerá una ventana donde hay que poner en el cuadro de texto la terminal y la  \n\n"
            "aerolínea que queremos buscar.")

    Show_Text_Window("Tutorial - Ver aerolínea en terminal", text)

def Tut_Search_Terminal():
    text = ("Este botón muestra en qué terminal opera cierta aerolínea. Al darle al botón, \n\n"
            "aparecerá una ventana donde hay que poner en el cuadro de texto la aerolínea que \n\n"
            "queremos buscar.")

    Show_Text_Window("Tutorial - Buscar terminal", text)

def Tut_Assign_Gates_Arrivals():
    text = ("Este botón asigna a cada vuelo que llega al aeropuerto una gate. Al darle al botón, \n\n"
            "después de asignar puertas a los vuelos, aparecerá una ventana que dirá el número \n\n"
            "de puertas que han sido asignadas y el número de vuelos que no se han podido \n\n"
            "asignar a una puerta.")

    Show_Text_Window("Tutorial - Asignar puertas a las llegadas", text)

def Tut_Load_Departures():
    text = ("Con este botón puedes cargar un archivo “Departures.txt” que contiene el ID del \n\n"
            "avión, su aeropuerto de destino, la hora a la que sale del aeropuerto LEBL y la \n\n"
            "aerolínea a la que pertenece. Al darle al botón, el programa te abrirá el explorador \n\n"
            "de archivos, ahí podrás escoger el archivo que desees cargar y al darle a abrir, se te \n\n"
            "habrá cargado el archivo al programa. Una vez hecho esto, aparecerá una ventana \n\n"
            "diciendo que se cargaron los 511 vuelos con éxito.")

    Show_Text_Window("Tutorial - Cargar salidas", text)

def Tut_Merge_Movements():
    text = ("Este botón junta la información de los archivos “Arrivals.txt” y “Departures.txt” y los \n\n"
            "junta en una lista, ordenándolos del más temprano a más tarde (00:00 a 23:59). Al \n\n"
            "darle al botón, aparecerá una ventana informando que la fusión ha sido completada \n\n"
            "y que hay 548 aviones en total.\n\n"
            "Nota: Debes de tener cargados los archivos “Arrivals.txt” y “Departures.txt”")

    Show_Text_Window("Tutorial - Fusionar movimientos", text)

def Tut_Night_Departures():
    text = ("Este botón busca en la lista de los vuelos fusionados y te muestra información sobre \n\n"
            "los vuelos nocturnos (vuelos que son de 20:00 a 6:00). Al darle al botón, aparecerá \n\n"
            "una ventana con el ID del avión, su aerolínea, la hora a la que despegan y el \n\n"
            "aeropuerto de destino de los vuelos nocturnos.")

    Show_Text_Window("Tutorial - Salidas nocturnas", text)

def Tut_Assign_Night_Gates():
    text = ("Este botón busca de la lista fusionada y asigna una puerta para pasar la noche a los \n\n"
            "aviones que necesiten una. Al darle al botón, aparecerá una ventana informando de \n\n"
            "que no se pudo asignar una puerta (porque el aeropuerto está lleno) o de que se \n\n"
            "asignó puertas a cierto número de aviones.")

    Show_Text_Window("Tutorial - Asignar puertas noche", text)

def Tut_Assign_Gates_at_Time():
    text = ("Este botón asigna y libera puertas a aviones que lleguen o que tengan que salir \n\n"
            "dentro del periodo de una hora. Al darle al botón, aparecerá una ventana donde \n\n"
            "tienes que introducir la hora que necesites (tiene que ser una hora exacta, es decir, \n\n"
            "en punto) que te informará del número de vuelos que no pudieron ser asignados a \n\n"
            "una puerta debido a que el aeropuerto estaba lleno.")

    Show_Text_Window("Tutorial - Asignar puertas por hora", text)

def Tut_Plot_Occupancy():
    text = ("Este botón crea un gráfico de barras y de líneas donde muestra el número de gates \n\n"
            "que fueron ocupadas y el número de aviones que se quedaron sin puertas a lo largo \n\n"
            "de cada hora del día. ")

    Show_Text_Window("Tutorial - Gráfico de ocupaciones en un dia", text)

def Tut_Filtro():
    text = ("Este botón te permite encontrar información sobre los vuelos aplicando unos filtros. \n\n"
            "Al darle al botón, se crea una nueva ventana donde se hará la búsqueda por filtración. \n\n"
            "Se puede filtrar los vuelos por el ID del avión, a qué compañía pertenece, el país de \n\n"
            "origen, la hora de llegada o de salida, la puerta a la que están asignadas y la terminal \n\n"
            "en la que se encuentran. Puedes insertar estos datos por teclado (no hace falta rellenar \n\n"
            "todos) \n\ny al darle al botón de “Buscar” aparece la información en el cuadro de texto \n\n"
            "de abajo. La información que aparece es la siguiente: ID del avión del vuelo, aerolínea \n\n"
            "que realiza el vuelo, aeropuerto y país de origen o destino, hora de llegada o salida, \n\n"
            "puerta asignada, terminal, asignada y área asignada.")

    Show_Text_Window("Tutorial - Filtro", text)

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

# COLUMNA 4 - Departures (V4)
departures_frame = tk.LabelFrame(root, text='Departures')
departures_frame.grid(row=0, column=4, padx=5, pady=5, sticky=tk.NSEW)
label_departures = tk.Label(departures_frame, text="Salidas")
label_departures.pack(padx=5, pady=10)

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

# BOTONES VERSION 4 --
btn_load_departures = tk.Button(departures_frame, text='Load Departures', command=Load_Departures)
btn_load_departures.pack(padx=5, pady=5, fill=tk.X)

btn_merge_movements = tk.Button(departures_frame, text='Merge Movements', command=Merge_Movements)
btn_merge_movements.pack(padx=5, pady=5, fill=tk.X)

btn_night_aircraft = tk.Button(departures_frame, text='Night departures', command=Night_Aircraft)
btn_night_aircraft.pack(padx=5, pady=5, fill=tk.X)

btn_assign_night_gates = tk.Button(departures_frame, text='Assign night gates', command=Assign_Night_Gates)
btn_assign_night_gates.pack(padx=5, pady=5, fill=tk.X)

btn_free_gate = tk.Button(departures_frame, text='Free gates', command=Free_Gate)
btn_free_gate.pack(padx=5, pady=5, fill=tk.X)

btn_assign_gates_at_time = tk.Button(departures_frame, text='Assing gates at time', command=Assign_Gates_At_Time)
btn_assign_gates_at_time.pack(padx=5, pady=5, fill=tk.X)

btn_plot_day_occupancy = tk.Button(departures_frame, text='Plot occupacy in a day', command=Plot_Day_Occupacy)
btn_plot_day_occupancy.pack(padx=5, pady=5, fill=tk.X)

root.mainloop()

