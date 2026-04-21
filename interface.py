import tkinter as tk
from tkinter import filedialog, messagebox
# from airport import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from aircraft import *
airports=[]
aircrafts=[]
canvas=None

# Function to clean the canvas.
def show_plot(fig):
    global canvas
    if canvas is not None:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=3, rowspan=8)

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
    # ¿<= o <?__________________________________________________
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

# Interface.

root=tk.Tk()
root.title("Airport Manager")

#INPUTS.
tk.Label(root,text="ICAO code").grid(row=0,column=0)
entry_code=tk.Entry(root)
entry_code.grid(row=0, column=1)
tk.Label(root,text="Latitude").grid(row=1,column=0)
entry_lat=tk.Entry(root)
entry_lat.grid(row=1, column=1)
tk.Label(root,text="Longitude").grid(row=2,column=0)
entry_long=tk.Entry(root)
entry_long.grid(row=2, column=1)

# Buttons.

tk.Button(root,text="Load Airports", command=load_airports).grid(row=3, column=1)
tk.Button(root,text="Add Airport", command=add_airport).grid(row=3, column=0)
tk.Button(root,text="Remove Airport", command=remove_airport).grid(row=4, column=0)
tk.Button(root,text="Show Airports", command=show_aiports).grid(row=4, column=1)
tk.Button(root,text="Save Schengen Airports", command=save_schengen).grid(row=5, column=1)
tk.Button(root,text="Plot Schengen vs. Non-Schengen", command=plot_aiports).grid(row=5, column=0)
tk.Button(root,text="Map Airports", command=map_airports).grid(row=6, column=0)

#Version 2 Buttons.
tk.Button(root,text="Load Flights", command=load_aircrafts).grid(row=8, column=0)
tk.Button(root,text="Plot Arrivals", command=plot_arrivals).grid(row=8, column=1)
tk.Button(root,text="Save correct format Flights", command=save_flights).grid(row=9, column=0)
tk.Button(root,text="Plot Flights per Airline", command= plot_airlines).grid(row=9, column=1)
tk.Button(root,text="Plot Schengen vs. Non-Schengen arrivals", command=plot_flights_type).grid(row=10, column=0)
tk.Button(root,text="Trajectories Map", command=map_flights).grid(row=10, column=1)
tk.Button(root,text="Save Long Distance Arrivals", command=long_distance_arrivals).grid(row=11, column=0)

text=tk.Text(root,width=60,height=15)
text.grid(row=7,column=0,columnspan=2)
root.mainloop()