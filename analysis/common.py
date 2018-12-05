
def compute_foreground_value(c, x, Rsf):
    """
        Compute the value of the background (steady) workload
        Parameters:
            c:      Compute units need by the workload per frame-time (compute unit/frame-time)
            Rsf:    Share of the framework (compute unit/frame-time)
            x:      Value of 1 compute unit/frame-time (1/compute-unit/frame-time)
        
        Return: value = min(c, Rsf) * x

    """
    return min(c, Rsf) * x


def compute_burst_value(lamb, h, d, w, tau, Rva):
    """
        Compute the value of the bursty workload
        Parameters:
            lamb:   Average arrival frequency
            h:      Burst height (compute-unit)
            d:      Burst duration (frame-time)
            w:      highest value per duration (1/frame-time)
            tau:    Timeliness parameter (expenentiall decay per frame-time value)
            Rva:    Share of the framework
    
        Return: value = min(c, Rsf) * x

    """
    
    # If no resource provide then we get no value
    if Rva == 0:
        return 0

    # Excution time of 1 frame
    e = max(h / Rva, 1)
    # Vaue decay
    decay = tau**(1-e)
    if decay == 1:
        decay = 0.9999999

    return lamb * w/tau * (1-decay**d) / (1 - decay)
        

def compute_value(c, x, Rsf, lamb, h, d, w, tau, Rva):

    return compute_foreground_value(c, x, Rsf) + compute_burst_value(lamb, h, d, w, tau, Rva)



