import numpy as np
from operator import itemgetter
import time

def optimize(evaluate, params):
    # const values
    init_val, final_val, delta,max_iter = \
        itemgetter('init_val', 'final_val','delta', 'max_iter')(params)

    _, _, _, x0 = evaluate(None)
    x = x0
    print(f"initial reading {x}")
    
    print(f"initial value for the scan {init_val}")
    #print(f'evaluate x reshaped {evaluate(x.reshape(1, -1))}')
    cost_val, _, _, _ = evaluate(x.reshape(1, -1))  
    cost_val = cost_val[0,0]
    val_new=x

    for step in np.arange(max_iter):
        val_new = val_new + delta
        print(f"current values {val_new}")
        cost_val, _, _, _ = evaluate(val_new.reshape(1, -1))
        cost_val = cost_val[0,0]
        time.sleep(0.01)      