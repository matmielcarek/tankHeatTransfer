def help_me():
#define default width
    wth = r.winfo_screenwidth()/1.5
#build help window
    help_window = tk.Toplevel(r)
    help_window.title('Help')
    help_window.resizable(False, False)
    sizex = wth
    sizey = wth
    posx  = 0
    posy  = 0
    help_window.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
# build master frame
    myframe = Frame(help_window,width=wth,height=wth,bd=1)
    myframe.place(x=0,y=0)
# build help canvas
#     help_canvas = Canvas(myframe)
    # help_canvas.pack(side=LEFT, fill=BOTH)
# build scrollbar
#     scr = Scrollbar(myframe,orient="vertical",command=help_canvas.yview)
    # scr.pack(side=RIGHT, fill=Y)
# build help frame
#     help_frame = Frame(help_canvas)
    # help_frame.pack(side=LEFT, fill=BOTH)
    # help_frame.grid_columnconfigure(0, weight=1)
# configure canvas to work with scrollbar and put help_frame to canvas
#     help_canvas.configure(yscrollcommand=scr.set)
    # help_canvas.create_window((0,0),window=help_frame,anchor='nw')
    # help_frame.bind("<Configure>",myfunction)
#configure scrollbar
    # scr.config(orient="vertical", command=help_frame.yview)
    # help_canvas.configure(yscrollcommand=scr.set)




    help_canvas = Canvas(myframe)
    help_frame = Frame(help_canvas)
    scr = Scrollbar(myframe,orient="vertical",command=help_canvas.yview)
    help_canvas.configure(yscrollcommand=scr.set)

    scr.pack(side=RIGHT, fill=Y)
    help_canvas.pack(side=LEFT)
    help_canvas.create_window((0,0),window=help_frame,anchor='nw')
    help_frame.bind("<Configure>",help_canvas.configure(scrollregion=help_canvas.bbox("all"),width=wth,height=wth))

    wth = r.winfo_screenwidth()/2
    # width = int(r.winfo_screenwidth()/2)
    # height = int(r.winfo_screenheight()/2)
    # help_frame.geometry(f'{width}x{height}')
    # help_frame.grid(column=4, row=0, sticky="ew", columnspan=4)
    # help_frame.columnconfigure(0, weight=1)
    #0
    # tk.Frame(help_frame, bg="grey", height=2, bd=0).grid(row=0, sticky="ew")
    Label(help_frame, text='General').grid(row=1, column=0)
    ttk.Separator(help_frame, orient='horizontal').grid(row=2, sticky="ew")
    help0 = "This application is designed to calculate convective heat transfer coefficient (HTC) through a tank boundary. \
HTC [W / (m^2 K)] is required to calculate heat flow through the boundary, i.e. to calculate heat balance of ship tanks or \
to determine temperature of the boundary. Ship tanks are in most cases not insulated and therefore convection provides major \
heat resistance of the boundary and plays the main role in heat transfer. On the other hand, convection is a complex phenomena \
and HTC is dependent on many factors, such as dimensions of the boundary, temperature of the boundary surface and fluid, type of fluid, \
nature of flow in developed boundary layer and external factors. In ship tanks, the phenomena is even more \
complex due to periodic motion of the ship that triggers additional, forced periodic flow in the boundary layer, which interferes with the \
natural convective flow. \n\
This application uses correlations developed by various researchers for the phenomena of convection in ship tanks of different configurations. \
Research we based on is lister in the 'References' section. Please also note the 'Disclaimer'."
    Label(help_frame, text=help0, wraplength=int(wth), justify=LEFT).grid(row=3, column=0)
    #1
    tk.Frame(help_frame, bg="grey", height=2, bd=0).grid(row=10, sticky="ew")
    Label(help_frame, text=lab1).grid(row=11, column=0)
    ttk.Separator(help_frame, orient='horizontal').grid(row=12, sticky="ew")
    help1 = "\
[" + lab11 + "] shall be given as an average expected value of the one of the ship motions in design conditions. Roll an pitch motions are ones that are the most \
capable to induce motion of liquid in the tank. Roll will be relevant for vertical boundaries longitudinal to the ship axis. Pitch will be relevant \
vetrical boundaries transverse to the ship axis. For horizontal boundaries select one of the larger magnitude. \n\
[" + lab12 + "] shall be given as an average expected value for the one of the ship motions in design conditions. Roll an pitch motions are ones that are the most \
capable to induce motion of liquid in the tank. Roll will be relevant for vertical boundaries longitudinal to the ship axis. Pitch will be relevant \
vetrical boundaries transverse to the ship axis. For horizontal boundaries select one of the lower magnitude. \n\
[" + lab13 + "] is used for calculation of forced convection in sea water outside hull due to ship motion ahead on sailing. \n\
[" + lab14 + "] is used for calculation of forced convection in sea water outside hull due to ship motion ahead on sailing. If the design \
condition is that the ship is not sailing, set to 0."
    Label(help_frame, text=help1, wraplength=int(wth), justify=LEFT).grid(row=13, column=0)
    #2
    tk.Frame(help_frame, bg="grey", height=2, bd=0).grid(row=20, sticky="ew")
    Label(help_frame, text=lab2).grid(row=21, column=0)
    ttk.Separator(help_frame, orient='horizontal').grid(row=22, sticky="ew")
    help2 = "[" + lab21 + "] determines if the calculated boundary is a bottom, a wall or a top of the tank. Note that currently only \
vertical and horizontal configuration of boundary are supported. \n\
[" + lab22 + "] is dimension of the boundary that is tangent to the direction of motion of the boundary due to ship motion. For roll \
motion (along ship x axis) it is dimension along y axis for top and bottom and dimension along z axis for wall. For pitch motion \
(along ship y axis) it is dimension along x axis for top and bottom. \n\
[" + lab23 + "] is the second dimension of the boundary, used for calculation of the heat transfer rate. Set to 1 if only the HTC is of interest. \n\
[" + lab24 + "] determines distance of the boundary from the center of gravity of the ship, which is considered as approximate cener \
of motion of the ship. Distance shall be measured perpendicular to the surface of the boundary."
    Label(help_frame, text=help2, wraplength=int(wth), justify=LEFT).grid(row=23, column=0)
    #3
    tk.Frame(help_frame, bg="grey", height=2, bd=0).grid(row=30, sticky="ew")
    Label(help_frame, text=lab3).grid(row=31, column=0)
    ttk.Separator(help_frame, orient='horizontal').grid(row=32, sticky="ew")
    help3 = "\
    [" + lab31 + "]  \n\
    [" + lab32 + "] \n\
    [" + lab33 + "]"
    Label(help_frame, text=help3, wraplength=int(wth), justify=LEFT).grid(row=33, column=0)
    #
    ttk.Separator(help_frame, orient='horizontal').grid(row=90, sticky="ew")
    bt_exit = tk.Button(help_frame, text='Exit', width=7, command=help_frame.destroy)
    bt_exit.grid(row=91, column=0, sticky="e") # Exit