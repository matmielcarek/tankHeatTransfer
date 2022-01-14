################################## [defining number of significant digits based on relative error] !TO BE CHECKED!
import math
def sig_dig (rel): #give number of significant digits based on relative error
    if rel == 0:
        rn = 1
    else:
        rn = math.floor(-math.log(rel/0.5, 10))
    return rn

def sig (num, rel, sci): #give number of places after the comma to display based on number of significant digits and info if scientific notation
    if isinstance(num, str) or num == 0 or str(num) == "nan":
        rn = 0
    else:
        if sci == True:
            exp = math.floor(math.log(num, 10))
            rn = sig_dig(rel) - exp + 2 + exp #before reconsideration of sigfig rounding
            #rn = exp + 1 - sig_dig(rel) + exp
        else:
            exp = math.floor(math.log(num, 10))
            rn = sig_dig(rel) - exp + 2 #before reconsideration of sigfig rounding
            #rn = exp + 1 - sig_dig(rel)
    return rn

def fig_rn(num,fig,sci): #write number in correct format
    if isinstance(num, str) or num == 0 or num == float("nan") or num == "nan":
        rn = 0
    else:
        num = round(num,fig)
        form = "f"
        if sci == True:
            form = "e"
        if fig < 1:
            rn = ('{:.0'+ form +'}').format(num)
        else:
            rn = ('{:.'+str(fig)+form+'}').format(num)
    return rn

def rn_err(num,rel,sci): #round error appropriately to given number and relative error
    if isinstance(num, str) or num == 0 or num == float("nan") or num == "nan":
        rn = 0
    else:
        a = math.floor(math.log(num, 10))
        b = math.floor(math.log(num*rel, 10))
        if sci == True:
            fig = sig(num, rel, sci) - (a-b)
        else:
            fig = sig(num, rel, sci)
        rn = fig_rn(num*rel, fig, sci)
    return rn

def rn_sig (num, rel, sci): #round number appropriately to given relative error
    if isinstance(num, str) or num == 0 or num == float("nan") or num == "nan":
        rn = 0
    else:
        fig = sig(num, rel, sci)
        rn = fig_rn(num, fig, sci)
    return rn

#SOMETHINGS WRONG WHEN SCI NOTATION SELECTED AND NUM IS E-

# num_test = 123445.23
# rel_test = 0.009
#
# print("raw number is: [" + str(num_test) + "+/-" + str(num_test*rel_test) + "]")
# print("relative error is: [" + str(rel_test*100) + "%]")
# print("count of significant figures, based on relative error is (sig_dig): [" + str(sig_dig(rel_test)) + "]")
# print("count of places to round number to, based on relative error is (sig): [" + str(sig(num_test,rel_test, 0)) + "]")
# print("properly rounded number is (rn_sig): [" + \
#       str(rn_sig(num_test, rel_test, 0)) + \
# #" +/- " + str(fig_rn(num_test*rel_test, sig(num_test,rel_test,0),0)) + \
# " +/- " + str(rn_err(num_test, rel_test,0)) + \
# "] [" + str(rn_sig(num_test, rel_test, 1)) + \
# #" +/- " + str(fig_rn(num_test*rel_test, sig(num_test,rel_test,1)-2,1)) + "]")
# " +/- " + str(rn_err(num_test, rel_test,1)) + "]")