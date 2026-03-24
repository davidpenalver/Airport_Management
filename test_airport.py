from airport import *
airport = Airport ("LEBL", 41.297445, 2.0832941)
SetSchengen(airport)
PrintAirport (airport)

# Probar si han cargado los aeropuertos.
airports=LoadAirports ("Airports.txt")
if len(airports)==0:
    print("Error loading")
else:
    print(str(len(airports)) + " aeropuertos cargados.")

#Set Schengen de todos los aeropuetos.
i = 0
while i<len(airports):
    SetSchengen(airports[i])
    i=i+1

# Probar Save Schengen.
ssa=SaveSchengenAirports(airports, "SaveSchengenAirports.txt")
if ssa==0:
    print("Successfully saved.")
else:
    print("Error saving")

# Probar añadir aeropuerto.
new_air=Airport("Test", 10.0, 20.0)
ap=AddAirport(airports,new_air)
if ap==0:
    print("Successfully added")
else:
    print("Error adding")

# Probar eliminar aeropuerto.
ra=RemoveAirport(airports,new_air.icao)
if ra==0:
    print("Successfully removed")
else:
    print("Error removing")

# Probar Schengen vs. Non Schengen Graph.
PlotAirports(airports)

# Probar Mapas aeropuertos.
result=MapAirports(airports)
if result==0:
    print("Successfully mapped")
else:
    print("Error mapping")