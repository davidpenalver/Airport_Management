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

#Function 2: Update list of airlines in each terminal. - AI helped to determine the order of the analysis.
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

#Function 3: Returns class BarcelonaAP:
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
def GateOccupany(bcn):
    if bcn is None:
        return []
    result=[]
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
                result.append((gate.name, status, aircraft))
                k=k+1
            j=j+1
        i=i+1
    return result

#Function 4.extra: Plot.