# step 5
import matplotlib.pyplot as plt
def PlotFlightPlan (fp):
    for wp in fp.waypoints:
        plt.plot(wp.lat,wp.lon, 'o', color='red', markersize=5)
        plt.text( wp.lat + 0.5, wp.lon + 0.5, wp.name,color='green', weight='bold', fontsize=6)
    # Coordenadas de un punto en el extremo Noroeste de la penñinsula ibérica
    latNW = 43.62481631158062
    lonNW = -8.902207838560653
    # Coordenadas de un punto en el extremo Sureste de la península ibérica
    latSE = 35.98754955400314
    lonSE = 3.8847514743561953

    plt.axis([latSE, latNW, lonNW, lonSE])
    plt.grid(color='red', linestyle='dashed', linewidth=0.5)
    plt.title('Tu plan de vuelo: '+ fp.name)
    plt.show()
