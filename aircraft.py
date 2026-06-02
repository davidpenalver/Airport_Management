from airport import *
#Aircraft class
class Aircraft:
    def __init__(self, aircraft_id="", origin_airport="", landing_time="", airline_company="", destination_airport="", departure_time=""):
        self.aircraft_id = aircraft_id
        self.origin_airport = origin_airport
        self.landing_time = landing_time
        self.airline_company = airline_company
#Reconstruction for V4.
        self.destination_airport = destination_airport
        self.departure_time = departure_time

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
        return -1
    Vx=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    hours=[0]*24
    for aircraft in aircrafts:
        try:
            time=aircraft.landing_time
            h=int(time.split(":")[0])
            hours[h]+=1
        except:
            continue
    plt.figure()
    plt.bar(Vx, hours)
    plt.xlabel("Hours")
    plt.ylabel("Arrivals")
    plt.title("Arrivals frequency per hour")
    return plt
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
    plt.figure()
    plt.bar(airlines, count)
    plt.xlabel("Airlines")
    plt.ylabel("Number of flights")
    plt.title("Flights per airline")
    return plt

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
    plt.figure()
    plt.bar("Flights", schengen_count, label="Schengen")
    plt.bar("Flights", non_schengen_count, bottom=schengen_count, label="Non-Schengen")
    plt.ylabel("Number of flights")
    plt.title("Schengen vs. Non-Schengen flights")
    plt.legend()
    return plt

#Function 6: Shows in Google Earth the trajectories of all flights.
def MapFlights(aircrafts, airports):
    if len(aircrafts) == 0 or len(airports) == 0:
        print("No data available")
        return -1
#Update schengen.
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1
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

#Functions V4:
#Function 1: Load departures and return list only with departures info of each aircraft.
def LoadDepartures(filename):
    departures=[]
    try:
        with open(filename, "r") as file:
            file.readline()
            for line in file:
                parts = line.split()
                if len(parts)!=4:
                    continue
                aircraft_id = parts[0]
                destination=parts[1]
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
                departure=Aircraft(aircraft_id,"","",airline,destination,time)
                departures.append(departure)
    except:
        return []
    return departures

#Function 2: Final list with all the info of the aircraft.
def MergeMovements (aircrafts, departures):
    if len(aircrafts)==0 or len(departures)==0:
        return -1
    result=[]
    used_departures=[]
#Merge arrivals with compatible departures.
    i=0
    while i<len(aircrafts):
        arrival=aircrafts[i]
        merged=False
        j=0
        while j<len(departures) and not merged:
            departure = departures[j]
#Same aircraft and departure not used yet.
            if departure not in used_departures:
                if arrival.aircraft_id==departure.aircraft_id:
#Compare.
                    arrival_h, arrival_m=arrival.landing_time.split(":")
                    departure_h, departure_m=departure.departure_time.split(":")
                    arrival_minutes=int(arrival_h) * 60 + int(arrival_m)
                    departure_minutes=int(departure_h) * 60 + int(departure_m)
#Compatible times.
                    if arrival_minutes<departure_minutes:
                        aircraft=Aircraft(arrival.aircraft_id,arrival.origin_airport,arrival.landing_time,arrival.airline_company,departure.destination_airport,departure.departure_time)
                        result.append(aircraft)
                        used_departures.append(departure)
                        merged=True
            j+=1
#Arrival without departure.
        if not merged:
            aircraft=Aircraft(arrival.aircraft_id,arrival.origin_airport,arrival.landing_time,arrival.airline_company,"","")
            result.append(aircraft)
        i+=1
#Add departure without arrival.
    j=0
    while j<len(departures):
        departure=departures[j]
        if departure not in used_departures:
            aircraft=Aircraft(departure.aircraft_id,"","",departure.airline_company,departure.destination_airport,departure.departure_time)
            result.append(aircraft)
        j+=1
    return result

#Function 3: List of aircraft with only departure information.
def NightAircraft(aircrafts):
    if len(aircrafts)==0:
        return -1
    night_aircrafts=[]
    i = 0
    while i<len(aircrafts):
        aircraft=aircrafts[i]
#No arrival information available.
        if aircraft.origin_airport=="" and aircraft.landing_time=="":
#Has departure information available.
            if aircraft.destination_airport!="" and aircraft.departure_time!="":
                night_aircrafts.append(aircraft)
        i+=1
    return night_aircrafts

#Function 7: Plot the assgined gates per terminal per hour.
def PlotDayOccupancy(aircrafts):
    import matplotlib.pyplot as plt
    if len(aircrafts)==0:
        print("No aircrafts found")
        return -1
    morning=0  #06:00 a 11:59
    afternoon=0  #12:00 a 17:59
    evening=0  #18:00 a 23:59
    night=0  #00:00 a 05:59
    i=0
    while i<len(aircrafts):
        ac=aircrafts[i]
        try:
            h=int(ac.landing_time.split(':')[0])
            if h>=6 and h<12:
                morning+=1
            elif h>=12 and h<18:
                afternoon+=1
            elif h>=18 and h<=23:
                evening+=1
            elif h>=0 and h<6:
                night+=1
        except:
            pass
        i+=1
    vx=["Morning (6-12h)", "Afternoon (12-18h)", "Evening (18-24h)", "Night (0-6h)"]
    vy=[morning, afternoon, evening, night]
    plt.figure()
    plt.bar(vx, vy, color='lightblue', edgecolor='black')
    plt.xlabel("Time Slots")
    plt.ylabel("Number of Arrivals")
    plt.title("Airport Occupancy per Time Slot")
    return plt

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.widgets as widgets

# EXTRA FUNCTION: AirportGateMap

def AirportGateMap(aircrafts, bcn):

    # Validación
    if bcn is None or len(aircrafts) == 0:
        print("AirportGateMap: faltan datos.")
        return -1

    try:
        from LEBL import Gate, BoardingArea, Terminal, BarcelonaAP
        from LEBL import SearchTerminal
        from airport import IsSchengenAirport
    except Exception as e:
        print("AirportGateMap: error importando módulos. " + str(e))
        return -1

    # BLOQUE 1 — Copia profunda manual de bcn
    def clone_bcn(original):
        clone = BarcelonaAP(original.code)
        t = 0
        while t < len(original.terminals):
            ot = original.terminals[t]
            nt = Terminal(ot.name)
            k = 0
            while k < len(ot.airlines):
                nt.airlines.append(ot.airlines[k])
                k += 1
            a = 0
            while a < len(ot.boarding_areas):
                oa = ot.boarding_areas[a]
                na = BoardingArea(oa.name, oa.type)
                g = 0
                while g < len(oa.gates):
                    og = oa.gates[g]
                    ng = Gate(og.name)
                    ng.occupied = og.occupied
                    ng.aircraft_id = og.aircraft_id
                    na.gates.append(ng)
                    g += 1
                nt.boarding_areas.append(na)
                a += 1
            clone.terminals.append(nt)
            t += 1
        return clone

    # BLOQUE 2 — Funciones internas de asignación/liberación
    def _assign_gate(b, aircraft):
        t_name = SearchTerminal(b, aircraft.airline_company)
        if t_name == "":
            return -1
        terminal = None
        i = 0
        while i < len(b.terminals) and terminal is None:
            if b.terminals[i].name == t_name:
                terminal = b.terminals[i]
            i += 1
        if terminal is None:
            return -1
        schengen = IsSchengenAirport(aircraft.origin_airport)
        j = 0
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]
            match = (schengen and area.type == "Schengen") or \
                    (not schengen and area.type == "non-Schengen")
            if match:
                k = 0
                while k < len(area.gates):
                    if not area.gates[k].occupied:
                        area.gates[k].occupied = True
                        area.gates[k].aircraft_id = aircraft.aircraft_id
                        return 0
                    k += 1
            j += 1
        return -1

    def _free_gate(b, ac_id):
        i = 0
        while i < len(b.terminals):
            j = 0
            while j < len(b.terminals[i].boarding_areas):
                k = 0
                while k < len(b.terminals[i].boarding_areas[j].gates):
                    g = b.terminals[i].boarding_areas[j].gates[k]
                    if g.occupied and g.aircraft_id == ac_id:
                        g.occupied = False
                        g.aircraft_id = None
                        return 0
                    k += 1
                j += 1
            i += 1
        return -1

    # BLOQUE 3 — Simular las 24h y guardar snapshot de cada hora
    # snapshots[h] = lista de (terminal_name, area_name, area_type, gate_name, occupied, aircraft_id)
    sim = clone_bcn(bcn)
    snapshots = []

    # Inicializar hora 0 vacío
    h = 0
    while h < 24:
        snapshots.append([])
        h += 1

    h = 0
    while h < 24:
        # Liberar puertas de aviones que ya despegaron
        k = 0
        while k < len(aircrafts):
            ac = aircrafts[k]
            if ac.departure_time != "":
                try:
                    dh = int(ac.departure_time.split(":")[0])
                    dm = int(ac.departure_time.split(":")[1])
                    if dh * 60 + dm <= h * 60:
                        _free_gate(sim, ac.aircraft_id)
                except:
                    pass
            k += 1

        # Asignar puertas a aviones que aterrizan en esta hora
        k = 0
        while k < len(aircrafts):
            ac = aircrafts[k]
            if ac.landing_time != "":
                try:
                    ah = int(ac.landing_time.split(":")[0])
                    am = int(ac.landing_time.split(":")[1])
                    arr_min = ah * 60 + am
                    if h * 60 <= arr_min < (h + 1) * 60:
                        _assign_gate(sim, ac)
                except:
                    pass
            k += 1

        # Guardar snapshot
        snap = []
        t = 0
        while t < len(sim.terminals):
            term = sim.terminals[t]
            a = 0
            while a < len(term.boarding_areas):
                area = term.boarding_areas[a]
                g = 0
                while g < len(area.gates):
                    gate = area.gates[g]
                    snap.append((term.name,area.name,area.type,gate.name,gate.occupied,gate.aircraft_id))
                    g += 1
                a += 1
            t += 1
        snapshots[h] = snap
        h += 1


    # BLOQUE 4 — Calcular layout de puertas por terminal y área para dibujarlas como rectángulos en el plano
    # Recopilar estructura: terminales → áreas → nº puertas
    terminal_info = []   # lista de (terminal_name, [(area_name, area_type, n_gates)])
    t = 0
    while t < len(bcn.terminals):
        term = bcn.terminals[t]
        areas = []
        a = 0
        while a < len(term.boarding_areas):
            area = term.boarding_areas[a]
            areas.append((area.name, area.type, len(area.gates)))
            a += 1
        terminal_info.append((term.name, areas))
        t += 1

    # Constantes de layout
    GATE_W = 0.35   # ancho de cada puerta
    GATE_H = 0.55   # alto de cada puerta
    GATE_PAD = 0.08   # separación entre puertas
    AREA_PAD = 0.5    # separación entre áreas
    TERM_PAD = 1.2    # separación entre terminales
    AREA_LABEL_H = 1   # altura reservada para el nombre del área
    TERM_LABEL_H = 0.2   # altura reservada para el nombre del terminal

    # Pre-calcular posición X de cada puerta
    gp_keys = []   # (t_name, a_name, g_idx)
    gp_x = []
    gp_y = []
    gp_atype = []

    cur_x = 0.5
    t = 0
    while t < len(terminal_info):
        t_name, areas = terminal_info[t]
        term_start_x = cur_x
        a = 0
        while a < len(areas):
            a_name, a_type, n_gates = areas[a]
            area_start_x = cur_x
            g = 0
            while g < n_gates:
                gp_keys.append((t_name, a_name, g))
                gp_x.append(cur_x)
                gp_y.append(AREA_LABEL_H + TERM_LABEL_H)
                gp_atype.append(a_type)
                cur_x += GATE_W + GATE_PAD
                g += 1
            cur_x += AREA_PAD
            a += 1
        cur_x += TERM_PAD
        t += 1

    total_width = cur_x

    # BLOQUE 5 — Construir la figura con slider
    fig, ax = plt.subplots(figsize=(22, 7))
    plt.subplots_adjust(bottom=0.22, left=0.03, right=0.97, top=0.88)
    ax.set_facecolor("#1a1a2e")
    fig.patch.set_facecolor("#16213e")
    ax.set_xlim(-0.5, total_width)
    ax.set_ylim(-0.3, GATE_H + AREA_LABEL_H + TERM_LABEL_H + 0.8)
    ax.axis("off")

    title_obj = fig.text(0.5, 0.93, "LEBL Gate Map — 00:00h",ha="center", fontsize=13, fontweight="bold", color="white")
    stats_obj = fig.text(0.5, 0.90, "",ha="center", fontsize=9, color="#dfe6e9")

    #Dibujar fondos de terminales y áreas (estáticos)
    t = 0
    while t < len(terminal_info):
        t_name, areas = terminal_info[t]

        # Calcular inicio y fin del terminal
        t_x_start = None
        t_x_end   = None
        k = 0
        while k < len(gp_keys):
            if gp_keys[k][0] == t_name:
                if t_x_start is None:
                    t_x_start = gp_x[k]
                t_x_end = gp_x[k]
            k += 1
        if t_x_start is None:
            t += 1
            continue

        t_x_end += GATE_W
        term_rect = mpatches.FancyBboxPatch((t_x_start - 0.2, 0),t_x_end - t_x_start + 0.4,GATE_H + AREA_LABEL_H + TERM_LABEL_H + 0.1,boxstyle="round,pad=0.1",linewidth=1.5, edgecolor="#4a90d9",facecolor="#0f3460", zorder=1)
        ax.add_patch(term_rect)
        ax.text((t_x_start + t_x_end) / 2, GATE_H + AREA_LABEL_H + TERM_LABEL_H + 0.15,"Terminal " + t_name,ha="center", va="bottom",fontsize=11, fontweight="bold", color="#4a90d9", zorder=3)

        # Fondos de áreas
        a = 0
        while a < len(areas):
            a_name, a_type, n_gates = areas[a]
            # calcular x de esta área
            a_x_start = None
            a_x_end   = None
            k = 0
            while k < len(gp_keys):
                if gp_keys[k][0] == t_name and gp_keys[k][1] == a_name:
                    if a_x_start is None:
                        a_x_start = gp_x[k]
                    a_x_end = gp_x[k]
                k += 1
            if a_x_start is None:
                a += 1
                continue
            a_x_end += GATE_W
            if a_type == "Schengen":
                area_color = "#1a3a5c"
                label_color = "#74b9ff"
            else:
                area_color = "#3a1a1a"
                label_color = "#ff7675"
            area_rect = mpatches.FancyBboxPatch((a_x_start - 0.1, AREA_LABEL_H * 0.3),a_x_end - a_x_start + 0.2,GATE_H + AREA_LABEL_H * 0.5,boxstyle="round,pad=0.05",linewidth=0.8, edgecolor=label_color,facecolor=area_color, zorder=2)
            ax.add_patch(area_rect)
            ax.text((a_x_start + a_x_end) / 2, AREA_LABEL_H * 0.15,a_name + (" [SCH]" if a_type == "Schengen" else " [NON]"),ha="center", va="center",fontsize=7, color=label_color, zorder=3)
            a += 1
        t += 1

    #Crear rectángulos de puertas (dinámicos, se actualizan con el slider)
    gate_rects  = []   # objetos del rectángulo
    gate_texts  = []   # objetos Text con el ID del avión

    k = 0
    while k < len(gp_keys):
        x = gp_x[k]
        y = gp_y[k]
        rect = mpatches.FancyBboxPatch(
            (x, y), GATE_W, GATE_H,boxstyle="round,pad=0.04",linewidth=0.8, edgecolor="#2d3436",facecolor="#00b894", zorder=4)
        ax.add_patch(rect)
        gate_rects.append(rect)
        txt = ax.text(x + GATE_W / 2, y + GATE_H / 2, "",ha="center", va="center",fontsize=4.5, color="white", fontweight="bold",zorder=5, wrap=False, rotation=90)
        gate_texts.append(txt)
        k += 1

    # Leyenda
    leg_free = mpatches.Patch(color="#00b894", label="Free gate")
    leg_occ = mpatches.Patch(color="#d63031", label="Occupied (arrival)")
    leg_night = mpatches.Patch(color="#e17055", label="Night aircraft")
    leg_sch = mpatches.Patch(color="#74b9ff", label="Schengen area", alpha=0.5)
    leg_nsch = mpatches.Patch(color="#ff7675", label="Non-Schengen area", alpha=0.5)
    ax.legend(handles=[leg_free, leg_occ, leg_night, leg_sch, leg_nsch],loc="lower right", fontsize=8, framealpha=0.85,facecolor="#0f3460", labelcolor="white", edgecolor="#4a90d9")

    # BLOQUE 6 — Función de actualización del slider
    def update(hour_val):
        hour = int(hour_val)
        snap = snapshots[hour]
        snap_keys     = []
        snap_occupied = []
        snap_ac_id    = []
        s = 0
        while s < len(snap):
            t_name, a_name, a_type, g_name, occ, ac_id = snap[s]
            snap_keys.append((t_name, a_name, g_name))
            snap_occupied.append(occ)
            snap_ac_id.append(ac_id)
            s += 1

        # Determinar qué aviones son nocturnos (solo departure, sin landing)
        night_ids = []
        k2 = 0
        while k2 < len(aircrafts):
            ac = aircrafts[k2]
            if ac.landing_time == "" and ac.departure_time != "":
                night_ids.append(ac.aircraft_id)
            k2 += 1

        total_gates = len(gp_keys)
        occupied_count = 0

        k = 0
        while k < len(gp_keys):
            t_name, a_name, g_idx = gp_keys[k]

            # Buscar puerta correspondiente en el snapshot
            area_gates_in_snap = []
            s = 0
            while s < len(snap_keys):
                if snap_keys[s][0] == t_name and snap_keys[s][1] == a_name:
                    area_gates_in_snap.append(s)
                s += 1

            occ  = False
            ac_id  = None
            if g_idx < len(area_gates_in_snap):
                snap_idx = area_gates_in_snap[g_idx]
                occ = snap_occupied[snap_idx]
                ac_id = snap_ac_id[snap_idx]

            # Color según estado
            if not occ:
                color = "#00b894"
                label = ""
            else:
                is_night = False
                if ac_id is not None:
                    n = 0
                    while n < len(night_ids):
                        if night_ids[n] == ac_id:
                            is_night = True
                        n += 1
                if is_night:
                    color = "#e17055"
                else:
                    color = "#d63031"
                label = ac_id if ac_id is not None else "?"
                occupied_count += 1

            gate_rects[k].set_facecolor(color)
            gate_texts[k].set_text(label)
            k += 1

        free_count = total_gates - occupied_count
        sat_pct = (occupied_count / total_gates * 100) if total_gates > 0 else 0
        title_obj.set_text("LEBL Gate Map — {:02d}:00h".format(hour))
        stats_obj.set_text("Total gates: {}   |   Occupied: {}   |   Free: {}   |   Saturation: {:.1f}%".format(total_gates, occupied_count, free_count, sat_pct))
        fig.canvas.draw_idle()

    # Slider
    ax_slider = plt.axes([0.12, 0.07, 0.76, 0.04], facecolor="#0f3460")
    slider = widgets.Slider(ax_slider, "Hour", 0, 23,valinit=0, valstep=1,color="#4a90d9")
    slider.label.set_color("white")
    slider.valtext.set_color("white")
    slider.on_changed(update)

    # Dibujar hora 0 al inicio
    update(0)
    fig.patch.set_facecolor("#16213e")

    plt.show()

# test section
if __name__ == "__main__":
    from airport import *
    airports = LoadAirports("Airports.txt")
    aircrafts = LoadArrivals("Arrivals.txt")
    longdistance = LongDistanceArrivals(aircrafts, airports)
    if len(longdistance) == 0:
        print("Fail")
        print(len(airports))
        print(len(aircrafts))
    else:
        print("Success")
    mf = MapFlights(aircrafts, airports)
    if mf == -1:
        print("Fail")
        print(len(airports))
    else:
        print("Success")
    if len(aircrafts)>0:
        print("Success")
    else:
        print("Fail")
    sf=SaveFlights(aircrafts, "SaveFlights.txt")
    if sf==-1:
        print("Fail")
    else:
        print("Success")
    print(str(len(aircrafts)) + " aircrafts")
    '''
    sd=ShortDistanceArrivalsMaps(aircrafts, airports)
    if sd == -1:
        print("Fail")
    else:
        print("Success: " + str(len(aircrafts)) + " aircrafts remaining")
        print(str(len(sd)) +" aircrafts deleted.")
    
    PlotArrivals(aircrafts)
    PlotAirlines(aircrafts)
    PlotFlightsType(aircrafts)
    PlotAirlinesAvsE(aircrafts)
    '''