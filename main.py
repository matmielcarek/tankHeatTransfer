
# pozbyć się migotania obliczeń
# sprawdzić korelacje - coś jest grubo nie tak
# HELP # sea water / fresh water wyjaśnić w help
# HELP # Doerrfer na dnie wyjaśnić w help
# HELP # current limitations
# pimp messages
import pandas as pd
import aux
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as fnt
import CoolProp.CoolProp as CP
import MMImath
import matplotlib.pyplot as plt
################################## [defining symbols]
deg = u"\N{DEGREE SIGN}"
################################## [defining constants]
g = 9.81
pi = 3.14
acc = 0.05
################################## [defining tuples]
bnds = ("horizontal tank bottom", "vertical tank wall", "horizontal tank top")
oris = ("horizontal", "vertical")
tanks = ("tank filled with liquid", "tank with free surface", "fluid outside hull", "ambient air", "ventilated compartment", "unventilated void")
################################## [defining main window and frames]
r = tk.Tk()
errors_frame = Frame(r)
buttons_frame = Frame(r)
r.title('Calculate convective heat transfer through a boundary')
r.resizable(False, False)
r.grid_columnconfigure(0, weight=1)
################################## [defining separators

################################## [read data]
fluid_array = pd.read_csv("db/fluids.csv")
Col_No = fluid_array.loc[:, 'display_name']
fluids1 = list(Col_No.values)
fluids2 = fluids1
# print(fluids)
################################## [defining variables]
# ori = BooleanVar()
# ori.set(1)
# ch4_text = StringVar()
# ch4_text.set("vertical")
fluid1 = StringVar(r)
fluid1.set("fresh water") # default value
fluid2 = StringVar(r)
fluid2.set("fresh water") # default value
ftemp1 = StringVar(r)
ftemp1.set("15") # default value
ftemp2 = StringVar(r)
ftemp2.set("5") # default value
tank_type_1 = StringVar(r)
tank_type_1.set(tanks[0]) # default value
tank_type_2 = StringVar(r)
tank_type_2.set(tanks[0]) # default value
ship_ang = StringVar(r)
ship_ang.set("15") # default value
ship_per = StringVar(r)
ship_per.set("5") # default value
ship_len = StringVar(r)
ship_len.set("100") # default value
ship_vel = StringVar(r)
ship_vel.set("8") # default value
bnd_ori_1 = StringVar(r)
bnd_ori_1.set(bnds[1]) # default value
# bnd_ang = StringVar()
# bnd_ang.set("90")
dim1 = StringVar(r)
dim1.set("10")
dim2 = StringVar(r)
dim2.set("10")
dist = StringVar(r)
dist.set("10")
################################## [widgets' and variables' actions]
#ch4 checkbutton - change text and seto to "checked" once boundary function is selected
def checkFluids(self):
    # global fluids1
    # global fluids2
    # global fluid1
    # global fluid2
    # global tank_type_1
    # global tank_type_2
    # tank_type_1_ = tank_type_1.get()
    # tank_type_2_ = tank_type_2.get()
    # fluid1_ = fluid1.get()
    # fluid2_ = fluid2.get()
#if "air-based" tank type is selected, force air as a liquid
    if tanks.index(tank_type_1.get()) > 2:
        fluid1.set(fluids1[0])
    elif tanks.index(tank_type_1.get()) <= 2 and fluids1.index(fluid1.get()) == 0:
        fluid1.set(fluids1[1])
    if tanks.index(tank_type_2.get()) > 2:
        fluid2.set(fluids2[0])
    elif tanks.index(tank_type_2.get()) <= 2 and fluids2.index(fluid2.get()) == 0:
        fluid2.set(fluids2[1])
# # change boundary function if tank top is selected while type of tank 1 is tank with free surface
#     if bnd_ori_1.get() == bnds[2] and tank_type_1.get() == tanks[1]:
#         bnd_ori_1.set(bnds[0])
# # change boundary function if tank bottom is selected while type of tank 2 is tank with free surface
#     if bnd_ori_1.get() == bnds[0] and tank_type_2.get() == tanks[1]:
#         bnd_ori_1.set(bnds[2])
# if air is selected, force ambient air as a tank type
def checkTanks(self):
    # global tank_type_1
    # global tank_type_2
    if fluids1.index(fluid1.get()) > 0 and tanks.index(tank_type_1.get()) > 2:
        tank_type_1.set(tanks[0])
    elif fluids1.index(fluid1.get()) == 0 and tanks.index(tank_type_1.get()) <= 2:
        tank_type_1.set(tanks[3])
        # opt2 = OptionMenu(r, fluid1, *fluids)
    if fluids2.index(fluid2.get()) > 0 and tanks.index(tank_type_2.get()) > 2:
        tank_type_2.set(tanks[0])
    elif fluids2.index(fluid2.get()) == 0 and tanks.index(tank_type_2.get()) <= 2:
        tank_type_2.set(tanks[3])
################################## [calculate fluid properties]
def draw_props(ftempK, fluid_CP):
    rho = CP.PropsSI('D','T', ftempK, 'P', 101325, fluid_CP)
    Cp = CP.PropsSI('C','T', ftempK, 'P', 101325, fluid_CP)
    mu = CP.PropsSI('V','T', ftempK, 'P', 101325, fluid_CP)
    nu = mu/rho
    lam = CP.PropsSI('L','T', ftempK, 'P', 101325, fluid_CP)
    if fluid_CP[0:6] == "INCOMP":
        beta = 7e-4
    else:
        beta = CP.PropsSI('ISOBARIC_EXPANSION_COEFFICIENT','T', ftempK, 'P', 101325, fluid_CP)
    # print("Fluid parameters at film temperature are:")
    # print("density (\u03C1): " + str(MMImath.rn_sig(rho, acc, 0)) + " kg/m3")
    # print("specific heat capacity (Cp): " + str(MMImath.rn_sig(Cp, acc, 0)) + " J/kgK")
    # print("dynamic viscosity (\u03BC): " + str(MMImath.rn_sig(mu, acc, 1)) + " Pa*s")
    # print("kinematic viscosity (\u03BD): " + str(MMImath.rn_sig(nu, acc, 1)) + " m2/s")
    # print("thermal conductivity (\u03BB): " + str(MMImath.rn_sig(lam, acc, 0)) + " J/mK")
    # print("volumetric thermal expansion coefficient (\u03B2): " + str(MMImath.rn_sig(beta, acc, 1)) + " 1/K.")
    return [rho, Cp, mu, nu, lam, beta]
################################## [select correlations and characteristic dimensions based on input]
def sel_corr(tank_type_in, tanks_in, fluid_in, fluid_list_in):
    L1_type = 0
    if fluid_in == fluid_list_in[0]:#air
        if tank_type_in == tanks_in[3]: #Ambient air
            corr_name = "ISO_out"
            corr_label = "ISO7547:2002 Standard"
        elif tank_type_in == tanks_in[4]: #Ventilated compartment
            corr_name = "ISO_in"
            corr_label = "ISO7547:2002 Standard"
        elif tank_type_in == tanks_in[5]: #Unventilated void
            corr_name = "db/exp_mcadams.csv"
            corr_label = "W. H. McAdams (1954)"
            L1_type = 1
    else: #liquids
        if tank_type_in == tanks_in[0]: #Tank filled with liquid
            corr_name = "db/exp_mielcarek.csv"
            corr_label = "M. Mielcarek (2021)"
        elif tank_type_in == tanks_in[1]: #Tank with free liquid surface
            corr_name = "db/exp_doerffer.csv"
            corr_label = "S. Doerrfer (1981)"
        elif tank_type_in == tanks_in[2]: #Water outside hull
            corr_name = "db/exp_forced.csv"
            corr_label = "analitical solution"
        else:
            corr_name = "error"
            corr_label = "error"
        # print(corr_name)
        # print(corr_label)
    return [corr_name, corr_label, L1_type]
def sel_dims(bnd_ori_in, L1_type_in, dim1, dim2, dist): #select characteristic dimensions based on boundary type and orientation
    if L1_type_in == 1 and (bnd_ori_in == bnds[2] or bnd_ori_in == bnds[0]):
        L1 = dim1 * dim2 / (2 * dim1 + 2 * dim2)
    else:
        L1 = dim1
    L2 = dist
    return [L1,L2]
def sel_Pr_exp(bnd_ori_in,corr_name_in):
    col = 0
    if corr_name_in == "db/exp_mielcarek.csv" and bnd_ori_in == bnds[0]:
        col = 1
    return col
################################## [calculate characteristic numbers]
def calc_numbers(properties,dT,L1_in,L2_in,ang,per,len,vel,tank_type_in):
    # rho = properties[0]
    Cp = properties[1]
    mu = properties[2]
    nu = properties[3]
    lam = properties[4]
    beta = properties[5]
    Pr = Cp * mu / lam
    # print("Prandtl number (Pr) is: " + str(MMImath.rn_to_sig_dig(Pr,acc)))
    Gr = abs(beta * dT * g * (L1_in ** 3) / (nu ** 2))
    # print("Grashof number (Gr) for roll is: " + str(MMImath.rn_to_sig_dig(Gr_X,acc)))
    Ra = Gr * Pr
    # print("Rayleigh number (Ra) for roll is: " + str(MMImath.rn_to_sig_dig(Ra,acc)))
    if ang != 0:
        if tank_type_in == tanks[2]:
            Re = vel * len / nu
        else:
            Re = ang / per * L2_in * L1_in / nu
        # print("Reynolds number (Re) for roll is: " + str(MMImath.rn_to_sig_dig(Re_X,acc)))
        Sr = L1_in / ang / L2_in
        Fr = ang * per * L2_in / ((g * L1_in)**0.5)
    else:
        Re = 0
        Sr = 0
        Fr = 0
    return [Re,Ra,Pr,Sr,Fr]
#compare criteria value to appropriate value from the crit_array and calculate Nuss and alpha
def calc_nuss(Re_in,Ra_in,Pr_in,Sr_in,Fr_in,lam_in,L1_in,corr_name_in,corr_label_in,bnd_ori_in):
#read an appropiate array of criteria values and exponent values based on selected correlation
    if corr_name_in == "ISO_out":
        Nuss = "not calculated"
        alpha = 80
        mess1 = " convection enhanced by wind"
        mess2 = "HTC (\u03B1) = 80 W m^-2 K^-1 acc to " + corr_label_in + "."
    elif corr_name_in == "ISO_in":
        Nuss = "not calculated"
        alpha = 8
        mess1 = " convection enhanced by internal ventilation and heating appliances"
        mess2 = "HTC (\u03B1) = 8 W m^-2 K^-1 acc. to " + corr_label_in + "."
    else:
        corr_array = pd.read_csv(corr_name_in)
        col = sel_Pr_exp(bnd_ori_in,corr_name_in)
        if Re_in != 0:
            Crit = eval(corr_array.iat[0, col])
        else:
            Crit = 0
        # print(Crit)
        # print(bnd_ori_in)
        for i, b in enumerate(bnds):
            if bnd_ori_in == b:
            #for stationary cases (Re = 0)
                if Crit == 0:
                    j = 1
                    mess1 = ", not subjected to oscillations, with " + str(corr_array.iat[i*4+j, 2]) + " convection"
                # construct an array of applicable ranges of subsequent characteristic numbers
                    Rn = list()
                    Rn_chk = list()
                    for f in range(6):
                        Rn.append(float(corr_array.iat[i * 4 + j, f + 9]))
                # collect characteristic numbers, converted by the scale, in an array
                    L1_model = 0.4
                    Num = [Re_in * (L1_model / L1_in)**2, Ra_in * (L1_model / L1_in) ** 3, Pr_in]
                # check applicability range (Reynolds number, Rayleigh number Prandtl number)
                    for s in range(3):
                        if Rn[s * 2] < Num[s] < Rn[s * 2 + 1]:
                            Rn_chk.append(True)
                        else:
                            Rn_chk.append(False)
                    print("min: " + str(MMImath.rn_sig(Rn[0], acc, 1)), str(MMImath.rn_sig(Rn[2], acc, 1)),str(MMImath.rn_sig(Rn[4], acc, 0)))
                    print("val: " + str(MMImath.rn_sig(Num[0], acc, 1)), str(MMImath.rn_sig(Num[1], acc, 1)),
                          str(MMImath.rn_sig(Num[2], acc, 0)))
                    print("max: " + str(MMImath.rn_sig(Rn[1], acc, 1)), str(MMImath.rn_sig(Rn[3], acc, 1)),str(MMImath.rn_sig(Rn[5], acc, 0)))
                    print(Rn_chk)
            #construct the array of exponents applicable for selected type of convection
                    C = list()
                    for k in range(6):
                        C.append(float(corr_array.iat[i * 4 + j, k + 3]))
                    Nuss = C[0] * (Ra_in ** C[2]) * (Pr_in ** C[3])
            #for dynamic cases (Re > 0)
                else:
                    for j in range(2,5):
                        # print(float(corr_array.iat[i*4+j, 0]),float(corr_array.iat[i*4+j, 1]))
                        if float(corr_array.iat[i*4+j, 0]) <= Crit < float(corr_array.iat[i*4+j, 1]):
                            # print(Crit)
                            # print("crit is: " + str(Crit) + "i is: " + str(i) + " / j is : " + str(j) + " / row is " + str(i*4+j))
                            mess1 = ", subjected to oscillations, with " + corr_array.iat[i*4+j, 2] + " convection"
                            if j != 3:
                                 mess1 = mess1 + " domination"
                        # construct an array of applicable ranges of subsequent characteristic numbers
                            Rn = list()
                            Rn_chk = list()
                            for f in range(6):
                                Rn.append(float(corr_array.iat[i * 4 + j, f + 9]))
                        # collect characteristic numbers, converted by the scale, in an array
                            L1_model = 0.4
                            Num = [Re_in * (L1_model / L1_in)**2, Ra_in * (L1_model / L1_in) ** 3, Pr_in]
                        # check applicability range (Reynolds number, Rayleigh number Prandtl number)
                            for s in range(3):
                                if Rn[s * 2] < Num[s] < Rn[s * 2 + 1]:
                                    Rn_chk.append(True)
                                else:
                                    Rn_chk.append(False)
                            print("min: " + str(MMImath.rn_sig(Rn[0], acc, 1)), str(MMImath.rn_sig(Rn[2], acc, 1)),
                                  str(MMImath.rn_sig(Rn[4], acc, 0)))
                            print("val: " + str(MMImath.rn_sig(Num[0], acc, 1)), str(MMImath.rn_sig(Num[1], acc, 1)),
                                  str(MMImath.rn_sig(Num[2], acc, 0)))
                            print("max: " + str(MMImath.rn_sig(Rn[1], acc, 1)), str(MMImath.rn_sig(Rn[3], acc, 1)),
                                  str(MMImath.rn_sig(Rn[5], acc, 0)))
                            print(Rn_chk)
            #construct the array of exponents applicable for selected type of convection
                            C = list()
                            for k in range(6):
                                C.append(float(corr_array.iat[i*4+j, k+3]))
                            # print(C)
            #calculate Nusselt number based on correlation parameters in exp_mielcarek.csv
                            Nuss = C[0]*(Re_in**C[1])*(Ra_in**C[2])*(Pr_in**C[3])*(Sr_in**C[4])*(Fr_in**C[5])
                cn = ["Re","Ra","Pr","Sr","Fr"]
                # print(C[0])
                # print(bnd_ori_in)
                mess2 = "Nu = " + str(C[0])
                for f, n in enumerate(cn):
                    if C[f+1] != 0:
                        mess2 = mess2 + " " + n + "^" + str(C[f+1])
                    # mess2 = mess2 + str(C[f]) + " Re^" + str(C[1]) + " Ra^" + str(C[2]) + " Pr^" + str(C[3])
            # calculate Nusselt number based on correlation parameters in exp_mielcarek.csv
                alpha = Nuss * lam_in / L1_in
                # print(alpha)
    return [Nuss,alpha,mess1,mess2]#Rn_chk
################################## [main program]
def calc_bnd():
#assign boundary type of "the other" tank
    if bnd_ori_1.get() == bnds[0]:
        bnd_ori_2 = bnds[2]
    elif bnd_ori_1.get() == bnds[2]:
        bnd_ori_2 = bnds[0]
    else:
        bnd_ori_2 = bnd_ori_1.get()
    # print(bnd_ori_1.get(),bnd_ori_2)
#read CoolProp fluid name based on given name
    fluid_cp1 = fluid_array.loc[fluid_array.display_name == fluid1.get(), 'CoolProp_name'].values[0]
    fluid_cp2 = fluid_array.loc[fluid_array.display_name == fluid2.get(), 'CoolProp_name'].values[0]
#read and check input data
    msg_list = list()
    # labels = list()
    # wth = r.winfo_width()
#
    #check tank type and boundary type to avoid calculation of "tank top" with correlations for tank with free surface
    if (bnd_ori_1.get() == bnds[2] and tank_type_1.get() == tanks[1]):
        msg = "Cannot calculate convection at the top of tank at side 1, that is not filled with luquid: tank with free surface."
    elif (bnd_ori_1.get() == bnds[0] and tank_type_2.get() == tanks[1]):
        msg = "Cannot calculate convection at the top of tank at side 2, that is not filled with luquid: tank with free surface."
    else:
        msg = "OK"
    msg_list.append(msg)
    # lab1 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # lab1.grid(row=(40 + 0 + 2), column=0, sticky="w", columnspan=4)
    # labels.append(lab1)
#
    a_range = aux.Trange(fluid_cp1)
    ftemp1_ = aux.checkNumVal(ftemp1, [a_range[0], a_range[1]])
    if ftemp1_[1] == "range":
        msg = "Given temperature of " + fluid1.get() + " is outside allowed range of: " + str(a_range[0]) + " to " + str(a_range[1]) + "."
    elif ftemp1_[1] == "NaN":
        msg = "Given input: " + fluid1.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    ftemp1_ = ftemp1_[0]
    # lab2 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # lab2.grid(row=(40 + 1 + 2), column=0, sticky="w", columnspan=4)
    # labels.append(lab2)
#
    a_range = aux.Trange(fluid_cp2)
    ftemp2_ = aux.checkNumVal(ftemp2, [a_range[0], a_range[1]])
    if ftemp2_[1] == "range":
        msg = "Given temperature of " + fluid2.get() + " is outside allowed range of: " + str(a_range[0]) + " to " + str(a_range[1]) + "."
    elif ftemp2_[1] == "NaN":
        msg = "Given input: " + fluid2.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    ftemp2_ = ftemp2_[0]
    # lab3 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab3)
#
    a_range = [0, 45]
    ship_ang_ = aux.checkNumVal(ship_ang, [a_range[0], a_range[1]])
    if ship_ang_[1] == "range":
        msg = "Given angle of ship motion is outside allowed range of: " + str(a_range[0]) + deg + " to " + str(a_range[1]) + deg + "."
    elif ship_ang_[1] == "NaN":
        msg = "Given input: " + ship_ang.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    ship_ang_ = ship_ang_[0]
    # lab4 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab4)
#
    a_range = [0, 50]
    ship_per_ = aux.checkNumVal(ship_per, [a_range[0], a_range[1]])
    if ship_per_[1] == "range":
        msg = "Given period of of ship motion is outside allowed range of: " + str(a_range[0]) + " to " + str(a_range[1]) + "."
    elif ship_per_[1] == "NaN":
        msg = "Given input: " + ship_per.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    ship_per_ = ship_per_[0]
    # lab5 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab5)
#
    a_range = [1, 500]
    ship_len_ = aux.checkNumVal(ship_len, [a_range[0], a_range[1]])
    if ship_len_[1] == "range":
        msg = "Given length of ship is outside allowed range of: " + str(a_range[0]) + " to " + str(
            a_range[1]) + "."
    elif ship_len_[1] == "NaN":
        msg = "Given input: " + ship_len.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    ship_len_ = ship_len_[0]
    # lab6 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab6)
#
    a_range = [0, 50]
    ship_vel_ = aux.checkNumVal(ship_vel, [a_range[0], a_range[1]])
    if ship_vel_[1] == "range":
        msg = "Given velocity of ship is outside allowed range of: " + str(a_range[0]) + " to " + str(a_range[1]) + "."
    elif ship_vel_[1] == "NaN":
        msg = "Given input: " + ship_vel.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    ship_vel_ = ship_vel_[0]
    # lab7 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab7)
#
    a_range = [0, 60]
    dim1_ = aux.checkNumVal(dim1, [a_range[0], a_range[1]])
    if dim1_[1] == "range":
        msg = "Given dimension X of the boundary is outside allowed range of: " + str(a_range[0]) + " to " + str(a_range[1]) + "."
    elif dim1_[1] == "NaN":
        msg = "Given input: " + dim1.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    dim1_ = dim1_[0]
    # lab8 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab8)
#
    a_range = [0, 60]
    dim2_ = aux.checkNumVal(dim2, [a_range[0], a_range[1]])
    if dim2_[1] == "range":
        msg = "Given dimension Y of the boundary is outside allowed range of: " + str(a_range[0]) + " to " + str(a_range[1]) + "."
    elif dim2_[1] == "NaN":
        msg = "Given input: " + dim2.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    dim2_ = dim2_[0]
    # lab9 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab9)
#
    a_range = [0, 100]
    dist_ = aux.checkNumVal(dist, [a_range[0], a_range[1]])
    if dist_[1] == "range":
        msg = "Given distance of th eboundary from COG is outside allowed range of: " + str(a_range[0]) + " to " + str(a_range[1]) + "."
    elif dist_[1] == "NaN":
        msg = "Given input: " + dist.get() + " is not numeric."
    else:
        msg = "OK"
    msg_list.append(msg)
    dist_ = dist_[0]
    # lab10 = Label(errors_frame, text=msg, wraplength=int(wth), justify=LEFT)
    # labels.append(lab10)
#
    # print(len(msg_list))
    # print(len(labels))
#HERE SELECT CORR AND CHAR DIMS
#check error messages
    err = False
    for i in range(len(msg_list)):
        if not msg_list[i] == "OK":
            err = True
    # print(err)
#start calculations if inputs are correct
#convert input data
    if err == True:
        print("Check input data.")
# construct "Errors" section
# section 4
# clear all children (labels) in errors_frame to avoiid tkinter building new instances every time which are later impossible to idnetify and delete
        for widget in errors_frame.winfo_children():
            widget.destroy()
# place errors frame
        errors_frame.grid(row=40, sticky="ew", columnspan=4)
        errors_frame.columnconfigure(0, weight=1)
        wth = r.winfo_width()
# header of errors frame
        Label(errors_frame, text='Errors').grid(row=40, column=0, columnspan=4)
        ttk.Separator(errors_frame, orient='horizontal').grid(row=41, sticky="ew", columnspan=4)
# go through list of error messages and put labels in grid / delete if not "OK"
        for i, mess in enumerate(msg_list):
            lab = Label(errors_frame, text=mess, wraplength=int(wth), justify=LEFT)
            lab.grid(row=(40 + int(i) + 2), column=0, sticky="w", columnspan=4)
            if mess == "OK":
                lab.grid_forget()
        ttk.Separator(errors_frame, orient='horizontal').grid(row=59, sticky="ew", columnspan=4)
    else:
#clean errors frame and list
        errors_frame.grid_forget()
#convert inputs
        ship_ang_R = ship_ang_ * pi / 180
        ship_vel_ms = ship_vel_ * 0.5144
#assign initial value od alphas
        acc_calc = 0.001
        R_1 = 1 #INITIAL STEP
        R_2 = 1 #INITIAL STEP
        R_tot = R_1+R_2
        R_tot_old = (R_1+R_2)*(1+acc_calc*2)  # INITIAL STEP
#initiate register arrays
        dT_fb1_reg = ["dT_1"]
        dT_fb2_reg = ["dT_2"]
        alpha1_reg = ["alpha1"]
        alpha2_reg = ["alpha2"]
        iter = int()
        R_1_olds = list()
        R_2_olds = list()
        block = bool()
        while abs(R_tot_old-R_tot)/R_tot > acc_calc:
#calculate temperature differences between fluid and boundary based on heat resistances
            dT_fb1 = (R_1)/(R_1+R_2)*(ftemp1_-ftemp2_)
            dT_fb2 = (ftemp1_-ftemp2_) - dT_fb1
            dT_fb1_reg.append(dT_fb1)
            dT_fb2_reg.append(dT_fb2)
            film_tempK1 = (ftemp1_ + dT_fb1 / 2) + 273.15
            film_tempK2 = (ftemp2_ + dT_fb2 / 2) + 273.15
#calculate fluid properties and characteristic numbers
            props1 = draw_props(film_tempK1, fluid_cp1)
            props2 = draw_props(film_tempK2, fluid_cp2)
#select appropiate correlation for calculations
            corr1 = sel_corr(tank_type_1.get(), tanks, fluid1.get(), fluids1)
            corr_name_1 = corr1[0]
            corr_label_1 = corr1[1]
            L1_type_1 = corr1[2]
            corr2 = sel_corr(tank_type_2.get(), tanks, fluid2.get(), fluids2)
            corr_name_2 = corr2[0]
            corr_label_2 = corr2[1]
            L1_type_2 = corr2[2]
#select appropiate characteristic dimensions for the correlation
            L_t1 = sel_dims(bnd_ori_1.get(), L1_type_1, dim1_, dim2_, dist_)
            L_t2 = sel_dims(bnd_ori_2, L1_type_2, dim1_, dim2_, dist_)
            L1_1 = L_t1[0]
            L2_1 = L_t1[1]
            L1_2 = L_t2[0]
            L2_2 = L_t2[1]
#calculate characteristic numbers fot both tanks
            #calc_numbers(properties,dT,L1_in,L2_in,ang,per):
            nums1 = calc_numbers(props1,dT_fb1,L1_1,L2_1,ship_ang_R,ship_per_,ship_len_,ship_vel_,tank_type_1)
            nums2 = calc_numbers(props2, dT_fb2, L1_2, L2_2, ship_ang_R, ship_per_,ship_len,ship_vel_,tank_type_2)
            Re1 = nums1[0]
            Ra1 = nums1[1]
            Pr1 = nums1[2]
            Sr1 = nums1[3]
            Fr1 = nums1[4]
            Re2 = nums2[0]
            Ra2 = nums2[1]
            Pr2 = nums2[2]
            Sr2 = nums2[3]
            Fr2 = nums2[4]
#change correlation from Mielcarek to Doerrfer if stationary and bottom (no results in Mielcarek)
            if corr_name_1 == "db/exp_mielcarek.csv" and bnd_ori_1.get() == bnds[0] and Re1 == 0:
                corr_name_1 = "db/exp_doerffer.csv"
                corr_label_1 = "S. Doerrfer (1981)"
            if corr_name_2 == "db/exp_mielcarek.csv" and bnd_ori_2 == bnds[0] and Re1 == 0:
                corr_name_2 = "db/exp_doerffer.csv"
                corr_label_2 = "S. Doerrfer (1981)"
#read crit_array of values of criteria of domination of certain type of convection
            res1 = calc_nuss(Re1, Ra1, Pr1, Sr1, Fr1, props1[4], L1_1, corr_name_1, corr_label_1, bnd_ori_1.get())
            res2 = calc_nuss(Re2, Ra2, Pr2, Sr2, Fr2, props2[4], L1_2, corr_name_2, corr_label_2, bnd_ori_2)
            Nu1 = res1[0]
            alpha1 = res1[1]
            alpha1_reg.append(MMImath.rn_sig(alpha1, acc, 0))
            mess1_1 = res1[2]
            mess2_1 = res1[3]
            Q1 = alpha1 * (dim1_*dim2_) * dT_fb1
            Nu2 = res2[0]
            alpha2 = res2[1]
            alpha2_reg.append(MMImath.rn_sig(alpha2, acc, 0))
            mess1_2 = res2[2]
            mess2_2 = res2[3]
            # Q2 = alpha2 * (dim1_*dim2_) * dT_fb2
            R_tot_old = R_tot
            R_1 = 1 / alpha1
            R_2 = 1 / alpha2
# flickering solution proposal - voting to a list and taking value as average... still flickering
            R_1_olds.append(R_1)
            R_2_olds.append(R_2)
            len1 = len(R_1_olds)
            len2 = len(R_2_olds)
            # R_1 = sum(R_1_olds) / float(len1)
            # R_2 = sum(R_2_olds) / float(len2)
            R_tot = R_1 + R_2
# print progress of calculation
            iter = iter + 1
            print(" ____________________________________________________________")
            print("|                    [Calculating step " + str(iter) + "]                   |")
            print(" ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
            print("dT1 = " + str(dT_fb1) + "; dT2 = " + str(dT_fb2))
            print("Side 1: correlation by " + corr_label_1 + " for a tank " + mess1_1 + " / " + mess2_1)
            print(props1)
            print("Side 1: Re1 = " + str(MMImath.rn_sig(Re1, acc, 1)) + ", Ra1 = " + str(MMImath.rn_sig(Ra1, acc, 1)) + ", Pr1 = " + str(MMImath.rn_sig(Pr1, acc, 0)))
            print("Side 1 \u03B11 = " + str(MMImath.rn_sig(alpha1, acc, 0)))
            print("Side 2: correlation by " + corr_label_2 + " for a tank " + mess1_2 + " / " + mess2_2)
            print(props2)
            print("Side21: Re2 = " + str(MMImath.rn_sig(Re2, acc, 1)) + ", Ra2 = " + str(MMImath.rn_sig(Ra2, acc, 1)) + ", Pr2 = " + str(MMImath.rn_sig(Pr2, acc, 0)))
            print("Side 2 \u03B11 = " + str(MMImath.rn_sig(alpha2, acc, 0)))
            # print("calc R_1 = " + str(round(R_1c,5)) + "; calc R_2 = " + str(round(R_2c,5)))
            print("R_1 = " + str(round(R_1,5)) + "; R_2 = " + str(round(R_2,5)))
            print("R_diff = " + str(abs(round((R_tot_old-R_tot)/R_tot,5))))
# fuse to prevent flickering of the results due to jumping between correlations
            # read which numbers are in applicable range
            # Range_ch_1 = res1[4]
            # Range_ch_2 = res2[4]
            # pr1=int()
            # pr2=int()
            # # assign points for numbers in applicable range (Re = 1 point; Ra = 2 points; Pr = 0 points)
            # if Range_ch_1[0] == True:
            #     pr1 += 1
            # if Range_ch_1[1] == True:
            #     pr1 += 2
            #detesct flickering
            # print((abs(sum(R_1_olds) / float(len1) - R_1))/R_1)
            if len1 > 10 and ((abs(sum(R_1_olds) / float(len1) - R_1))/R_1) > 0.3:
                print("migotanie")
                # R_1 = (R_1 + R_2) / 2
                # if len1 > 30:
                #     R_tot_old = R_tot
#print the results of calculation steps
        # print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        # print("Results of calculation of HTC (\u03B1) at each step:")
        # print(alpha1_reg)
        # print(alpha2_reg)
        # print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
#print final messages
#side 1
        print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
        print("[Side 1]")
        text_side_1_1 = "At side 1 of the boundary, a correlation developed by " + corr_label_1 + ", \
for considered case of " + bnd_ori_1.get() + " of " + tank_type_1.get() + \
mess1_1 + ", is: " + mess2_1 + ""
        text_side_1_2 = "At " + str(MMImath.rn_sig(dT_fb1, acc, 0)) + " K temperature difference \
between fluid and the boundary, the characteristic numbers are: Reynolds: " + str(MMImath.rn_sig(Re1, acc, 1))\
+ "; Rayleigh: " + str(MMImath.rn_sig(Ra1, acc, 1)) + "; Prandtl: " + str(MMImath.rn_sig(Pr1, acc, 0)) + "."
        print(text_side_1_1)
        print(text_side_1_2)
        print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
#side 2
        print("[Side 2]")
        text_side_2_1 = "At side 1 of the boundary, a correlation developed by " + corr_label_2 + ", \
for considered case of ''" + bnd_ori_2 + " of " + tank_type_2.get() + \
mess1_2 + ", is: " + mess2_2 + ""
        text_side_2_2 = "At " + str(MMImath.rn_sig(dT_fb2, acc, 0)) + " K temperature difference \
between fluid and the boundary, the characteristic numbers are: Reynolds: " + str(MMImath.rn_sig(Re2, acc, 1)) \
+ "; Rayleigh: " + str(MMImath.rn_sig(Ra2, acc, 1)) + "; Prandtl: " + str(MMImath.rn_sig(Pr2, acc, 0)) + "."
        print(text_side_2_1)
        print(text_side_2_2)
        print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")

#construct "Results" section
#clean
        for widget in errors_frame.winfo_children():
            widget.destroy()
#section 0

#section 5
        spc = "              "
        Label(r, text='Results').grid(row=60, column=0, columnspan=4)
        Label(r, text='Side 1').grid(row=62, column=1, sticky="w", columnspan=3)
        Label(r, text='Side 2').grid(row=62, column=2, sticky="w", columnspan=3)
        #
        Label(r, text='Reynolds number (Re):').grid(row=63, column=0, sticky=E)
        Label(r, text=str(MMImath.rn_sig(Re1, acc, 1))+spc).grid(row=63, column=1, sticky=W)
        Label(r, text=str(MMImath.rn_sig(Re2, acc, 1))+spc).grid(row=63, column=2, sticky=W)
        #
        Label(r, text='Rayleigh number (Ra):').grid(row=64, column=0, sticky=E)
        Label(r, text=str(MMImath.rn_sig(Ra1, acc, 1))+spc).grid(row=64, column=1, sticky=W)
        Label(r, text=str(MMImath.rn_sig(Ra2, acc, 1))+spc).grid(row=64, column=2, sticky=W)
        #
        Label(r, text='Prandtl number (Pr):').grid(row=65, column=0, sticky=E)
        Label(r, text=str(MMImath.rn_sig(Pr1, acc, 0))+spc).grid(row=65, column=1, sticky=W)
        Label(r, text=str(MMImath.rn_sig(Pr2, acc, 0))+spc).grid(row=65, column=2, sticky=W)
        #
        Label(r, text='Nusselt number (Nu):').grid(row=66, column=0, sticky=E)
        Label(r, text=str(MMImath.rn_sig(Nu1, acc, 0))+spc).grid(row=66, column=1, sticky=W)
        Label(r, text=str(MMImath.rn_sig(Nu2, acc, 0))+spc).grid(row=66, column=2, sticky=W)
        #
        Label(r, text='Convective HTC (\u03B1):', font="-weight bold").grid(row=67, column=0, sticky=E)
        Label(r, text=str(MMImath.rn_sig(alpha1, acc, 0)) + ' W/m2K'+spc, font="-weight bold").grid(row=67, column=1, sticky=W)
        Label(r, text=str(MMImath.rn_sig(alpha2, acc, 0)) + ' W/m2K'+spc, font="-weight bold").grid(row=67, column=2, sticky=W)
        #
        Label(r, text='Total HTC (k):').grid(row=71, column=0, sticky=E)
        Label(r, text=str(MMImath.rn_sig(1/R_tot, acc, 0)) + ' W/m2K'+spc).grid(row=71, column=1, sticky=W)
        #
        Label(r, text='Heat transfer rate (Q\u0307):').grid(row=72, column=0, sticky=E)
        Label(r, text=str(MMImath.rn_sig(Q1/1000, acc, 0)) + ' kW'+spc).grid(row=72, column=1, sticky=W)
        #
        ttk.Separator(r, orient='horizontal').grid(row=61, sticky="ew", columnspan=3)
        ttk.Separator(r, orient='vertical').grid(row=61, column=3, sticky="nsw", rowspan=20)
        ttk.Separator(r, orient='vertical').grid(row=61, column=2, sticky="nsw", rowspan=10)
        ttk.Separator(r, orient='vertical').grid(row=61, column=1, sticky="nsw", rowspan=20)
        ttk.Separator(r, orient='horizontal').grid(row=70, sticky="ew", columnspan=3)
        tk.Frame(r, bg="grey", height=2, bd=0).grid(row=80, sticky="ew", columnspan=4)
        #
        Fin_message1 = Text(r, wrap=WORD, height=10, width=50)
        Fin_message1.insert(END, "DETAILS OF THE CALCULATION" + "\n" + "\n")
        Fin_message1.insert(END, "[Side 1]" + "\n" + "\n")
        Fin_message1.insert(END, text_side_1_1 + "\n")
        Fin_message1.insert(END, text_side_1_2 + "\n" + "\n")
        Fin_message1.insert(END, "[Side 2]" + "\n" + "\n")
        Fin_message1.insert(END, text_side_2_1 + "\n")
        Fin_message1.insert(END, text_side_2_2 + "\n")
        Fin_message1.grid(row=90, column=0, sticky="ew", columnspan=4)
        Fin_message1.configure(state='disabled')


#name inputs in the main program window
lab1 = 'Ship parameters'
lab11 = 'Amplitude of roll/pitch:'
lab12 = 'Period of roll/pitch'
lab13 = 'Ship length'
lab14 = 'Ship speed'
#
lab2 = 'Boundary parameters'
lab21 = 'Boundary function'
lab22 = 'Dimension A'
lab23 = 'Dimension B'
lab24 = 'Distance from COG (D)'
#
lab3 = 'Fluid parameters'
lab31 = 'Volume type'
lab32 = 'Fluid type'
lab33 = 'Temperature'

################################## [DISCLAIMER]
# pop-up scrollable toplevel window
def disclaimer():
#define default width
    wth = r.winfo_screenwidth()/1.5
#build help window
    help_window = tk.Toplevel(r)
    help_window.title('Disclaimer')
    help_window.resizable(False, False)
# scrollable canvas
    help_canvas = tk.Canvas(help_window, width=wth, height=wth/2)
    scroll_y = tk.Scrollbar(help_window, orient="vertical", command=help_canvas.yview)
#frame to be put into canves
    help_frame = tk.Frame(help_canvas)
# CONTENT ####################
    help0 = '\
Convective heat transfer calculator for ship tanks by Mateusz Mielcarek \n\
Last updated: November 15, 2021 \n\
[Interpretation and Definitions] \n\
The words of which the initial letter is capitalized have meanings defined under the following conditions. The following definitions shall have the same meaning regardless of whether they appear in singular or in plural. \n\
Definitions:\n\
For the purposes of this Disclaimer:\n\
Author (referred to as either "the Author", "We", "Us" or "Our" in this Disclaimer) refers to Ship Tank HTC.\n\
You means the individual accessing the Application Program, or the company, or other legal entity on behalf of which such individual is accessing or using the Application Program, as applicable.\n\
Application means the software program provided by the Author downloaded by You on any electronic device named Ship Tank HTC. \n\
[Disclaimer] \n\
The information contained in the Application Program is provided for free and for general information purposes only. \n\
The Author assumes no responsibility for errors or omissions in the contents of the Application Program. \n\
In no event shall the Author be liable for any special, direct, \
indirect, consequential, or incidental damages or any damages whatsoever, whether in an action of contract, negligence or \
other tort, arising out of or in connection with the use of the Application Program or the contents of the Application Program. The Author reserves \
the right to make additions, deletions, or modifications to the contents in the Application Program at any time without prior notice. This \
Disclaimer has been created with the help of the Disclaimer Generator. \n\
The Author does not warrant that the Application Program is free of viruses or other harmful components. \n\
[External Links Disclaimer] \n\
The Application Program may contain links to external websites that are not provided or maintained by or in any way affiliated with the Author. \n\
Please note that the Author does not guarantee the accuracy, relevance, timeliness, or completeness of any information on these external websites. \n\
[Errors and Omissions Disclaimer] \n\
The information given by the Application Program is for general guidance on matters of interest only. Even if the Author takes every precaution \
to insure that the content of the Application Program is both current and accurate, errors can occur. Plus, given the changing nature of laws, \
rules and regulations, there may be delays, omissions or inaccuracies in the information contained in the Application Program. \n\
The Author is not responsible for any errors or omissions, or for the results obtained from the use of this information. \n\
[Fair Use Disclaimer] \n\
The Author may use copyrighted material which has not always been specifically authorized by the copyright owner. The Author \
is making such material available for criticism, comment, news reporting, teaching, scholarship, or research. \n\
The Author believes this constitutes a "fair use" [PL na zasadach dozwolonego użytku] of any such copyrighted material as provided for in \
Polish Copyright law. \n\
If You wish to use copyrighted material from the Application Program for your own purposes that go beyond fair use, You must obtain permission \
from the copyright owner. \n\
[No Responsibility Disclaimer] \n\
The information in the Application Program is provided with the understanding that the Author is not herein engaged in rendering legal, accounting, \
tax, or other professional advice and services. As such, it should not be used as a substitute for consultation with professional \
accounting, tax, legal or other competent advisers. \n\
In no event shall the Author or its suppliers be liable for any special, incidental, indirect, or consequential damages whatsoever \
arising out of or in connection with your access or use or inability to access or use the Application Program. \n\
["Use at Your Own Risk" Disclaimer] \n\
All information in the Application Program is provided "as is", with no guarantee of completeness, accuracy, timeliness or of the results obtained \
from the use of this information, and without warranty of any kind, express or implied, including, but not limited to warranties of \
performance, merchantability and fitness for a particular purpose. \n\
The Author will not be liable to You or anyone else for any decision made or action taken in reliance on the information given by the \
Application Program or for any consequential, special or similar damages, even if advised of the possibility of such damages. \n\
[Contact Us] \n\
If you have any questions, You can contact Us by email: matmielcarek@gmail.com'
# END OF CONTENT ####################
    Label(help_frame, text=help0, wraplength=int(wth), justify=LEFT).grid(row=3, column=0)
    #
    ttk.Separator(help_frame, orient='horizontal').grid(row=90, sticky="ew")
    bt_exit = tk.Button(help_frame, text='Consent', width=7, command=help_window.destroy)
    bt_exit.grid(row=91, column=0, sticky="e") # Exit
# END OF CONTENT
# put the frame in the canvas
    help_canvas.create_window(0, 0, anchor='nw', window=help_frame)
# make sure everything is displayed before configuring the scrollregion
    help_canvas.update_idletasks()

    help_canvas.configure(scrollregion=help_canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)

    help_canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
################################## [END OF DISCLAIMER]

################################## [HELP]
# pop-up scrollable toplevel window
def help_me():
#define default width
    wth = r.winfo_screenwidth()/1.5
#build help window
    help_window = tk.Toplevel(r)
    help_window.title('Help')
    help_window.resizable(False, False)
# scrollable canvas
    help_canvas = tk.Canvas(help_window, width=wth, height=wth/2)
    scroll_y = tk.Scrollbar(help_window, orient="vertical", command=help_canvas.yview)
#frame to be put into canves
    help_frame = tk.Frame(help_canvas)
# CONTENT
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
    help2 = "\
[" + lab21 + "] determines if the calculated boundary is a bottom, a wall or a top of the tank. Note that currently only \
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
[" + lab31 + "] defines type of environment to be calculated at each side of the boundary. Different tank arrangements, i.e. different \
tank fill level or fluid motion characteristics will lead to different intensity of convection.\n\
-> <" + tanks[0] + "> is a situation where liquid level is up to the top of tank - tank completely filled\n\
-> <" + tanks[1] + "> is a situation where tank is filled with liquid up to a certain level\n\
-> <" + tanks[2] + "> is a situation where at considered side of the boundary there is seawater flowing outside the hull\n\
-> <" + tanks[3] + "> is a situation where at considered side of the boundary there is ambient air\n\
-> <" + tanks[4] + "> is a situation where at considered side of the boundary there is a compartment where people have access\n\
-> <" + tanks[5] + "> is a situation where at considered side of the boundary there is a closed void - i.e. a cofferdam or normally closed compartment \n\
[" + lab32 + "] defines closes representative of the fluid stored in considered volume - list of fluid types or specific fluids will be developed further \n\
[" + lab33 + "] defines average temperature in considered volume"
    Label(help_frame, text=help3, wraplength=int(wth), justify=LEFT).grid(row=33, column=0)
    #
    ttk.Separator(help_frame, orient='horizontal').grid(row=90, sticky="ew")
    bt_exit = tk.Button(help_frame, text='Exit', width=7, command=help_window.destroy)
    bt_exit.grid(row=91, column=0, sticky="e") # Exit
# END OF CONTENT
# put the frame in the canvas
    help_canvas.create_window(0, 0, anchor='nw', window=help_frame)
# make sure everything is displayed before configuring the scrollregion
    help_canvas.update_idletasks()

    help_canvas.configure(scrollregion=help_canvas.bbox('all'),
                     yscrollcommand=scroll_y.set)

    help_canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
################################## [END OF HELP]

################################## [REFERENCES]
# pop-up scrollable toplevel window
def references():
#define default width
    wth = r.winfo_screenwidth()/1.5
#build help window
    help_window = tk.Toplevel(r)
    help_window.title('References')
    help_window.resizable(False, False)
# scrollable canvas
    help_canvas = tk.Canvas(help_window, width=wth, height=225)
    # scroll_y = tk.Scrollbar(help_window, orient="vertical", command=help_canvas.yview)
#frame to be put into canves
    help_frame = tk.Frame(help_canvas)
# CONTENT
    ref1 = "\
[1] DOERFFER, S. (1981) Zagadnienia wpływu oscylacji ośrodka płynnego na konwekcyjne przekazywanie ciepła w zastosowaniu \
do zbiorników okrętowych transportujących ciecze o dużych lepkościach [Issues of influence of oscillations of liquid on \
convective heat transfer, in application for ship tanks for transport of liquids of high viscosity]. PhD dissertation. Institute of \
Fluid-Flow Machinery Polish Academy of Sciences. \n\
[2] MIELCAREK, M. (2021) Konwekcyjna wymiana ciepła w zbiorniku statku poddanego wymuszeniom okresowym [Convective \
heat transfer in ship tank subjected to harmonic oscillations]. PhD dissertation. Institute of Fluid-Flow Machinery Polish Academy of Sciences. \n\
[3] INTERNATIONAL ORGANIZATION FOR STANDARDIZATION (2002) Ships and marine technology — Air-conditioning and ventilation of accommodation spaces — \
Design conditions and basis of calculations ISO 7547:2002 \n\
[4] MCADAMS, W.H. (1954) Heat Transmission. McGraw-Hill, New York."
    Label(help_frame, text=ref1, wraplength=int(wth), justify=LEFT).grid(row=0, column=0)
    #
    ttk.Separator(help_frame, orient='horizontal').grid(row=1, column=0, sticky="ew")
    bt_exit = tk.Button(help_frame, text='Exit', width=7, command=help_window.destroy)
    bt_exit.grid(row=2, column=0, sticky="e") # Exit
# END OF CONTENT
# put the frame in the canvas
    help_canvas.create_window(0, 0, anchor='nw', window=help_frame)
# make sure everything is displayed before configuring the scrollregion
    help_canvas.update_idletasks()

    # help_canvas.configure(scrollregion=help_canvas.bbox('all'),
    #                  yscrollcommand=scroll_y.set)

    # help_canvas.pack(fill='y', expand=False, side='left')
    help_canvas.grid(row=0, sticky="nsew")
    # scroll_y.pack(fill='y', side='right')
################################## [END OF REFERENCES]


################################## [locating widgets]
#bg='red'
#section 0
# r
# Label(r, text='3', bg='blue', font=("Courier", 5)).grid(row=0, column=3, sticky="we")
# Label(r, text='4', bg='red', font=("Courier", 5)).grid(row=0, column=3, sticky="we")
# Label(r, text='5', bg='blue', font=("Courier", 5)).grid(row=0, column=5, sticky="we")
# Label(r, text='6', bg='red', font=("Courier", 5)).grid(row=0, column=6, sticky="we")
# Label(r, text='7', bg='blue', font=("Courier", 5)).grid(row=0, column=7, sticky="we")

#section 1
tk.Frame(r, bg="grey", height=2, bd=0).grid(row=9, sticky="ew", columnspan=4)
Label(r, text=lab1).grid(row=10, column=0, columnspan=4)
#
ttk.Separator(r,orient='horizontal').grid(row=11, sticky="ew", columnspan=4)
#
Label(r, text=lab11).grid(row=12, column=0, sticky=E)
f11 = Frame(r)
f11.grid(row=12, column=1, sticky=W, padx=3)
em1 = Entry(f11, textvariable=ship_ang, width=3, justify='right')
em1.pack(side="left", fill=None, expand=False)
Label(f11, text=deg, anchor='w').pack(side="left", fill=None, expand=False)
#
Label(r, text=lab12).grid(row=13, column=0, sticky=E)
f12 = Frame(r)
f12.grid(row=13, column=1, sticky=W, padx=3)
em2 = Entry(f12, textvariable=ship_per, width=3, justify='right')
em2.pack(side="left", fill=None, expand=False)
Label(f12, text="s", anchor='w').pack(side="left", fill=None, expand=False)
#
f13n = Frame(r)
f13n.grid(row=12, column=2, columnspan=2, sticky=W)
Label(f13n, text=lab13).grid(row=0, column=0, sticky=E)
f13 = Frame(f13n)
f13.grid(row=0, column=1, sticky=W, padx=3)
em3 = Entry(f13, textvariable=ship_len, width=3, justify='right')
em3.pack(side="left", fill=None, expand=False)
Label(f13, text="m", anchor='w').pack(side="left", fill=None, expand=False)
#
f14n = Frame(r)
f14n.grid(row=13, column=2, columnspan=2, sticky=W)
Label(f14n, text=lab14).grid(row=0, column=0, sticky=E)
f14 = Frame(f14n)
f14.grid(row=0, column=1, sticky=W, padx=3)
em4 = Entry(f14, textvariable=ship_vel, width=3, justify='right')
em4.pack(side="left", fill=None, expand=False)
Label(f14, text="knot", anchor='w').pack(side="left", fill=None, expand=False)
#
tk.Frame(r, bg="grey", height=2, bd=0).grid(row=14, sticky="ew", columnspan=4)
# ttk.Separator(r,orient='horizontal', style="Line.TSeparator").grid(row=14, sticky="ew", columnspan=4)

#section 2
Label(r, text=lab2).grid(row=20, column=0, columnspan=4)
#
ttk.Separator(r,orient='horizontal').grid(row=21, sticky="ew", columnspan=4)
#
Label(r, text=lab21).grid(row=22, column=0, sticky=E)
opt1 = OptionMenu(r, bnd_ori_1, *bnds) #command=isVert
opt1.configure(width=15)
opt1.grid(row=22, column=1, sticky=W, padx=5)
#
f21n = Frame(r)
f21n.grid(row=22, column=2, columnspan=2, sticky=W)
Label(f21n, text=lab22).grid(row=0, column=0, sticky=E)
f21 = Frame(f21n)
f21.grid(row=0, column=1, sticky=W, padx=3)
e1 = Entry(f21, textvariable=dim1, width=3, justify='right')
e1.pack(side="left", fill=None, expand=False)
Label(f21, text="m", anchor='w').pack(side="left", fill=None, expand=False)
#
f22n = Frame(r)
f22n.grid(row=23, column=2, sticky=W)
Label(f22n, text=lab23).grid(row=0, column=0, sticky=E)
f22 = Frame(f22n)
f22.grid(row=0, column=1, sticky=W, padx=3)
e2 = Entry(f22, textvariable=dim2, width=3, justify='right')
e2.pack(side="left", fill=None, expand=False)
Label(f22, text="m", anchor='w').pack(side="left", fill=None, expand=False)
#
Label(r, text=lab24).grid(row=23, column=0, sticky=E)
f23 = Frame(r)
f23.grid(row=23, column=1, sticky=W, padx=3)
e4 = Entry(f23, textvariable=dist, width=3, justify='right')
e4.pack(side="left", fill=None, expand=False)
Label(f23, text="m", anchor='w').pack(side="left", fill=None, expand=False)
#
tk.Frame(r, bg="grey", height=2, bd=0).grid(row=24, sticky="ew", columnspan=4)
#
#section 3
Label(r, text=lab3).grid(row=30, column=0, columnspan=4)
#
ttk.Separator(r,orient='horizontal').grid(row=31, sticky="ew", columnspan=4)
#
Label(r, text='Side 1').grid(row=32, column=1, sticky="w")
Label(r, text='Side 2').grid(row=32, column=2, sticky="w")
#
Label(r, text=lab31).grid(row=33, column=0, sticky=E)
Label(r, text=lab32).grid(row=34, column=0, sticky=E)
Label(r, text=lab33).grid(row=35, column=0, sticky=E)
#
opt2 = OptionMenu(r, fluid1, *fluids1, command=checkTanks)
opt2.configure(width=7)
opt2.grid(row=34, column=1, sticky=W, padx=5)
#
# Label(r, text='Volume type:').grid(row=33, column=3, sticky=E)
opt3 = OptionMenu(r, fluid2, *fluids2, command=checkTanks)
opt3.configure(width=7)
opt3.grid(row=34, column=2, sticky=W, padx=5)
#

opt4 = OptionMenu(r, tank_type_1, *tanks, command=checkFluids)
opt4.grid(row=33, column=1, sticky=W, padx=5)
opt4.configure(width=15)
#
# Label(r, text='Fluid type:').grid(row=34, column=3, sticky=E)
opt5 = OptionMenu(r, tank_type_2, *tanks, command=checkFluids)
opt5.grid(row=33, column=2, sticky=W, padx=5)
opt5.configure(width=15)
#
f31 = Frame(r)
f31.grid(row=35, column=1, sticky=W, padx=3)
et1 = Entry(f31, textvariable=ftemp1, width=3, justify='right')
et1.pack(side="left", fill=None, expand=False)
Label(f31, text=deg + "C", anchor='w').pack(side="left", fill=None, expand=False)
#
# Label(r, text='Temperature:').grid(row=35, column=3, sticky=E)
f32 = Frame(r)
f32.grid(row=35, column=2, sticky=W, padx=3)
et2 = Entry(f32, textvariable=ftemp2, width=3, justify='right')
et2.pack(side="left", fill=None, expand=False)
Label(f32, text=deg + "C", anchor='w').pack(side="left", fill=None, expand=False)
#
# ttk.Separator(r, orient='vertical').grid(row=31, column=3, sticky="nsw", rowspan=9)
ttk.Separator(r, orient='vertical').grid(row=31, column=1, sticky="nsw", rowspan=7)
ttk.Separator(r, orient='vertical').grid(row=31, column=2, sticky="nsw", rowspan=7)
tk.Frame(r, bg="grey", height=2, bd=0).grid(row=36, sticky="ew", columnspan=4)

#section 5
buttons_frame.grid(row=38, sticky="ew", columnspan=4, pady=(0,4))
# buttons_frame.columnconfigure(0, weight=1)
bt_exit = tk.Button(buttons_frame, text='Exit', width=7, command=r.destroy)
bt_calc = tk.Button(buttons_frame, text='Calculate', width=14, command=calc_bnd)
bt_ref = tk.Button(buttons_frame, text='References', width=7, command=references)
bt_dis = tk.Button(buttons_frame, text='Disclaimer', width=7, command=disclaimer)
bt_help = tk.Button(buttons_frame, text='Help', width=7, command=help_me)
bt_exit.pack(side="right", fill=None, expand=False) #Exit
bt_ref.pack(side="right", fill=None, expand=False) #References
bt_dis.pack(side="right", fill=None, expand=False) #Disclaimer
bt_help.pack(side="right", fill=None, expand=False) #Help
bt_calc.pack(side="left", fill=None, expand=False) #Calculate
tk.Frame(r, bg="grey", height=2, bd=0).grid(row=39, sticky="ew", columnspan=4)

################################## [main loop]
r.mainloop()