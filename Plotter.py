import pandas as pd
import numpy as np
import aux
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as fnt
import CoolProp.CoolProp as CP
import MMImath
import matplotlib.pyplot as plt
import math


################################## [PLOTTER]

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

def sel_Pr_exp(bnd_ori_in,corr_name_in):
    col = 0
    if corr_name_in == "db/exp_mielcarek.csv" and bnd_ori_in == bnds[0]:
        col = 1
    return col

def calc_nuss(Re_in,Ra_in,Pr_in,Sr_in,Fr_in,lam_in,L1_in,corr_name_in,bnd_ori_in):
#read an appropiate array of criteria values and exponent values based on selected correlation
    corr_array = pd.read_csv(corr_name_in)
    col = sel_Pr_exp(bnd_ori_in,corr_name_in)
    L1_model = 0.4
    Re_in_e = Re_in * (L1_model / L1_in) ** 2
    Ra_in_e = Ra_in * (L1_model / L1_in) ** 3
    # Re_in_e = Re_in
    # Ra_in_e = Ra_in
    if Re_in != 0:
        Crit = eval(corr_array.iat[0, col])
    else:
        Crit = 0
    for i, b in enumerate(bnds):
        if bnd_ori_in == b:
        #for stationary cases (Re = 0)
            if Crit == 0:
                j = 1
            # construct an array of applicable ranges of subsequent characteristic numbers
                Rn = list()
                Rn_chk = list()
                for f in range(6):
                    Rn.append(float(corr_array.iat[i * 4 + j, f + 9]))
            # collect characteristic numbers, converted by the scale, in an array
                Num = [Re_in_e, Ra_in_e, Pr_in]
            # check applicability range (Reynolds number, Rayleigh number Prandtl number)
                for s in range(3):
                    if Rn[s * 2] < Num[s] < Rn[s * 2 + 1]:
                        Rn_chk.append(True)
                    else:
                        Rn_chk.append(False)
        #construct the array of exponents applicable for selected type of convection
                C = list()
                for k in range(6):
                    C.append(float(corr_array.iat[i * 4 + j, k + 3]))
                Nuss = C[0] * (Ra_in ** C[2]) * (Pr_in ** C[3])
                conv = "free"
        #for dynamic cases (Re > 0)
            else:
                for j in range(2,5):
                    if float(corr_array.iat[i*4+j, 0]) <= Crit < float(corr_array.iat[i*4+j, 1]):
                        j_check = j
                    # construct an array of applicable ranges of subsequent characteristic numbers
                        Rn = list()
                        Rn_chk = list()
                        for f in range(6):
                            Rn.append(float(corr_array.iat[i * 4 + j, f + 9]))
                    # collect characteristic numbers, converted by the scale, in an array
                        L1_model = 0.4
                        Num = [Re_in_e, Ra_in_e, Pr_in]
                    # check applicability range (Reynolds number, Rayleigh number Prandtl number)
                        for s in range(3):
                            if Rn[s * 2] < Num[s] < Rn[s * 2 + 1]:
                                Rn_chk.append(True)
                            else:
                                Rn_chk.append(False)
        #construct the array of exponents applicable for selected type of convection
                        C = list()
                        for k in range(6):
                            C.append(float(corr_array.iat[i*4+j, k+3]))
                        # print(C)
        #calculate Nusselt number based on correlation parameters in exp_mielcarek.csv
                        Nuss = C[0]*(Re_in**C[1])*(Ra_in**C[2])*(Pr_in**C[3])*(Sr_in**C[4])*(Fr_in**C[5])
                        conv = str(corr_array.iat[i*4+j, 2])
            alpha = Nuss * lam_in / L1_in
    return [Nuss,alpha,Rn_chk,conv,Crit,j_check]


#tuples
bnds = ("horizontal tank bottom", "vertical tank wall", "horizontal tank top")

#inputs - constants
g=9.81
acc = 0.0001
pi = 3.14
bnd_ori = bnds[1]
corr_name = "db/exp_mielcarek.csv"
# corr_name = "db/exp_doerffer.csv"
# fluid = "water"
fluid = "water"
# #inputs - quasi constants
ftemp = 50
ftempK = ftemp + 273.15
L1_m = 0.3
L1 = 10
L2 = 5
#inputs - variables
dT = 10
ang = 10
per = 10

# inputs calculated
T_film = ftempK + dT/2
props = draw_props(T_film, fluid)
lam = props[4]
nu = props[3]
Pr = props[1] * props[2] / lam
Sr = L1 / ang / L2
Fr = ang * per * L2 / ((g * L1)**0.5)

eps = L1_m/L1

nu_m1 = draw_props(T_film, "water")[3]
nu_m2 = nu * (eps ** (3/2))

print("e is: " + str(eps) + "; e^(3/2) is: " + str(eps ** (3/2)) + "; nu should be: " + str(MMImath.rn_sig(nu_m1,0.01,0)) + " and it is: " + str(MMImath.rn_sig(nu_m2,0.01,0)))

# Sr = 1
# Fr = 1
# Gr = abs(beta * dT * g * (L1_in ** 3) / (nu ** 2))
# print(Pr)

############## ACTUAL L's AND  Ra Re RANGES
# MMImath.rn_sig(Ra_ls, acc, 1)
# return [rho, Cp, mu, nu, lam, beta]
# make an array of Rayleigh numbers based on range of temperatures and dimensions
# dT = [1,50]
# L1 = [1,10]
# L1_steps = 5
# L1_step = (L1[1]-L1[0])/(L1_steps-1)
# print(L1_step)
# L1_ls = list()
# L1_ls.append(L1[0])
# for i in range(L1_steps-1):
#     L1_ls.append(1+(i+1)*L1_step)
# print(L1_ls)
# per = 10
# ang = [1,10]
# ang_per = [(ang[0] * pi / 180)/per,(ang[1] * pi / 180)/per]
#
# Ra = list()
# Re = list()
# lam = list()
# for k in range(2):
#     T_film = ftempK + dT[k] / 2
#     props = draw_props(T_film, fluid)
# #
#     Gr = abs(props[5] * dT[k] * g * (1 ** 3) / (props[3] ** 2)) #1 zamiast L1 - jednostkowy wymiar
#     Pr = props[1] * props[2] / props[4]
#     Ra.append(Gr*Pr)
# #
#     Re.append(ang_per[k] * (1 ** 2) / props[3])
# #
#     lam.append(props[4])
# # L1 = [1,10]
# # Ra_min = math.floor(math.log(Ra[0], 10))
# # Ra_max = math.ceil(math.log(Ra[0], 10))
#
# Ra_steps = 30
# # Ra_min = Ra[0]
# # Ra_max = Ra[1]
# #
# Re_steps = 3
# # Re_min = Re[0]
# # Re_max = Re[1]
#
# lam = [lam[0], (lam[0]+lam[1]) / 2,lam[1]]
#
# #ZROBIC Z TEGO TABLICE 3 wartosci
#
# # Ra_n = 3
# Ra_arr0 = list()
# Re_arr0 = list()
# Nu_arr0 = list()
# ax = plt.subplot(111)
# # for each case of fixed L1 value (which affects both Ra and Re)
# for i, a in enumerate(L1_ls):
# # calculate min and max value of Ra and Re
#     Ra_min = Ra[0] * (a ** 3)
#     Ra_max = Ra[1] * (a ** 3)
#     Re_min = Re[0] * (a ** 2)
#     Re_max = Re[1] * (a ** 2)
#     Ra_min_e = math.floor(math.log(Ra_min, 10))
#     Ra_max_e = math.ceil(math.log(Ra_max, 10))
# # make a list of Ra for each case of Re and for each case of fixed L1 value
#     Re_arr1 = list()
#     Ra_arr1 = list()
#     Nu_arr1 = list()
#     for j in np.linspace(Re_min,Re_max,num=(Re_steps), endpoint=True):
#         Ra_arr2 = list()
#         Nu_arr2 = list()
#         cCbJ_old = 0
#         for k in np.logspace(Ra_min_e,Ra_max_e,num=(Ra_steps), endpoint=True):
#             arr = calc_nuss(j, k, Pr, Sr, Fr, lam[0], a, corr_name, bnd_ori)  # Prandtl jest jeden i lam też!!
# # check for incontinuities reported from "calc_nuss" and add nan where existent
#             if arr[5] != cCbJ_old:
#                 Ra_arr2.append(np.nan)
#                 Nu_arr2.append(np.nan)
#                 cCbJ_old = arr[5]
# # append to 2-level list
#             Ra_arr2.append(k)
#             Nu_arr2.append(arr[0])
# # append to 1-level list
#         Re_arr1.append(j)
#         Ra_arr1.append(Ra_arr2)
#         Nu_arr1.append(Nu_arr2)
#         plt.plot(Ra_arr2, Nu_arr2,
#                  label="L: " + str(a) + "m; Re: " + str(MMImath.rn_sig(j, 0.1, 1)))
# # append to 0-level list
#     Re_arr0.append(Re_arr1)
#     Ra_arr0.append(Ra_arr1)
#     Nu_arr0.append(Nu_arr1)
# print(Re_arr0[0][0])
# print(Ra_arr0[0][0])
# print(Nu_arr0[0]0[0])

Ra_min = 9
Ra_max = 15

Re_min = 4
Re_max = 7

Ra_n = 20
Re_n = 3

# make an array of Rayleigh numbers
Ra_ls = list()
for i in np.logspace(Ra_min,Ra_max,num=(Ra_max-Ra_min)*Ra_n, endpoint=True):
    Ra_ls.append(i)
print(Ra_ls)

# make an array of Reynolds numbers


Re_ls = list()
for i in np.logspace(Re_min,Re_max,num=(Re_max-Re_min)*Re_n, endpoint=True):
    Re_ls.append(i)
print(Re_ls)

# make an array of results by Rayleigh
Nu_ls_Ra = list()
Ra_ls_ls = list()
# conv_Ra = list()
# Crit_Ra = list()
for j in range(len(Re_ls)):
#initiate lists
    lsty = list()
    lstx = list()
    cCbJ_old = 0
    i_rec = 0
#go through lists of Ra and Re and calculate nusselt for each set of values
    for i in range(len(Ra_ls)):
        arr = calc_nuss(Re_ls[j], Ra_ls[i], Pr, Sr, Fr, lam, L1, corr_name, bnd_ori)  # Prandtl jes jeden!!
        if arr[5] != cCbJ_old:
            lsty.append(np.nan)
            lstx.append(np.nan)
            # if cCbJ_old == 0:
            #     i_rec = 0
            # else:
            #     i_Rec = i
            cCbJ_old = arr[5]
        lsty.append(arr[0])
        lstx.append(Ra_ls[i])
        # print(cCbJ_old,arr[5])
    # print(len(lstx),len(lsty))
    # print(lstx)
    # print(lsty)
#add to matrix
    Nu_ls_Ra.append(lsty)
    Ra_ls_ls.append(lstx)
print(Nu_ls_Ra)
print(Ra_ls_ls)
# print(Crit_Ra)
ax = plt.subplot(111)
for k in range(len(Re_ls)):
    plt.plot(Ra_ls_ls[k], Nu_ls_Ra[k], label="Re: " + str(MMImath.rn_sig(Re_ls[k],0.1,1)))
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Rayleigh number")
plt.ylabel("Nusselt number")
# Shrink current axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.legend(title="Reynolds number:",loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()


# Ra_n = 1
# Re_n = 30
#
# # make an array of Rayleigh numbers
# Ra_ls = list()
# for i in np.logspace(Ra_min,Ra_max,num=(Ra_max-Ra_min)*Ra_n, endpoint=True):
#     Ra_ls.append(i)
# print(Ra_ls)
#
# # make an array of Reynolds numbers
# Re_ls = list()
# for i in np.logspace(Re_min,Re_max,num=(Re_max-Re_min)*Re_n, endpoint=True):
#     Re_ls.append(i)
# print(Re_ls)
#
# # make an array of results by Reynolds
# Nu_ls_Re = list()
# Re_ls_ls = list()
# # conv_Ra = list()
# # Crit_Ra = list()
# for j in range(len(Ra_ls)):
# #initiate lists
#     lsty = list()
#     lstx = list()
#     cCbJ_old = 0
#     i_rec = 0
# #go through lists of Ra and Re and calculate nusselt for each set of values
#     for i in range(len(Re_ls)):
#         # arr = calc_nuss(Re_ls[(j-1)*3+i],Ra_ls[(j-1)*3+i],Pr,Sr,Fr,lam,L1,corr_name,bnd_ori) #Prandtl jes jeden!!
#         arr = calc_nuss(Re_ls[i], Ra_ls[j], Pr, Sr, Fr, lam, L1, corr_name, bnd_ori)  # Prandtl jes jeden!!
#         if arr[5] != cCbJ_old:
#             lsty.append(np.nan)
#             lstx.append(np.nan)
#             # if cCbJ_old == 0:
#             #     i_rec = 0
#             # else:
#             #     i_Rec = i
#             cCbJ_old = arr[5]
#         lsty.append(arr[0])
#         lstx.append(Re_ls[i])
#         # print(cCbJ_old,arr[5])
#     # print(len(lstx),len(lsty))
#     # print(lstx)
#     # print(lsty)
# #add to matrix
#     Nu_ls_Re.append(lsty)
#     Re_ls_ls.append(lstx)
# print(Nu_ls_Re)
# print(Re_ls_ls)
# # print(Crit_Ra)
# ax = plt.subplot(111)
# for k in range(len(Ra_ls)):
#     plt.plot(Re_ls_ls[k], Nu_ls_Re[k], label="Ra: " + str(MMImath.rn_sig(Ra_ls[k],0.1,1)))
# plt.xscale('log')
# plt.yscale('log')
# plt.xlabel("Reynolds number")
# plt.ylabel("Nusselt number")
# # Shrink current axis by 20%
# box = ax.get_position()
# ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
# ax.legend(title="Rayleigh number:",loc='center left', bbox_to_anchor=(1, 0.5))
# plt.show()



