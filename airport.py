#Aiport class.
class Airport:
    def __init__(self, icao="", latitude=0.0, longitude=0.0):
        self.icao = icao
        self.latitude = latitude
        self.longitude = longitude
        self.schengen=False

#Function 1: Is Schengen Airport.
def IsSchengenAirport(code):
    if len(code)<2:
        return False
    schengen_codes=['LO','EB','LK','LC','EK','EE','EF','LF','ED','LG',
            'EH','LH','BI','LI','EV','EY','EL','LM','EN','EP',
            'LP','LZ','LJ','LE','ES','LS']
    found=False
    i=0
    while i<len(schengen_codes) and not found:
        if code[:2].upper()==schengen_codes[i]:
            found=True
        else:
            i=i+1
    if found:
        return True
    else:
        return False

#Function 2: Set Schengen.
def SetSchengen(airport):
    if IsSchengenAirport(airport.icao):
        airport.schengen=True
    else:
        airport.schengen=False

#Function 3: Print airport.
def PrintAirport(airport):
    print("Airport ICAO code: " + airport.icao)
    print("Latitude: "+ str(airport.latitude))
    print("Longitude: " + str(airport.longitude))
    print("Schengen: " + str(airport.schengen))

#Function 4: Return list. STEP 3.
def LoadAirports(filename):
    airports=[]
    try:
        with open(filename, "r") as file:
#Saltar la cabecera:
            file.readline()
            for line in file:
                parts=line.split()
#Si hay error en una fila, la salta, no elimina el proceso.
                if len(parts)!=3:
                    continue
                code=parts[0]
                str_lat=parts[1]
                str_long=parts[2]
#Convertir LAT a floats.
                dire=str_lat[0]
                deg=float(str_lat[1:3])
                min=float(str_lat[3:5])
                sec=float(str_lat[5:7])
                latitude= deg + min/60 + sec/3600
                if dire=="S" or dire=="W":
                    latitude=-latitude
#Convertir LON a floats.
                dire=str_long[0]
                deg=float(str_long[1:4])
                min=float(str_long[4:6])
                sec=float(str_long[6:8])
                longitude= deg + min/60 + sec/3600
                if dire=="S" or dire=="W":
                    longitude = -longitude
                airport=Airport(code, latitude, longitude)
                airports.append(airport)
    except:
        return[]
    return airports

#Function 5: Write only Schengen Airports information.
def SaveSchengenAirports(airports, filename):
    if len(airports)==0:
        return -1
    try:
        with open(filename, "w") as file:
            file.write("CODE LATITUDE LONGITUDE\n")
            i=0
            while i<len(airports):
                airport=airports[i]
                if airport.schengen:
                    file.write(airport.icao + " " + str(airport.latitude) + " " + str(airport.longitude) + "\n")
                i=i+1
        return 0
    except:
        return -1

#Function 6: Add Airport.
def AddAirport(airports, airport):
    i=0
    found=False
    while i<len(airports) and not found:
        if airport.icao == airports[i].icao:
            found=True
        else:
            i=i+1
    if not found:
        airports.append(airport)
        return 0
    else:
        return -1

#Function 7: Remove Airports.
def RemoveAirport(airports, code):
    i=0
    found=False
    while i<len(airports) and not found:
        if code == airports[i].icao:
            found=True
        else:
            i=i+1
    if found:
        airports.pop(i)
        return 0
    else:
        return -1

#Function 8: Graph Schengen and non Schengen airports.
def PlotAirports(airports):
    import matplotlib.pyplot as plt
    if len(airports)==0:
        print("No airports found")
        return
    schengen_count=0
    non_schengen_count=0
    i=0
    while i<len(airports):
        if airports[i].schengen:
            schengen_count+=1
        else:
            non_schengen_count+=1
        i=i+1
    plt.figure()
    plt.bar("Airport", schengen_count, label="Schengen")
    plt.bar("Airport", non_schengen_count, bottom=schengen_count, label="Non Schengen")
    plt.title("Schengen vs Non-Schengen")
    plt.ylabel("Count")
    plt.legend()
    return plt

#Function 9: Google Earth Plot.
def MapAirports(airports):
    if len(airports)==0:
        print("No airports found")
        return -1
    try:
        with open("AirportsMaps.kml", "w") as file:
            file.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            file.write('<Document>\n')
            i=0
            while i<len(airports):
                airport=airports[i]
                if airport.schengen:
                    color="ff0000ff"
                else:
                    color="ff00ff00"
                file.write("<Placemark>\n")
                file.write("<name>" + airport.icao + "</name>\n")
                file.write("<Style>\n")
                file.write("<IconStyle>\n")
                file.write("<color>" + color + "</color>\n")
                file.write("</IconStyle>\n")
                file.write("</Style>\n")
                file.write("<Point>\n")
                file.write("<coordinates>" + str(airport.longitude) + "," + str(airport.latitude) + ",0</coordinates>\n")
                file.write("</Point>\n")
                file.write("</Placemark>\n")
                i=i+1
            file.write("</Document>\n")
            file.write("</kml>\n")
            return 0
    except:
        return -1