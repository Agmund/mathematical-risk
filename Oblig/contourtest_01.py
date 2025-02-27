##########################################################
#                                                        #
#    Environmental contour testing                       #
#                                                        #
##########################################################

import numpy as np
import matplotlib.pyplot as plt
from c_contour import *
from util import setInnerRadiusFactor

#################################################
#     -- Environmental contour scenarios --     #
#################################################
nwAustraliaSwell    = Transformator("nwAustraliaSwell", 24, 0.450, 1.580, 0.132, 0.010, 2.543, 0.032, 0.137, 0.000, 0.000)
nwAustraliaTotalSea = Transformator("nwAustraliaTotalSea", 24, 0.606, 0.892, 0.452, 0.750, 1.150, 0.153, 0.061, 0.882, -1.023)
nwAustraliaWindSea  = Transformator("nwAustraliaWindSea", 24, 0.605, 0.867, 0.322, 0.000, 1.798, 0.134, 0.042, 0.224, -0.500)

wAfricaSwell        = Transformator("wAfricaSwell", 8, 0.709, 1.688, 0.297, 0.100, 2.146, 0.193, 0.035, 0.957, -1.053)

wShetlandSwell      = Transformator("wShetlandSwell", 8, 2.527, 1.460, 0.337, 1.069, 0.898, 0.243, 0.025, 0.263, -0.148)
wShetlandTotalSea   = Transformator("wShetlandTotalSea", 8, 2.259, 1.285, 0.701, 1.069, 0.898, 0.243, 0.025, 0.263, -0.148)
wShetlandWindSea    = Transformator("wShetlandWindSea", 8, 2.139, 1.176, 0.318, 0.005, 1.694, 0.186, 0.050, 0.191, -1.074)

###################################################
#  -- Alt. scenarios with lower sampling rate --  #
###################################################
nwAustraliaSwell_x     = Transformator("nwAustraliaSwell_x", 3, 0.450, 1.580, 0.132, 0.010, 2.543, 0.032, 0.137, 0.000, 0.000)
nwAustraliaTotalSea_x  = Transformator("nwAustraliaTotalSea_x", 3, 0.606, 0.892, 0.452, 0.750, 1.150, 0.153, 0.061, 0.882, -1.023)
nwAustraliaWindSea1_x  = Transformator("nwAustraliaWindSea_x", 3, 0.605, 0.867, 0.322, 0.000, 1.798, 0.134, 0.042, 0.224, -0.500)

wAfricaSwell1_x        = Transformator("wAfricaSwell_x", 1, 0.709, 1.688, 0.297, 0.100, 2.146, 0.193, 0.035, 0.957, -1.053)

wShetlandSwell_x       = Transformator("wShetlandSwell_x", 1, 2.527, 1.460, 0.337, 1.069, 0.898, 0.243, 0.025, 0.263, -0.148)
wShetlandTotalSea_x    = Transformator("wShetlandTotalSea_x", 1, 2.259, 1.285, 0.701, 1.069, 0.898, 0.243, 0.025, 0.263, -0.148)
wShetlandWindSea_x     = Transformator("wShetlandWindSea_x", 1, 2.139, 1.176, 0.318, 0.005, 1.694, 0.186, 0.050, 0.191, -1.074)



#################################################
#             -- Input settings --              #
#################################################
radiusFactor = 0.95         # <-------- Choose the radius factor (< 1) here
numSimulations = 25000      # <-------- Choose the number of simulations here
numTangents = 360           # <-------- Choose the number of tangents here
doStandardize = True        # <-------- Choose if the data should be standardized here
smoothWidth = 6             # <-------- Choose smoothness width here (0 = no smoothing)
returnPeriod = 10           # <-------- Choose the return period here (in years)
tr = wShetlandTotalSea      # <-------- Choose the environment contour scenario here

printMoments = False        # <-------- Choose if the moments should be printed out
printC = False              # <-------- Choose if the c-function should be printed out
printContour = False        # <-------- Choose if the contour points should be printed out
plotC = True               # <-------- Choose if c(theta) plot should be created
plotDC = True              # <-------- Choose if the c'(theta) plot should be created
plotDC2 = True             # <-------- Choose if the c''(theta) plot should be created
plotCDC2 = True            # <-------- Choose if the c(theta) + c''(theta) plot should be created
plotScatter = True         # <-------- Choose if a scatter plot should be created
plotContour = True          # <-------- Choose if a contour curve plot should be created
save_plots = True           # <-------- Choose if the plot(s) should be saved here


setInnerRadiusFactor(radiusFactor)    
setNumberOfSimulations(numSimulations)
setNumberOfTangents(numTangents)
setStandardize(doStandardize)
    

ec = Contour(tr, returnPeriod)
ec.runSimulation()
ec.estimateC()
ec.calculateContour()

if printMoments:
    print("")
    ec.printMoments()
    
if printC:
    print("")
    ec.printC()

if printContour:
    print("")
    ec.printContour()
    
if plotC:
    fig = plt.figure(figsize = (7, 5))
    a = np.zeros(numTangents)
    c = np.zeros(numTangents)
    for i in range(numTangents):
        a[i] = ec.getAngle(i)
        c[i] = ec.getC(i)
    plt.plot(a, c, label=tr.getName())
    plt.xlabel('theta')
    plt.ylabel('C(theta)')
    plt.title("The C-function")
    plt.legend()
    if save_plots:
        plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_c" + ".pdf")
    plt.show()    
    
if plotDC:
    fig = plt.figure(figsize = (7, 5))
    a = np.zeros(numTangents)
    dc = np.zeros(numTangents)
    for i in range(numTangents):
        a[i] = ec.getAngle(i)
        dc[i] = ec.getDC(i)
    plt.plot(a, dc, label=tr.getName())
    plt.xlabel('theta')
    plt.ylabel('DC(theta)')
    plt.title("The derivative of the C-function")
    plt.legend()
    if save_plots:
        plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_dc" + ".pdf")
    plt.show()    
    
if plotDC2:
    fig = plt.figure(figsize = (7, 5))
    a = np.zeros(numTangents)
    dc2 = np.zeros(numTangents)
    for i in range(numTangents):
        a[i] = ec.getAngle(i)
        dc2[i] = ec.getDC2(i)
    plt.plot(a, dc2, label=tr.getName())
    plt.xlabel('theta')
    plt.ylabel('DC2(theta)')
    plt.title("The second derivative of the C-function")
    plt.legend()
    if save_plots:
        plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_dc2" + ".pdf")
    plt.show()    
    
if plotCDC2:
    fig = plt.figure(figsize = (7, 5))
    a = np.zeros(numTangents)
    cdc2 = np.zeros(numTangents)
    for i in range(numTangents):
        a[i] = ec.getAngle(i)
        cdc2[i] = ec.getCDC2(i)
    plt.plot(a, cdc2, label=tr.getName())
    plt.xlabel('theta')
    plt.ylabel('CDC2(theta)')
    plt.title("The sum of the C-function and its second derivative")
    plt.legend()
    if save_plots:
        plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_cdc2" + ".pdf")
    plt.show()    
    
if plotScatter:
    t = np.zeros(numSimulations)
    h = np.zeros(numSimulations)
    for i in range(numSimulations):
        p = ec.getUnstandardizedPoint(i)
        t[i] = p[0]
        h[i] = p[1]
    fig = plt.figure(figsize = (7, 5))
    plt.scatter(t, h, c ="red", marker=".")
    plt.plot(ec.contour_x, ec.contour_y, label=tr.getName())
    plt.xlabel('T_p')
    plt.ylabel('H_s')
    plt.title("Scatter plot")
    plt.legend()
    if save_plots:
        plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_scat" + ".pdf")
    plt.show()    

if plotContour:
    fig = plt.figure(figsize = (7, 5))
    plt.plot(ec.contour_x, ec.contour_y, label=tr.getName())
    plt.xlabel('T_p')
    plt.ylabel('H_s')
    plt.title("Environmental contour")
    plt.legend()
    if save_plots:
        plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")" + ".pdf")
    plt.show()

# Calculate smooth contour
if smoothWidth > 0:
    old_contour_x = ec.copyContour_x()
    old_contour_y = ec.copyContour_y()
    ec.smoothC(smoothWidth)
    ec.calculateContour()   
        
    if plotC:
        fig = plt.figure(figsize = (7, 5))
        a = np.zeros(numTangents)
        c = np.zeros(numTangents)
        for i in range(numTangents):
            a[i] = ec.getAngle(i)
            c[i] = ec.getC(i)
        plt.plot(a, c, label=tr.getName())
        plt.xlabel('theta')
        plt.ylabel('C(theta)')
        plt.title("The C-function")
        plt.legend()
        if save_plots:
            plt.savefig("contourtest01/" + tr.getName() + "("  + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_c_s" + ".pdf")
        plt.show()    
        
    if plotDC:
        fig = plt.figure(figsize = (7, 5))
        a = np.zeros(numTangents)
        dc = np.zeros(numTangents)
        for i in range(numTangents):
            a[i] = ec.getAngle(i)
            dc[i] = ec.getDC(i)
        plt.plot(a, dc, label=tr.getName())
        plt.xlabel('theta')
        plt.ylabel('DC(theta)')
        plt.title("The derivative of the C-function")
        plt.legend()
        if save_plots:
            plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_dc_s" + ".pdf")
        plt.show()    
        
    if plotDC2:
        fig = plt.figure(figsize = (7, 5))
        a = np.zeros(numTangents)
        dc2 = np.zeros(numTangents)
        for i in range(numTangents):
            a[i] = ec.getAngle(i)
            dc2[i] = ec.getDC2(i)
        plt.plot(a, dc2, label=tr.getName())
        plt.xlabel('theta')
        plt.ylabel('DC2(theta)')
        plt.title("The second derivative of the C-function")
        plt.legend()
        if save_plots:
            plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_dc2_s" + ".pdf")
        plt.show()    
        
    if plotCDC2:
        fig = plt.figure(figsize = (7, 5))
        a = np.zeros(numTangents)
        cdc2 = np.zeros(numTangents)
        for i in range(numTangents):
            a[i] = ec.getAngle(i)
            cdc2[i] = ec.getCDC2(i)
        plt.plot(a, cdc2, label=tr.getName())
        plt.xlabel('theta')
        plt.ylabel('CDC2(theta)')
        plt.title("The sum of the C-function and its second derivative")
        plt.legend()
        if save_plots:
            plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_cdc2_s" + ".pdf")
        plt.show()    
        
    if plotContour:
        fig = plt.figure(figsize = (7, 5))
        plt.plot(old_contour_x, old_contour_y, label=tr.getName())
        plt.plot(ec.contour_x, ec.contour_y, label=tr.getName() + "_s(" + str(smoothWidth) + ")")
        plt.xlabel('T_p')
        plt.ylabel('H_s')
        plt.title("Environmental contour")
        plt.legend()
        if save_plots:
            plt.savefig("contourtest01/" + tr.getName() + "(" + str(radiusFactor) + ", " + str(numTangents) + ", " + str(returnPeriod) + ")_s" + ".pdf")
        plt.show()
    
