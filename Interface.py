import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from PIL import Image, ImageTk

from airSpace import *
import os


# --- Variables Globales ---#

foto1= Image.open("f2.jpg")
current_airspace = AirSpace()
fig = None
canvas = None
toolbar = None
canvas_widget = None

current_nav_file = None
current_seg_file = None
current_aer_file = None
current_graph_name = ""

x_min, x_max, y_min, y_max = None, None, None, None

modo_click = None
segmento_click = []

boton_nodo_activo = False
boton_segmento_activo = False

entry_nombre = None
entry_x = None
entry_y = None

entry_segmento_origen = None
entry_segmento_destino = None

entry_eliminar_nodo_nombre = None

entry_eliminar_segmento_origen = None
entry_eliminar_segmento_destino = None

grafos_data = {
    "Cataluña": ("Catalonia_graph/Cat_nav.txt", "Catalonia_graph/Cat_seg.txt", "Catalonia_graph/Cat_aer.txt"),
    "España": ("Spain_graph/Spain_nav.txt", "Spain_graph/Spain_seg.txt", "Spain_graph/Spain_aer.txt"),
    "ECAC": ("ECAC_graph/ECAC_nav.txt", "ECAC_graph/ECAC_seg.txt", "ECAC_graph/ECAC_aer.txt")}


# --- Funciones ---#
def _obtener_siguiente_id_nodo():
    if not current_airspace or not current_airspace.NavPoints:
        return 1
    existing_numbers = [p.number for p in current_airspace.NavPoints if hasattr(p, 'number')]
    if existing_numbers:
        return max(existing_numbers) + 1
    else:
        return 1


def _find_navpoint_by_name(name):
    if current_airspace and current_airspace.NavPoints:
        for p in current_airspace.NavPoints:
            if p.name.lower() == name.lower():
                return p
    return None

def redraw_graph():
    global fig, canvas, toolbar, canvas_widget

    # Clear the graph_frame (important to remove old widgets)
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Always create a new Figure and Axes
    fig = plt.Figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)

    # Plot the airspace ONLY if there are points or segments
    if current_airspace and (current_airspace.NavPoints or current_airspace.NavSegments):
        PlotAirSpace_on_ax(current_airspace, ax)
    else:
        # For a truly blank map, set generic labels/title and perhaps no grid
        ax.set_title(f"Mapa Personal - {current_graph_name}", fontsize=12)
        ax.set_xlabel("Longitud")
        ax.set_ylabel("Latitud")
        ax.set_aspect("equal", adjustable='box')
        # You might want to remove the grid for a truly blank look, or keep a light one
        ax.grid(True, color='lightgray', linestyle=':', linewidth=0.5)

        # Set some default limits for the blank map, otherwise it might be too zoomed in/out
        # These are arbitrary values, adjust as needed for your "blank" view
        ax.set_xlim(-10, 10) # Example longitude range
        ax.set_ylim(35, 45)  # Example latitude range (e.g., covering parts of Spain)

    # Embed the plot in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Add the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    # Reconnect click events for interactive modes
    if modo_click == "nodo" and boton_nodo_activo:
        canvas._click_cid = canvas.mpl_connect("button_press_event", on_click)
    elif modo_click == "segmento" and boton_segmento_activo:
        canvas._click_cid = canvas.mpl_connect("button_press_event", on_click)

    # Make sure the canvas is drawn
    canvas.draw()
def añadir_nodo():
    if current_airspace is None:
        messagebox.showwarning("Sin Grafo", "Por favor, carga un grafo primero.")
        return

    nombre = entry_nombre.get().strip()
    try:
        x = float(entry_x.get().strip())
        y = float(entry_y.get().strip())
    except ValueError:
        messagebox.showerror("Error", "Coordenadas (Latitud/X, Longitud/Y) inválidas. Deben ser números.")
        return

    if not nombre:
        messagebox.showerror("Error", "El nombre del nodo no puede estar vacío.")
        return

    if _find_navpoint_by_name(nombre):
        messagebox.showerror("Error", f"Ya existe un nodo con el nombre '{nombre}'.")
        return

    nuevo_id = _obtener_siguiente_id_nodo()

    new_nav_point = NavPoint(nuevo_id, nombre, y, x)
    current_airspace.NavPoints.append(new_nav_point)

    redraw_graph()


def añadir_nodo_manualmente():
    global modo_click, boton_nodo_activo, boton_segmento_activo

    if boton_segmento_activo:
        añadir_segmento_manualmente()

    if boton_nodo_activo:
        modo_click = None
        boton_nodo_activo = False
        btn_nodo_manual.config(style='TButton')
        if canvas:
            canvas.mpl_disconnect(canvas._click_cid)
    else:
        modo_click = "nodo"
        boton_nodo_activo = True
        btn_nodo_manual.config(style='Active.TButton')
        if canvas:
            canvas._click_cid = canvas.mpl_connect("button_press_event", on_click)
        messagebox.showinfo("Modo Activo", "Modo 'Añadir Nodo Manualmente' activado. Escribe el nombre del nodo y haz clic en el grafo para añadirlo.")

def añadir_segmento():
    if current_airspace is None:
        messagebox.showwarning("Sin Grafo", "Por favor, carga un grafo primero.")
        return

    nombre_origen = entry_segmento_origen.get().strip()
    nombre_destino = entry_segmento_destino.get().strip()

    if not nombre_origen or not nombre_destino:
        messagebox.showerror("Error", "Los nombres de origen y destino del segmento no pueden estar vacíos.")
        return

    nodo_origen = _find_navpoint_by_name(nombre_origen)
    nodo_destino = _find_navpoint_by_name(nombre_destino)

    if not nodo_origen:
        messagebox.showerror("Error", f"El nodo de origen '{nombre_origen}' no existe.")
        return
    if not nodo_destino:
        messagebox.showerror("Error", f"El nodo de destino '{nombre_destino}' no existe.")
        return

    if nodo_origen == nodo_destino:
        messagebox.showerror("Error", "Un segmento no puede conectar un nodo consigo mismo.")
        return

    segment_exists = False
    for seg in current_airspace.NavSegments:
        if (seg.OriginNumber == nodo_origen.number and seg.DestinationNumber == nodo_destino.number) or \
                (seg.OriginNumber == nodo_destino.number and seg.DestinationNumber == nodo_origen.number):
            segment_exists = True
            break

    if segment_exists:
        messagebox.showerror("Error", f"El segmento entre '{nombre_origen}' y '{nombre_destino}' ya existe.")
        return

    new_segment = NavSegment(nodo_origen.number, nodo_destino.number, 0.0)
    current_airspace.NavSegments.append(new_segment)

    entry_segmento_origen.delete(0, tk.END)
    entry_segmento_destino.delete(0, tk.END)

    redraw_graph()


def añadir_segmento_manualmente():
    global modo_click, segmento_click, boton_segmento_activo, boton_nodo_activo

    if boton_nodo_activo:
        añadir_nodo_manualmente()

    if boton_segmento_activo:
        modo_click = None
        segmento_click.clear()
        boton_segmento_activo = False
        btn_segmento_manual.config(style='TButton')
        # messagebox.showinfo("Modo Desactivado", "Modo 'Añadir Segmento Manualmente' desactivado.") # Mensaje eliminado
    else:
        modo_click = "segmento"
        segmento_click.clear()
        boton_segmento_activo = True
        btn_segmento_manual.config(style='Active.TButton')  # Aplica el estilo activo
        if canvas:
            if hasattr(canvas, "_click_cid") and canvas._click_cid is not None:
                canvas.mpl_disconnect(canvas._click_cid)
            canvas._click_cid = canvas.mpl_connect("button_press_event", on_click)


def eliminar_nodo():
    if current_airspace is None:
        messagebox.showwarning("Sin Grafo", "Por favor, carga un grafo primero.")
        return

    nombre_a_eliminar = entry_eliminar_nodo_nombre.get().strip()

    if not nombre_a_eliminar:
        messagebox.showerror("Error", "El nombre del nodo a eliminar no puede estar vacío.")
        return

    nodo_a_eliminar = _find_navpoint_by_name(nombre_a_eliminar)

    if not nodo_a_eliminar:
        messagebox.showerror("Error", f"El nodo '{nombre_a_eliminar}' no existe.")
        return

    # Eliminar el nodo de la lista de NavPoints
    current_airspace.NavPoints = [p for p in current_airspace.NavPoints if p != nodo_a_eliminar]

    # Eliminar todos los segmentos que involucren a este nodo
    current_airspace.NavSegments = [s for s in current_airspace.NavSegments
                                    if
                                    s.OriginNumber != nodo_a_eliminar.number and s.DestinationNumber != nodo_a_eliminar.number]

    entry_eliminar_nodo_nombre.delete(0, tk.END)
    redraw_graph()


def eliminar_segmento():
    if current_airspace is None:
        messagebox.showwarning("Sin Grafo", "Por favor, carga un grafo primero.")
        return

    nombre_origen = entry_eliminar_segmento_origen.get().strip()
    nombre_destino = entry_eliminar_segmento_destino.get().strip()

    if not nombre_origen or not nombre_destino:
        messagebox.showerror("Error", "Los nombres de origen y destino del segmento no pueden estar vacíos.")
        return

    nodo_origen = _find_navpoint_by_name(nombre_origen)
    nodo_destino = _find_navpoint_by_name(nombre_destino)

    if not nodo_origen:
        messagebox.showerror("Error", f"El nodo de origen '{nombre_origen}' no existe.")
        return
    if not nodo_destino:
        messagebox.showerror("Error", f"El nodo de destino '{nombre_destino}' no existe.")
        return

    segmento_encontrado = None
    for seg in current_airspace.NavSegments:
        if (seg.OriginNumber == nodo_origen.number and seg.DestinationNumber == nodo_destino.number) or \
                (seg.OriginNumber == nodo_destino.number and seg.DestinationNumber == nodo_origen.number):
            segmento_encontrado = seg
            break

    if not segmento_encontrado:
        messagebox.showerror("Error", f"No se encontró un segmento entre '{nombre_origen}' y '{nombre_destino}'.")
        return

    current_airspace.NavSegments.remove(segmento_encontrado)

    entry_eliminar_segmento_origen.delete(0, tk.END)
    entry_eliminar_segmento_destino.delete(0, tk.END)

    redraw_graph()

def on_click(event):
    global modo_click, segmento_click

    if not event.inaxes or not current_airspace:
        return

    x, y = event.xdata, event.ydata

    if modo_click == "nodo":
        nombre = entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Nombre requerido", "Escribe un nombre para el nodo antes de hacer clic.")
            return

        if _find_navpoint_by_name(nombre):
            messagebox.showerror("Error", f"Ya existe un nodo llamado '{nombre}'.")
            return

        nuevo_id = _obtener_siguiente_id_nodo()
        new_nav_point = NavPoint(nuevo_id, nombre, y, x)
        current_airspace.NavPoints.append(new_nav_point)
        redraw_graph()


    elif modo_click == "segmento":

        closest = None
        min_dist = float("inf")
        for p in current_airspace.NavPoints:
            dist = ((p.longitude - x) ** 2 + (p.latitude - y) ** 2) ** 0.5

            if dist < min_dist:
                min_dist = dist
                closest = p

        if min_dist > 0.5:
            messagebox.showwarning("Demasiado lejos", "Haz clic más cerca de un nodo existente.")
            return

        segmento_click.append(closest)

        if len(segmento_click) == 1:
            messagebox.showinfo("Primer nodo", f"Seleccionado: '{closest.name}'. Ahora selecciona el segundo nodo.")
        elif len(segmento_click) == 2:
            n1, n2 = segmento_click
            if n1 == n2:
                messagebox.showerror("Error", "No puedes crear un segmento entre el mismo nodo.")
            else:
                exists = any((s.OriginNumber == n1.number and s.DestinationNumber == n2.number) or
                             (s.OriginNumber == n2.number and s.DestinationNumber == n1.number)
                             for s in current_airspace.NavSegments)
                if exists:
                    messagebox.showerror("Error", f"Ya existe un segmento entre '{n1.name}' y '{n2.name}'.")
                else:
                    current_airspace.NavSegments.append(NavSegment(n1.number, n2.number, 0.0))
                    redraw_graph()
            segmento_click.clear()
            añadir_segmento_manualmente()





def guardar_archivos():
    nombre_grafo = simpledialog.askstring("Guardar Grafo", "Escribe el nombre para guardar este grafo:")
    if not nombre_grafo:
        return

    carpeta = os.path.join("guardados", nombre_grafo)
    os.makedirs(carpeta, exist_ok=True)

    # Guardar nodos
    nav_path = os.path.join(carpeta, "nodos.nav")
    with open(nav_path, 'w', encoding='utf-8') as f_nav:
        for p in current_airspace.NavPoints:
            f_nav.write(f"{p.number},{p.name},{p.latitude},{p.longitude}\n")

    # Guardar segmentos
    seg_path = os.path.join(carpeta, "segmentos.seg")
    with open(seg_path, 'w', encoding='utf-8') as f_seg:
        for s in current_airspace.NavSegments:
            f_seg.write(f"{s.OriginNumber},{s.DestinationNumber},{s.Distance}\n")

    # Guardar air.txt
    air_txt_path = os.path.join(carpeta, "air.txt")
    with open(air_txt_path, 'w', encoding='utf-8') as f_air:
        # Aquí puedes guardar la info que consideres
        f_air.write(f"Grafo guardado: {nombre_grafo}\n")
        # O si tienes contenido, copia o genera contenido aquí

    messagebox.showinfo("Guardado", f"Grafo guardado en carpeta:\n{carpeta}")

def cargar_archivo_grafo(nombre_grafo):
    carpeta = os.path.join("guardados", nombre_grafo)
    nav_path = os.path.join(carpeta, "nodos.nav")
    seg_path = os.path.join(carpeta, "segmentos.seg")
    air_txt_path = os.path.join(carpeta, "air.txt")

    if not os.path.exists(nav_path) or not os.path.exists(seg_path):
        messagebox.showerror("Error", f"No se encontraron archivos para el grafo '{nombre_grafo}'.")
        return

    # Vaciar listas actuales
    current_airspace.NavPoints.clear()
    current_airspace.NavSegments.clear()

    # Cargar nodos
    with open(nav_path, 'r', encoding='utf-8') as f_nav:
        for linea in f_nav:
            number, name, lat, lon = linea.strip().split(",")
            current_airspace.NavPoints.append(NavPoint(int(number), name, float(lat), float(lon)))

    # Cargar segmentos
    with open(seg_path, 'r', encoding='utf-8') as f_seg:
        for linea in f_seg:
            origin, dest, dist = linea.strip().split(",")
            current_airspace.NavSegments.append(NavSegment(int(origin), int(dest), float(dist)))

    # Podrías cargar air.txt si lo necesitas, o usarlo para info

    redraw_graph()
    messagebox.showinfo("Cargado", f"Grafo '{nombre_grafo}' cargado correctamente")

def cargar_grafo_menu():
    carpeta = filedialog.askdirectory(title="Selecciona la carpeta del grafo a cargar", initialdir="guardados")
    if not carpeta:
        return  # Canceló

    # Comprobamos que los archivos existen
    nav_path = os.path.join(carpeta, "nodos.nav")
    seg_path = os.path.join(carpeta, "segmentos.seg")

    if not os.path.exists(nav_path) or not os.path.exists(seg_path):
        messagebox.showerror("Error", "La carpeta seleccionada no contiene los archivos necesarios (nodos.nav y segmentos.seg).")
        return

    # Limpiamos datos actuales
    current_airspace.NavPoints.clear()
    current_airspace.NavSegments.clear()

    # Cargamos nodos
    with open(nav_path, 'r', encoding='utf-8') as f_nav:
        for linea in f_nav:
            number, name, lat, lon = linea.strip().split(",")
            current_airspace.NavPoints.append(NavPoint(int(number), name, float(lat), float(lon)))

    # Cargamos segmentos
    with open(seg_path, 'r', encoding='utf-8') as f_seg:
        for linea in f_seg:
            origin, dest, dist = linea.strip().split(",")
            current_airspace.NavSegments.append(NavSegment(int(origin), int(dest), float(dist)))

    redraw_graph()
    messagebox.showinfo("Cargado", "Grafo cargado correctamente desde:\n" + carpeta)


def crear_grafo_en_blanco():
    global current_graph_name
    current_airspace.NavPoints.clear()
    current_airspace.NavSegments.clear()
    if hasattr(current_airspace, 'NavAirports'):
        current_airspace.NavAirports.clear()
    current_graph_name = "Mapa Personal"
    redraw_graph()
    messagebox.showinfo("Mapa Personal", "Mapa personal creado. Ahora puedes añadir nodos y segmentos.")

def boton_reachable():
    global fig, canvas, toolbar
    if current_airspace is None:
        text_reachable.delete(1.0, tk.END)
        text_reachable.insert(tk.END, "Error: Por favor, carga un grafo primero.")
        return

    name = entry_reachable.get()
    if not name:
        text_reachable.delete(1.0, tk.END)
        text_reachable.insert(tk.END, "Error: Introduce el nombre del nodo inicial.")
        return

    try:
        if fig is None:
            text_reachable.delete(1.0, tk.END)
            text_reachable.insert(tk.END, "Error: No hay un gráfico inicial cargado.")
            return

        # Limpiar el área de texto antes de mostrar nuevos resultados
        text_reachable.delete(1.0, tk.END)

        # Obtener los nodos alcanzables primero para mostrarlos en el texto
        reachable_nodes = GetReachableNodes(current_airspace, name)
        text_reachable.insert(tk.END, f"Nodos alcanzables desde {name}:\n")
        text_reachable.insert(tk.END, ", ".join(reachable_nodes) + "\n\n")

        # Dibujar en el gráfico
        ax = fig.gca()
        ax.clear()  # Limpiar el gráfico antes de dibujar
        PlotReachable(current_airspace, name, ax=ax)

        # Actualizar la visualización
        canvas.draw()
        toolbar.update()

        text_reachable.insert(tk.END, "¡Gráfico actualizado correctamente!")

    except ValueError as e:
        text_reachable.delete(1.0, tk.END)
        text_reachable.insert(tk.END, f"Error de entrada: {str(e)}")
    except Exception as e:
        text_reachable.delete(1.0, tk.END)
        text_reachable.insert(tk.END, f"Error inesperado: {str(e)}")


def boton_camino_mas_corto():
    global fig, canvas, toolbar
    if current_airspace is None:
        text_camino.delete(1.0, tk.END)
        text_camino.insert(tk.END, "Error: Por favor, carga un grafo primero.")
        return

    start = entry_camino_origen.get()
    end = entry_camino_destino.get()

    if not start or not end:
        text_camino.delete(1.0, tk.END)
        text_camino.insert(tk.END, "Error: Introduce ambos nodos (origen y destino).")
        return

    try:
        if fig is None:
            text_camino.delete(1.0, tk.END)
            text_camino.insert(tk.END, "Error: No hay un gráfico inicial cargado.")
            return

        # Limpiar el área de texto antes de mostrar nuevos resultados
        text_camino.delete(1.0, tk.END)

        # Obtener el camino más corto primero para mostrarlo en el texto
        path, distance = GetShortestPath(current_airspace, start, end)

        if not path:
            text_camino.insert(tk.END, f"No existe camino entre {start} y {end}")
        else:
            text_camino.insert(tk.END, f"Camino más corto de {start} a {end}:\n")
            text_camino.insert(tk.END, " → ".join(path) + "\n")
            text_camino.insert(tk.END, f"Distancia total: {distance:.2f} km\n\n")

        # Dibujar en el gráfico
        ax = fig.gca()
        ax.clear()  # Limpiar el gráfico antes de dibujar
        PlotShortestPathSimple(current_airspace, start, end, ax=ax)

        # Actualizar la visualización
        canvas.draw()
        toolbar.update()

        text_camino.insert(tk.END, "¡Gráfico actualizado correctamente!")

    except ValueError as e:
        text_camino.delete(1.0, tk.END)
        text_camino.insert(tk.END, f"Error de entrada: {str(e)}")
    except Exception as e:
        text_camino.delete(1.0, tk.END)
        text_camino.insert(tk.END, f"Error inesperado: {str(e)}")


def PlotAirSpace_on_ax(airspace, ax):
    ax.clear() # Clear the axes if it's reused

    for seg in airspace.NavSegments:
        p1 = airspace.get_navpoint_by_id(seg.OriginNumber)
        p2 = airspace.get_navpoint_by_id(seg.DestinationNumber)
        if p1 and p2:
            ax.plot([p1.longitude, p2.longitude], [p1.latitude, p2.latitude], color='cyan', linewidth=0.5, zorder=1)
            mid_x = (p1.longitude + p2.longitude) / 2
            mid_y = (p1.latitude + p2.latitude) / 2
            ax.text(mid_x, mid_y, f"{seg.Distance:.1f}", fontsize=5, color='gray', ha='center', zorder=1)

    # Draw all NavPoints (black by default for general nodes)
    for p in airspace.NavPoints:
        ax.plot(p.longitude, p.latitude, 'ko', markersize=2, zorder=2) # 'k' for black
        ax.text(p.longitude + 0.01, p.latitude + 0.01, p.name, fontsize=5, ha="left", va="bottom", zorder=2)

    # Apply special styling for airports using the 'gray' style
    for airport in airspace.NavAirports:
        # Find the NavPoint associated with this airport
        associated_navpoint = next((p for p in airspace.NavPoints if p.name.lower() == airport.associated_navpoint_name.lower()), None)
        if associated_navpoint:
            # Plot the airport's associated NavPoint with the desired style
            ax.plot(associated_navpoint.longitude, associated_navpoint.latitude, color='gray', marker='o', markersize=3, zorder=3)
            ax.text(associated_navpoint.longitude, associated_navpoint.latitude, airport.Name_airport, fontsize=7, color='gray', ha="center", va="bottom", zorder=3)


    ax.set_title(f"Gráfico del espacio aéreo de {current_graph_name}", fontsize=12)
    ax.set_xlabel("Longitud")
    ax.set_ylabel("Latitud")
    ax.set_aspect("equal", adjustable='box')
    ax.grid(True, color='red', linestyle='--', linewidth=0.3)
    ax.autoscale_view()





# --- Reachables ---
def GetReachableNodes(airspace, start_name):

    if airspace is None:
        raise ValueError("Error: Grafo no cargado.")

    start_node = airspace.get_navpoint_by_name(start_name)
    if not start_node:
        airport_found = next((a for a in airspace.NavAirports if a.Name_airport.lower() == start_name.lower()), None)
        if airport_found and airport_found.associated_navpoint_name:
            start_node = airspace.get_navpoint_by_name(airport_found.associated_navpoint_name)

        if not start_node:
            raise ValueError(f"Error: Nodo o aeropuerto '{start_name}' no encontrado o no tiene NavPoint asociado.")

    visited_numbers = set()
    queue = [start_node]
    reachable_names = []

    while queue:
        current = queue.pop(0)
        if current.number not in visited_numbers:
            visited_numbers.add(current.number)
            reachable_names.append(current.name)

            for seg in airspace.NavSegments:
                if seg.OriginNumber == current.number:
                    neighbor = airspace.get_navpoint_by_id(seg.DestinationNumber)
                    if neighbor and neighbor.number not in visited_numbers:
                        queue.append(neighbor)
                elif seg.DestinationNumber == current.number:
                    neighbor = airspace.get_navpoint_by_id(seg.OriginNumber)
                    if neighbor and neighbor.number not in visited_numbers:
                        queue.append(neighbor)
    return reachable_names


# --- Camino más corto ---#
def GetShortestPath(airspace, start_name, end_name):

    if airspace is None:
        raise ValueError("Error: Grafo no cargado.")

    start_node = airspace.get_navpoint_by_name(start_name)
    if not start_node:
        airport_start = next((a for a in airspace.NavAirports if a.Name_airport.lower() == start_name.lower()), None)
        if airport_start and airport_start.associated_navpoint_name:
            start_node = airspace.get_navpoint_by_name(airport_start.associated_navpoint_name)
    if not start_node:
        raise ValueError(
            f"Error: Nodo o aeropuerto de origen '{start_name}' no encontrado o no tiene NavPoint asociado.")

    end_node = airspace.get_navpoint_by_name(end_name)
    if not end_node:
        airport_end = next((a for a in airspace.NavAirports if a.Name_airport.lower() == end_name.lower()), None)
        if airport_end and airport_end.associated_navpoint_name:
            end_node = airspace.get_navpoint_by_name(airport_end.associated_navpoint_name)
    if not end_node:
        raise ValueError(
            f"Error: Nodo o aeropuerto de destino '{end_name}' no encontrado o no tiene NavPoint asociado.")

    distances = {p.number: float('inf') for p in airspace.NavPoints}
    distances[start_node.number] = 0
    previous = {p.number: None for p in airspace.NavPoints}
    unvisited = {p.number for p in airspace.NavPoints}

    while unvisited:
        current_node_number = min(unvisited, key=lambda node_num: distances[node_num])

        if distances[current_node_number] == float('inf'):
            break

        unvisited.remove(current_node_number)

        if current_node_number == end_node.number:
            break

        for seg in airspace.NavSegments:
            neighbor_number = None
            segment_distance = seg.Distance

            if seg.OriginNumber == current_node_number:
                neighbor_number = seg.DestinationNumber
            elif seg.DestinationNumber == current_node_number:
                neighbor_number = seg.OriginNumber

            if neighbor_number is not None and neighbor_number in unvisited:
                new_dist = distances[current_node_number] + segment_distance
                if new_dist < distances[neighbor_number]:
                    distances[neighbor_number] = new_dist
                    previous[neighbor_number] = current_node_number

    path_numbers = []
    current_node_num = end_node.number
    while current_node_num is not None:
        path_numbers.append(current_node_num)
        current_node_num = previous[current_node_num]

    if path_numbers and path_numbers[-1] == start_node.number:
        path_numbers.reverse()
        path_names = [airspace.get_navpoint_by_id(num).name for num in path_numbers]
        return path_names, distances[end_node.number]
    else:
        return [], 0


def mostrar_grafo(graph_name, nav_file_path, seg_file_path, aer_file_path):
    global current_airspace, current_graph_name, x_min, x_max, y_min, y_max

    try:
        # Limpiar el grafo actual antes de cargar uno nuevo
        if current_airspace is not None:
            current_airspace.NavPoints.clear()
            current_airspace.NavSegments.clear()
            if hasattr(current_airspace, 'NavAirports'):
                current_airspace.NavAirports.clear()

        # Verificar que los archivos existen
        if not all(os.path.exists(f) for f in [nav_file_path, seg_file_path, aer_file_path]):
            raise FileNotFoundError(f"Archivos no encontrados para {graph_name}")

        # Cargar el nuevo grafo
        loaded_airspace = LoadAirSpace(nav_file_path, seg_file_path, aer_file_path)

        # Actualizar la instancia actual con los nuevos datos
        current_airspace.NavPoints = loaded_airspace.NavPoints
        current_airspace.NavSegments = loaded_airspace.NavSegments
        if hasattr(loaded_airspace, 'NavAirports'):
            current_airspace.NavAirports = loaded_airspace.NavAirports

        current_graph_name = graph_name
        x_min, x_max, y_min, y_max = None, None, None, None

        redraw_graph()

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el grafo {graph_name}:\n{str(e)}")
        # Limpiar todo si falla
        current_airspace.NavPoints.clear()
        current_airspace.NavSegments.clear()
        if hasattr(current_airspace, 'NavAirports'):
            current_airspace.NavAirports.clear()
        redraw_graph()

#---INTERFAZ---#

root = tk.Tk()
root.title("AeroSketch")
root.geometry("1200x700")

#---Estilos para botones ttk con tamaños ajustados---#
style = ttk.Style()
style.configure('TButton',
                background='#e1e1e1',
                foreground='black',
                padding=6,
                font=('Arial', 10, 'bold'))
style.map('TButton', background=[('active', '#d0d0d0')])
style.configure('Active.TButton',
                background='#c0c0c0',
                relief='sunken',
                foreground='black',
                padding=6,
                font=('Arial', 10, 'bold'))
style.map('Active.TButton', background=[('active', '#a0a0a0')])

# Tamaño de fuente para las pestañas

style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))

# Menú

menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Guardar grafo", command=guardar_archivos)
filemenu.add_command(label="Cargar grafo", command=cargar_grafo_menu)
menubar.add_cascade(label="Archivo", menu=filemenu)
root.config(menu=menubar)

# Configuración columnas y filas principales

root.columnconfigure(0, weight=1, minsize=300)
root.columnconfigure(1, weight=4, minsize=800)
root.rowconfigure(0, weight=1)

# Panel izquierdo con scroll y pestañas

left_panel_scroll_frame = ttk.Frame(root)
left_panel_scroll_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

canvas_left_panel = tk.Canvas(left_panel_scroll_frame)
scrollbar_left_panel = ttk.Scrollbar(left_panel_scroll_frame, orient="vertical", command=canvas_left_panel.yview)
scrollbar_left_panel.pack(side="right", fill="y")

canvas_left_panel.pack(side="left", fill="both", expand=True)
canvas_left_panel.configure(yscrollcommand=scrollbar_left_panel.set)

left_panel_inner_frame = ttk.Frame(canvas_left_panel)
canvas_left_panel.create_window((0, 0), window=left_panel_inner_frame, anchor="nw", tags="inner_frame")


def on_configure(event):
    canvas_left_panel.configure(scrollregion=canvas_left_panel.bbox("all"))

left_panel_inner_frame.bind("<Configure>", lambda e: canvas_left_panel.configure(scrollregion=canvas_left_panel.bbox("all")))
canvas_left_panel.bind("<Configure>", lambda e: canvas_left_panel.itemconfig("inner_frame", width=e.width))
scrollbar_left_panel.pack(side="right", fill="y")

#---Frame para botones de selección de grafo---#

graph_selection_frame = ttk.LabelFrame(left_panel_inner_frame, text="Selección de Grafo")
graph_selection_frame.pack(pady=(10, 5), padx=5, fill="x")

button_style = {'pady': 1, 'padx': 2, 'fill': 'x', 'ipady': 3}

ttk.Button(graph_selection_frame,
           text="Mostrar grafo Cataluña",
           command=lambda: mostrar_grafo("Cataluña", *grafos_data["Cataluña"])).pack(**button_style)

ttk.Button(graph_selection_frame,
           text="Mostrar grafo España",
           command=lambda: mostrar_grafo("España", *grafos_data["España"])).pack(**button_style)

ttk.Button(graph_selection_frame,
           text="Mostrar grafo ECAC",
           command=lambda: mostrar_grafo("ECAC", *grafos_data["ECAC"])).pack(**button_style)

ttk.Button(graph_selection_frame,
           text="Mapa Personal",
           command=crear_grafo_en_blanco).pack(**button_style)

# --- Pestañas para operaciones---#

notebook = ttk.Notebook(left_panel_inner_frame)
notebook.pack(pady=(5, 10), padx=5, fill="both", expand=True)

#---Pestaña Añadir---#

add_tab = ttk.Frame(notebook)
notebook.add(add_tab, text="Añadir")
add_tab.columnconfigure(0, weight=1)

add_sub_notebook = ttk.Notebook(add_tab)
add_sub_notebook.pack(fill="both", expand=True, padx=5, pady=5)

label_style = {'pady': 3, 'padx': 5, 'anchor': 'w'}
entry_style = {'pady': 3, 'padx': 5, 'fill': 'x'}
button_style_inner = {'pady': 5, 'padx': 5, 'fill': 'x', 'ipady': 2}  # Reducido ipady

# Añadir Nodo
add_node_tab = ttk.Frame(add_sub_notebook)
add_sub_notebook.add(add_node_tab, text="Nodo")
add_node_tab.columnconfigure(0, weight=1)

ttk.Label(add_node_tab, text="Nombre:").pack(**label_style)
entry_nombre = ttk.Entry(add_node_tab)
entry_nombre.pack(**entry_style)

ttk.Label(add_node_tab, text="Longitud (X):").pack(**label_style)
entry_x = ttk.Entry(add_node_tab)
entry_x.pack(**entry_style)

ttk.Label(add_node_tab, text="Latitud (Y):").pack(**label_style)
entry_y = ttk.Entry(add_node_tab)
entry_y.pack(**entry_style)

ttk.Button(add_node_tab, text="Añadir nodo (por texto)", command=añadir_nodo).pack(**button_style_inner)
btn_nodo_manual = ttk.Button(add_node_tab, text="Añadir nodo (por click)", command=añadir_nodo_manualmente)
btn_nodo_manual.pack(**button_style_inner)

# Añadir Segmento
add_segment_tab = ttk.Frame(add_sub_notebook)
add_sub_notebook.add(add_segment_tab, text="Segmento")
add_segment_tab.columnconfigure(0, weight=1)

ttk.Label(add_segment_tab, text="Nodo Origen (Nombre):").pack(**label_style)
entry_segmento_origen = ttk.Entry(add_segment_tab)
entry_segmento_origen.pack(**entry_style)

ttk.Label(add_segment_tab, text="Nodo Destino (Nombre):").pack(**label_style)
entry_segmento_destino = ttk.Entry(add_segment_tab)
entry_segmento_destino.pack(**entry_style)

ttk.Button(add_segment_tab, text="Añadir Segmento (por texto)", command=añadir_segmento).pack(**button_style_inner)
btn_segmento_manual = ttk.Button(add_segment_tab, text="Añadir Segmento (por click)", command=añadir_segmento_manualmente)
btn_segmento_manual.pack(**button_style_inner)

#---Pestaña eliminar---#

delete_tab = ttk.Frame(notebook)
notebook.add(delete_tab, text="Eliminar")
delete_tab.columnconfigure(0, weight=1)

delete_sub_notebook = ttk.Notebook(delete_tab)
delete_sub_notebook.pack(fill="both", expand=True, padx=5, pady=5)

# Eliminar Nodo
delete_node_tab = ttk.Frame(delete_sub_notebook)
delete_sub_notebook.add(delete_node_tab, text="Nodo")
delete_node_tab.columnconfigure(0, weight=1)

ttk.Label(delete_node_tab, text="Nombre del Nodo a Eliminar:").pack(**label_style)
entry_eliminar_nodo_nombre = ttk.Entry(delete_node_tab)
entry_eliminar_nodo_nombre.pack(**entry_style)

ttk.Button(delete_node_tab, text="Eliminar Nodo", command=eliminar_nodo).pack(**button_style_inner)

# Eliminar Segmento
delete_segment_tab = ttk.Frame(delete_sub_notebook)
delete_sub_notebook.add(delete_segment_tab, text="Segmento")
delete_segment_tab.columnconfigure(0, weight=1)

ttk.Label(delete_segment_tab, text="Nodo Origen del Segmento:").pack(**label_style)
entry_eliminar_segmento_origen = ttk.Entry(delete_segment_tab)
entry_eliminar_segmento_origen.pack(**entry_style)

ttk.Label(delete_segment_tab, text="Nodo Destino del Segmento:").pack(**label_style)
entry_eliminar_segmento_destino = ttk.Entry(delete_segment_tab)
entry_eliminar_segmento_destino.pack(**entry_style)

ttk.Button(delete_segment_tab, text="Eliminar Segmento", command=eliminar_segmento).pack(**button_style_inner)

#---Pestaña Caminos---#

caminos_tab = ttk.Frame(notebook)
notebook.add(caminos_tab, text="Caminos")
caminos_tab.columnconfigure(0, weight=1)
caminos_tab.rowconfigure(0, weight=1) # Para reachable_frame
caminos_tab.rowconfigure(1, weight=1) # Para shortest_path_frame

# Frame para reachable
reachable_frame = ttk.LabelFrame(caminos_tab, text="Nodos Alcanzables")
reachable_frame.grid(row=0, column=0, pady=5, padx=5, sticky="nsew")
reachable_frame.columnconfigure(0, weight=1)
reachable_frame.rowconfigure(0, weight=0)
reachable_frame.rowconfigure(1, weight=1)

# Contenedor para los elementos de entrada y el botón de "Reachable"

reachable_input_and_button_frame = ttk.Frame(reachable_frame)
reachable_input_and_button_frame.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
reachable_input_and_button_frame.columnconfigure(0, weight=1)

# Frame para las entradas
reachable_entries_frame = ttk.Frame(reachable_input_and_button_frame)
reachable_entries_frame.pack(side="top", fill="x") # Pack arriba en el frame combinado

ttk.Label(reachable_entries_frame, text="Nodo origen:").pack(side="left", padx=5)
entry_reachable = ttk.Entry(reachable_entries_frame)
entry_reachable.pack(side="left", padx=5, fill="x", expand=True)

reachable_button_frame = ttk.Frame(reachable_input_and_button_frame)
reachable_button_frame.pack(side="top", pady=5, fill="x")

ttk.Button(reachable_button_frame,
           text="Calcular Nodos Alcanzables",
           command=boton_reachable).pack(fill="x", padx=5)

# Área de texto para resultados
text_reachable = tk.Text(reachable_frame, height=5, wrap="word")
text_reachable.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")
scroll_reachable = ttk.Scrollbar(reachable_frame, command=text_reachable.yview)
scroll_reachable.grid(row=1, column=1, sticky="ns", pady=5)
text_reachable.config(yscrollcommand=scroll_reachable.set)

# Cuadro de texto y botón para exportar segmentos con coste alto
frame_export = ttk.Frame(root)
frame_export.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

# Camino más corto
shortest_path_frame = ttk.LabelFrame(caminos_tab, text="Camino más corto")
shortest_path_frame.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")
shortest_path_frame.columnconfigure(0, weight=1)
shortest_path_frame.rowconfigure(0, weight=0)
shortest_path_frame.rowconfigure(1, weight=1)

# Contenedor para los elementos de entrada y el botón de "Camino más corto"
path_input_and_button_frame = ttk.Frame(shortest_path_frame)
path_input_and_button_frame.grid(row=0, column=0, pady=5, padx=5, sticky="ew")
path_input_and_button_frame.columnconfigure(0, weight=1)

path_entries_frame = ttk.Frame(path_input_and_button_frame)
path_entries_frame.pack(side="top", fill="x")
path_entries_frame.columnconfigure(1, weight=1)
path_entries_frame.columnconfigure(3, weight=1)

# Nodo origen
ttk.Label(path_entries_frame, text="Origen:").grid(row=0, column=0, padx=5, sticky="w")
entry_camino_origen = ttk.Entry(path_entries_frame)
entry_camino_origen.grid(row=0, column=1, padx=5, sticky="ew")

# Nodo destino
ttk.Label(path_entries_frame, text="Destino:").grid(row=0, column=2, padx=5, sticky="w")
entry_camino_destino = ttk.Entry(path_entries_frame)
entry_camino_destino.grid(row=0, column=3, padx=5, sticky="ew")
path_button_frame = ttk.Frame(path_input_and_button_frame)
path_button_frame.pack(side="top", pady=5, fill="x")

ttk.Button(path_button_frame,
           text="Calcular Camino",
           command=boton_camino_mas_corto).pack(fill="x", padx=5)

# Área de texto para resultados
text_camino = tk.Text(shortest_path_frame, height=5, wrap="word")
text_camino.grid(row=1, column=0, pady=5, padx=5, sticky="nsew")
scroll_camino = ttk.Scrollbar(shortest_path_frame, command=text_camino.yview)
scroll_camino.grid(row=1, column=1, sticky="ns", pady=5)
text_camino.config(yscrollcommand=scroll_camino.set)


#---Créditos---#


cred_tab = ttk.Frame(notebook)
notebook.add(cred_tab, text="Créditos")
cred_tab.columnconfigure(0, weight=1)
cred_tab.rowconfigure(0, weight=1) # Row for centering frame
cred_tab.rowconfigure(1, weight=0) # Row for text

# Frame para centrar el contenido en la pestaña de créditos
center_frame_credits = ttk.Frame(cred_tab)
center_frame_credits.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
center_frame_credits.columnconfigure(0, weight=1)
center_frame_credits.rowconfigure(0, weight=1)
center_frame_credits.rowconfigure(1, weight=0) # For the text

# Load and display the image (f2.txt)
image_label_credits = None # Global reference for image to prevent garbage collection
try:
    script_dir = os.path.dirname(__file__)
    image_path = os.path.join(script_dir, "f2.jpg") # Assuming f2.txt is an image file

    img = Image.open(image_path)
    # Define a medium size, e.g., max 300x300 pixels
    max_size = (300, 300)
    img.thumbnail(max_size, Image.LANCZOS) # Resize while maintaining aspect ratio

    photo = ImageTk.PhotoImage(img)
    image_label_credits = ttk.Label(center_frame_credits, image=photo)
    image_label_credits.image = photo # Keep a reference!
    image_label_credits.grid(row=0, column=0, pady=(20, 5), sticky="s") # Stick to south to push text down

except FileNotFoundError:
    error_label = ttk.Label(center_frame_credits, text="Error: 'f2.txt' no encontrada.", foreground="red")
    error_label.grid(row=0, column=0, pady=20)
except Exception as e:
    error_label = ttk.Label(center_frame_credits, text=f"Error al cargar la imagen: {e}", foreground="red")
    error_label.grid(row=0, column=0, pady=20)

# Label for "Qian Li"
name_label = ttk.Label(center_frame_credits, text="Qian Li", font=('Arial', 12, 'bold'))
name_label.grid(row=1, column=0, pady=(5, 20), sticky="n") # Stick to north to pull text up


#---Parte derecha del grafo---#

graph_frame = ttk.LabelFrame(root, text="Grafo")
graph_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
graph_frame.rowconfigure(0, weight=1)
graph_frame.columnconfigure(0, weight=1)


mostrar_grafo("Cataluña", *grafos_data["Cataluña"])


root.update_idletasks()
root.mainloop()