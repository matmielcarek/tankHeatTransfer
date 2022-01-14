# ################################## [importing array with numpy]
# import numpy as np
# with open("db/exp_mielcarek.csv") as file_name:
#     array = np.loadtxt(file_name, delimiter=",")
#
# print(array[2,1])
################################## [importing array with pandas]
################################## [accessing pandas DataFrame]
# import pandas as pd
# array = pd.read_csv("db/exp_mielcarek.csv")
# print(pd.DataFrame(array))
# print("##############################")
# print(array.iat[0,1])
# print("##############################")
# print(array.shape[0])
# ################################## [looping through tuple]
# bnds = (("B","W","T"), ("bottom", "wall", "top"))
# for i, b in enumerate(bnds[0]):
#     print(i)
# ################################## [using CoolProp]
# import CoolProp.CoolProp as CP
# import CoolProp.CoolProp as CP
# fluid = 'Water'
# temp = 20
# tempK = temp + 273.15
# pressure_at_critical_point = CP.PropsSI(fluid,'pcrit')
# # Massic volume (in m^3/kg) is the inverse of density
# # (or volumic mass in kg/m^3). Let's compute the massic volume of liquid
# # at 1bar (1e5 Pa) of pressure
# rho = CP.PropsSI('D','T',tempK,'P',101325,fluid)
# Cp = CP.PropsSI('C','T',tempK,'P',101325,fluid)
# nu = CP.PropsSI('V','T',tempK,'P',101325,fluid)
# lam = CP.PropsSI('L','T',tempK,'P',101325,fluid)
# beta = CP.PropsSI('ISOBARIC_EXPANSION_COEFFICIENT','T',tempK,'P',101325,fluid)
# print([rho,Cp,nu,lam,beta])

# # ################################## [CoolProp check temperature range]
# def Trange(fluid_CP):
#     if fluid_CP == "water":
#         Tmin = 0
#         Tmax = 100
#     else:
#         Tmax = CP.PropsSI('TMAX', 'P', 101325, 'Q', 0, fluid_CP)-273.15
#         Tmin = CP.PropsSI('TMIN', 'P', 101325, 'Q', 0, fluid_CP)-273.15
#     return [Tmax,Tmin]
#
# print(Trange("INCOMP::PHR"))
# print(Trange("water"))

# ################################## [using CoolProp for making plots]
# ph_plot = CPP.PropertyPlot('Water','Ph')
# ph_plot.savefig('enthalpy_pressure_graph_for_Water.png')

# # ################################## [make list from DataFrame column]
# import pandas as pd
#
# fluid_array = pd.read_csv("db/fluids.csv")
# number_column = fluid_array.loc[:,'display_name']
# numbers = list(number_column.values)
# print(numbers)

# #EVAL function
# Pr = 5
# Gr = 5E9
# Ra = Gr*Pr
# Re = 3E4
# Pr_exp = 0.3
#
# print(Gr / ((Re ** 2) * (Pr ** Pr_exp)))
# print(Gr * Re ** -2 * Pr ** -Pr_exp)
# print(Ra * Pr ** -1 * Re ** -2 * Pr ** -Pr_exp)
# print(Ra * Re ** -2 * Pr ** -(Pr_exp+1))
#
# print(eval("Ra * Re ** -2 * Pr ** -(Pr_exp+1)"))

# print(float("inf") > 0)
# area = 2
# print("The area of your rectangle is {}cm\u00b2".format(area))

# import tkinter as TK
# from tkinter import ttk
#
# line_style = ttk.Style()
# line_style.configure("Line.TSeparator", background="#000000")
# line = ttk.Separator(tk, orient=TK.VERTICAL, style="Line.TSeparator")
# line.place(x = 1250,y = 0, height = tk.winfo_screenheight(), width = 8)

# # ################################## [Scrollbar]
# import tkinter as tk
# from tkinter import *
#
# def data():
#     for i in range(50):
#        Label(frame,text=i).grid(row=i,column=0)
#        Label(frame,text="my text"+str(i)).grid(row=i,column=1)
#        Label(frame,text="..........").grid(row=i,column=2)
#
# def myfunction(event):
#     canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)
#
# root=Tk()
# sizex = 800
# sizey = 600
# posx  = 100
# posy  = 100
# root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
#
# myframe=Frame(root,relief=GROOVE,width=50,height=100,bd=1)
# myframe.place(x=10,y=10)
#
# canvas=Canvas(myframe)
# frame=Frame(canvas)
# myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
# canvas.configure(yscrollcommand=myscrollbar.set)
#
# myscrollbar.pack(side="right",fill="y")
# canvas.pack(side="left")
# canvas.create_window((0,0),window=frame,anchor='nw')
# frame.bind("<Configure>",myfunction)
# data()
# root.mainloop()

# ################################## [Scrollbar object-oriented]
# import tkinter as tk
#
# class Example(tk.Frame):
#     def __init__(self, parent):
#
#         tk.Frame.__init__(self, parent)
#         self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
#         self.frame = tk.Frame(self.canvas, background="#ffffff")
#         self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
#         self.canvas.configure(yscrollcommand=self.vsb.set)
#
#         self.vsb.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.create_window((4,4), window=self.frame, anchor="nw",
#                                   tags="self.frame")
#
#         self.frame.bind("<Configure>", self.onFrameConfigure)
#
#         self.populate()
#
#     def populate(self):
#         '''Put in some fake data'''
#         for row in range(100):
#             tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
#                      relief="solid").grid(row=row, column=0)
#             t="this is the second column for row %s" %row
#             tk.Label(self.frame, text=t).grid(row=row, column=1)
#
#     def onFrameConfigure(self, event):
#         '''Reset the scroll region to encompass the inner frame'''
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#
# if __name__ == "__main__":
#     root=tk.Tk()
#     example = Example(root)
#     example.pack(side="top", fill="both", expand=True)
#     root.mainloop()

for i in range(16):
    print(i)
