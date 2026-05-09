import sys
import tkinter as tk
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties
import interface
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
        line=f.readline()
        parts=line.split().strip()
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