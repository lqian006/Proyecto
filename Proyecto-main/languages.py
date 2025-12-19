LANGUAGES = {
    "ES": {
        # Tabs
        "tab_airports": "🛫 Aeropuertos",
        "tab_flights": "✈️ Vuelos",
        "tab_gates": "🛬 Puertas",
        "tab_departures": "📝 Salidas",

        # Airports
        "airports": "Aeropuertos",
        "load_airports": "Cargar aeropuertos",
        "add_airports": "Añadir aeropuerto",
        "airport_code": "Código (ej. LEBL)",
        "latitude": "Latitud (ej. N412851)",
        "longitude": "Longitud (ej. E0020500)",
        "add": "Añadir",
        "delete_airports": "Borrar aeropuerto",
        "delete": "Borrar",
        "show_airports": "Mostrar aeropuertos",
        "show": "Mostrar",
        "set_schengen": "Definir Schengen",
        "schengen": "Schengen",
        "set": "Definir",
        "save_schengen": "Guardar aeropuertos Schengen",
        "file_name": "Nombre de archivo",
        "save": "Guardar",
        "plot_schengen": "Graficar aeropuertos Schengen",
        "map_airports": "Ver aeropuertos en Google Earth",

        # Flights
        "flights": "Vuelos",
        "load_flights": "Cargar vuelos",
        "save_flights": "Guardar vuelos",
        "file_name": "Nombre de archivo (.txt)",
        "save": "Guardar",
        "plot_flights_hour": "Graficar vuelos por hora",
        "plot_flights_company": "Graficar vuelos por aerolínea",
        "plot_flights_type": "Graficar tipos de aviones",
        "map_flights_LEBL": "Ver vuelos hacia LEBL",
        "map_long_distance": "Ver vuelos de larga distancia (>2000km)",

        "tab_gates": "🚪 Puertas",
        "gates_frame": "Puertas",
        "load_airport_structure": "Cargar estructura del aeropuerto",
        "btn_set_gates": "Configurar puertas",
        "terminal_label": "Terminal:",
        "area_label": "Área:",
        "prefix_label": "Prefijo:",
        "gate_start_label": "Gate inicio:",
        "gate_end_label": "Gate final:",
        "create_button": "Crear",
        "btn_load_airlines": "Cargar aerolíneas",
        "load_airlines_button": "Cargar aerolíneas",
        "show_gate_occupancy": "Mostrar ocupación de puertas",
        "btn_is_airline_in_terminal": "Comprobar aerolínea en terminal",
        "airline_label": "Aerolínea (ICAO):",
        "check_airline_button": "Comprobar aerolínea",
        "btn_search_terminal": "Buscar terminal",
        "search_terminal_button": "Buscar terminal",
        "assign_gates_arrivals": "Asignar puertas a llegadas",

        # Departures
        "departures": "Salidas",
        "load_departures": "Cargar salidas",
        "merge_movements": "Combinar movimientos",
        "night_departures": "Salidas nocturnas",
        "assign_night_gates": "Asignar puertas nocturnas",
        "free_gates": "Puertas libres",
        "assign_gates_at_time": "Asignar puertas por hora",
        "plot_day_occupancy": "Disponibilidad en un día",
        "flight_search": "🔍 Buscar vuelo",

        # Títulos y textos de tutoriales
        "tut_load_airports_title": "Tutorial - Cargar aeropuertos",
        "tut_load_airports_text": "Con este botón puedes cargar un archivo “airports.txt” que contiene el código ICAO del aeropuerto con su latitud y longitud y te lo muestra en un gráfico en la interfaz. En el gráfico aparecen los aeropuertos según su latitud y longitud, pintados de verde si son Schengen y de rojo si no son Schengen.\nAl darle al botón, el programa te abrirá el explorador de archivos, ahí podrás escoger el archivo que desees cargar y al darle a abrir, se te habrá cargado el archivo al programa.",

        "tut_add_airports_title": "Tutorial - Añadir aeropuertos",
        "tut_add_airports_text": "Esta función te permite añadir aeropuertos al sistema. Debes escribir el código, latitud y longitud del aeropuerto y pulsar el botón 'Añadir'.",

        "tut_delete_airports_title": "Tutorial - Eliminar aeropuertos",
        "tut_delete_airports_text": "Esta función te permite borrar cualquier aeropuerto que se encuentre en el mapa. Para ello, debes escribir el código del aeropuerto que desees borrar y darle al botón 'Borrar'.\nNota: Es necesario tener cargado el archivo 'airports.txt' para poder usar esta función.",

        "tut_show_airports_title": "Tutorial - Ver datos aeropuertos",
        "tut_show_airports_text": "Esta función enseña los datos del aeropuerto que quieras. Escribiendo el código del aeropuerto del que quieres saber datos y dándole al botón 'Mostrar', te enseña el código ICAO del aeropuerto, su latitud, su longitud y si tiene propiedad Schengen o no.\nNota: Es necesario tener cargado el archivo 'airports.txt' para poder usar esta función.",

        "tut_set_schengen_title": "Tutorial - Dar atributo Schengen a aeropuertos",
        "tut_set_schengen_text": "Esta función te permite darle o quitar el atributo Schengen a un aeropuerto. Escribe el código del aeropuerto y marca o desmarca la casilla 'Schengen', luego pulsa 'Cambiar'.\nNota: Es necesario tener cargado el archivo 'airports.txt' para poder usar esta función.",

        "tut_save_schengen_title": "Tutorial - Guardar aeropuertos Schengen",
        "tut_save_schengen_text": "Esta función te permite crear un archivo .txt con la información de todos los aeropuertos con el atributo Schengen. Escribiendo en la caja de texto el nombre del archivo y pulsando 'Guardar' se creará el archivo.\nNota: Es necesario tener cargado el archivo 'airports.txt'.",

        "tut_plot_schengen_title": "Tutorial - Gráficos de aeropuertos Schengen",
        "tut_plot_schengen_text": "Este botón te crea un gráfico de barras con el número de aeropuertos Schengen y no Schengen.\nNota: Es necesario tener cargado el archivo 'airports.txt'.",

        "tut_map_airports_title": "Tutorial - Mapa de aeropuertos",
        "tut_map_airports_text": "Este botón abre en Google Earth los aeropuertos Schengen y no Schengen, mostrando los datos de la interfaz en un mapa 3D.\nNota: Es necesario tener Google Earth instalado y cargado 'airports.txt'.",

        "tut_load_flights_title": "Tutorial - Cargar vuelos",
        "tut_load_flights_text": "Con este botón puedes cargar un archivo 'arrivals.txt' que contiene ID del avión, aeropuerto de origen, hora de llegada a LEBL y aerolínea. El programa abrirá el explorador de archivos para seleccionar el archivo. Una vez cargado, se mostrará una ventana con los vuelos cargados con éxito.",

        "tut_save_flights_title": "Tutorial - Guardar vuelos",
        "tut_save_flights_text": "Esta función crea un archivo .txt con la información de todos los vuelos cargados actualmente. Escribiendo el nombre y pulsando 'Guardar', se guardará el archivo.\nNota: Debes haber cargado 'arrivals.txt'.",

        "tut_plot_flights_hour_title": "Tutorial - Gráfico de vuelos por hora",
        "tut_plot_flights_hour_text": "Este botón crea un gráfico mostrando el número de vuelos que aterrizan cada hora en el aeropuerto.\nNota: Debes haber cargado 'arrivals.txt'.",

        "tut_plot_flights_company_title": "Tutorial - Gráfico de vuelos por compañías",
        "tut_plot_flights_company_text": "Este botón crea un gráfico mostrando el número de vuelos que pertenecen a cada compañía.",

        "tut_plot_flights_type_title": "Tutorial - Gráfico de vuelos",
        "tut_plot_flights_type_text": "Este botón crea un gráfico de barras con el número de vuelos Schengen y no Schengen.\nNota: Debes haber cargado 'arrivals.txt'.",

        "tut_map_flights_LEBL_title": "Tutorial - Mapa de vuelos a LEBL",
        "tut_map_flights_LEBL_text": "Este botón abre en Google Earth todos los vuelos que llegan a LEBL, mostrando en verde los vuelos Schengen y en rojo los no Schengen.\nNota: Debes haber cargado 'arrivals.txt' y 'airports.txt'.",

        "tut_map_long_distance_title": "Tutorial - Mapa de vuelos a distancia",
        "tut_map_long_distance_text": "Este botón abre en Google Earth los vuelos que llegan a LEBL y que tienen más de 2000 km, mostrando en verde los Schengen y en rojo los no Schengen.\nNota: Debes haber cargado 'arrivals.txt' y 'airports.txt'.",

        "tut_load_airport_structure_title": "Tutorial - Cargar estructura del aeropuerto",
        "tut_load_airport_structure_text": "Este botón carga la estructura del aeropuerto LEBL desde 'Terminal.txt'.",

        "tut_set_gate_title": "Tutorial - Generar puertas",
        "tut_set_gate_text": "Este botón genera puertas a partir de la información introducida en las cajas de texto (terminal, área, inicio, final y prefijo) y pulsando 'Crear'.\nNota: Debes haber cargado 'Terminals.txt'.",

        "tut_load_airlines_title": "Tutorial - Cargar aerolíneas",
        "tut_load_airlines_text": "Este botón carga las aerolíneas en la terminal deseada. Debes indicar la terminal en la caja de texto.\nNota: Debes haber cargado 'Terminals.txt'.",

        "tut_show_gate_occupancy_title": "Tutorial - Ver ocupación de puertas",
        "tut_show_gate_occupancy_text": "Este botón muestra una ventana con el número de puertas totales, libres y ocupadas.\nNota: Debes haber cargado 'Terminals.txt'.",

        "tut_is_airline_in_terminal_title": "Tutorial - Ver aerolínea en terminal",
        "tut_is_airline_in_terminal_text": "Este botón muestra si una aerolínea se encuentra en cierta terminal. Indica la terminal y aerolínea y pulsa 'Buscar'.\nNota: Debes haber cargado 'Terminals.txt'.",

        "tut_search_terminal_title": "Tutorial - Buscar terminal",
        "tut_search_terminal_text": "Este botón muestra en qué terminal opera cierta aerolínea. Indica la aerolínea y pulsa 'Buscar'.\nNota: Debes haber cargado 'Terminals.txt'.",

        "tut_assign_gates_arrivals_title": "Tutorial - Asignar puertas a las llegadas",
        "tut_assign_gates_arrivals_text": "Este botón asigna una puerta a cada vuelo que llega al aeropuerto. Muestra cuántos vuelos no pudieron ser asignados.\nNota: Debes haber cargado 'Terminals.txt' y 'arrivals.txt'.",

        "tut_load_departures_title": "Tutorial - Cargar salidas",
        "tut_load_departures_text": "Carga el archivo 'Departures.txt' con ID, destino, hora de salida y aerolínea. Se abre el explorador para seleccionar el archivo.",

        "tut_merge_movements_title": "Tutorial - Fusionar movimientos",
        "tut_merge_movements_text": "Junta 'Arrivals.txt' y 'Departures.txt' en una lista ordenada de 00:00 a 23:59.\nNota: Debes tener cargados ambos archivos.",

        "tut_night_departures_title": "Tutorial - Salidas nocturnas",
        "tut_night_departures_text": "Muestra información de vuelos nocturnos (20:00 a 6:00) de la lista fusionada.\nNota: Debes haber usado Merge Movements.",

        "tut_assign_night_gates_title": "Tutorial - Asignar puertas noche",
        "tut_assign_night_gates_text": "Asigna puertas de noche a los aviones. Informa cuántos no pudieron ser asignados.\nNota: Debes haber usado Merge Movements.",

        "tut_assign_gates_at_time_title": "Tutorial - Asignar puertas por hora",
        "tut_assign_gates_at_time_text": "Asigna y libera puertas a aviones dentro de un periodo de una hora. Indica la hora exacta y pulsa 'Asignar'.\nNota: Debes haber usado Merge Movements.",

        "tut_plot_occupancy_title": "Tutorial - Gráfico de ocupaciones en un dia",
        "tut_plot_occupancy_text": "Muestra un gráfico de barras y líneas de ocupación de gates y aviones sin puerta a lo largo del día.\nNota: Debes haber usado Merge Movements.",

        "tut_filter_title": "Tutorial - Filtro",
        "tut_filter_text": "Permite buscar vuelos aplicando filtros: ID, compañía, país, hora, puerta y terminal. Pulsa 'Buscar' para mostrar resultados."


    },

    "EN": {
        # Tabs
        "tab_airports": "🛫 Airports",
        "tab_flights": "✈️ Flights",
        "tab_gates": "🛬 Gates",
        "tab_departures": "📝 Departures",

        # Airports
        "airports": "Airports",
        "load_airports": "Load airports",
        "add_airports": "Add airport",
        "airport_code": "Code (e.g. LEBL)",
        "latitude": "Latitude (e.g. N412851)",
        "longitude": "Longitude (e.g. E0020500)",
        "add": "Add",
        "delete_airports": "Delete airport",
        "delete": "Delete",
        "show_airports": "Show airport data",
        "show": "Show",
        "set_schengen": "Set Schengen attribute",
        "schengen": "Schengen",
        "set": "Set",
        "save_schengen": "Save Schengen airports",
        "file_name": "File name",
        "save": "Save",
        "plot_schengen": "Plot Schengen airports in stacked bar",
        "map_airports": "Map airports in Google Earth",

        # Flights
        "flights": "Flights",
        "load_flights": "Load flights",
        "save_flights": "Save flights",
        "file_name": "File name (.txt)",
        "save": "Save",
        "plot_flights_hour": "Plot flights per hour",
        "plot_flights_company": "Plot flights per company",
        "plot_flights_type": "Plot flights by type",
        "map_flights_LEBL": "Map flights to LEBL",
        "map_long_distance": "Map long distance arrivals (>2000km)",

        "tab_gates": "🚪 Gates",
        "gates_frame": "Gates",
        "load_airport_structure": "Load Airport Structure",
        "btn_set_gates": "Set Gates",
        "terminal_label": "Terminal:",
        "area_label": "Area:",
        "prefix_label": "Prefix:",
        "gate_start_label": "Gate start:",
        "gate_end_label": "Gate end:",
        "create_button": "Create",
        "btn_load_airlines": "Load Airlines",
        "load_airlines_button": "Load Airlines",
        "show_gate_occupancy": "Show Gate Occupancy",
        "btn_is_airline_in_terminal": "Is Airline In Terminal",
        "airline_label": "Airline (ICAO):",
        "check_airline_button": "Check Airline",
        "btn_search_terminal": "Search Terminal",
        "search_terminal_button": "Search Terminal",
        "assign_gates_arrivals": "Assign Gates to Arrivals",

        # Departures
        "departures": "Departures",
        "load_departures": "Load Departures",
        "merge_movements": "Merge Movements",
        "night_departures": "Night departures",
        "assign_night_gates": "Assign night gates",
        "free_gates": "Free gates",
        "assign_gates_at_time": "Assign gates at time",
        "plot_day_occupancy": "Plot occupancy in a day",
        "flight_search": "🔍 Flight Search",

        # Titles and tutorial texts
        "tut_load_airports_title": "Tutorial - Load airports",
        "tut_load_airports_text": "This button allows you to load 'airports.txt' containing ICAO codes, latitude, and longitude, and displays them in a graph. Green airports are Schengen, red are not.\nThe file explorer will open to select the file, then it will be loaded into the program.",

        "tut_add_airports_title": "Tutorial - Add airports",
        "tut_add_airports_text": "This function allows you to add airports to the system. Enter the code, latitude and longitude and press 'Add'.",

        "tut_delete_airports_title": "Tutorial - Delete airports",
        "tut_delete_airports_text": "This function allows you to delete airports from the map. Enter the airport code and press 'Delete'.\nYou must have loaded 'airports.txt'.",

        "tut_show_airports_title": "Tutorial - Show airport data",
        "tut_show_airports_text": "This function shows data for the selected airport. Enter the ICAO code and press 'Show' to see code, latitude, longitude, and Schengen property.\nYou must have loaded 'airports.txt'.",

        "tut_set_schengen_title": "Tutorial - Set Schengen attribute",
        "tut_set_schengen_text": "This function allows you to set or remove Schengen status for an airport. Enter the code, check/uncheck 'Schengen', and press 'Set'.\nYou must have loaded 'airports.txt'.",

        "tut_save_schengen_title": "Tutorial - Save Schengen airports",
        "tut_save_schengen_text": "This function creates a .txt file with all Schengen airports. Enter a file name and press 'Save'.\nYou must have loaded 'airports.txt'.",

        "tut_plot_schengen_title": "Tutorial - Schengen airports plot",
        "tut_plot_schengen_text": "This button creates a bar chart showing the number of Schengen and non-Schengen airports.\nYou must have loaded 'airports.txt'.",

        "tut_map_airports_title": "Tutorial - Map airports",
        "tut_map_airports_text": "This button opens Google Earth showing Schengen and non-Schengen airports on a 3D map.\nGoogle Earth must be installed and 'airports.txt' loaded.",

        "tut_load_flights_title": "Tutorial - Load flights",
        "tut_load_flights_text": "Load 'arrivals.txt' with plane ID, origin, arrival time at LEBL, and airline. The file explorer will open to select the file. After loading, a window confirms flights loaded successfully.",

        "tut_save_flights_title": "Tutorial - Save flights",
        "tut_save_flights_text": "Creates a .txt file with all loaded arrivals. Enter a name and press 'Save'.\nYou must have loaded 'arrivals.txt'.",

        "tut_plot_flights_hour_title": "Tutorial - Plot arrivals per hour",
        "tut_plot_flights_hour_text": "Creates a chart showing number of arrivals per hour.\nYou must have loaded 'arrivals.txt'.",

        "tut_plot_flights_company_title": "Tutorial - Plot arrivals per company",
        "tut_plot_flights_company_text": "Creates a chart showing number of flights per airline.",

        "tut_plot_flights_type_title": "Tutorial - Flights chart",
        "tut_plot_flights_type_text": "Creates a bar chart showing Schengen and non-Schengen flights.\nYou must have loaded 'arrivals.txt'.",

        "tut_map_flights_LEBL_title": "Tutorial - Map flights to LEBL",
        "tut_map_flights_LEBL_text": "Opens Google Earth showing flights arriving at LEBL. Green = Schengen, Red = non-Schengen.\nMust have 'arrivals.txt' and 'airports.txt' loaded.",

        "tut_map_long_distance_title": "Tutorial - Map long distance flights",
        "tut_map_long_distance_text": "Opens Google Earth showing flights >2000 km arriving at LEBL. Green = Schengen, Red = non-Schengen.\nMust have 'arrivals.txt' and 'airports.txt' loaded.",

        "tut_load_airport_structure_title": "Tutorial - Load airport structure",
        "tut_load_airport_structure_text": "Loads the structure of LEBL from 'Terminal.txt'.",

        "tut_set_gate_title": "Tutorial - Generate gates",
        "tut_set_gate_text": "Generates gates based on provided information (terminal, area, start, end, prefix). Press 'Create'.\nMust have 'Terminals.txt'.",

        "tut_load_airlines_title": "Tutorial - Load airlines",
        "tut_load_airlines_text": "Loads airlines into the specified terminal. Enter the terminal number.\nMust have 'Terminals.txt'.",

        "tut_show_gate_occupancy_title": "Tutorial - Show gate occupancy",
        "tut_show_gate_occupancy_text": "Shows total, free and occupied gates.\nMust have 'Terminals.txt'.",

        "tut_is_airline_in_terminal_title": "Tutorial - Check airline in terminal",
        "tut_is_airline_in_terminal_text": "Shows if an airline is in a terminal. Enter terminal and airline and press 'Search'.\nMust have 'Terminals.txt'.",

        "tut_search_terminal_title": "Tutorial - Search terminal",
        "tut_search_terminal_text": "Shows in which terminal a certain airline operates. Enter airline and press 'Search'.\nMust have 'Terminals.txt'.",

        "tut_assign_gates_arrivals_title": "Tutorial - Assign gates to arrivals",
        "tut_assign_gates_arrivals_text": "Assigns a gate to each arriving flight. Shows unassigned flights.\nMust have 'Terminals.txt' and 'arrivals.txt'.",

        "tut_load_departures_title": "Tutorial - Load departures",
        "tut_load_departures_text": "Load 'Departures.txt' with ID, destination, departure time, and airline. File explorer opens to select the file.",

        "tut_merge_movements_title": "Tutorial - Merge movements",
        "tut_merge_movements_text": "Merges 'Arrivals.txt' and 'Departures.txt' into a single list ordered by time (00:00 to 23:59).\nMust have both files loaded.",

        "tut_night_departures_title": "Tutorial - Night departures",
        "tut_night_departures_text": "Shows information about night flights (20:00 to 6:00) from the merged list.\nMust have used Merge Movements.",

        "tut_assign_night_gates_title": "Tutorial - Assign night gates",
        "tut_assign_night_gates_text": "Assigns night gates to planes. Shows unassigned planes.\nMust have used Merge Movements.",

        "tut_assign_gates_at_time_title": "Tutorial - Assign gates by time",
        "tut_assign_gates_at_time_text": "Assigns and releases gates for planes within a one-hour period. Enter exact hour and press 'Assign'.\nMust have used Merge Movements.",

        "tut_plot_occupancy_title": "Tutorial - Daily occupancy chart",
        "tut_plot_occupancy_text": "Shows a bar and line chart of gate occupancy and planes without gate over the day.\nMust have used Merge Movements.",

        "tut_filter_title": "Tutorial - Filter",
        "tut_filter_text": "Allows searching flights applying filters: ID, airline, country, time, gate, and terminal. Press 'Search' to show results."

    }
}
