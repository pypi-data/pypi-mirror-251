
import math
import numpy as np
from scipy.special import gamma
from scipy.interpolate import CubicSpline
from scipy.stats import rv_histogram


def res_free_desc(tmax, H:np.ndarray, TT=None, TTmin=0, TTmax=None):
    # rewrite this with ddist instead of rv_histogram
    if np.isscalar(H):
        H = [H]
    nTT = len(H)
    if TT is None:
        if TTmax is None:
            TTmax = tmax
        TT = np.linspace(TTmin, TTmax, nTT+1)
    else:
        if len(TT) != nTT+1:
            msg = 'The array of transit time boundaries needs to have length N+1, '
            msg += '\n with N the size of the transit time distribution H.'
            raise ValueError(msg)
    dist = rv_histogram((H,TT), density=True)
    return {
        'mean': dist.mean(),
        'median': dist.median(),
        'stdev': dist.std(),
        }

def interp(x,y, pos=False, floor=False):
    # Interpolate y on x, assuming y-values are uniformly distributed over the x-range
    if np.isscalar(y):
        yi = y*np.ones(len(x))
    elif len(y)==1:
        yi = y[0]*np.ones(len(x))
    elif len(y)==2:
        yi = lin(x,y)
    elif len(y)==3:
        yi = quad(x,y)
    else:
        x_y = np.linspace(np.amin(x), np.amax(x), len(y))
        yi = CubicSpline(x_y, y)(x)
    if pos:
        yi[yi<0] = 0
    if floor:
        y0 = np.amin(y)
        yi[yi<y0] = y0
    return yi

def quad(t, K):
    # Helper
    nt = len(t)
    mid = math.floor(nt/2)
    return quadratic(t, t[0], t[mid], t[-1], K[0], K[1], K[2])

def lin(t, K):
    # Helper
    return linear(t, t[0], t[-1], K[0], K[1])

def linear(x, x1, x2, y1, y2):
    # Helper
    #returns a linear function of x 
    #that goes through the two points (xi, yi)
    L1 = (x2-x)/(x2-x1)
    L2 = (x-x1)/(x2-x1)
    return y1*L1 + y2*L2

def quadratic(x, x0, x1, x2, y0, y1, y2):
    # Helper
    #returns a quadratic function of x 
    #that goes through the three points (xi, yi)
    L0 = (x-x1)*(x-x2)/((x0-x1)*(x0-x2))
    L1 = (x-x0)*(x-x2)/((x1-x0)*(x1-x2))
    L2 = (x-x0)*(x-x1)/((x2-x0)*(x2-x1))
    return y0*L0 + y1*L1 + y2*L2


def tarray(n, t=None, dt=1.0):
    # Helper function - generate time array.
    if t is None:
        t = dt*np.arange(n)
    else:
        if not isinstance(t, np.ndarray):
            t = np.array(t)
        if len(t) != n:
            raise ValueError('Time array must have same length as the input.')   
    return t


def trapz(f, t=None, dt=1.0):
    # Helper function - perform trapezoidal integration.
    # Replace by scipy.integrate.trapezoid
    f = np.array(f)
    n = len(f)
    t = tarray(n, t=t, dt=dt)
    g = np.empty(n)
    g[0] = 0
    for i in range(n-1):
        g[i+1] = g[i] + (t[i+1]-t[i]) * (f[i+1]+f[i]) / 2
    return g


def ddelta(T, t):
    # Helper function - discrete delta
    if not isinstance(t, np.ndarray):
        t=np.array(t)
    n = len(t)
    h = np.zeros(n)
    if T<t[0]:
        return h
    if T>t[-1]:
        return h
    if T==t[0]:
        h[0]=2/(t[1]-t[0])
        return h
    if T==t[-1]:
        h[-1]=2/(t[-1]-t[-2])
        return h
    i = np.where(T>=t)[0][-1]
    u = (T-t[i])/(t[i+1]-t[i])
    if i==0:
        h[i] = (1-u)*2/(t[i+1]-t[i])
    else:
        h[i] = (1-u)*2/(t[i+1]-t[i-1])
    if i==n-2:
        h[i+1] = u*2/(t[i+1]-t[i])
    else:
        h[i+1] = u*2/(t[i+2]-t[i])
    return h


def dstep(T0, T1, t):
    # Helper function - discrete step
    if not isinstance(t, np.ndarray):
        t=np.array(t)
    n = len(t)
    i = np.where((t>T0)*(t<T1))[0]
    if len(i)==0:
        return ddelta((T0+T1)/2, t)
    i0, i1 = i[0], i[-1]
    t0, t1 = t[i0], t[i1]
    hi = 0
    if i0>0:
        u0 = (t0-T0)/(t0-t[i0-1])
        hi += 0.5*(1+u0)*(t0-t[i0-1])
        if i0>1:
            hi += 0.5*u0*(t[i0-1]-t[i0-2])   
    hi += t1-t0
    if i1<n-1:
        u1 = (T1-t1)/(t[i1+1]-t1)
        hi += 0.5*(1+u1)*(t[i1+1]-t1)
        if i1<n-2:
            hi += 0.5*u1*(t[i1+2]-t[i1+1])
    h = np.zeros(n)
    h[i] = 1/hi
    if i0>0:
        h[i0-1] = u0/hi
    if i1<n-1:
        h[i1+1] = u1/hi
    return h


def ddist(H, T, t):
    # discrete distribution - T is an array of times with the boundaries of the histogram bins
    h = np.zeros(len(t))
    for k in range(len(T)-1):
        h += H[k]*dstep(T[k], T[k+1], t)
    return h


def intprod(f, h, t=None, dt=1.0):
    # Helper function
    # Integrate the product of two piecewise linear functions
    # by analytical integration over each interval.
    # Derivation:
    # If f and h are linear between x and y, then we can define slopes:
    # dx = y-x
    # sf(x) = (f(y)-f(x))/dx
    # sh(x) = (h(y)-h(x))/dx
    # With this the integral over the interval becomes:
    # \int_x^y du f(u)h(u)
    # = \int_0^dx du [f(x)+usf(x)] [h(x)+ush(x)]
    # = f(x)*h(x)*dx
    # + [f(x)*sh(x)+sf(x)*h(x)]dx**2/2
    # + sf(x)*sh(x)*dx**3/3
    g = 0
    for l in range(len(f)-1):
        if t is not None:
            dt = t[l+1]-t[l]
        sf = (f[l+1]-f[l])/dt
        sh = (h[l+1]-h[l])/dt
        g += h[l]*f[l]*dt
        g += (sh*f[l]+sf*h[l])*dt**2/2
        g += sh*sf*dt**3/3
    return g


def uconv(f, h, dt=1.0):
    # Helper function: convolution over uniformly sampled grid.
    n = len(f) 
    g = np.zeros(n)
    h = np.flip(h)
    for k in range(1, n):
        g[k] = intprod(f[:k+1], h[-(k+1):], dt=dt)
    return g


def conv(f, h, t=None, dt=1.0):
    """Convolve two 1D-arrays.

    This function returns the convolution :math:`f(t)\\otimes h(t)`, using piecewise linear integration to approximate the integrals in the convolution product.

    Args:
        f (array_like): the first 1D array to be convolved.
        h (array_like): the second 1D array to be convolved.
        t (array_like, optional): the time points where the values of f are defined. If t=None, the time points are assumed to be uniformly spaced with spacing dt. Defaults to None.
        dt (float, optional): spacing between time points for uniformly spaced time points. This parameter is ignored if t is explicity provided. Defaults to 1.0.

    Raises:
        ValueError: if f and h have a different length.

    Returns:
        numpy.ndarray: a 1D numpy array of the same length as f and h.

    See Also:
        `expconv`, `biexpconv`, `nexpconv`, `stepconv`

    Notes: 
        The convolution product :math:`f(t)\\otimes h(t)` implemented by `conv` is explicitly defined as:

        .. math::
            g(t) = \\int_0^t du\\, f(u) h(t-u)

        `conv` returns an approximation to this continuous convolution product, calculated by piecewise linear integration. This is not to be confused with other convolution functions, such as `numpy.convolve` which performs discrete convolution. Tracer-kinetic theory is defined by continuous equations and therefore should be performed with `conv` for maximal accuracy, though the difference may be small at high temporal resolution.

        `conv` is generally applicable to any f(t) and h(t), but more accurate formulae for some special cases exists and should be used if available. An example is `expconv`, to be used when either f(t) or h(t) is an exponential.

    Example:
        Import package and create vectors f and h:

        >>> import dcmri as dc
        >>> f = [5,4,3,6]
        >>> h = [2,9,1,3]

        Calculate :math:`g(t) = f(t) \\otimes h(t)` over a uniformly sampled grid of time points with spacing dt=1:

        >>> dc.conv(f, h)
        array([ 0.        , 25.33333333, 41.66666667, 49.        ])

        Calculate the same convolution over a grid of time points with spacing dt=2:

        >>> dc.conv(f, h, dt=2)
        array([ 0.        , 50.66666667, 83.33333333, 98.        ])

        Calculate the same convolution over a non-uniform grid of time points:

        >>> t = [0,1,3,7]
        >>> dc.conv(f, h, t)
        array([  0.        ,  25.33333333,  57.41666667, 108.27083333])
    """
    if len(f) != len(h):
        raise ValueError('f and h must have the same length.')
    if t is None:
        return uconv(f, h, dt)
    n = len(t)
    g = np.zeros(n)
    tf = np.flip(t)
    f = np.flip(f)
    for k in range(1, n):
        tkf = t[k]-tf[-(k+1):]
        tk = np.unique(np.concatenate((t[:k+1], tkf)))
        fk = np.interp(tk, tkf, f[-(k+1):], left=0, right=0)
        hk = np.interp(tk, t[:k+1], h[:k+1], left=0, right=0)
        g[k] = intprod(fk, hk, tk)
    return g


def inttrap(f, t, t0, t1):
    # Helper function: integrate f from t0 to t1
    ti = t[(t0<t)*(t<t1)]
    ti = np.concatenate(([t0],ti,[t1]))
    fi = np.interp(ti, t, f, left=0, right=0)
    return np.trapz(fi,ti)


def stepconv(f, T, D, t=None, dt=1.0):
    """Convolve a 1D-array with a normalised step function.

    Args:
        f (array_like): the 1D array to be convolved.
        T (float): the central time point of the step function. 
        D (float): half-width of the step function, as a fraction of T. D must be less or equal to 1.
        t (array_like, optional): the time points where the values of f are defined, in the same units as T. If t=None, the time points are assumed to be uniformly spaced with spacing dt. Defaults to None.
        dt (float, optional): spacing between time points for uniformly spaced time points. This parameter is ignored if t is explicity provided. Defaults to 1.0.

    Raises:
        ValueError: if D > 1.

    Returns:
        numpy.ndarray: a 1D numpy array of the same length as f.

    See Also:
        `conv`, `expconv`, `biexpconv`, `nexpconv`

    Notes: 
        `stepconv` implements the same convolution product as `conv`, but is more accurate and faster in the special case where one of the factors is known to be a step function.

    Example:
        Import package, create a vector f and an array of time points:

        >>> import dcmri as dc
        >>> f = [5,4,3,6]
        >>> t = [0,2,4,7]

        Convolve f with a step function that is centered on t=3 with a half width of 1.5 = 0.5*3: 

        >>> dc.stepconv(f, 3, 0.5, t)
        array([0.        , 0.8125    , 3.64583333, 3.5625    ])
    """
    if D>1:
        raise ValueError('The dispersion factor D must be <= 1')
    TW = D*T      # Half width of step
    T0 = T-TW     # Initial time point of step
    T1 = T+TW
    n = len(f)
    t = tarray(n, t=t, dt=dt)
    g = np.zeros(n)
    k = len(t[t<T0])
    ti = t[(T0<=t)*(t<=T1)]
    for tk in ti:
        g[k] = inttrap(f, t, 0, tk-T0)
        k+=1
    ti = t[T1<t]
    for tk in ti:
        g[k] = inttrap(f, t, tk-T1, tk-T0)
        k+=1
    return g/(2*TW)


def expconv(f, T, t=None, dt=1.0):
    """Convolve a 1D-array with a normalised exponential.

    This function returns the convolution :math:`f(t)\\otimes\\exp(-t/T)/T` using an efficient and accurate numerical formula, as detailed in the appendix of `Flouri et al (2016) <https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.25991>`_ 

    Args:
        f (array_like): the 1D array to be convolved.
        T (float): the characteristic time of the normalized exponential function. 
        t (array_like, optional): the time points where the values of f are defined, in the same units as T. If t=None, the time points are assumed to be uniformly spaced with spacing dt. Defaults to None.
        dt (float, optional): spacing between time points for uniformly spaced time points. This parameter is ignored if t is explicity provided. Defaults to 1.0.

    Returns:
        numpy.ndarray: a 1D numpy array of the same length as f.

    See Also:
        `conv`, `biexpconv`, `nexpconv`, `stepconv`

    Notes: 
        `expconv` implements the same convolution product as `conv`, but is more accurate and faster in the special case where one of the factors is known to be an exponential:

        .. math::
            g(t) = \\frac{e^{-t/T}}{T} \\otimes f(t)

        In code this translates as:

        .. code-block:: python

            g = expconv(f, T, t)

        `expconv` should be used instead of `conv` whenever this applies. Since the transit time distribution of a compartment is exponential, this is an important use case.  

        `expconv` can calculate a convolution between two exponential factors, but in that case an analytical formula can be used which is faster and more accurate. It is implemented in the function `biexpconv`.

    Example:
        Import package and create a vector f:

        >>> import dcmri as dc
        >>> f = [5,4,3,6]

        Calculate :math:`g(t) = f(t) \\otimes \\exp(-t/3)/3` over a uniformly sampled grid of time points with spacing dt=1:

        >>> dc.expconv(f, 3)
        array([0.        , 1.26774952, 1.89266305, 2.6553402 ])

        Calculate the same convolution over a grid of time points with spacing dt=2:

        >>> dc.expconv(f, 3, dt=2)
        array([0.        , 2.16278873, 2.7866186 , 3.70082337])

        Calculate the same convolution over a non-uniform grid of time points:

        >>> t = [0,1,3,7]
        >>> dc.expconv(f, 3, t)
        array([0.        , 1.26774952, 2.32709015, 4.16571645])
    """

    if T==0: 
        return f
    f = np.array(f)
    n = len(f)
    t = tarray(n, t=t, dt=dt)
    g = np.zeros(n)
    x = (t[1:n] - t[0:n-1])/T
    df = (f[1:n] - f[0:n-1])/x
    E = np.exp(-x)
    E0 = 1-E
    E1 = x-E0
    add = f[0:n-1]*E0 + df*E1
    for i in range(0,n-1):
        g[i+1] = E[i]*g[i] + add[i]      
    return g


def biexpconv(T1, T2, t):
    """Convolve two normalised exponentials analytically.

    Args:
        T1 (float): the characteristic time of the first exponential function. 
        T2 (float): the characteristic time of the second exponential function, in the same units as T1. 
        t (array_like, optional): the time points where the values of f are defined, in the same units as T. 

    Returns:
        numpy.ndarray: The result of the convolution as a 1D array.

    See Also:
        `conv`, `expconv`, `nexpconv`, `stepconv`

    Notes: 
        `biexpconv` returns the exact analytical result of the following convolution:

        .. math::
            g(t) = \\frac{e^{-t/A}}{A} \\otimes \\frac{e^{-t/B}}{B}

        The formula is a biexponential with unit area:

        .. math::
            g(t) = \\frac{Ae^{-t/A}-Be^{-t/B}}{A-B}
    
        In code this translates as:

        .. code-block:: python
        
            g = biexpconv(A, B, t)

    Example:
        Import package and create a vector of uniformly sampled time points t with spacing 5.0s:

        >>> import dcmri as dc
        >>> t = 5.0*np.arange(4)

        Calculate the convolution of two normalised exponentials with time constants 10s and 15s:

        >>> g = dc.biexpconv(10, 15, t)
        array([-0.        ,  0.02200013,  0.02910754,  0.02894986])
    """
    if T1==T2:
        return (t/T1) * np.exp(-t/T1)/T1
    else:
        return (np.exp(-t/T1)-np.exp(-t/T2))/(T1-T2)


def nexpconv(n, T, t):
    """Convolve n identical normalised exponentials analytically.

    Args:
        n (float): number of exponentials. Since an analytical formula is used this can also be non-integer.
        T (float): the characteristic time of the exponential. 
        t (array_like, optional): the time points where the values of f are defined, in the same units as T. 

    Returns:
        numpy.ndarray: The result of the convolution as a 1D array.

    Raises:
        ValueError: if n<1 and if T<0

    See Also:
        `conv`, `expconv`, `biexpconv`, `stepconv`

    Notes: 
        `nexpconv` returns the exact analytical result of the following n convolutions:

        .. math::
            g(t) = \\frac{e^{-t/T}}{T} \\otimes \\ldots \\otimes \\frac{e^{-t/T}}{T} 

        The result is a gamma variate function with unit area:

        .. math::
            g(t) = \\frac{1}{\\Gamma(n)}\\left(\\frac{t}{T}\\right) \\frac{e^{-t/T}}{T} 

    Example:
        Import package and create a vector of uniformly sampled time points t with spacing 5.0s:

        >>> import dcmri as dc
        >>> t = 5.0*np.arange(4)

        Calculate the convolution of 4 normalised exponentials with time constants 5s:

        >>> g = dc.nexpconv(4, 5, t)
        array([0.        , 0.01226265, 0.03608941, 0.04480836])
    """
    if T<0:
        raise ValueError('T must be non-negative')
    if n<1:
        raise ValueError('n cannot be smaller than 1')
    if not isinstance(t, np.ndarray):
        t = np.array(t)
    u = t/T
    g = u**(n-1) * np.exp(-u)/T/gamma(n)
    if False in np.isfinite(g):
        # At large n the analytical formula runs into overflow
        # use numerical calculation in this case (slower and less accurate)
        g = np.exp(-t/T)/T
        n0 = int(np.floor(n))
        for _ in range(n0-1):
            g = expconv(g, T, t)
        if n!=n0:
            # Interpolate between n0 and n0+1
            g1 = expconv(g, T, t)
            u = n-n0
            g = g*u + g1*(1-u)
    return g

