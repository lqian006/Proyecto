import tkinter as tk
from tkinter import messagebox
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



def Load_flights():
    pass  # no hace nada


def Plot_Arrivals_per_Hour():
    global arrives
    arrives = LoadArrivals("arrivals.txt")
    if len(arrives) == 0:
        messagebox.showwarning("Aviso", "No hay vuelos cargados.")
        return
    PlotArrivals(arrives)


def Save_Flights():
    global arrives

    try:
        arrives
    except NameError:
        arrives = []

    if len(arrives) == 0:
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
        result = Save_Flights()

        if result == -1:
            messagebox.showwarning("Aviso", "No hay vuelos para guardar.")
        else:
            messagebox.showinfo("Éxito", f"vuelos guardados en '{filename}'.")
        new_win.destroy()

    btn_save = tk.Button(new_win, text="Guardar", command=confirm_save)
    btn_save.grid(row=1, column=0, columnspan=2, pady=10)

    # 🔹 Enter también ejecuta la acción
    new_win.bind("<Return>", lambda event: confirm_save())

def Plot_FlightsType():
    global flights  # hacemos global para reutilizarla en Add_Airports

    filename = entry_filename.get().strip()
    if not filename:
        messagebox.showerror("Error", "No hay vuelos cargados.")
        return

    try:
        flights = LoadArrivals(filename)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo '{filename}'.")
        return

    contando_schengen = 0
    contando_no_schengen = 0

    i = 0
    while i < len(flights):
        if flights[i].origin.schengen:
            contando_schengen += 1
        else:
            contando_no_schengen += 1
        i += 1

    fig, ax = plt.subplots()

    ax.bar(
        ['Flights'],
        [contando_schengen],
        label='Schengen',
        color='steelblue'
    )
    ax.bar(
        ['Flights'],
        [contando_no_schengen],
        bottom=[contando_schengen],
        label='No Schengen',
        color='lightcoral'
    )
    ax.set_ylabel('Número de vuelos')
    ax.set_title('Flights by Type (Schengen vs Non-Schengen)')
    ax.legend()

    plt.show()



def Map_Airports():
    """Genera un archivo KML y lo abre directamente en Google Earth Pro"""
    global airports

    # Verificar que exista la lista
    try:
        airports
    except NameError:
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados. Use 'Load airports' primero.")
        return

    if len(airports) == 0:
        messagebox.showwarning("Aviso", "No hay aeropuertos para mapear.")
        return

    # Obtener el nombre del archivo original (sin extensión)
    original_filename = entry_filename.get().strip()
    if not original_filename:
        base_name = "airports"
    else:
        # Quitar la extensión .txt si existe
        base_name = original_filename.replace('.txt', '').replace('.TXT', '')

    filename = f"{base_name}.kml"

    # Crear KML content
    kml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml_content += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml_content += '<Document>\n'
    kml_content += '  <name>Airports Map</name>\n'
    kml_content += '  <description>Schengen and Non-Schengen Airports</description>\n'

    # Add styles for Schengen (green) and non-Schengen (red)
    kml_content += '  <Style id="schengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff00ff00</color>\n'
    kml_content += '      <scale>1.3</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '    <LabelStyle>\n'
    kml_content += '      <scale>0.9</scale>\n'
    kml_content += '    </LabelStyle>\n'
    kml_content += '  </Style>\n'

    kml_content += '  <Style id="nonschengen">\n'
    kml_content += '    <IconStyle>\n'
    kml_content += '      <color>ff0000ff</color>\n'
    kml_content += '      <scale>1.3</scale>\n'
    kml_content += '    </IconStyle>\n'
    kml_content += '    <LabelStyle>\n'
    kml_content += '      <scale>0.9</scale>\n'
    kml_content += '    </LabelStyle>\n'
    kml_content += '  </Style>\n'

    # Add each airport as a placemark
    for airport in airports:
        style = 'schengen' if airport.schengen else 'nonschengen'
        schengen_text = 'Schengen' if airport.schengen else 'Non-Schengen'

        kml_content += '  <Placemark>\n'
        kml_content += f'    <name>{airport.code}</name>\n'
        kml_content += f'    <description>{schengen_text} Airport<br/>Lat: {airport.lat:.4f}<br/>Lon: {airport.lon:.4f}</description>\n'
        kml_content += f'    <styleUrl>#{style}</styleUrl>\n'
        kml_content += '    <Point>\n'
        kml_content += f'      <coordinates>{airport.lon},{airport.lat},0</coordinates>\n'
        kml_content += '    </Point>\n'
        kml_content += '  </Placemark>\n'

    kml_content += '</Document>\n'
    kml_content += '</kml>\n'

    # Guardar archivo KML
    # 1. Obtiene el nombre del entry_filename
    original_filename = entry_filename.get().strip()

    # 2. Si está vacío, usa "airports" por defecto
    if not original_filename:
        base_name = "airports"
    else:
        # 3. Quita la extensión .txt
        base_name = original_filename.replace('.txt', '').replace('.TXT', '')

    # 4. Genera el nombre del KML
    filename = f"{base_name}.kml"

    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(kml_content)

        # Obtener ruta absoluta del archivo
        abs_path = os.path.abspath(filename)

        # Detectar sistema operativo y abrir Google Earth Pro
        system = platform.system()
        google_earth_opened = False

        if system == "Windows":
            # Rutas comunes de Google Earth Pro en Windows
            possible_paths = [
                r"C:\Program Files\Google\Google Earth Pro\client\googleearth.exe",
                r"C:\Program Files (x86)\Google\Google Earth Pro\client\googleearth.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Google Earth Pro\client\googleearth.exe")
            ]

            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        subprocess.Popen([path, abs_path])
                        google_earth_opened = True
                        break
                    except:
                        continue

        elif system == "Darwin":  # macOS
            try:
                subprocess.Popen(["open", "-a", "Google Earth Pro", abs_path])
                google_earth_opened = True
            except:
                pass

        elif system == "Linux":
            # Intentar con google-earth-pro command
            try:
                subprocess.Popen(["google-earth-pro", abs_path])
                google_earth_opened = True
            except:
                pass

        # Si no se pudo abrir automáticamente, intentar con el handler por defecto
        if not google_earth_opened:
            try:
                if system == "Windows":
                    os.startfile(abs_path)
                elif system == "Darwin":
                    subprocess.Popen(["open", abs_path])
                else:
                    subprocess.Popen(["xdg-open", abs_path])
                google_earth_opened = True
            except:
                pass

        if not google_earth_opened:
            messagebox.showwarning("Aviso",
                                   f"Archivo KML '{filename}' creado.\n\n"
                                   f"No se pudo abrir Google Earth Pro automáticamente.\n\n"
                                   f"Por favor:\n"
                                   f"1. Abre Google Earth Pro manualmente\n"
                                   f"2. Archivo → Abrir → Selecciona '{filename}'\n\n"
                                   f"O haz doble clic en '{filename}' si Google Earth está instalado.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el KML: {str(e)}")



def Plot_Airlines():
    global aircrafts

    if len(aircrafts) == 0:
        messagebox.showwarning("Aviso", "No hay vuelos cargados.")
        return

    try:
        PlotAirlines(aircrafts)
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el gráfico: {str(e)}")


def Map_Flights():
    """
    Función de interfaz que mapea los vuelos usando las variables globales.
    Genera un KML con las trayectorias y lo abre en Google Earth Pro.
    """
    global aircrafts, airports

    # Verificar que existan las listas
    try:
        aircrafts
        airports
    except NameError:
        from tkinter import messagebox
        messagebox.showwarning("Aviso", "No hay datos cargados. Cargue aeropuertos y aviones primero.")
        return

    if len(aircrafts) == 0:
        from tkinter import messagebox
        messagebox.showwarning("Aviso", "No hay aviones para mapear.")
        return

    if len(airports) == 0:
        from tkinter import messagebox
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados.")
        return

    # Llamar a la función base
    MapFlights(aircrafts, airports)

    from tkinter import messagebox
    messagebox.showinfo("Éxito",
                        f"Mapa de vuelos creado.\n\n"
                        f"Total vuelos: {len(aircrafts)}\n"
                        f"🟢 Verde = Origen Schengen\n"
                        f"🔴 Rojo = Origen Non-Schengen\n\n"
                        f"Google Earth Pro se abrirá automáticamente.")


def Long_Distance_Arrivals():
    """
    Función de interfaz que muestra los aviones que llegan desde más de 2000 km.
    """
    global aircrafts, airports

    # Verificar que existan las listas
    try:
        aircrafts
        airports
    except NameError:
        from tkinter import messagebox
        messagebox.showwarning("Aviso", "No hay datos cargados. Cargue aeropuertos y aviones primero.")
        return

    if len(aircrafts) == 0:
        from tkinter import messagebox
        messagebox.showwarning("Aviso", "No hay aviones cargados.")
        return

    if len(airports) == 0:
        from tkinter import messagebox
        messagebox.showwarning("Aviso", "No hay aeropuertos cargados.")
        return

    # Llamar a la función base
    long_distance = LongDistanceArrivals(aircrafts, airports)

    from tkinter import messagebox

    if len(long_distance) == 0:
        messagebox.showinfo("Resultado",
                            "No hay aviones que lleguen desde más de 2000 km.")
        return

    # Construir mensaje con la lista de aviones
    message = f"Aviones que llegan desde más de 2000 km:\n\n"
    message += f"Total: {len(long_distance)} aviones\n"
    message += "-" * 40 + "\n"

    for aircraft in long_distance:
        origin_airport = FindAirportByCode(airports, aircraft.origin)
        lebl = FindAirportByCode(airports, 'LEBL')

        if origin_airport and lebl:
            distance = HaversineDistance(
                origin_airport.lat, origin_airport.lon,
                lebl.lat, lebl.lon
            )
            message += f"• {aircraft.id}: {aircraft.origin} → LEBL ({distance:.0f} km)\n"
        else:
            message += f"• {aircraft.id}: {aircraft.origin} → LEBL\n"

    messagebox.showinfo("Long Distance Arrivals", message)

def Plot_FlightsType():
    global flights  # hacemos global para reutilizarla en Add_Airports

    filename = entry_filename.get().strip()
    if not filename:
        messagebox.showwarning("Error", "No hay vuelos cargados.")
        return

    try:
        flights = LoadAirports(filename)
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró el archivo '{filename}'.")
        return


    contando_schengen = 0
    contando_no_schengen = 0

    i = 0
    while i < len(flights):
        if flights[i].origin.schengen:
            contando_schengen += 1
        else:
            contando_no_schengen += 1
        i += 1

    fig, ax = plt.subplots()

    ax.bar(
        ['Flights'],
        [contando_schengen],
        label='Schengen',
        color='steelblue'
    )
    ax.bar(
        ['Flights'],
        [contando_no_schengen],
        bottom=[contando_schengen],
        label='No Schengen',
        color='lightcoral'
    )
    ax.set_ylabel('Número de vuelos')
    ax.set_title('Flights by Type (Schengen vs Non-Schengen)')
    ax.legend()

    plt.show()

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
entry_filename.bind("<Return>", lambda event: Load_airports())  # Enter para ejecutar

# ----- COLUMNA [2], FILA [0]
flights_frame = tk.LabelFrame(root, text='Flights')
flights_frame.grid(row=0, column=2, padx=5, pady=5, sticky=tk.NSEW)

label_flights = tk.Label(flights_frame, text="Archivo de vuelos (.txt):")
label_flights.pack(padx=5, pady=5)

# Cajita para flights
entry_flights = tk.Entry(flights_frame, width=30)
entry_flights.pack(padx=5, pady=5)
entry_flights.bind("<Return>", lambda event: Load_flights())

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
load_flights = tk.Button(flights_frame, text='Load flights', command=Load_flights)
load_flights.pack(padx=5, pady=10, fill=tk.X)

#boton para plotar tipos de vuelos
PlotFlightsType = tk.Button(flights_frame, text='Plot Flights', command=Plot_FlightsType)
PlotFlightsType.pack(padx=5, pady=10, fill=tk.X)

# Botón para Show trajectories in Google Earth
button2 = tk.Button(flights_frame, text='Map Flights to LEBL', command=Map_Flights)
button2.pack(padx=5, pady=10, fill=tk.X)

#Botón para Show only long-distance trajectories in Google Earth
button3 = tk.Button(flights_frame, text='Long Distance Arrivals (>2000km)', command=Long_Distance_Arrivals)
button3.pack(padx=5, pady=10, fill=tk.X)

button4 = tk.Button(flights_frame, text='Plot arrivals per company', command=Plot_Airlines)
button4.pack(padx=5, pady=5, fill=tk.X)

# Botón para mapear vuelos por hora
button5=tk.Button(flights_frame, text='Map arrivals per hours',command=Plot_Arrivals_per_Hour)
button5.pack(padx=5, pady=10, fill=tk.X)
'''
# Botón para guardar la info de vuelos en un archivo
button6=tk.Button(flights_frame, text='Save flights',command=Save_Flights)
button6.pack(padx=5, pady=10, fill=tk.X)'''

root.mainloop()

root.mainloop()