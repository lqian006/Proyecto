from LEBL import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox,filedialog
import matplotlib.pyplot as plt
from aircraft import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os


# --------- FUNCIONES --------- #

# VERSIÓN 1

# Carga el mapa
def Load_airports():
    global airports,entry_filename

    filename=filedialog.askopenfilename(
        title="Choose the file of departures",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    entry_filename=os.path.basename(filename)

    if not filename:
        return

    try:
        airports = LoadAirports(filename)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found '{filename}'.")
        return

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.set_title("Aeroports", pad=20)
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    xs = [a.lon for a in airports]
    ys = [a.lat for a in airports]
    colors = ['green' if a.schengen else 'red' for a in airports]

    # 2. Añadir transparencia (alpha) para ver puntos solapados
    ax.scatter(xs, ys, c=colors, marker='o', edgecolors='white', linewidth=0.5, alpha=0.8)

    # 3. Desplazar el texto ligeramente para que no sature el punto
    for a in airports:
        ax.text(a.lon + 0.1, a.lat + 0.1, a.code, fontsize=7, alpha=0.7)

    # 4. Mantener la proporción geográfica real (evita que se vea "compactado")
    ax.set_aspect('equal', adjustable='datalim')

    # 5. Ajustar márgenes automáticos para aprovechar el espacio
    fig.tight_layout()

    # --- El resto del código de limpieza y canvas se mantiene igual ---
    for widget in picture_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    picture_frame.canvas = canvas



# Añadir aeropuertos

def Add_Airports():
    global airports

    code = entry_airport_code.get().strip().upper()
    lat_str = entry_airport_lat.get().strip().upper()
    lon_str = entry_airport_lon.get().strip().upper()

    if not code or not lat_str or not lon_str:
        messagebox.showwarning("Warning", "All fields are required.")
        return

    try:
        lat = ConvertCoordinate(lat_str)
        lon = ConvertCoordinate(lon_str)
    except Exception:
        messagebox.showerror(
            "Error",
            "Invalid coordinate format.\nExample: N412851 o W0734640"
        )
        return

    new_airport = Airport(code, lat, lon)
    SetSchengen(new_airport)

    result = AddAirport(airports, new_airport)
    if result == -1:
        messagebox.showwarning("Warning", f"The airport {code} already exists.")
        return

    # Dibujar en el gráfico si existe
    if hasattr(picture_frame, "canvas"):
        canvas = picture_frame.canvas
        fig = canvas.figure
        ax = fig.axes[0]

        color = "green" if new_airport.schengen else "red"
        ax.scatter(new_airport.lon, new_airport.lat, c=color, s=60)
        ax.text(new_airport.lon, new_airport.lat, new_airport.code, fontsize=8)

        canvas.draw()

    # Limpiar cajas
    entry_airport_code.delete(0, tk.END)
    entry_airport_lat.delete(0, tk.END)
    entry_airport_lon.delete(0, tk.END)



# Elimina aeropuerto
def Remove_Airport():
    global airports

    code = entry_delete_code.get().strip().upper()
    if not code:
        messagebox.showwarning("Warning", "ID required")
        return

    result = RemoveAirport(airports, code)
    if result == -1:
        messagebox.showerror("Error", f"{code} does not exist.")
        return

    if hasattr(picture_frame, "canvas"):
        ax = picture_frame.canvas.figure.axes[0]
        ax.clear()

        xs = [a.lon for a in airports]
        ys = [a.lat for a in airports]
        colors = ['green' if a.schengen else 'red' for a in airports]
        ax.scatter(xs, ys, c=colors)

        for a in airports:
            ax.text(a.lon, a.lat, a.code, fontsize=8)

        picture_frame.canvas.draw()

    entry_delete_code.delete(0, tk.END)


# Muestra la información del aeropuerto
def Print_Airport():
    global airports

    try:
        airports
    except NameError:
        airports = []

    if not airports:
        messagebox.showwarning("Warning", "There is no airports loaded.")
        return

    code = entry_show_code.get().strip().upper()

    if not code:
        info = ""
        for a in airports:
            schengen = "Sí" if a.schengen else "No"
            info += (
                f"{a.code}  |  "
                f"Lat: {a.lat:.4f}  |  "
                f"Lon: {a.lon:.4f}  |  "
                f"Schengen: {schengen}\n"
            )

        if not info:
            info = "There is no airports loaded."

        messagebox.showinfo("List of airports", info)
        return

    found = None
    for a in airports:
        if a.code == code:
            found = a
            break

    if not found:
        messagebox.showerror("Error", f"There is no airport {code} loaded .")
        return

    schengen = "Sí" if found.schengen else "No"
    info = (
        f"--- Aeroport information ---\n\n"
        f"ID: {found.code}\n"
        f"Latitude: {found.lat:.6f}\n"
        f"Longitude: {found.lon:.6f}\n"
        f"Schengen Area: {schengen}"
    )

    messagebox.showinfo(f"Airport {code}", info)

    entry_show_code.delete(0, tk.END)



def Set_Schengen():
    global airports

    try:
        airports
    except NameError:
        airports = []

    if not airports:
        messagebox.showwarning("Warning", "There is no airports loaded")
        return

    code = entry_schengen_code.get().strip().upper()
    if not code:
        messagebox.showwarning("Warning", "You must enter an airport ID.")
        return

    found = None
    for a in airports:
        if a.code == code:
            found = a
            break

    if not found:
        messagebox.showerror("Error", f"There is no airport {code} loaded .")
        return


    found.schengen = schengen_var.get()

    # Redibujar gráfico si existe
    if hasattr(picture_frame, 'canvas'):
        canvas = picture_frame.canvas
        fig = canvas.figure
        ax = fig.axes[0]
        ax.clear()

        ax.set_title("Airports")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        xs = [a.lon for a in airports]
        ys = [a.lat for a in airports]
        colors = ['green' if a.schengen else 'red' for a in airports]
        ax.scatter(xs, ys, c=colors)

        for a in airports:
            ax.text(a.lon, a.lat, a.code, fontsize=8)

        canvas.draw()

    entry_schengen_code.delete(0, tk.END)



# Guardar el nuevo aeropuerto
def Save_SchengenAirports():
    global airports

    try:
        airports
    except NameError:
        airports = []

    if not airports:
        messagebox.showwarning("Warning", "There is no airports loaded.")
        return

    filename = entry_save_schengen.get().strip()
    if not filename:
        messagebox.showwarning("Warning", "You must enter a file name.")
        return

    if not filename.endswith(".txt"):
        filename += ".txt"

    result = SaveSchengenAirports(airports, filename)

    if result == -1:
        messagebox.showwarning("Warning", "There are no Schengen airports to save.")
    else:
        messagebox.showinfo("Success", f"Schengen airports saved in '{filename}'.")

    entry_save_schengen.delete(0, tk.END)



# Hace el plot de los aeropuertos schengen y no schengen
def Plot_Airports():
    global airports

    try:
        airports
    except NameError:
        airports = []

    if not airports:
        messagebox.showwarning("Warning", "You must enter a file name.")
        return

    # Limpiar el frame del gráfico
    for widget in picture_frame.winfo_children():
        widget.destroy()

    # Obtener la figura
    fig = PlotAirports(airports)

    # Insertarla en Tkinter
    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



# Envía al Google Earth ver los aeropuertos que hay
def Map_Airports():
    global airports, entry_filename

    if not airports:
        messagebox.showwarning("Warning", "There is no airports loaded.")
        return

    if 'entry_filename' in globals():
        base_name = entry_filename.replace(".txt", "").replace(".TXT", "")
    else:
        base_name = "airports"

    success, message, filename = MapAirports(airports, base_name)

    if not success:
        messagebox.showerror("Error", message)
    elif "No se pudo abrir" in message:
        messagebox.showwarning("Aviso", message)



# VERSIÓN 2



#Carga las llegadas de aviones
def Load_aircrafts():
    global aircrafts

    filename = filedialog.askopenfilename(
        title="Select the departures file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )

    if not filename:
        return

    aircrafts = LoadArrivals(filename)

    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "Flights could not be loaded or the file does not exist.")
    else:
        messagebox.showinfo("Success", f"Loaded {len(aircrafts)} arrives")



# Guarda las llegadas
def Save_Flights():
    global aircrafts

    try:
        aircrafts
    except NameError:
        aircrafts = []

    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "There is no airports loaded.")
        return

    filename = entry_save2.get().strip()
    if not filename:
        messagebox.showwarning("Warning", "You must enter a file name.")
        return
    if not filename.endswith(".txt"):
        filename += ".txt"

    result = SaveFlights(aircrafts, filename)

    if result == -1:
        messagebox.showwarning("Warning", "There are no flights to save.")
    else:
        messagebox.showinfo("Success", f"Flghts saved in '{filename}'.")

    entry_save2.delete(0, tk.END)


# Hace plot de las llegadas por hora
def Plot_Arrivals_per_Hour():
    global aircrafts

    try:
        aircrafts
    except NameError:
        aircrafts = []

    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "There is no flight loaded")
        return

    # Limpiar frame
    for widget in picture_frame.winfo_children():
        widget.destroy()

    # Crear figura desde matplotlib
    fig = PlotArrivals(aircrafts)
    if fig is None:
        messagebox.showwarning("Warning", "The graph could not be generated..")
        return

    # Canvas
    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return fig



# Hce plot de las aerolineas por llegada
def Plot_Airlines():
    global aircrafts

    if len(aircrafts) == 0:
        messagebox.showwarning("Warning", "There is no flight loaded")
        return

    try:
        for widget in picture_frame.winfo_children():
            widget.destroy()

            # Crear figura desde matplotlib
        fig = PlotAirlines(aircrafts)
        if fig is None:
            messagebox.showwarning("Warning", "The graph could not be generated.")
            return

        # Canvas
        canvas = FigureCanvasTkAgg(fig, master=picture_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        return fig

    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el gráfico: {str(e)}")



# Hace plot de las llegadas de aeropuertos schenven vs no schengen
def Plot_FlightsType():
    global aircrafts

    if 'aircrafts' not in globals() or len(aircrafts) == 0:
        messagebox.showerror("Error", "No se ha cargado el archivo 'arrives.txt' o está vacío")
        return

    for widget in picture_frame.winfo_children():
        widget.destroy()

        # Crear figura desde matplotlib
    fig = PlotFlightsType(aircrafts)
    if fig is None:
        messagebox.showwarning("Aviso", "No se pudo generar el gráfico.")
        return

    # Canvas
    canvas = FigureCanvasTkAgg(fig, master=picture_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return fig



# Se ve en Google Earth las llegadas
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



# Se ve en Google Earth las llegadas más lejanas
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



# VERSIÓN 3




bcn = None

# Se selecciona los gates
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



#Carga las aerolíneas
def Load_Airlines():
    global bcn

    win = tk.Toplevel()
    win.title("Load Airlines")

    tk.Label(win, text="Terminal:").grid(row=0, column=0)
    entry_term = tk.Entry(win)
    entry_term.grid(row=0, column=1)

    def run():
        tname = entry_term.get().strip()

        for t in bcn.terms:
            if t.Name == tname:
                r = LoadAirlines(t, tname)
                if r == 0:
                    messagebox.showinfo("Success", f"Airline loaded in {tname}.")
                else:
                    messagebox.showerror("Error", "The file could not be loaded.")
                win.destroy()
                return

        messagebox.showerror("Error", "Terminal not found.")

    tk.Button(win, text="Load", command=run).grid(row=1, column=0, columnspan=2, pady=10)


# Carga la estructura del aeropuerto LEBL desde archivo
def Load_Airport_Structure():

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
    
    message = (f"Airport structure {bcn.code} loaded.\n\n"
               f"Terminals: {len(bcn.terms)}\n"
               f"Total gates: {total_gates}\n"
               f"Airlines loades: {total_airlines}")
    
    if total_airlines == 0:
        message += "\n\n⚠️ Warning: No airlines were loaded.\n"
        message += "Ensure to have T1_Airlines.txt y T2_Airlines.txt\n"
        message += "in the same folder to assign doors correctly."
    
    messagebox.showinfo("Success", message)


# Asigna puertas a las llegadas
def Assign_Gates_to_Arrivals():

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


# Mira si hay una puerta libre
def Show_Gate_Occupancy():

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


# Muestra si la aerolínea está en cierto terminal
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


# Te busca un terminal
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




# VERSIÓN 4




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



# Fusiona las llegadas y salidas usando aircraft.py
def Merge_Movements():

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



# Mira los vuelos nocturnos
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



#Asigna los vuelos nocturnos a una puerta
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



# Muestra las puertas libres
def Free_Gate():
    global aircrafts,bcn

    if not aircrafts:
        messagebox.showerror("Error", "La lista de vuelos está vacía.")
        return

    new_win = tk.Toplevel()
    new_win.title("Free gate")

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

    tk.Button(new_win, text="Free gate",command=confirm_search).grid(row=1,column=0,columnspan=3,pady=10)

    new_win.bind("<Return>", lambda event: confirm_search())



# Te asigna a una puerta dependiendo del tiempo
def Assign_Gates_At_Time():
    global bcn, aircrafts

    if not aircrafts:
        messagebox.showerror("Error", "La lista de vuelos está vacía.")
        return

    new_win = tk.Toplevel()
    new_win.title("Hora")

    tk.Label(new_win, text="Exact time(XX:00): ").grid(row=0, column=0, padx=5, pady=5)
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



# Hce plot de las puertas y desasigna aerolíneas por el día
def Plot_Day_Occupacy():
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



# FUNCIÓN EXTRA


#Filtro que busca el vuelo dependiendo de los parámetros que selecciones
def Flight_Search():
    global bcn, aircrafts, aeroports

    # Mira si los datos están cargados
    try:
        if not aircrafts or len(aircrafts) == 0:
            messagebox.showwarning("Warning",
                                   "Please load flight data first!\n\n"
                                   "1. Column 2: Load arrivals\n"
                                   "2. Column 4: Load Departures\n"
                                   "3. Column 4: Merge Movements")
            return
    except:
        messagebox.showwarning("Warning",
                               "Please load flight data first!")
        return

    # Crea una ventana
    search_win = tk.Toplevel()
    search_win.title("🔍 Advanced Flight Search")
    search_win.geometry("900x700")
    search_win.configure(bg='#2c3e50')

    # Título
    title_label = tk.Label(search_win, text="🔍 ADVANCED FLIGHT SEARCH",
                           font=('Arial', 16, 'bold'), bg='#2c3e50', fg='white')
    title_label.pack(pady=10)

    # Filtros para el frame
    filters_frame = tk.LabelFrame(search_win, text="Filters",
                                  bg='#34495e', fg='orange', font=('Arial', 12, 'bold'))
    filters_frame.pack(padx=10, pady=10, fill=tk.X)

    # Row 1: Flight ID and Airline
    row1 = tk.Frame(filters_frame, bg='#34495e')
    row1.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(row1, text="✈️ Flight ID:", bg='#34495e', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    entry_id = tk.Entry(row1, width=15, font=('Arial', 10))
    entry_id.pack(side=tk.LEFT, padx=5)

    tk.Label(row1, text="Airline:", bg='#34495e', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    entry_airline = tk.Entry(row1, width=15, font=('Arial', 10))
    entry_airline.pack(side=tk.LEFT, padx=5)

    # Row 2: Origin and Time
    row2 = tk.Frame(filters_frame, bg='#34495e')
    row2.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(row2, text="🌍 Origin:", bg='#34495e', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    entry_origin = tk.Entry(row2, width=15, font=('Arial', 10))
    entry_origin.pack(side=tk.LEFT, padx=5)

    tk.Label(row2, text="⏰ Time (HH:MM):", bg='#34495e', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    entry_time = tk.Entry(row2, width=15, font=('Arial', 10))
    entry_time.pack(side=tk.LEFT, padx=5)

    # Row 3: Gate and Terminal
    row3 = tk.Frame(filters_frame, bg='#34495e')
    row3.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(row3, text="🚪 Gate:", bg='#34495e', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    entry_gate = tk.Entry(row3, width=15, font=('Arial', 10))
    entry_gate.pack(side=tk.LEFT, padx=5)

    tk.Label(row3, text="🏢 Terminal:", bg='#34495e', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    terminal_var = tk.StringVar(value="All")
    terminal_combo = tk.OptionMenu(row3, terminal_var, "All", "T1", "T2")
    terminal_combo.config(bg='#2c3e50', fg='white', width=10)
    terminal_combo.pack(side=tk.LEFT, padx=5)

    # Search button
    def perform_search():
        # Get filter values
        filter_id = entry_id.get().strip().upper()
        filter_airline = entry_airline.get().strip().upper()
        filter_origin = entry_origin.get().strip().upper()
        filter_time = entry_time.get().strip()
        filter_gate = entry_gate.get().strip().upper()
        filter_terminal = terminal_var.get()

        # Search through aircrafts
        results = []

        for aircraft in aircrafts:
            # Apply filters
            if filter_id and filter_id not in aircraft.id:
                continue
            if filter_airline and filter_airline != aircraft.AirlineCompany:
                continue
            if filter_origin and filter_origin != aircraft.OriginAirport:
                continue
            if filter_time and filter_time != aircraft.TimeLanding:
                continue

            # Find gate info
            gate_info = "Not Assigned"
            terminal_info = "N/A"
            area_info = "N/A"

            if bcn is not None:
                for terminal in bcn.terms:
                    for area in terminal.BoardingArea:
                        for gate in area.gate:
                            if gate.id == aircraft.id:
                                gate_info = gate.name
                                terminal_info = terminal.Name
                                area_info = area.name
                                break

            # Apply gate/terminal filters
            if filter_gate and filter_gate not in gate_info:
                continue
            if filter_terminal != "All" and filter_terminal != terminal_info:
                continue

            # Get origin airport info
            origin_name = aircraft.OriginAirport
            origin_country = "Unknown"
            # Try to get airport name from aeroports list
            try:
                if aeroports and len(aeroports) > 0:
                    for apt in aeroports:
                        if apt.code == aircraft.OriginAirport:
                            origin_name = apt.name if hasattr(apt, 'name') else aircraft.OriginAirport
                            # Extract country from code (first 2 letters)
                            origin_country = aircraft.OriginAirport[:2]
                            break
            except:
                # If aeroports not loaded, just use the code
                origin_country = aircraft.OriginAirport[:2] if len(aircraft.OriginAirport) >= 2 else "??"

            # Add to results
            results.append({
                'id': aircraft.id,
                'airline': aircraft.AirlineCompany,
                'origin': aircraft.OriginAirport,
                'origin_name': origin_name,
                'country': origin_country,
                'arrival': aircraft.TimeLanding,
                'departure': aircraft.TimeDeparture if aircraft.TimeDeparture else 'N/A',
                'gate': gate_info,
                'terminal': terminal_info,
                'area': area_info
            })

        # Display results
        results_text.delete('1.0', tk.END)

        if len(results) == 0:
            results_text.insert('end', "❌ No flights found matching your criteria.\n\n")
            results_text.insert('end', "Try:\n")
            results_text.insert('end', "- Using fewer filters\n")
            results_text.insert('end', "- Checking your spelling\n")
            results_text.insert('end', "- Searching by airline code (e.g., VLG, RYR, IBE)\n")
        else:
            results_text.insert('end', f"✅ Found {len(results)} flight(s)\n")
            results_text.insert('end', "=" * 80 + "\n\n")

            for i, result in enumerate(results, 1):
                results_text.insert('end', f"{'=' * 80}\n")
                results_text.insert('end', f"FLIGHT #{i}\n")
                results_text.insert('end', f"{'=' * 80}\n")
                results_text.insert('end', f"✈️  Flight ID:     {result['id']}\n")
                results_text.insert('end', f"Airline:       {result['airline']}\n")
                results_text.insert('end', f"🌍 Origin:        {result['origin']} ({result['origin_name']})\n")
                results_text.insert('end', f"🌏 Country:       {result['country']}\n")
                results_text.insert('end', f"⏰ Arrival:       {result['arrival']}\n")
                results_text.insert('end', f"🛫 Departure:     {result['departure']}\n")
                results_text.insert('end', f"🚪 Gate:          {result['gate']}\n")
                results_text.insert('end', f"🏢 Terminal:      {result['terminal']}\n")
                results_text.insert('end', f"📍 Area:          {result['area']}\n")
                results_text.insert('end', f"\n")

        # Update count label
        count_label.config(text=f"📊 Results: {len(results)} flights")

    btn_search = tk.Button(filters_frame, text="🔍 SEARCH", command=perform_search,
                           bg='#27ae60', fg='black', font=('Arial', 12, 'bold'),
                           width=15, height=2)
    btn_search.pack(pady=10)

    # Clear filters button
    def clear_filters():
        entry_id.delete(0, tk.END)
        entry_airline.delete(0, tk.END)
        entry_origin.delete(0, tk.END)
        entry_time.delete(0, tk.END)
        entry_gate.delete(0, tk.END)
        terminal_var.set("All")
        results_text.delete('1.0', tk.END)
        count_label.config(text="📊 Results: 0 flights")

    btn_clear = tk.Button(filters_frame, text="🗑️ Clear Filters", command=clear_filters,
                          bg='#e74c3c', fg='black', font=('Arial', 11, 'bold'),
                          width=15)
    btn_clear.pack(pady=5)

    # Results count
    count_label = tk.Label(search_win, text="📊 Results: 0 flights",
                           bg='#2c3e50', fg='white', font=('Arial', 11, 'bold'))
    count_label.pack(pady=5)

    # Results Frame
    results_frame = tk.LabelFrame(search_win, text="Search Results",
                                  bg='#34495e', fg='orange', font=('Arial', 13, 'bold'))
    results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(results_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Results text
    results_text = tk.Text(results_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                           bg='#ecf0f1', fg='#2c3e50', font=('Courier', 10),
                           padx=10, pady=10)
    results_text.pack(fill=tk.BOTH, expand=True)
    scrollbar.config(command=results_text.yview)

    # Initial message
    results_text.insert('end', " Enter search criteria above and click 🔍 SEARCH\n\n")
    results_text.insert('end', "Examples:\n")
    results_text.insert('end', "- Search by airline: VLG, RYR, IBE\n")
    results_text.insert('end', "- Search by time: 14:00, 08:30\n")
    results_text.insert('end', "- Search by origin: EGCC, LMML, LGTS\n")
    results_text.insert('end', "- Search by gate: A1, B25, M5\n")
    results_text.insert('end', "- Combine filters for precise results!\n")

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



# Para crear los signos de interrogación

def help_button(parent, command):return tk.Button(parent,text="?",width=2,command=command)



# --------- INTERFAZ --------- #

root = tk.Tk()
root.title("Interface")
root.geometry("1400x700")
root.configure(bg='#2c3e50')

# LAYOUT PRINCIPAL
main_pane = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=6, bg='#2c3e50')
main_pane.pack(fill=tk.BOTH, expand=True)

# NOTEBOOK IZQUIERDA
notebook = ttk.Notebook(main_pane)
main_pane.add(notebook, width=350)

# FRAME DERECHO (GRÁFICO)
picture_frame = tk.LabelFrame(main_pane,text='Graphic',bg='#34495e',fg='orange',font=('Arial', 12, 'bold'))
picture_frame.columnconfigure(0, weight=1)
picture_frame.rowconfigure(0, weight=1)

main_pane.add(picture_frame)

content_frame = tk.Frame(picture_frame, bg='#2c3e50')
content_frame.pack(fill=tk.BOTH, expand=True)



# -----  AIRPORTS (VERSIÓN 1) ----- #


tab_airports = tk.Frame(notebook, bg='#2c3e50')
notebook.add(tab_airports, text='🛫 Airports')

button_frame = tk.LabelFrame(tab_airports, text='Airports')
button_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


# Botón para cargar grafo
button_Load_airports = tk.Frame(button_frame)
button_Load_airports.pack(fill=tk.X, pady=10)

tk.Button(button_Load_airports, text='Load airports', command=Load_airports)\
    .pack(side=tk.LEFT, fill=tk.X, expand=True)

#Botón de ayuda
help_button(button_Load_airports, Tut_Load_Airports).pack(side=tk.LEFT, padx=5)


# Botón para añadir aeropuertos
btn_add = tk.LabelFrame(button_frame, text="Add airport")
btn_add.pack(fill=tk.X, pady=5)

tk.Label(btn_add, text="ID (ej. LEBL):").pack(padx=5, pady=2)
entry_airport_code = tk.Entry(btn_add, width=20)
entry_airport_code.pack(padx=5, pady=2)

tk.Label(btn_add, text="Latitude (ej. N412851):").pack(padx=5, pady=2)
entry_airport_lat = tk.Entry(btn_add, width=20)
entry_airport_lat.pack(padx=5, pady=2)

tk.Label(btn_add, text="Longitude (ej. E0020500):").pack(padx=5, pady=2)
entry_airport_lon = tk.Entry(btn_add, width=20)
entry_airport_lon.pack(padx=5, pady=2)

#(Este es el botón)
button_add_airport = tk.Frame(btn_add)
button_add_airport.pack(fill=tk.X, pady=5)

tk.Button(button_add_airport, text='Add', command=Add_Airports)\
    .pack(side=tk.LEFT, fill=tk.X, expand=True)

#Botón de ayuda
help_button(button_add_airport, Tut_Add_Airports).pack(side=tk.LEFT, padx=5)


# Botón para borrar aeropuertos
btn_delete = tk.LabelFrame(button_frame, text="Delete airport")
btn_delete.pack(fill=tk.X, pady=5)

tk.Label(btn_delete, text="ID").grid(row=0, column=0, padx=5, pady=5)
entry_delete_code = tk.Entry(btn_delete, width=15)
entry_delete_code.grid(row=0, column=1, padx=5, pady=5)

#(Este es el botón)
row_delete = tk.Frame(btn_delete)
row_delete.grid(row=0, column=3, padx=5)

tk.Button(row_delete, text="Delete", command=Remove_Airport)\
    .pack(side=tk.LEFT)

#Botón de ayuda
help_button(row_delete, Tut_Delete_Airports).pack(side=tk.LEFT, padx=3)


# Botón para mostrar la información de los aeropuertos en la lista
btn_show = tk.LabelFrame(button_frame, text="Show airport data")
btn_show.pack(fill=tk.X, pady=5)

tk.Label(btn_show, text="ID").grid(row=0, column=0, padx=5, pady=5)
entry_show_code = tk.Entry(btn_show, width=15)
entry_show_code.grid(row=0, column=1, padx=5, pady=5)

#(Este es el botón)
row_show = tk.Frame(btn_show)
row_show.grid(row=0, column=3, padx=5)

tk.Button(row_show, text="Show", command=Print_Airport)\
    .pack(side=tk.LEFT)

help_button(row_show, Tut_Show_Data_of_Airports).pack(side=tk.LEFT, padx=3)


# Botón para definir los aeropuertos Schengen o no
btn_schengen = tk.LabelFrame(button_frame,text="Set Schengen attribute")
btn_schengen.pack(fill=tk.X, pady=5)

tk.Label(btn_schengen, text="ID").grid(row=0, column=0, padx=5, pady=5)

entry_schengen_code = tk.Entry(btn_schengen, width=15)
entry_schengen_code.grid(row=0, column=1, padx=5, pady=5)

#(Este es el tick)
schengen_var = tk.BooleanVar()
tk.Checkbutton(btn_schengen,text="Schengen",variable=schengen_var,).grid(row=0, column=2, padx=5, pady=5)

#(Este es el botón)
row_set = tk.Frame(btn_schengen)
row_set.grid(row=0, column=4, padx=5)

tk.Button(row_set, text='Set', command=Set_Schengen)\
    .pack(side=tk.LEFT)

help_button(row_set, Tut_Set_Schengen_to_Airports).pack(side=tk.LEFT, padx=3)



# Botón para guardar Schengen aeropuertos en el archivo
btn_save = tk.LabelFrame(button_frame, text="Save Schengen airports")
btn_save.pack(fill=tk.X, pady=5)

tk.Label(btn_save, text="File name").grid(row=0, column=0, padx=5, pady=5)
entry_save_schengen = tk.Entry(btn_save, width=20)
entry_save_schengen.grid(row=0, column=1, padx=5, pady=5)

#(Este es el botón)
row_save = tk.Frame(btn_save)
row_save.grid(row=0, column=3, padx=5)

tk.Button(row_save, text='Save', command=Save_SchengenAirports)\
    .pack(side=tk.LEFT)

help_button(row_save,Tut_Save_Schengen_Airports).pack(side=tk.LEFT, padx=3)



# Botón para hacer plot de los schengen aeropuertos en la barra
button_plot_schengen = tk.Frame(button_frame)
button_plot_schengen.pack(fill=tk.X, pady=5)

tk.Button(button_plot_schengen, text='Plot Schengen airports in a stacked bar', command=Plot_Airports)\
    .pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(button_plot_schengen,Tut_Plot_Schengen).pack(side=tk.LEFT, padx=5)


#Botón para ver en el Google Earth los aeropuertos
button_map_airports = tk.Frame(button_frame)
button_map_airports.pack(fill=tk.X, pady=5)

tk.Button(button_map_airports, text='Map airports', command=Map_Airports)\
    .pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(button_map_airports, Tut_Map_Airports).pack(side=tk.LEFT, padx=5)




# ----- FLIGHTS (VERSIÓN 2) ----- #

tab_flights = tk.Frame(notebook, bg='#2c3e50')
notebook.add(tab_flights, text='✈️ Flights')

flights_frame = tk.LabelFrame(tab_flights, text='Flights')
flights_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

#boton para cargar vuelos
row_load_flights = tk.Frame(flights_frame)
row_load_flights.pack(fill=tk.X, pady=10)

load_flights = tk.Button(row_load_flights, text='Load flights', command=Load_aircrafts)
load_flights.pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(row_load_flights, Tut_Load_Flights).pack(side=tk.RIGHT, padx=5)

# Botón para guardar la info de vuelos en un archivo
save_flights_frame = tk.LabelFrame(flights_frame, text="Save flights")
save_flights_frame.pack(fill=tk.X,pady=5)

tk.Label(save_flights_frame, text="File name(.txt)").pack(padx=5, pady=2)

entry_save2 = tk.Entry(save_flights_frame)
entry_save2.pack(padx=5, pady=2, fill=tk.X)

#(Este es el botón)
row_save = tk.Frame(save_flights_frame)
row_save.pack(fill=tk.X, pady=5)

tk.Button(row_save, text='Save', command=Save_Flights).pack(side=tk.LEFT,fill=tk.X, expand=True)

help_button(row_save,Tut_Save_Flights).pack(side=tk.LEFT, padx=3)

# Botón para mapear vuelos por hora
button_plot_flight_hour = tk.Frame(flights_frame)
button_plot_flight_hour.pack(fill=tk.X, pady=5)

tk.Button(button_plot_flight_hour, text='Plot flights per hour', command=Plot_Arrivals_per_Hour).pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(button_plot_flight_hour,Tut_Plot_Arrivals_Hour).pack(side=tk.LEFT, padx=5)

#Botón para ver las aerolineas por llegada
button_plot_flight_company = tk.Frame(flights_frame)
button_plot_flight_company.pack(fill=tk.X, pady=5)

tk.Button(button_plot_flight_company, text='Plot flights per company', command=Plot_Airlines).pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(button_plot_flight_company,Tut_Plot_Arrivals_Company).pack(side=tk.LEFT, padx=5)

#Botón para hacer plot de los tipos de aviones que llegan
button_plot_flight = tk.Frame(flights_frame)
button_plot_flight.pack(fill=tk.X, pady=5)

tk.Button(button_plot_flight, text='Plot Flights', command=Plot_FlightsType).pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(button_plot_flight,Tut_Plot_Flights).pack(side=tk.LEFT, padx=5)

# Botón para Show trajectories in Google Earth
button_map_flights_LEBL = tk.Frame(flights_frame)
button_map_flights_LEBL.pack(fill=tk.X, pady=5)

tk.Button(button_map_flights_LEBL, text='Map Flights to LEBL', command=Tut_Map_Flights_LEBL).pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(button_map_flights_LEBL, Tut_Map_Flights_LEBL).pack(side=tk.LEFT, padx=5)

# Botón para Show only long-distance trajectories in Google Earth
button_map_flights_distance = tk.Frame(flights_frame)
button_map_flights_distance.pack(fill=tk.X, pady=5)

tk.Button(button_map_flights_distance, text='Map Long Distance Arrivals (>2000km)', command=Long_Distance_Arrivals).pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(button_map_flights_distance, Tut_Map_Long_Distance).pack(side=tk.LEFT, padx=5)

# ----- GATES (VERSIÓN 3) ----- #
tab_gates = tk.Frame(notebook, bg='#2c3e50')
notebook.add(tab_gates, text='🚪 Gates')

gates_frame = tk.LabelFrame(tab_gates, text='Gates')
gates_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


# Botón para cargar la estructura del aeropuerto
row_load_airport_structure = tk.Frame(gates_frame)
row_load_airport_structure.pack(fill=tk.X, pady=10)

load_airport_structure = tk.Button(row_load_airport_structure, text='Load Airport Structure', command=Load_Airport_Structure)
load_airport_structure.pack(side=tk.LEFT, fill=tk.X, expand=True)

help_button(row_load_airport_structure, Tut_Load_Airport_Structure).pack(side=tk.RIGHT, padx=5)

# Botón para set gates
btn_set_gates = tk.LabelFrame(gates_frame, text="Set Gates")
btn_set_gates.pack(fill=tk.X, pady=5, padx=5)

# Frames internos para columnas
col1 = tk.Frame(btn_set_gates)
col1.pack(side=tk.LEFT, padx=5, pady=5)

col2 = tk.Frame(btn_set_gates)
col2.pack(side=tk.LEFT, padx=5, pady=5)

# ---- Columna 1 ----
tk.Label(col1, text="Terminal:").pack(anchor="w", pady=2)
entry_Terminal = tk.Entry(col1, width=20)
entry_Terminal.pack(pady=2)

tk.Label(col1, text="Área:").pack(anchor="w", pady=2)
entry_Area = tk.Entry(col1, width=20)
entry_Area.pack(pady=2)

tk.Label(col1, text="Prefijo:").pack(anchor="w", pady=2)
entry_prefijo = tk.Entry(col1, width=20)
entry_prefijo.pack(pady=2)

# ---- Columna 2 ----
tk.Label(col2, text="Gate inicio:").pack(anchor="w", pady=2)
entry_gate_inicio = tk.Entry(col2, width=20)
entry_gate_inicio.pack(pady=2)

tk.Label(col2, text="Gate final:").pack(anchor="w", pady=2)
entry_gate_final = tk.Entry(col2, width=20)
entry_gate_final.pack(pady=2)

# Botón Crear al final de la segunda columna
tk.Button(col2, text="Crear", command=Set_Gates).pack(pady=10)

# Botón para cargar aerolíneas
btn_load_airlines = tk.Button(gates_frame, text='Load Airlines', command=Load_Airlines)
btn_load_airlines.pack(padx=5, pady=5, fill=tk.X)


# Botón para mostrar disponibilidad en las puertas
btn_show_occupancy = tk.Button(gates_frame, text='Show Gate Occupancy', command=Show_Gate_Occupancy)
btn_show_occupancy.pack(padx=5, pady=10, fill=tk.X)


# Botón para determinar si hay una aerolínea en la terminal
btn_is_airline_in_terminal = tk.Button(gates_frame, text='Is Airline In Terminal', command=IsAirline_InTerminal)
btn_is_airline_in_terminal.pack(padx=5, pady=5, fill=tk.X)


# Botón para buscar terminal
btn_search_terminal = tk.Button(gates_frame, text='Search Terminal', command=Search_Terminal)
btn_search_terminal.pack(padx=5, pady=5, fill=tk.X)


#Botón para asignar puertas a las llegadas
btn_assign_gates = tk.Button(gates_frame, text='Assign Gates to Arrivals', command=Assign_Gates_to_Arrivals)
btn_assign_gates.pack(padx=5, pady=10, fill=tk.X)



# ----- DEPARTURES (VERSIÓN 4) ----- #



tab_departures = tk.Frame(notebook, bg='#2c3e50')
notebook.add(tab_departures, text='🛫 Departures')

departures_frame = tk.LabelFrame(tab_departures, text='Departures')
departures_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)



# Botón para cargar salidas
btn_load_departures = tk.Button(departures_frame, text='Load Departures', command=Load_Departures)
btn_load_departures.pack(padx=5, pady=5, fill=tk.X)


#Botón para juntar llegadas y salidas usando aircraft.py
btn_merge_movements = tk.Button(departures_frame, text='Merge Movements', command=Merge_Movements)
btn_merge_movements.pack(padx=5, pady=5, fill=tk.X)


# Botón para ver las salidas nocturnas
btn_night_aircraft = tk.Button(departures_frame, text='Night departures', command=Night_Aircraft)
btn_night_aircraft.pack(padx=5, pady=5, fill=tk.X)


#Botón que asigna las puertas por la noche
btn_assign_night_gates = tk.Button(departures_frame, text='Assign night gates', command=Assign_Night_Gates)
btn_assign_night_gates.pack(padx=5, pady=5, fill=tk.X)


#Botón que ve qué puertas están libres
btn_free_gate = tk.Button(departures_frame, text='Free gates', command=Free_Gate)
btn_free_gate.pack(padx=5, pady=5, fill=tk.X)


#Botón que asigna puertas por hora
btn_assign_gates_at_time = tk.Button(departures_frame, text='Assing gates at time', command=Assign_Gates_At_Time)
btn_assign_gates_at_time.pack(padx=5, pady=5, fill=tk.X)


#Botón que hace un plot de la disponibilidad en un día
btn_plot_day_occupancy = tk.Button(departures_frame, text='Plot occupacy in a day', command=Plot_Day_Occupacy)
btn_plot_day_occupancy.pack(padx=5, pady=5, fill=tk.X)


#Botón para el tutorial de la versión 4
btn_tutorial4 = tk.Button(departures_frame, text='Tutorial of DEPERATURES', command=Plot_Day_Occupacy)
btn_tutorial4.pack(padx=5, pady=5, fill=tk.X)


#Botón extra
btn_search = tk.Button(departures_frame, text='🔍 Flight Search', command=Flight_Search)
btn_search.pack(padx=5, pady=5, fill=tk.X)

root.mainloop()
