import tkinter as tk
from tkinter import filedialog, messagebox
# from airport import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from aircraft import *
from LEBL import *
airports=[]
aircrafts=[]
departures=[]
night_aircrafts=[]
canvas=None
root=None
bcn=None

#Functions of the interface V4:
def load_departures():
    global departures
    filename = filedialog.askopenfilename()
    departures=LoadDepartures(filename)
    if len(departures)==0:
        messagebox.showerror("Error", "Error loading file.")
    else:
        messagebox.showinfo("Success", str(len(departures)) + " departures loaded.")

def merge_movements():
    global aircrafts, departures
    if len(aircrafts)==0:
        messagebox.showerror("Error", "No arrivals loaded.")
        return
    if len(departures)==0:
        messagebox.showerror("Error", "No departures loaded.")
        return
    merged = MergeMovements(aircrafts, departures)
    if merged==-1 or len(merged)==0:
        messagebox.showerror("Error", "Merge failed.")
    else:
        aircrafts=merged
        messagebox.showinfo("Success", str(len(aircrafts)) + " movements merged successfully.")

def night_aircraft():
    global aircrafts, night_aircrafts
    if len(aircrafts)==0:
        messagebox.showerror("Error", "No aircraft list available.")
        return
    result=NightAircraft(aircrafts)
    if result==-1 or len(result)==0:
        messagebox.showerror("Error", "No night aircraft found.")
    else:
        night_aircrafts=result
        text.delete(1.0, tk.END)
        i=0
        while i<len(night_aircrafts):
            ac=night_aircrafts[i]
            line = (ac.aircraft_id + " | " + ac.destination_airport + " | " + ac.departure_time + " | " + ac.airline_company)
            text.insert(tk.END, line + "\n")
            i+=1
        messagebox.showinfo("Success",str(len(night_aircrafts)) + " night aircraft found.")

#Functions of the interface V3:
def assign_gate():
    global bcn,aircrafts
    if bcn is None:
        messagebox.showerror("Error", "Load airport structure first.")
        return
    if len(aircrafts)==0:
        messagebox.showerror("Error", "No aircrafts loaded.")
        return
    assigned=0
    failed=0
    i=0
    while i<len(aircrafts):
        ac=aircrafts[i]
        r=AssignGate(bcn,ac)
        if r==0:
            assigned += 1
        else:
            failed += 1
        i+=1

    messagebox.showinfo("Result","Gates assigned: " + str(assigned) + "\nFailed: " + str(failed))

def gate_occupancy():
    global bcn
    if bcn is None:
        messagebox.showerror("Error", "Load airport structure first.")
        return
    gates=GateOccupancy(bcn)
    text.delete(1.0, tk.END)
    i=0
    while i<len(gates):
        name, status, aircraft = gates[i]
        line=name + " | " + status + " | " + str(aircraft) + "\n"
        text.insert(tk.END,line)
        i+=1

def plot_gate_occupancy():
    global bcn
    if bcn is None:
        messagebox.showerror("Error", "Load airport structure first.")
        return
    gates=GateOccupancy(bcn)
    fig=PlotGateOccupancy(gates)
    show_plot(fig)

def load_airport_structure():
    global bcn
    filename=filedialog.askopenfilename()
    bcn=LoadAirportStructure(filename)
    if bcn==-1 or bcn is None:
        messagebox.showerror("Error", "Error loading airport structure.")
    else:
        messagebox.showinfo("Success", "Airport structure loaded correctly.")

def search_terminal():
    global bcn
    if bcn is None:
        messagebox.showerror("Error", "Load airport first.")
        return
    airline=entry_code.get()
    result=SearchTerminal(bcn, airline)
    if result=="":
        messagebox.showerror("Error", "Airline not found.")
    else:
        messagebox.showinfo("Result", "Terminal: " + result)

# Functions of the plots:
def show_plot(fig):
    global canvas
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
# Functions of the interface V2.
def load_aircrafts():
    global aircrafts
    filename = filedialog.askopenfilename()
    aircrafts=LoadArrivals(filename)
    if len(aircrafts)==0:
        messagebox.showerror("Error", "Error loading file.")
    else:
        messagebox.showinfo("Success", str(len(aircrafts)) + " aircrafts loaded.")

def plot_arrivals():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No aircrafts.")
        return
    plt_obj = PlotArrivals(aircrafts)
    fig = plt_obj.gcf()
    show_plot(fig)

def save_flights():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    result = SaveFlights(aircrafts, filename)
    if result == 0:
        messagebox.showinfo("Success", "File successfully saved.")
    else:
        messagebox.showerror("Error", "File not saved.")

def plot_airlines():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No aircrafts.")
        return
    plt_obj = PlotAirlines(aircrafts)
    fig = plt_obj.gcf()
    show_plot(fig)

def plot_flights_type():
    if len(aircrafts) == 0:
        messagebox.showerror("Error", "No aircrafts.")
        return
    plt_obj = PlotFlightsType(aircrafts)
    fig = plt_obj.gcf()
    show_plot(fig)

def map_flights():
    result = MapFlights(aircrafts, airports)
    if result == 0:
        messagebox.showinfo("Success", "Map successfully created.")
        os.system("Start FlightsMap.kml")
    else:
        messagebox.showerror("Error", "Map not created.")

def long_distance_arrivals():
    result = LongDistanceArrivals(aircrafts, airports)
    if len(result)==0:
            messagebox.showerror("Error", "List not created.")
    else:
        messagebox.showinfo("Success", "List successfully created.")

# Functions of the interface V1.
def load_airports():
    global airports
    filename=filedialog.askopenfilename()
    airports=LoadAirports(filename)
    if len(airports) == 0:
        messagebox.showerror("Error","Error loading file.")
    else:
        messagebox.showinfo("Success", str(len(airports)) + " airports loaded.")
    i=0
    while i<len(airports):
        SetSchengen(airports[i])
        i=i+1

def add_airport():
    code=entry_code.get()
    if len(code)!=4:
        messagebox.showerror("Error","Invalid code. Must be 4 characters.")
        return
    try:
        lat=float(entry_lat.get())
    except:
        messagebox.showerror("Error","Invalid latitude.")
        return
    try:
        long=float(entry_long.get())
    except:
        messagebox.showerror("Error","Invalid longitude")
        return
    airport = Airport(code, lat, long)
    SetSchengen(airport)
    result=AddAirport(airports,airport)
    if result == 0:
        messagebox.showinfo("Success","Successfully added.")
    else:
        messagebox.showerror("Error","Airport already exists")

def remove_airport():
    code=entry_code.get()
    result=RemoveAirport(airports,code)
    if result == 0:
        messagebox.showinfo("Success","Successfully removed.")
    else:
        messagebox.showerror("Error","Airport not found.")

def show_aiports():
    text.delete(1.0,tk.END)
    if len(airports)==0:
        text.insert(tk.END,"No airports loaded.\n")
        return
    i=0
    line="ICAO code | Latitude | Longitude | Schengen \n"
    text.insert(tk.END, line + "\n")
    while i<len(airports):

        line=airports[i].icao + " | " + str(airports[i].latitude) + " | " + str(airports[i].longitude) + " | " + str(
            airports[i].schengen)
        text.insert(tk.END, line + "\n")
        i=i+1

def save_schengen():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    result = SaveSchengenAirports(airports, filename)
    if result == 0:
        messagebox.showinfo("Success","File successfully saved.")
    else:
        messagebox.showerror("Error","File not saved.")

def plot_aiports():
    if len(airports) == 0:
        messagebox.showerror("Error", "No airports.")
        return
    plt_obj=PlotAirports(airports)
    fig = plt_obj.gcf()
    show_plot(fig)

def map_airports():
    result=MapAirports(airports)
    if result == 0:
        messagebox.showinfo("Success","Map successfully created.")
        os.system("Start AirportsMaps.kml")
    else:
        messagebox.showerror("Error","Map not created.")

#Interface boxes.
root=tk.Tk()
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.geometry("1200x650")
root.resizable(True, True)
root.title("Airport Manager")
root.configure(bg="#ffffff")

title_frame = tk.Frame(root,bg="#2d3436",pady=10)
title_frame.grid(row=0,column=0,columnspan=3,sticky="ew")
title_label = tk.Label(title_frame,text="Airport Management System",bg="#2d3436",fg="white",font=("Arial", 18, "bold"))
title_label.pack()
subtitle_label = tk.Label(title_frame,text="LEBL arrivals, departures and gate management",bg="#2d3436",fg="#dfe6e9",font=("Arial", 10))
subtitle_label.pack()

left_canvas = tk.Canvas(root,bg="#ffffff",highlightthickness=0, width=260)
left_canvas.grid(row=1,column=0,sticky="ns")
left_scroll = tk.Scrollbar(root,orient="vertical",command=left_canvas.yview)
left_scroll.grid(row=1,column=0,sticky="nse", padx=(245,0))
left_canvas.configure(yscrollcommand=left_scroll.set)
left_panel = tk.Frame(left_canvas,bg="#ffffff") #dfe6e9
left_canvas.create_window((0,0),window=left_panel,anchor="nw", width=250)

def update_scroll(event):
    left_canvas.configure(scrollregion=left_canvas.bbox("all"))
left_panel.bind("<Configure>",update_scroll)

right_canvas = tk.Canvas(root,bg="#ffffff",highlightthickness=0)
right_canvas.grid(row=1,column=1,sticky="nsew")
right_scroll = tk.Scrollbar(root,orient="vertical",command=right_canvas.yview)
right_scroll.grid(row=1,column=2,sticky="ns")
right_canvas.configure(yscrollcommand=right_scroll.set)
right_panel = tk.Frame(right_canvas,bg="#ffffff") #f5f6fa
right_window = right_canvas.create_window((0,0),window=right_panel,anchor="nw")

def update_right_scroll(event):
    right_canvas.configure(scrollregion=right_canvas.bbox("all"))
def resize_right_panel(event):
    right_canvas.itemconfig(right_window,width=event.width)
right_canvas.bind("<Configure>",resize_right_panel)
right_panel.bind("<Configure>",update_right_scroll)

input_frame = tk.LabelFrame(left_panel,text="📝 Inputs",padx=10,pady=10,bg="#5B00F2",fg="black",font=("Arial", 10, "bold"), bd=0)
input_frame.pack(fill="x")
airport_frame = tk.LabelFrame(left_panel, text="🌍 Airport", padx=10, pady=10, bg="#5B15D1",font=("Arial", 10, "bold"), bd=0)
airport_frame.pack(fill="x")
flight_frame = tk.LabelFrame(left_panel, text="✈️ Flights", padx=10, pady=10, bg="#571DB8",font=("Arial", 10, "bold"), bd=0)
flight_frame.pack(fill="x")
gate_frame = tk.LabelFrame(left_panel, text="🚪 Gate Management", padx=10, pady=5, bg="#5222A3",font=("Arial", 10, "bold"), bd=0)
gate_frame.pack(fill="x")
v4_frame=tk.LabelFrame(left_panel, text="🛫 V4", padx=10, pady=5, bg="#4E248F",font=("Arial", 10, "bold"), bd=0)
v4_frame.pack(fill="x")

#INPUTS.
tk.Label(input_frame,text="ICAO code", bg="#5B00F2").grid(row=0,column=0)
entry_code=tk.Entry(input_frame)
entry_code.grid(row=0, column=1)
tk.Label(input_frame,text="Latitude", bg="#5B00F2").grid(row=1,column=0)
entry_lat=tk.Entry(input_frame)
entry_lat.grid(row=1, column=1)
tk.Label(input_frame,text="Longitude", bg="#5B00F2").grid(row=2,column=0)
entry_long=tk.Entry(input_frame)
entry_long.grid(row=2, column=1)

#Version 1 Buttons.
tk.Button(airport_frame,text="Load Airports",command=load_airports,width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=3)
tk.Button(airport_frame,text="Add Airport", command=add_airport, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(airport_frame,text="Remove Airport", command=remove_airport, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(airport_frame,text="Show Airports", command=show_aiports, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(airport_frame,text="Save Schengen Airports", command=save_schengen, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(airport_frame,text="Plot type of airport", command=plot_aiports, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(airport_frame,text="Map Airports", command=map_airports, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)

#Version 2 Buttons.
tk.Button(flight_frame,text="Load Flights", command=load_aircrafts, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(flight_frame,text="Plot Arrivals", command=plot_arrivals, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(flight_frame,text="Save correct format Flights", command=save_flights, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(flight_frame,text="Plot Flights per Airline", command= plot_airlines, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(flight_frame,text="Plot type of arrivals", command=plot_flights_type, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(flight_frame,text="Trajectories Map", command=map_flights, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(flight_frame,text="Save Long Distance Arrivals", command=long_distance_arrivals, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)

#Version 3 Buttons.
tk.Button(gate_frame, text="Load Aiport Structure",command=load_airport_structure, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(gate_frame, text="Assign Gates",command=assign_gate, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(gate_frame, text="Show Gate Occupancy",command=gate_occupancy, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(gate_frame, text="Plot Gate Occupancy",command=plot_gate_occupancy, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)

#Version 4 Buttons.
tk.Button(v4_frame, text="Load Departures",command=load_departures, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(v4_frame, text="Merge Movements",command=merge_movements, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)
tk.Button(v4_frame, text="Show Night Aircrafts",command=night_aircraft, width=22,font=("Arial", 10, "bold"),relief="flat",pady=5,cursor="hand2").pack(fill="x", pady=2)

'''
#Exam Button.
tk.Button(root, text="Delete short distance arrivals",command=short_distance_arrivals_maps).grid(row=14, column=0)
'''

#Text and plot box.
output_frame = tk.LabelFrame(right_panel,text="Output / Results",padx=12,pady=12,bg="white",fg="#2d3436",font=("Arial", 11, "bold"),bd=2,relief="groove")
output_frame.pack(fill="x",expand=True,padx=10,pady=10)
text=tk.Text(output_frame,width=75,height=18,font=("Consolas", 10),bg="#fdfdfd",fg="#2d3436",bd=1,relief="solid")
text.pack(fill="x",expand=True)
plot_frame = tk.LabelFrame(right_panel,text="Plots",padx=12,pady=12,bg="white",fg="#2d3436",font=("Arial", 11, "bold"),bd=2,relief="groove", height=500)
plot_frame.pack(fill="x", padx=10, pady=10)
plot_frame.pack_propagate(False)
root.mainloop()