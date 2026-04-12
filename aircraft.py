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
        return
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