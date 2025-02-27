##########################################################
#                                                        #
#    Environmental contour classes and methods           #
#                                                        #
##########################################################

import numpy as np

from math import *
from numba import jit
from random import uniform, seed
from util import getInnerRadius, getExceedenceProbability, getAdjNonExceedenceProbability, ran_gaussian_cdf


NUMSIMS = 500000

def setNumberOfSimulations(num):
    global NUMSIMS
    NUMSIMS = num


TANGENTS = 180

def setNumberOfTangents(tang):
    global TANGENTS 
    TANGENTS = tang
    
    
SEED = 12345678

def setSeed(num):
    global SEED
    SEED = num
    
    
STANDARDIZE = True

def setStandardize(flag):
    global STANDARDIZE
    STANDARDIZE = flag
    
    
##########################################################
#      jit function for estimating the C-function        #
##########################################################
@jit(nopython=True)
def doEstimateC(samplingRate, returnPeriod, xx, yy):
    q_e_prime = getAdjNonExceedenceProbability(samplingRate, returnPeriod)
    critIndex = int(round(NUMSIMS * q_e_prime))
    projections = np.zeros(NUMSIMS)
    cc = np.zeros(TANGENTS)
    
    for i in range(TANGENTS):
        angle = 2.0 * pi * i / TANGENTS
        cosine = cos(angle)
        sine = sin(angle)
        
        for j in range(NUMSIMS):
            projections[j] = xx[j] * cosine + yy[j] * sine
        
        projections.sort()
        cc[i] = projections[critIndex]
    
    return cc
    

    
    
##########################################################
#    Class handling contour construction                 #
##########################################################
class Contour():
    def __init__(self, transformator, returnPeriod):
        self.transformator = transformator
        self.samplingRate = transformator.getSamplingRate()
        self.returnPeriod = returnPeriod
        self.x = np.zeros(NUMSIMS)
        self.y = np.zeros(NUMSIMS)
        self.mean_x = 0
        self.stdv_x = 0
        self.mean_y = 0
        self.stdv_y = 0
        self.rho = 0
        self.rho2 = 0
        self.delta = (2 * pi) / TANGENTS
        self.c = None
        self.contour_x = np.zeros(TANGENTS + 1)
        self.contour_y = np.zeros(TANGENTS + 1)
        
    def randomPoint(self, min_r):
        r = sqrt(min_r * min_r - 2 * log(uniform(0,1)))
        a = uniform(-1, 1) * pi
        return r * cos(a), r * sin(a)        
        
    def standardize(self, x, y):
        if STANDARDIZE:
            u = (x - self.mean_x) / self.stdv_x
            w = (y - self.mean_y) / self.stdv_y
            v = (w - self.rho * u) / self.rho2
            return u, v
        else:
            return x, y
    
    def unstandardize(self, u, v):
        if STANDARDIZE:
            x = self.stdv_x * u + self.mean_x
            y = self.stdv_y * (self.rho * u + self.rho2 * v) + self.mean_y
            return x, y
        else:
            return u, v
    
    def getUnstandardizedPoint(self, i):
        return self.unstandardize(self.x[i], self.y[i])
    
    def getAngle(self, i):
        return (2 * pi * i) / TANGENTS
    
    def getC(self, i):
        return self.c[(TANGENTS + i) % TANGENTS]
    
    def getDC(self, i):
        return (self.getC(i+1) - self.getC(i-1)) / (2 * self.delta)

    def getDC2(self, i):
        return (self.getDC(i+1) - self.getDC(i-1)) / (2 * self.delta)
        
    def getCDC2(self, i):
        return self.getC(i) + self.getDC2(i)
    
    def smoothC(self, width):
        print("smoothC(" + str(width) + ")")
        cc = np.zeros(TANGENTS)
        wsum = (width + 1) * (width + 1)
        for i in range(TANGENTS):
            csum = 0
            for j in range(-width, width+1):
                w = (width + 1) - abs(j)
                csum += self.getC(i+j) * w 
            cc[i] = csum / wsum
        self.c = cc

    def runSimulation(self):
        print("runSimulation(" + str(SEED) + ") -- Contour")
        seed(SEED)
        pe = getExceedenceProbability(self.samplingRate, self.returnPeriod)
        min_r = getInnerRadius(self.samplingRate, self.returnPeriod)
        print("pe = " + str(pe) + ", min_r = " + str(min_r))
        
        sum_x = 0
        sum_x2 = 0
        sum_y = 0
        sum_y2 = 0
        sum_xy = 0
        
        for i in range(NUMSIMS):
            p = self.transformator.transform(self.randomPoint(min_r))
            self.x[i] = p[0]
            self.y[i] = p[1]
            sum_x += self.x[i]
            sum_x2 += self.x[i] * self.x[i]
            sum_y += self.y[i]
            sum_y2 += self.y[i] * self.y[i]
            sum_xy += self.x[i] * self.y[i]
        
        self.mean_x = sum_x / NUMSIMS
        self.stdv_x = sqrt((sum_x2 - (sum_x * sum_x / NUMSIMS))/(NUMSIMS - 1.0))
        self.mean_y = sum_y / NUMSIMS
        self.stdv_y = sqrt((sum_y2 - (sum_y * sum_y / NUMSIMS))/(NUMSIMS - 1.0))
        
        if self.stdv_x > 0 and self.stdv_y > 0:
            self.rho = ((sum_xy/ NUMSIMS) - self.mean_x * self.mean_y) / (self.stdv_x * self.stdv_y)
        else:
            self.rho = 0.0
        
        self.rho2 = sqrt(1 - self.rho * self.rho)
        
        for i in range(NUMSIMS):
            p = self.standardize(self.x[i], self.y[i])
            self.x[i] = p[0]
            self.y[i] = p[1]
            
    def printMoments(self):
        print("mean_x = " + str(self.mean_x))
        print("stdv_x = " + str(self.stdv_x))
        print("mean_y = " + str(self.mean_y))
        print("stdv_y = " + str(self.stdv_y))
        print("rho = " + str(self.rho))
                
    def estimateC(self):
        print("estimateC()")
        self.c = doEstimateC(self.samplingRate, self.returnPeriod, self.x, self.y)
            
    def printC(self):
        for i in range(TANGENTS):
            print("c[" + str(i) + "] = " + str(self.c[i]))
                   
    def calculateContour(self):
        print("calculateContour()")
        for i in range(TANGENTS):
            angle0 = 2.0 * pi * (i-1) / TANGENTS
            angle1 = 2.0 * pi * i / TANGENTS
            
            a00 = cos(angle0)
            a01 = sin(angle0)
            a10 = cos(angle1)
            a11 = sin(angle1)
            
            determ = a00 * a11 - a01 * a10
            
            if i == 0:
                c0 = self.c[TANGENTS-1]
            else:
                c0 = self.c[i-1]
            
            u = (a11 * c0 - a01 * self.c[i]) / determ
            v = (-a10 * c0 + a00 * self.c[i]) / determ
            
            p = self.unstandardize(u, v)
            self.contour_x[i] = p[0]
            self.contour_y[i] = p[1]
            
        self.contour_x[TANGENTS] = self.contour_x[0]
        self.contour_y[TANGENTS] = self.contour_y[0]
        
    def copyContour_x(self):
        copy_x = np.zeros(TANGENTS + 1)
        for i in range(TANGENTS + 1):
            copy_x[i] = self.contour_x[i]
        return copy_x    

    def copyContour_y(self):
        copy_y = np.zeros(TANGENTS + 1)
        for i in range(TANGENTS + 1):
            copy_y[i] = self.contour_y[i]
        return copy_y  

    def printContour(self):
        for i in range(TANGENTS + 1):
            print("contour[" + str(i) + "] = [" + str(self.contour_x[i]) + ", " + str(self.contour_y[i]) + "]")
            

##########################################################
#      jit function for transforming a point             #
##########################################################
@jit(nopython=True)
def doTransform(alpha, beta, gamma, a1, a2, a3, b1, b2, b3, p0, p1):
    if p0 <= 0.0:
        u = ran_gaussian_cdf(p0)           
        y = gamma + alpha * pow(-log(1.0 - u), 1.0 / beta)
    else:
        u = ran_gaussian_cdf(-p0)           
        y = gamma + alpha * pow(-log(u), 1.0 / beta)
    
    muX = a1 + a2 * pow(y, a3)
    sigmaX = b1 + b2 * exp(b3 * y)
    x = exp(sigmaX * p1 + muX)       
    return x, y
    


##########################################################
#    Class handling Weibull/lognormal transformations    #
##########################################################
class Transformator():
    def __init__(self, name, samplingRate, alpha, beta, gamma, a1, a2, a3, b1, b2, b3):
        self.name = name
        self.samplingRate = samplingRate
        self.alpha = alpha 
        self.beta = beta
        self.gamma = gamma
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.b1 = b1
        self.b2 = b2
        self.b3 = b3
        
    def getName(self):
        return self.name
        
    def getSamplingRate(self):
        return self.samplingRate
        
    def transform(self, p):
        return doTransform(self.alpha, self.beta, self.gamma, self.a1, self.a2, self.a3, self.b1, self.b2, self.b3, p[0], p[1])

    