
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
btn_load_structure = tk.Button(gates_frame, text='Load Airport Structure', command=Load_Airport_Structure)
btn_load_structure.pack(padx=5, pady=10, fill=tk.X)


# Botón para set gates
btn_set_gates = tk.Button(gates_frame, text='Set Gates', command=Set_Gates)
btn_set_gates.pack(padx=5, pady=5, fill=tk.X)


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

#Botón para tutorial
button_tutorial3 = tk.Button(gates_frame, text='Tutotial of GATES', command=None)
button_tutorial3.pack(padx=5, pady=10, fill=tk.X)



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


