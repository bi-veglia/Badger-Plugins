import numpy as np
from operator import itemgetter
import time



def ES_normalize(p, pmin, pmax):
        """
        Normalize parameter values to within [-2 2]

        :param p:
        :return:
        """
        pdiff = (pmax - pmin)
        pmean = (pmax + pmin)/2.0
        pnorm = 2.0*(p - pmean)/pdiff
        return pnorm
    
def ES_UNnormalize(p, pmin, pmax):
    """
    Un normalize parameters back to physical values
    """
    pdiff = (pmax - pmin)
    pmean = (pmax + pmin)/2
    pUNnorm = (p*pdiff/2.0) + pmean
    return pUNnorm

def optimize(evaluate, params):
    # const values
    w0 = 500.0
    amplitude = 1.0
    decay_rate = 0.999
    dtES = 2*np.pi/(10*1.75*w0)

    kES , norm_coef, max_iter, pmin, pmax = \
        itemgetter('k', 'norm_coeff', 'max_iter','pmin','pmax')(params)

    _, _, _, x0 = evaluate(None)
    x = x0[0]
    print(f"x {x}")
    nparams = len(x)
    wES = w0*(0.75*(1+np.arange(nparams))/(nparams)+1)
    pnew = x
    cost_val, _, _, _ = evaluate(x.reshape(1, -1))
    #normalize the cost function to the initial value
    magic=1.0e14
    
    #normal_coeff=cost_val[0,0]
    cost_val = cost_val[0,0]*magic
    print(f"!!!!!!!!!!!magic: {magic} ")

    alphaES= (norm_coef * 2)**2*(wES)/4

    for step in np.arange(max_iter):
        # Normalize parameters within [-1 1]
        pnorm = ES_normalize(pnew, pmin, pmax)
        
        # Do the ES update
        pnorm = pnorm + amplitude*dtES*np.cos(wES*step*dtES+kES*cost_val)*(alphaES*wES)**0.5
        print(f"pnorm {pnorm}")
        # Check that parameters stay within normalized range [-1, 1]
        for jn in np.arange(nparams):
            if abs(pnorm[jn]) > 1:
                pnorm[jn]=pnorm[jn]/(0.0+abs(pnorm[jn]))
            
        # Calculate unnormalized parameter value for next cost "
        pnew = ES_UNnormalize(pnorm, pmin, pmax)
        amplitude= amplitude*decay_rate
        cost_val, _, _, _ = evaluate(pnew.reshape(1, -1))
        cost_val = cost_val[0,0]*magic
        time.sleep(0.01)      