import tkinter as tk
import CoolProp.CoolProp as CP
################################## [defining symbols]
deg = u"\N{DEGREE SIGN}"
#check if entered string is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#set text to entry by code
def set_text(ent,text):
    ent.delete(0,tk.END)
    ent.insert(0,text)
    return

#CoolProp check temperature range
def Trange(fluid_CP):
    if fluid_CP == "water":
        Tmin = 0
        Tmax = 100
    else:
        Tmax = CP.PropsSI('TMAX', 'P', 101325, 'Q', 0, fluid_CP)-273.15
        Tmin = CP.PropsSI('TMIN', 'P', 101325, 'Q', 0, fluid_CP)-273.15
    return [Tmin,Tmax]

#check anyv numeric value if number and if in allowed limits
def checkNumVal(val,lim):
    num = val.get()
    if is_number(num):
        num = float(num)
        if lim[0] <= num <= lim[1]:
            return [num, "OK"]
        else:
            return ["NaN","range"]
            # return ["NaN", "Given value is outside allowed range: " + str(lim[0]) + "-" + str(lim[1])]
    else:
        return ["NaN","NaN"]
        # return ["NaN", "Given input is not numeric."]
