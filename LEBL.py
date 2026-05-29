'''
import sys
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties
import interface
'''
import re
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
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
'''
#Function 4.extra: Plot occupancy.
def buildDataToPlot(allGates):
    struct = {}

    for gatedata in allGates:
        #separar cada codigo, es decir, ej. T1BAbG3 = (1,b,3)
        template = r"(T\d+)(BA[a-zA-Z]+)(G\d+)"
        result = re.match(template, gatedata.name)
        if not result:
            return -1
        # con (1,b,3) igualo terminal a 1, area a "b", y gate a 3
        terminal, area, gate = result.groups()
        if terminal is None:
            return -1
        if terminal not in struct:
            struct[terminal] = {}
        #crea un vector de len=2 xq es bcn (T1,T2) dentro de cada terminal las distintas areas y append de la gate correspondientes en cada area
        if area not in struct[terminal]:
            struct[terminal][area] = []

        if gatedata.occupied == True:
            struct[terminal][area].append("o"+gate)
        else:
            struct[terminal][area].append(gate)

    return struct

def calculateFigureSize(structData):
    max_areas = 0
    total_height = 0

    gate_sep_y = 0.55
    terminal_margin = 4

    for terminal in structData:
        areas = structData[terminal]
        max_areas = max(max_areas, len(areas))

        max_gates = 0

        for area in areas:
            max_gates = max(max_gates, len(areas[area]))

        terminal_height = max(7, max_gates * gate_sep_y + terminal_margin)
        total_height += terminal_height

    fig_width = max(12, max_areas * 3.4)
    fig_height = max(10, total_height)

    return fig_width, fig_height

def initCanvas(structData):

    frame = tk.Frame(interface.root)
    frame.pack(fill=tk.BOTH, expand=True)

    tk_canvas = tk.Canvas(frame, bg="white")
    tk_canvas.grid(row=0, column=0, sticky="nsew")

    scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=tk_canvas.yview)
    scrollbar_y.grid(row=0, column=1, sticky="ns")

    scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=tk_canvas.xview)
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    tk_canvas.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    fig_width, fig_height = calculateFigureSize(structData)

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=100)

    fig.subplots_adjust(
        left=0,
        right=1,
        top=1,
        bottom=0
    )

    mpl_canvas = FigureCanvasTkAgg(fig, master=tk_canvas)
    mpl_widget = mpl_canvas.get_tk_widget()

    tk_canvas.create_window(
        0,
        0,
        window=mpl_widget,
        anchor="nw"
    )

    def update_scroll_region(event=None):
        tk_canvas.configure(scrollregion=tk_canvas.bbox("all"))

    mpl_widget.bind("<Configure>", update_scroll_region)

    return mpl_canvas, fig, ax, tk_canvas


def plotAllGates(structData, fig, ax):
    ax.clear()


    x_init = 1
    y_init = 0

    between_areas = 2.8
    struct_color = "#0f5f78"

    font_gate = FontProperties(
        weight="bold",
        size=7
    )

    gate_height = 0.28
    gate_sep_y = 0.55

    y_terminal = y_init

    max_width = 0
    total_height = 0

    for terminal in structData:
        areas = list(structData[terminal].keys())
        max_gates = max(len(structData[terminal][area]) for area in areas)

        terminal_height = max(7, max_gates * gate_sep_y + 4)

        total_height += terminal_height
        max_width = max(max_width, len(areas) * between_areas + 4)

    for terminal in structData:

        areas = list(structData[terminal].keys())
        width_terminal = len(areas) * between_areas

        max_gates = max(len(structData[terminal][area]) for area in areas)
        terminal_height = max(7, max_gates * gate_sep_y + 4)

        ax.plot(
            [x_init, x_init + width_terminal],
            [y_terminal, y_terminal],
            linewidth=18,
            color=struct_color
        )

        ax.text(
            x_init - 0.8,
            y_terminal,
            terminal,
            fontsize=20,
            va="center"
        )

        for area_idx, area in enumerate(areas):

            x_area = x_init + area_idx * between_areas + 0.8
            gates = structData[terminal][area]

            area_height = max(2.0, len(gates) * gate_sep_y + 0.8)

            ax.plot(
                [x_area, x_area],
                [y_terminal + 0.3, y_terminal + area_height],
                linewidth=18,
                color=struct_color
            )

            ax.text(
                x_area,
                y_terminal + area_height + 0.6,
                terminal + area,
                fontsize=14,
                ha="center"
            )

            for gate_idx, gate in enumerate(gates):

                y_gate = y_terminal + 0.8 + gate_idx * gate_sep_y
                number_gate = gate_idx + 1
                gate_name = terminal + area + gate

                temp_text = ax.text(
                    0,
                    0,
                    gate_name,
                    fontproperties=font_gate
                )

                fig.canvas.draw()

                bbox = temp_text.get_window_extent(
                    renderer=fig.canvas.get_renderer()
                )
                temp_text.remove()

                x0 = ax.transData.inverted().transform((bbox.x0, bbox.y0))[0]
                x1 = ax.transData.inverted().transform((bbox.x1, bbox.y1))[0]

                text_width = x1 - x0
                padding_x = 0.12

                dynamic_gate_width = text_width + padding_x * 2

                if number_gate % 2 == 1:
                    x_line_ini = x_area
                    x_line_fin = x_area - 0.45
                    x_rect = x_area - 0.45 - dynamic_gate_width
                else:
                    x_line_ini = x_area
                    x_line_fin = x_area + 0.45
                    x_rect = x_area + 0.45

                ax.plot(
                    [x_line_ini, x_line_fin],
                    [y_gate, y_gate],
                    linewidth=5,
                    color=struct_color
                )

                ax.add_patch(
                    plt.Rectangle(
                        (x_rect, y_gate - gate_height / 2),
                        dynamic_gate_width,
                        gate_height,
                        color = "red" if gate[0] == "o" else "limegreen"
                    )
                )

                ax.text(
                    x_rect + dynamic_gate_width / 2,
                    y_gate,
                    gate_name,
                    fontproperties=font_gate,
                    ha="center",
                    va="center",
                    color="black"
                )

        y_terminal += terminal_height

    ax.set_aspect("auto")
    ax.axis("off")

    ax.set_xlim(-2, max_width)
    ax.set_ylim(total_height + 1, -1)

    fig.canvas.draw()



#hay que llamar a esta última :)
def PlotGateOccupancy(allGates):

    dataAllGates = buildDataToPlot(allGates)

    canvas, fig, ax, tk_canvas = initCanvas(window, dataStruct)

    plotAllGates(dataAllGates, fig, ax)
    #canvas.draw()

    tk_canvas.update_idletasks()
    tk_canvas.configure(scrollregion=tk_canvas.bbox("all"))

    tk_canvas.xview_moveto(0)
    tk_canvas.yview_moveto(0)

    return fig
'''
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

#Function 8: Free the gate assigned to an aircraft.
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

#Function 9: Assign gates to aircrafts landing in a one-hour period.
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