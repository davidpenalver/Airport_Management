# Aircraft class
class Aircraft:
    def __init__(self, aircraft_id="", origin_airport="", landing_time="", airline_company=""):
        self.aircraft_id = aircraft_id
        self.origin_airport = origin_airport
        self.landing_time = landing_time
        self.airline_company = airline_company

#Function 1: Return arrivals information.
def LoadArrivals(filename):
    aircrafts=[]
    try:
        with open(filename, "r") as file:
            file.readline()
            for line in file:
                parts = line.split()
                if len(parts)!=4:
                    continue
                aircraft_id = parts[0]
                origin=parts[1]
                time=parts[2]
                airline=parts[3]
                if len(time)<3 or time[2]!=":":
                    continue
                try:
                    h, m=time.split(':')
                    h, m=int(h), int(m)
                    if (h<0 or h>23) or (m<0 or m>59):
                        continue
                except:
                    continue
                aircraft=Aircraft(aircraft_id, origin, time, airline)
                aircrafts.append(aircraft)
    except:
        return []
    return aircrafts

#Function 2: Plot landing frequency.
def PlotArrivals(aircrafts):
    import matplotlib.pyplot as plt
    if len(aircrafts)==0:
        print("No aircrafts found")
        return
    Vx=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    hours=[0]*24
    for aircraft in aircrafts:
        try:
            time=aircraft.landing_time
            h=int(time.split(":")[0])
            hours[h]+=1
        except:
            continue
    plt.bar(Vx, hours)
    plt.xlabel("Hours")
    plt.ylabel("Arrivals")
    plt.title("Arrivals frequency per hour")
    plt.show()

#Function 3: Write list of aircrafts info a file.
def SaveFlights(aircrafts, filename):
    if len(aircrafts)==0:
        print("No aircrafts found")
        return -1
    try:
        with open(filename, "w") as file:
            file.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")
            i=0
            while i<len(aircrafts):
                aircraft=aircrafts[i]

                aircraft_id=aircraft.aircraft_id
                origin_airport=aircraft.origin_airport
                landing_time=aircraft.landing_time
                airline_company=aircraft.airline_company

                if aircraft_id=="":
                    aircraft_id="-"
                if origin_airport=="":
                    origin_airport="-"
                if landing_time=="":
                    landing_time="-"
                if airline_company=="":
                    airline_company="-"
                file.write(aircraft_id + " " + origin_airport + " " + landing_time + " " + airline_company + "\n")
                i+=1
        return 0
    except:
        return -1

#Function 4: Plot of the number of flights per airline.
def PlotAirlines(aircrafts):
    import matplotlib.pyplot as plt
    if len(aircrafts) == 0:
        print("No aircrafts found")
        return -1
    airlines=[]
    count=[]
    i=0
    while i<len(aircrafts):
        airline=aircrafts[i].airline_company
        found = False
        j = 0
        while j<len(airlines) and not found:
            if airlines[j]==airline:
                count[j]+=1
                found=True
            j+=1
        if not found:
            airlines.append(airline)
            count.append(1)
        i+=1
    plt.bar(airlines, count)
    plt.xlabel("Airlines")
    plt.ylabel("Number of flights")
    plt.title("Flights per airline")
    plt.show()

#Function 5: Number of flights from Schengen and Non-Schengen.
def PlotFlightsType(aircrafts):
    import matplotlib.pyplot as plt
    if len(aircrafts) == 0:
        print("No aircrafts found")
        return -1
    schengen_codes=['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG',
                      'EH', 'LH', 'BI', 'LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP',
                      'LP', 'LZ', 'LJ', 'LE', 'ES', 'LS']
    schengen_count=0
    non_schengen_count=0
    i=0
    while i<len(aircrafts):
        code=aircrafts[i].origin_airport[:2].upper()
        found=False
        j=0
        while j<len(schengen_codes) and not found:
            if code==schengen_codes[j]:
                found=True
            else:
                j+=1
        if found:
            schengen_count+=1
        else:
            non_schengen_count+=1
        i+=1
    plt.bar("Flights", schengen_count, label="Schengen")
    plt.bar("Flights", non_schengen_count, bottom=schengen_count, label="Non-Schengen")
    plt.ylabel("Number of flights")
    plt.title("Schengen vs. Non-Schengen flights")
    plt.legend()
    plt.show()

#Function 6: Shows in Google Earth the trajectories of all flights.
def MapFlights(aircrafts, airports):
    from airport import *
    if len(aircrafts) == 0 or len(airports) == 0:
        print("No data available")
        return -1
#Update schengen.
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1
#Search LEBL with it's atributes.
    dest_airport = None
    i=0
    while i < len(airports):
        if airports[i].icao == "LEBL":
            dest_airport = airports[i]
        i += 1
    if dest_airport is None:
        print("Destination airport LEBL not found")
        return -1
    try:
        with open("FlightsMap.kml", "w") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
            file.write('<Document>\n')
            i = 0
            while i < len(aircrafts):
                aircraft = aircrafts[i]
                origin_code = aircraft.origin_airport
                #Search airport of origin.
                origin_airport = None
                j=0
                while j<len(airports):
                    if airports[j].icao==origin_code:
                        origin_airport=airports[j]
                    j+=1
                if origin_airport is None:
                    i+=1
                    continue
#Color.
                if origin_airport.schengen:
                    color="ff00ff00"
                else:
                    color="ff0000ff"
                file.write("<Placemark>\n")
                file.write("<Style>\n")
                file.write("<LineStyle>\n")
                file.write("<color>" + color + "</color>\n")
                file.write("<width>2</width>\n")
                file.write("</LineStyle>\n")
                file.write("</Style>\n")
                file.write("<LineString>\n")
                file.write("<coordinates>\n")
                file.write(str(origin_airport.longitude) + "," + str(origin_airport.latitude) + ",0 "+ str(dest_airport.longitude) + "," + str(dest_airport.latitude) + ",0\n")
                file.write("</coordinates>\n")
                file.write("</LineString>\n")
                file.write("</Placemark>\n")
                i+=1
            file.write("</Document>\n")
            file.write("</kml>\n")
        print("File 'FlightsMap.kml' created")
        return 0
    except:
        return -1

#Function 7: Aircrafts that come from +2000km away.
def LongDistanceArrivals(aircrafts, airports):
    import math
    longdistance=[]
    if len(aircrafts) == 0 or len(airports) == 0:
        return longdistance
    i=0
    destination=None
    found=False
    while i < len(airports) and not found:
        if airports[i].icao=="LEBL":
            destination=airports[i]
            found=True
        i=i+1
    if not found:
        return longdistance
    i=0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        origin=aircraft.origin_airport
        found= False
        j=0
        while j<len(airports) and not found:
            if origin==airports[j].icao:
                origin=airports[j]
                found=True
            j=j+1
        if not found:
            i=i+1
            continue
#Haversine formula.
        R=6371 #km
        lat1=math.radians(origin.latitude)
        lat2=math.radians(destination.latitude)
        lon1=math.radians(origin.longitude)
        lon2=math.radians(destination.longitude)
        dlat=abs(lat2-lat1)
        dlon=abs(lon2-lon1)
        a=(math.sin(dlat/2)**2)+math.cos(lat1)*math.cos(lat2)*(math.sin(dlon/2)**2)
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        d=R*c
#Compare distances.
        if d>2000:
            longdistance.append(aircraft)
        i=i+1
    return longdistance