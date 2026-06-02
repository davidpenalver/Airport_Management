import re
import matplotlib.pyplot as plt
#Classes.
class Gate:
    def __init__(self, name):
        self.name=name
        self.occupied=False
        self.aircraft_id=None

class BoardingArea:
    def __init__(self, name, type):
        self.name=name
        self.type=type
        self.gates=[]

class Terminal:
    def __init__(self, name):
        self.name=name
        self.boarding_areas=[]
        self.airlines=[]

class BarcelonaAP:
    def __init__(self, code):
        self.code=code
        self.terminals=[]

#Function 1: Update list of gates.
def SetGates(area,init_gate,end_gate,prefix):
    if end_gate<init_gate:
        return -1
    area.gates=[]
    i=init_gate
    while i<=end_gate:
        gate_name=prefix+str(i)
        gate=Gate(gate_name)
        area.gates.append(gate)
        i=i+1
    return 0

#Function 2: Update list of airlines in each terminal.
def LoadAirlines(terminal,t_name):
    airlines_list=[]
    name_file=str(t_name)+"_Airlines.txt"
    try:
        with open(name_file,"r") as f:
            for line in f:
                if line!="":
                    parts=line.split("\t")
                    if len(parts)>=2:
                        code=parts[1].strip()
                        airlines_list.append(code)
        terminal.airlines=airlines_list
        return 0
    except:
        return -1

#Function 3: Returns class BarcelonaAP - AI helped to determine the order of the analysis:
def LoadAirportStructure(filename):
    try:
        f=open(filename,"r")
    except:
        return -1
    line=f.readline().strip()
    parts=line.split()
    code=parts[0]
    bcn=BarcelonaAP(code)
    num_terminals=int(parts[1])
#Read terminals.
    i=0
    while i<num_terminals:
        line=f.readline().strip()
        parts=line.split()
        name_terminal=parts[1]
        areas_num=int(parts[2])
        terminal=Terminal(name_terminal)
        LoadAirlines(terminal,name_terminal)

#Boarding areas.
        j=0
        while j<areas_num:
            line=f.readline().strip()
            parts=line.split()
            area_name=parts[1]
            area_type=parts[2]
            init_gate=int(parts[4])
            end_gate=int(parts[6])
            area=BoardingArea(area_name,area_type)
            prefix=name_terminal+area_name
            SetGates(area,init_gate,end_gate,prefix)
            terminal.boarding_areas.append(area)
            j=j+1
        bcn.terminals.append(terminal)
        i=i+1
    f.close()
    return bcn

#Function 4: Status of each gate.
def GateOccupancy(bcn):
    if bcn is None:
        return []
    allGates=[]
    i=0
    while i<len(bcn.terminals):
        terminal=bcn.terminals[i]
        j=0
        while j<len(terminal.boarding_areas):
            area=terminal.boarding_areas[j]
            k=0
            while k<len(area.gates):
                gate=area.gates[k]
                if gate.occupied:
                    status="Occupied"
                    aircraft=gate.aircraft_id
                else:
                    status="Unoccupied"
                    aircraft=None
                allGates.append((gate.name, status, aircraft))
                k=k+1
            j=j+1
        i=i+1
    return allGates

#Function 4.extra - corrected with AI.
def buildDataToPlot(gates_list):
    struct = {}
    pattern = r"(T\d+)(BA[A-Za-z]+)G(\d+)"
    i = 0
    while i < len(gates_list):
        name, status, aircraft = gates_list[i]
        match = re.match(pattern, name) #separar cada gate en lo que es, por ejemplo T1BAbG5 1 b 5
        if match:
            terminal = match.group(1)
            area = match.group(2)
            gate_number = int(match.group(3))
            #asignar el 1 a terminal la b a area y 5 a gate ejemplo anterior
            if terminal not in struct:
                struct[terminal] = {}
            if area not in struct[terminal]:
                struct[terminal][area] = []
            info = {
                "number": gate_number,
                "occupied": (status == "Occupied"),
                "aircraft": aircraft
            }
            struct[terminal][area].append(info)
        i += 1
    return struct


def PlotGateOccupancy(gates_list):
    fig, ax = plt.subplots(figsize=(10,6))
    terminals = {}
    i = 0
    while i < len(gates_list):
        name, status, aircraft = gates_list[i]
        terminal = name[:2]
        rest = name[2:]
        j = 0
        while j < len(rest) and not rest[j].isdigit():
            j += 1
        area = rest[:j]
        gate_number = int(rest[j:])
        if terminal not in terminals:
            terminals[terminal] = {}
        if area not in terminals[terminal]:
            terminals[terminal][area] = []
        terminals[terminal][area].append(
            (gate_number, status)
        )
        i += 1
    y = 0
    terminals_names = list(terminals.keys())
    t = 0
    while t < len(terminals_names):
        terminal = terminals_names[t]
        ax.text(
            0,
            y,
            terminal,
            fontsize=16,
            weight="bold"
        )
        areas = list(terminals[terminal].keys())
        a = 0
        while a < len(areas):
            area = areas[a]
            y -= 10
            ax.plot(
                [1,1],
                [y-5, y+5],
                linewidth=10
            )
            ax.text(
                1.5,
                y,
                area,
                fontsize=12,
                weight="bold"
            )
            gates = terminals[terminal][area]
            g = 0
            while g < len(gates):
                gate_number, status = gates[g]
                x = 3 + g
                color = "red"
                if status == "Unoccupied":
                    color = "green"
                rect = plt.Rectangle(
                    (x, y-0.2),
                    0.8,
                    0.4,
                    color=color
                )
                ax.add_patch(rect)
                gate_name = (
                    terminal
                    + area
                    + "G"
                    + str(gate_number)
                )
                ax.text(
                    x + 0.4,
                    y,
                    gate_name,
                    ha="center",
                    va="center",
                    fontsize=6, rotation=90
                )
                g += 1
            a += 1
        y -= 12
        t += 1
    ax.set_title("Airport Gate Occupancy")
    ax.axis("off")
    return fig

#Function 5: Is the airline from that terminal.
def IsAirlineInTerminal(terminal, name):
    if name=="":
        return False
    if len(terminal.airlines)==0:
        return False
    i=0
    found=False
    while i<len(terminal.airlines) and not found:
        if terminal.airlines[i]==name:
            found=True
        i=i+1
    if found:
        return True
    if not found:
        return False

#Function 6: Name of the terminal where an airline should board.
def SearchTerminal (bcn, name):
    i=0
    found=False
    terminal=None
    while i<len(bcn.terminals) and not found:
        if IsAirlineInTerminal(bcn.terminals[i],name):
            terminal=bcn.terminals[i]
            found=True
        i=i+1
    if found:
        return terminal.name
    if not found:
        return ""

#Function 7: Look for the first free gate in the correct area for a given aircraft from Class Aircraft.
from airport import IsSchengenAirport
def AssignGate(bcn, aircraft):
#Buscar terminal por aerolínea
    terminal_name = SearchTerminal(bcn, aircraft.airline_company)
    if terminal_name == "":
        return -1
#Encontrar terminal
    terminal = None
    i = 0
    while i < len(bcn.terminals) and terminal is None:
        if bcn.terminals[i].name == terminal_name:
            terminal = bcn.terminals[i]
        i += 1
    if terminal is None:
        return -1
#Comprobar si el vuelo es Schengen
    schengen = IsSchengenAirport(aircraft.origin_airport)
#Buscar BoardingArea
    j = 0
    while j < len(terminal.boarding_areas):
        area = terminal.boarding_areas[j]
        if schengen == True and area.type=="Schengen":
            # buscar gate libre
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                if not gate.occupied:
                    gate.occupied = True
                    gate.aircraft_id = aircraft.aircraft_id
                    return 0
                k += 1
        elif schengen==False and area.type=="non-Schengen":
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                if not gate.occupied:
                    gate.occupied = True
                    gate.aircraft_id = aircraft.aircraft_id
                    return 0
                k += 1
        j += 1
    return -1


#V4
#Function 4: Assign gates to a list of aricrafts.
def AssignNightGates(bcn, aircrafts):
    if len(aircrafts) == 0:
        print("Error: The aircrafts list is empty.")
        return -1
    assigned_count = 0
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        if ac.origin_airport != "" and ac.origin_airport != "LEBL":
            i += 1
            continue
        resultado = AssignGate(bcn, ac)
        if resultado == 0:
            assigned_count += 1
        i += 1
    print(f"Night gates assignment are finished. Total assigned gates: {assigned_count}")
    return 0

#Function 5: Free the gate assigned to an aircraft.
def FreeGate(bcn, id):
    if bcn is None or id == "":
        return -1
    #Search through all terminals, areas and gates.
    i = 0
    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas):
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates):
                gate = area.gates[k]
                #If the gate is occupied by this aircraft, free it.
                if gate.occupied and gate.aircraft_id == id:
                    gate.occupied = False
                    gate.aircraft_id = None
                    return 0
                k += 1
            j += 1
        i += 1
    #Aircraft not found in any gate.
    return -1

#Function 6: Assign gates to aircrafts landing in a one-hour period.
def AssignGatesAtTime(bcn, aircrafts, time):
    if bcn is None or len(aircrafts) == 0:
        return -1
    #Get the hour of the time received as integer.
    try:
        h = int(time.split(":")[0])
        if h < 0 or h > 23:
            return -1
    except:
        return -1

    #Free gates of aircrafts that have already departed before this hour.
    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        if aircraft.departure_time != "":
            try:
                dep_h = int(aircraft.departure_time.split(":")[0])
                dep_m = int(aircraft.departure_time.split(":")[1])
                dep_minutes = dep_h * 60 + dep_m
                period_minutes = h * 60
                #If the aircraft departed before this period, free its gate.
                if dep_minutes <= period_minutes:
                    FreeGate(bcn, aircraft.aircraft_id)
            except:
                pass
        i += 1

    #Assign gates to aircrafts landing during this one-hour period.
    not_assigned = 0
    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        if aircraft.landing_time != "":
            try:
                arr_h = int(aircraft.landing_time.split(":")[0])
                arr_m = int(aircraft.landing_time.split(":")[1])
                arr_minutes = arr_h * 60 + arr_m
                period_start = h * 60
                period_end = (h + 1) * 60
                #If the aircraft lands within this one-hour period, assign a gate.
                if period_start <= arr_minutes < period_end:
                    result = AssignGate(bcn, aircraft)
                    if result == -1:
                        not_assigned += 1
            except:
                pass
        i += 1

    return not_assigned

#Function extra: Generate a TXT report for a specific gate and ask where to save it.
def GateReport(bcn, aircrafts, gate_input):
    gate_name = gate_input
    if gate_name == "":
        return -1

    # buscamos la puerta por el nombre en toda la estructura
    found_gate = None
    found_area = None
    found_terminal = None
    i = 0
    while i < len(bcn.terminals) and found_gate is None:
        terminal = bcn.terminals[i]
        j = 0
        while j < len(terminal.boarding_areas) and found_gate is None:
            area = terminal.boarding_areas[j]
            k = 0
            while k < len(area.gates) and found_gate is None:
                gate = area.gates[k]
                # si el nombre coincide ya la tenemos
                if gate.name == gate_name:
                    found_gate = gate
                    found_area = area
                    found_terminal = terminal
                k += 1
            j += 1
        i += 1

    # si no encontramos nada nos vamos
    if found_gate is None:
        return -1

    # miramos que aviones son compatibles con esta puerta
    # para eso comprobamos que la aerolinea este en el mismo terminal
    # y que el origen sea del mismo tipo schengen que el area
    compatible = []
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        ac_terminal = SearchTerminal(bcn, ac.airline_company)
        if ac_terminal == found_terminal.name:
            ac_schengen = IsSchengenAirport(ac.origin_airport)
            if ac_schengen and found_area.type == "Schengen":
                compatible.append(ac)
            elif not ac_schengen and found_area.type == "non-Schengen":
                compatible.append(ac)
        i += 1

    # ordenamos los compatibles por hora de llegada, burbuja de toda la vida
    i = 0
    while i < len(compatible) - 1:
        j = 0
        while j < len(compatible) - 1 - i:
            try:
                h1 = int(compatible[j].landing_time.split(":")[0]) * 60 + int(compatible[j].landing_time.split(":")[1])
                h2 = int(compatible[j+1].landing_time.split(":")[0]) * 60 + int(compatible[j+1].landing_time.split(":")[1])
                if h1 > h2:
                    compatible[j], compatible[j+1] = compatible[j+1], compatible[j]
            except:
                # si el tiempo esta mal lo dejamos donde esta
                pass
            j += 1
        i += 1

    # creamos el txt en la carpeta del proyecto
    filename = "Gate" + gate_name + ".txt"
    try:
        with open(filename, "w") as f:
            f.write("=" * 55 + "\n")
            f.write("  GATE REPORT: " + gate_name + "\n")
            f.write("  Barcelona El Prat Airport (LEBL)\n")
            f.write("=" * 55 + "\n\n")

            # info basica de la puerta
            f.write("--- GATE INFORMATION ---\n")
            f.write("Gate Name    : " + found_gate.name + "\n")
            f.write("Terminal     : " + found_terminal.name + "\n")
            f.write("Boarding Area: " + found_area.name + "\n")
            f.write("Area Type    : " + found_area.type + "\n")
            if found_gate.occupied:
                f.write("Status       : Occupied\n")
                f.write("Aircraft     : " + str(found_gate.aircraft_id) + "\n")
            else:
                f.write("Status       : Free\n")
                f.write("Aircraft     : -\n")

            # lista de vuelos que podrian usar esta puerta hoy
            f.write("\n--- COMPATIBLE FLIGHTS FOR THIS GATE TODAY ---\n")
            f.write("(Same terminal: " + found_terminal.name + " | Area type: " + found_area.type + ")\n\n")
            if len(compatible) == 0:
                f.write("No compatible flights found.\n")
            else:
                # cabecera de la tabla
                f.write("{:<12} {:<8} {:<8} {:<8} {:<12} {:<10}\n".format(
                    "Aircraft", "Origin", "Arrival", "Airline", "Destination", "Departure"))
                f.write("-" * 60 + "\n")
                i = 0
                while i < len(compatible):
                    ac = compatible[i]
                    f.write("{:<12} {:<8} {:<8} {:<8} {:<12} {:<10}\n".format(ac.aircraft_id if ac.aircraft_id else "-",ac.origin_airport if ac.origin_airport else "-",ac.landing_time if ac.landing_time else "-",ac.airline_company if ac.airline_company else "-", ac.destination_airport if ac.destination_airport else "-",ac.departure_time if ac.departure_time else "-",))
                    i += 1
            f.write("\n" + "=" * 55 + "\n")
            f.write("  Report by Airport Management System - LEBL\n")
            f.write("=" * 55 + "\n")
        return filename
    except:
        return -1

#TEST CODE:
if __name__ == "__main__":
#PROBAR LoadAirportStructure
    bcn = LoadAirportStructure("Terminals.txt")
    if bcn == -1 or bcn is None:
        print("ERROR: No se pudo cargar Terminals.txt\n")
    else:
        print("Estructura cargada correctamente")
        print(f"  Código aeropuerto: {bcn.code}")
        print(f"  Nº terminales: {len(bcn.terminals)}\n")
#LISTAR TERMINALES, AREAS Y GATES
    for terminal in bcn.terminals:
        print(f"Terminal {terminal.name}:")
        print(f"  Aerolíneas: {len(terminal.airlines)}")
        for area in terminal.boarding_areas:
            print(f"   Área {area.name} ({area.type}) -> {len(area.gates)} gates")
        print()
#IsAirlineInTerminal + SearchTerminal
    test_airline = None
    if len(bcn.terminals[0].airlines) > 0:
        test_airline = bcn.terminals[0].airlines[0]
        print(f"   Tomando aerolínea de ejemplo: {test_airline}")
        result = SearchTerminal(bcn, test_airline)
        print(f"   Resultado SearchTerminal({test_airline}) = {result}\n")
    else:
        print("No hay aerolíneas en T1 para probar\n")
#GateOccupancy
    gates = GateOccupancy(bcn)
    print(f"  Nº total de gates: {len(gates)}")
    print(f"  Gates desocupados: {sum(1 for g in gates if g[1]=='Unoccupied')}\n")
#TEST AssignGate
    class DummyAircraft: # - AI
        def __init__(self, ident, origin, airline):
            self.id = ident
            self.origin = origin
            self.airline = airline
    if test_airline:
        dummy = DummyAircraft("TEST01", "LEMD", test_airline)   # origen Schengen
        r = AssignGate(bcn, dummy)
        if r == 0:
            print("Gate asignado correctamente")
        else:
            print("ERROR asignando gate")
#mostrar gates ocupados
        gates_after = GateOccupancy(bcn)
        occupied = [g for g in gates_after if g[1] == "Occupied"]
        print(f"  Gates ocupados tras asignación: {len(occupied)}")
        print(f"  Ejemplo: {occupied[0] if occupied else '---'}\n")
    print("FIN TEST\n")