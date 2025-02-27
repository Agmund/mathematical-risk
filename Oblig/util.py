##########################################################
#                                                        #
#    Utility methods for Environmental Contours          #
#                                                        #
##########################################################

from math import *
from numba import jit


##########################################################
#    Gaussian distribution methods                       #
##########################################################
@jit(nopython=True)
def ran_gaussian_pdf(x):
    return exp(-x * x / 2.0) / 2.50662827463100029


@jit(nopython=True)
def ran_gaussian_cdf(x):
    if (x >= 0.0):
        t = 1.0/(1.0 + 0.33267 * x)
        return 1.0 - ran_gaussian_pdf(x) * (0.4361836*t - 0.1201676*t*t + 0.9372980*t*t*t)
    else:
        t = 1.0/(1.0 - 0.33267 * x)
        return ran_gaussian_pdf(x) * (0.4361836*t - 0.1201676*t*t + 0.9372980*t*t*t)


@jit(nopython=True)
def ran_gaussian_sdf(x):
    if (x >= 0.0):
        t = 1.0/(1.0 + 0.33267 * x)
        return ran_gaussian_pdf(x) * (0.4361836*t - 0.1201676*t*t + 0.9372980*t*t*t)
    else:
        t = 1.0/(1.0 - 0.33267 * x)
        return 1.0 - ran_gaussian_pdf(x) * (0.4361836*t - 0.1201676*t*t + 0.9372980*t*t*t)


@jit(nopython=True)
def ran_gaussian_invcdf(u):
        if (u < 0.5):
            t = sqrt(log(1.0/(u*u)))
            return -t + (2.515517 + 0.802853*t + 0.010328*t*t) / (1.0 + 1.432788*t + 0.189269*t*t + 0.001308*t*t*t)
        elif (u == 0.5):
            return 0.0;
        else:
            t = sqrt(log(1.0/((1.0 - u)*(1.0 - u))))
            return t - (2.515517 + 0.802853*t + 0.010328*t*t) / (1.0 + 1.432788*t + 0.189269*t*t + 0.001308*t*t*t)

      
@jit(nopython=True)
def ran_gaussian_invsdf(u):
        if (u < 0.5):
            t = sqrt(log(1.0/(u*u)))
            return t - (2.515517 + 0.802853*t + 0.010328*t*t) / (1.0 + 1.432788*t + 0.189269*t*t + 0.001308*t*t*t)
        elif (u == 0.5):
            return 0.0;
        else:
            t = sqrt(log(1.0/((1.0 - u)*(1.0 - u))))
            return -t + (2.515517 + 0.802853*t + 0.010328*t*t) / (1.0 + 1.432788*t + 0.189269*t*t + 0.001308*t*t*t)

       
##########################################################
#    Exceedence probability methods                      #
##########################################################

# Calculate the exceedence probability for a given return period (years)
# The sampling rate is the number of seastate samples pr. day (e.g., 8)
@jit(nopython=True)
def getExceedenceProbability(samplingRate, returnPeriod):
    return 1.0 / (returnPeriod * samplingRate * 365.25)

# Calculate the inceedence probability for a given return period (years)
# The sampling rate is the number of seastate samples pr. day (e.g., 8)
@jit(nopython=True)
def getNonExceedenceProbability(samplingRate, returnPeriod):
    return 1.0 - 1.0 / (returnPeriod * samplingRate * 365.25)

# The inner radius factor denotes the ratio between the
# radius of the circle which we sample outside when we
# estimate the form curve, and the radius of the circle 
# used to produce the Rosenblatt contour.
# 
# The inner radius factor should always be less than 1.0.
# Note, however, that if the radius factor is too close to 1.0,
# the boundary of the set of excluded sampling points, i.e, 
# the boundary of the transformed inner circle, may interfer 
# with the form curve, and thus yielding incorrect estimates. 
# 
# A factor of 0.95 appears to produce good results. 
# A lower value will also work, but then we need more 
# simulations in order to obtain stable results.
INNER_RADIUS_FACTOR = 0.95;
    
def setInnerRadiusFactor(irf):
    global INNER_RADIUS_FACTOR
    INNER_RADIUS_FACTOR = irf


# The arma inner radius factor denotes the ratio between the
# radius of the circle which we sample outside when we
# estimate the arma form curve, and the radius of the circle 
# used to produce the Rosenblatt contour.
# 
# The arma inner radius factor should always be less than 1.0.
# Note, however, that if the radius factor is too close to 1.0,
# the boundary of the set of excluded sampling points, i.e, 
# the boundary of the transformed inner circle, may interfer 
# with the arma form curve, and thus yielding incorrect estimates. 
# 
# A factor of 0.80 appears to produce good results. 
# A lower value will also work, but then we need more 
# simulations in order to obtain stable results.
ARMA_INNER_RADIUS_FACTOR = 0.80;
    
def setArmaInnerRadiusFactor(irf):
    global ARMA_INNER_RADIUS_FACTOR
    ARMA_INNER_RADIUS_FACTOR = irf


# Get the radius of the circle corresponding to a given returnPeriod.
@jit(nopython=True)
def getRadius(samplingRate, returnPeriod):
    qe = getNonExceedenceProbability(samplingRate, returnPeriod)
    return ran_gaussian_invcdf(qe)


# Use this method to calculate the radius of circle inside the circle
# corresponding to the given returnPeriod. This inner circle can be
# used when sampling points in order to calculate a form plot. By
# sampling points outside this inner circle only, we can reduce the
# number of samples needed to obtain a stable form estimate.
@jit(nopython=True)
def getInnerRadius(samplingRate, returnPeriod):
    qe = 1.0 - getExceedenceProbability(samplingRate, returnPeriod)
    return INNER_RADIUS_FACTOR * ran_gaussian_invcdf(qe)
    

# Use this method to calculate the radius of circle inside the circle
# corresponding to the given returnPeriod. This arma inner circle can be
# used when sampling points in order to calculate an arma form plot. By
# sampling points outside this inner circle only, we can reduce the
# number of samples needed to obtain a stable form estimate.
@jit(nopython=True)
def getArmaInnerRadius(samplingRate, returnPeriod):
    qe = 1.0 - getExceedenceProbability(samplingRate, returnPeriod)
    return ARMA_INNER_RADIUS_FACTOR * ran_gaussian_invcdf(qe)


# Use this method to calculate the probability that a random point is outside
# the circle corresponding to a given returnPeriod.
@jit(nopython=True)
def getCircleExceedenceProbability(samplingRate, returnPeriod):
    r = getRadius(samplingRate, returnPeriod)
    return exp(-0.5 * r * r)


# Use this method to calculate the probability that a random point is inside
# the circle corresponding to a given returnPeriod.    
@jit(nopython=True)
def getCircleNonExceedenceProbability(samplingRate, returnPeriod):
    r = getRadius(samplingRate, returnPeriod)
    return 1.0 - exp(-0.5 * r * r)
    

# Use this method to calculate the probability that a random point is outside
# the inner circle corresponding to a given returnPeriod.
@jit(nopython=True)
def getInnerCircleExceedenceProbability(samplingRate, returnPeriod):
    ir = getInnerRadius(samplingRate, returnPeriod)
    return exp(-0.5 * ir * ir)
    

# Use this method to calculate the probability that a random point is inside
# the inner circle corresponding to a given returnPeriod.    
@jit(nopython=True)
def getInnerCircleNonExceedenceProbability(samplingRate, returnPeriod):
    ir = getInnerRadius(samplingRate, returnPeriod)
    return 1.0 - exp(-0.5 * ir * ir)


# Use this method to calculate the probability that a random point is outside
# the arma inner circle corresponding to a given returnPeriod.    
@jit(nopython=True)
def getArmaInnerCircleExceedenceProbability(samplingRate, returnPeriod):
    ir = getArmaInnerRadius(samplingRate, returnPeriod)
    return exp(-0.5 * ir * ir)


# Use this method to calculate the probability that a random point is inside
# the arma inner circle corresponding to a given returnPeriod.    
@jit(nopython=True)
def getArmaInnerCircleNonExceedenceProbability(samplingRate, returnPeriod):
    ir = getArmaInnerRadius(samplingRate, returnPeriod)
    return 1.0 - exp(-0.5 * ir * ir)
    

# Use this method to calculate the "adjusted exceedence probability"
# P_e'. This probability is the probability that the projection of 
# a random point is exceeding the critical value C(theta) given that the 
# point is outside of the transformed inner circle. This adjusted
# probability can be used to estimate C(theta) given that all the
# sampled points are outside the inner circle.
# 
# Note that P_e = exp(-r^2/2) P_e', where the factor exp(-r^2/2)
# is the probability that a random point is outside the transformed
# inner circle.
@jit(nopython=True)
def getAdjExceedenceProbability(samplingRate, returnPeriod):
    ir = getInnerRadius(samplingRate, returnPeriod)
    pe = getExceedenceProbability(samplingRate, returnPeriod)
    return exp(0.5 * ir * ir) * pe / returnPeriod
    

# Use this method to calculate the "adjusted arma exceedence probability"
# P_e'. This probability is the probability that the projection of 
# a random point is exceeding the critical value C(theta) given that the 
# point is outside of the transformed arma inner circle. This adjusted
# probability can be used to estimate C(theta) given that all the
# sampled points are outside the arma inner circle.
# 
# Note that P_e = exp(-r^2/2) P_e', where the factor exp(-r^2/2)
# is the probability that a random point is outside the transformed
# arma inner circle.
@jit(nopython=True)
def getAdjArmaExceedenceProbability(samplingRate, returnPeriod):
    ir = getArmaInnerRadius(samplingRate, returnPeriod)
    pe = getExceedenceProbability(samplingRate, returnPeriod)
    return exp(0.5 * ir * ir) * pe / returnPeriod
    

# Use this method to calculate the "adjusted nonexceedence probability"
# Q_e'. This probability is the probability that the projection of 
# a random point is not exceeding the critical value C(theta) given that the 
# point is outside of the transformed inner circle. This adjusted
# probability can be used to estimate C(theta) given that all the
# sampled points are outside the inner circle.
@jit(nopython=True)
def getAdjNonExceedenceProbability(samplingRate, returnPeriod):
    ir = getInnerRadius(samplingRate, returnPeriod)
    pe = getExceedenceProbability(samplingRate, returnPeriod)
    return 1.0 - exp(0.5 * ir * ir) * pe
    

# Use this method to calculate the "adjusted arma nonexceedence probability"
# Q_e'. This probability is the probability that the projection of 
# a random point is not exceeding the critical value C(theta) given that the 
# point is outside of the transformed arma inner circle. This adjusted
# probability can be used to estimate C(theta) given that all the
# sampled points are outside the arma inner circle.
@jit(nopython=True)
def getAdjArmaNonExceedenceProbability(samplingRate, returnPeriod):
    ir = getArmaInnerRadius(samplingRate, returnPeriod)
    pe = getExceedenceProbability(samplingRate, returnPeriod)
    return 1.0 - exp(0.5 * ir * ir) * pe
