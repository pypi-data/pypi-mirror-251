import numpy as np
from scipy import stats
from scipy.interpolate import InterpolatedUnivariateSpline
from matplotlib import pyplot as plt
from Snoopy import logger
from Snoopy import Statistics as st
from Snoopy import Math as smath 
from scipy.optimize import minimize
import pandas as pd


def rolling_declustering( se , window=None, window_int=None ) : 
    """Return declustered events.
   
    Parameters
    ----------
    se : pd.Series
        Time series (time is index)
    window : float, optional
        window used to decluster the data. The default is None.
    window_int : int, optional
        window used to decluster the data, in number of time step. The default is None.

    Returns
    -------
    pd.Series
        The declustered sample
    """
    
    if window_int is not None : 
        # _se = se.reset_index(drop=True)
        # se_tmp = _se.rolling( window = window_int, min_periods=1, center=True, axis=0, closed = 'neither' ).max()   
        # se_tmp = se_tmp.loc[ se_tmp == _se ]
        # se_tmp.loc[ np.concatenate( [[True],(se_tmp.index[1:] - se_tmp.index[:-1]) >= window_int/2 ]) ]
        # se_tmp.index = se.index[se_tmp.index.values]
        
        # Faster version
        data_ = smath.movmax( se.values, window_int )
        id_max = np.where(data_ == se.values)[0]
        # Check for remaining case with small spacing (can happen if there several exact same value in the moving window)
        id_max_filtered = id_max[np.concatenate( [ [True], np.diff(id_max) >= window_int/2 ] )] 
        se_tmp = se.iloc[id_max_filtered]
    else :
        if isinstance(window,(pd._libs.tslibs.timestamps.Timestamp, pd._libs.tslibs.timestamps.Timedelta)):
            window = pd.tseries.frequencies.to_offset(window) # on convertit en offset
        se_tmp = se.rolling( window = window, min_periods=0, center=True, axis=0, closed = 'both' ).max()
        se_tmp = se_tmp.loc[ se_tmp == se ]
        se_tmp = se_tmp.loc[ np.concatenate( [[True], (se_tmp.index[1:] - se_tmp.index[:-1]) >= window/2] ) ]
    return se_tmp



#Gradient calculation for delta method's in use for CI
def gradXmTPareto(Zu , m, shape, scale):
    res = np.zeros((3))
    res[0] = scale*(m**(shape))*(Zu**(shape-1))
    res[1] = scale * (shape * ( m*Zu )**shape * np.log(m*Zu) - (m*Zu)**shape + 1) / shape**2
    res[2] = ((m*Zu)**shape - 1) / shape
    return res



# Faster than scipy.stats implementation. (no 'loc' parameter in our case), TODO : pass to c++ for efficiency ?
def nnlf_genpareto( shape_scale, data ):
    shape, scale = shape_scale
    good = np.where( data * shape  / scale > -1 + 1e-12  )[0]
    ngood = len(good)
    n = len(data)
    nbad = n - ngood
    if nbad > 0 : 
        penalty = st._xmax_log * nbad
        return penalty + ngood*np.log(scale) + ( 1. + 1. / shape)  * np.sum( np.log1p( shape * data[good] / scale) )
    else :
        return n*np.log(scale) + ( 1. + 1. / shape)  * np.sum( np.log1p( shape * data / scale) )
    
def nnlf_grad(coefs, x):
    res = np.empty((2))
    shape, scale = coefs
    res[0] = -np.sum((-shape * x * (shape + 1) + (scale + shape * x) * np.log((scale + shape * x) / scale)) / (shape**2 * (scale + shape * x)))
    res[1] = -np.sum((-scale + x) / (scale * (scale + shape * x)))
    return res



class POT():

    def __init__(self, sample, duration, threshold, time_label= "", variant = (0.,0.) ):
        """Peak over Threshold method to calcualte return values.
        
        Uses only empirical quantiles, for generalized pareto fit, see POT_GPD class. 

        Parameters
        ----------
        sample : np.ndarray
            Sample of independant observation
        duration : float
            Duration corresponding to the sample
        threshold : float
            Threshold
        """
        self.time_label = time_label #text refering to the unit of index, "" if not specified        
        if isinstance(sample, pd.core.series.Series):
            self._sample = sample.values
            self._sample_time = sample
        else :
            self._sample = sample
        
        if not isinstance(duration, (int, float)):
            duration = duration.total_seconds()/3600 #length of the sample in hours, TDB : is there a need to adapt with others time_label ? 
            self.time_label = "Hours"

        self.duration = duration
        
        
        self.time_step = self.duration / self._sample.size #value of timeStep (in time_label) between two consecutive sampled values
        
        self.threshold = threshold
        
        self.extremes = np.sort( sample[sample >= threshold] )
        self.exceedances = self.extremes - self.threshold
        
        #proportion of peaks over threshold in all observations (estimator for Probability of exceending threshold u)
        self.exceedance_ratio =  float( len(self.extremes)  / self._sample.size )
        
        #frequency of extremes above threshold
        self.f = len(self.extremes) / self.duration
        
        #Which variant for the empirical quantile calculation
        self._variant = variant
        
        #Interpolator, not always needed ==> lazy evaluated
        self._x_to_rp_empirical = None
        self._rp_to_x_empirical = None
        
        self._bootstrap_objects = []


        
    def x_to_rp_empirical(self, x):
        """Return period from return value, using interpolation between data.

        Parameters
        ----------
        x : float
            Return value

        Returns
        -------
        float
            Return period
        """
        if self._x_to_rp_empirical is None : 
            self._build_interp_x_to_rp()
        return self._x_to_rp_empirical(x)
    
    def rp_to_x_empirical(self, x):
        """Return value from return period.

        Parameters
        ----------
        rp : float
            return period

        Returns
        -------
        float
            return value
        """
        if self._rp_to_x_empirical is None : 
            self._build_interp_rp_to_x()
        return self._rp_to_x_empirical(x)    
            

    def _build_interp_rp_to_x(self):
        # Build interpolator
        logger.debug("Build return level interpolator")
        self._rp_to_x_empirical = InterpolatedUnivariateSpline( self.empirical_rp , self.extremes, ext = "raise", k = 1 )

    def _build_interp_x_to_rp(self):
        # Build interpolator
        logger.debug("Build return level interpolator")
        self._x_to_rp = InterpolatedUnivariateSpline( self.extremes , self.empirical_rp, ext = "raise", k = 1)


    @classmethod
    def FromTimeSeries( cls, se, duration, threshold = None, threshold_q = None, window = None , window_int = None, **kwargs ):
        """Create POT analysis using time series as input
        
        Parameters
        ----------
        se : pd.Series
            The time signal.
        duration : float
            Duration associated to the time-series.
        threshold : float
            Threshold.
        treshold_q : float
                Threshold.
        window : float, optional
            window used to decluster the data. The default is None.
        window_int : int, optional
            window used to decluster the data, in number of time step. The default is None.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        The POT analysis class
        """
        sample = rolling_declustering( se, window = window, window_int = window_int )
        
        if threshold_q is not None :
            threshold = np.quantile( sample, threshold_q, method = 'weibull') # Weibull corresponds to "i / (n+1)" method
        POT =  cls( sample.values, duration, threshold = threshold, **kwargs )
        POT._sample_time = sample
        return(POT)
    
    @property    
    def empirical_rp( self  ):
        """Return empirical return period of events above threshold (sorted).

        Parameters
        ----------
        variant : (float,float) or str, optional
            DESCRIPTION. The default is (0.0, 0.0), which corresponds to i/(n+1)

        Returns
        -------
        np.ndarray
            Return period of events above threshold (sorted).
        """
        return 1 / ( self.f * st.probN( len(self.extremes), variant = self._variant ) )

    @property
    def empirical_rv( self ):
        """Return "empirical values" of events above threshold (sorted).
        
        Keeped for compatibility between BM.rl API and PoT.
        """
        return self.extremes
    
    
    def empirical_rp_ci(self , alpha_ci):
            """Lower and upper bound of RP confidence interval of threshold exceedance.
    
            NOTE
            ----
            Not sure this correct, the uncertainity on frequency should be added ?
    
            Parameters
            ----------
            alpha : float, optional
                1 - Size of the confidence interval.
    
            Returns
            -------
            np.ndarray
                RP_low, RP_up
            """
            p_low , p_high = st.probN_ci( len(self.extremes), alpha = alpha_ci )
            return 1 / ( self.f * p_low  ), 1 / ( self.f *  p_high )
    

    def plot_rp_data(self, ax = None, variant = (0.0 , 0.0), marker = "+", linestyle = "", **kwargs):
        """Plot empircal value against return period.
        
        Parameters
        ----------
        ax : TYPE, optional
            DESCRIPTION. The default is None.
        variant : TYPE, optional
            DESCRIPTION. The default is (0.0 , 0.0).
        marker : TYPE, optional
            DESCRIPTION. The default is "+".
        linestyle : TYPE, optional
            DESCRIPTION. The default is "".

        Returns
        -------
        ax : TYPE
            DESCRIPTION.
        """
        
        if ax is None :
            fig, ax = plt.subplots()

        ax.plot( self.empirical_rp,  self.extremes, marker = marker , linestyle=linestyle, **kwargs)
        ax.set_xscale("log")
        return ax
    
    
    def plot_rp_data_ci(self, alpha_ci, ax=None, alpha = 0.5, data = "above_threshold", **kwargs) : 
        if ax is None :
            fig, ax = plt.subplots()
            
        if data == "above_threshold" :
            rp_low, rp_high = self.empirical_rp_ci(alpha_ci = alpha_ci)
            ax.fill_betweenx( self.extremes, rp_low, rp_high , alpha = alpha, **kwargs)
        elif data == "all" : 
            rl = st.ReturnLevel( self._sample, duration=self.duration, variant = self._variant )
            rl.plot_rp_ci(alpha_ci = alpha_ci, ax=ax, **kwargs)
            
        ax.set_xscale("log")

        
    def plot_threshold(self, ax=None):
        """Plot time trace, together data above threshold.
        """
        if hasattr(self, "_sample_time") == False:
            time_labeled=False
            sample_ = self._sample   
        else :
            time_labeled=True
            sample_ = self._sample_time
            
                
        if ax is None :
            fig , ax = plt.subplots()

        ax.plot( sample_ )
        if time_labeled:
            ax.plot( sample_.loc[sample_ > self.threshold] , marker = "+" , markersize=6, linestyle = "" )
        else:
            mask = np.isin(sample_, self.extremes, invert=True)
            ax.plot( np.ma.masked_array(data = sample_ , mask = mask, fill_value=np.nan )   , marker = "+" , markersize=4, linestyle = "" )
        ax.axhline(y=self.threshold, c= "red", linestyle = ":", linewidth = 2)
        xlabel = "Time"
        if self.time_label != "":
            xlabel += f" in {self.time_label}"
        ax.set_xlabel( xlabel )

        return ax



class POT_GPD( POT ):
    
    def __init__(self, sample, duration , threshold , time_label= "", shape_bounds = (-np.inf, 1.0), scale_bounds = (1e-12 , np.inf), solver = "minimize_mle", fit_kwargs = {}, mle_penalty = 1e20):
        """Peak over threshold, extremes are fitted with Generalize Pareto Distribution.
        
        Parameters
        ----------
        sample : np.ndarray
            Sample of independant observation
        duration : float
            Duration corresponding to the sample
        threshold : float
            Threshold
        shape_bounds : tuple, optional
            Bounds for the shape parameter
        solver : str, optional
            Which library to use for minimizing the likelyhood
        fit_kwargs : dict, optional
            Argument pass to scipy.stats.rv_continous.fit or scipy.optimize.minimize
        """
        POT.__init__(self , sample, duration , threshold, time_label=time_label)
        
        self._solver = solver

        # Update default minimizer settings        
        self._fit_kwargs = {}
        if self._solver == "minimize_mle":
            self._fit_kwargs = {"method" : "nelder-mead"}
        self._fit_kwargs.update( fit_kwargs )
        
        self.shape_bounds = shape_bounds
        self.scale_bounds = scale_bounds

        # Fitted gpd distribution, lazily evaluated
        self._gpd = None
        self._mle_penalty = mle_penalty
        

    
    def _fit(self):
        # Start coefficients, from method of moments        
        mu = np.mean(self.exceedances)
        s = np.std(self.exceedances)
        _shape = 0.5 * (1-( mu/s )**2  )
        _scale = mu * ( 1-_shape)
        
        if self._solver == "minimize_mle" :  # Generally faster than stats.genpareto.fit
            res = minimize( st.genpareto_2p.nnlf, x0 = [np.clip( _shape, *self.shape_bounds) , np.clip(_scale, *self.scale_bounds) ], args = (self.exceedances,self._mle_penalty), bounds = ( self.shape_bounds, self.scale_bounds ),  **self._fit_kwargs )
            self._shape , self._scale = res.x
        elif self._solver == "genpareto.fit" : 
            self._shape , _ , self._scale = stats.genpareto.fit( self.exceedances, _shape, scale = _scale, floc=0, **self._fit_kwargs)
        elif self._solver == "mom" : 
            self._shape , self._scale = _shape, _scale
        else : 
            raise(Exception())

        self._gpd = stats.genpareto(self._shape , 0.0 , self._scale)
        
        
    @property
    def gpd(self):
        if self._gpd is None:
            self._fit()
        return self._gpd

    @property
    def shape(self):
        return self.gpd.args[0]

    @property
    def scale(self):
        return self.gpd.args[2]
    

    def shape_ci(self, ci_level):
        coef = stats.norm.ppf( 0.5*(1. - ci_level) )
        var = self._variance_matrix()
        return self.shape - coef * var[ 1,1 ]**0.5, self.shape + coef * var[ 1,1 ]**0.5
    
    def scale_ci(self, ci_level):
        coef = stats.norm.ppf( 0.5*(1. - ci_level) )
        var = self._variance_matrix()
        return self.scale - coef * var[ 2,2 ]**0.5, self.scale + coef * var[ 2,2 ]**0.5
    
    @property
    def nnlf(self):
        """Negative loglikelyhood"""
        # return nnlf_genpareto( [self._shape , self.scale] , self.exceedances )  # penalized nnlf
        return stats.genpareto.nnlf( [self._shape , 0.0 , self.scale] , self.exceedances )
        
    
    @property
    def ks(self):
        """Return ks test p-value."""
        return stats.kstest(self.exceedances , self.gpd.cdf ).pvalue
    
    def x_to_rp( self, x ) :
        """Calculate return period from return value acc. to fitted distribution

        Parameters
        ----------
        x : float or np.ndarray
            Return value

        Returns
        -------
        float or np.ndarray
            return period
        """
        return  1 /  (self.f * ( self.gpd.sf( x - self.threshold  ))  )
        
    def rp_to_x(self , rp):
        """Provide return value at RP acc. to fitted distribution.
        
        Parameters
        ----------
        rp : float or array
            Return period.

        Returns
        -------
        float or np.ndarray
             Return value
        """
        return self.threshold + self.gpd.ppf( 1. - ( 1 / (rp * self.f ) ))
    
    def bootstrap(self, n = 1000):
        """Bootstrap the POT analysis.

        Parameters
        ----------
        n : int, optional
            Number of re-sample. The default is 1000.
        """
        logger.debug(f"Bootstrapping with n = {n:}")
        for i in range(n) : 
            self._bootstrap_objects.append( self.__class__( np.random.choice( self._sample , size = len(self._sample)  ) ,
                                                          duration = self.duration,
                                                          threshold = self.threshold,
                                                          fit_kwargs = self._fit_kwargs,
                                                          shape_bounds = self.shape_bounds,
                                                          scale_bounds = self.scale_bounds ))

    def rp_to_rel_ci(self, rp, ci_level=0.95, ci_type="bootstrap"):
        """Provides the relative error on x for a given RP and a given confidence-level.
        
        Parameters 
        ----------
        rp : float or array
            Return period.
        ci_level : in [0, 1], 
            Confidence-level
        ci_type : str
            Method in use to compute Confidence Intervals
        Returns
        -------
            float,
        Relative error on Return Value at a given confidence-Level
        """
        x = self.rp_to_x(rp)
        xci = self.rp_to_xci(rp=rp, ci_level=ci_level, ci_type=ci_type)
        return( np.mean([xci[1]-x, x-xci[0]]) /x )
    

    def rp_to_xci(self, rp, ci_level=0.95, ci_type = "delta", n_bootstrap = 1000):
        """Return lower and upper bound of the confidence interval.

        Parameters
        ----------
        rp : float or array
            Return period.
        ci_level : float
            Centered confidence interval.
        ci_type : str, optional
            How the CI is evaluated. The default is "bootstrap".
        n_bootstrap : int, optional
            Number of re-sample for the bootstrap. The default is 1000.

        Returns
        -------
        x_low : float or array
            Lower bound of the confidence interval.
        x_up : float or array
            Upper bound of the confidence interval.
        """
        if isinstance(rp, (float, int)):
            rp = np.array([rp])


        if ci_type == "bootstrap":
            alpha_ci = 1 - ci_level
            if len(self._bootstrap_objects) < n_bootstrap :
                self.bootstrap( n_bootstrap - len(self._bootstrap_objects) )
            v = [ b.rp_to_x( np.array(rp)) for b in self._bootstrap_objects ]
            x_low = np.quantile(v , alpha_ci/2 , axis = 0, method = "weibull")
            x_high = np.quantile(v , 1-alpha_ci/2 , axis = 0, method = "weibull")
            return x_low, x_high
        
        elif ci_type == "delta":
            #Compute the confidence interval

            #Do not compute under threshold value
            #ci = ci.loc[  ci.index > rpu  , : ]
            VarMatrix = self._variance_matrix()
    
            #-------  Delta method
            #Comute coefficient from confidence level assuming the asymptotic normal distribution
            x_low = np.zeros(rp.shape)
            x_high = np.zeros(rp.shape)
            coef = stats.norm.ppf( 0.5*(1. - ci_level) )
            m = rp / self.time_step #RP unit is equal to "1"
            R = self.rp_to_x( rp )
            

            for i in range(len(rp)) :
                dtxT =  gradXmTPareto(self.exceedance_ratio , m[i], self.shape, self.scale)
                Y = np.matmul(  dtxT , VarMatrix )
                VarXm = np.matmul( Y , dtxT )
                x_low[i] = R[i] + coef*(VarXm**0.5)
                x_high[i] = R[i] - coef*(VarXm**0.5)
                
            return x_low, x_high

        else : 
            raise(Exception( f"ci_type {ci_type:} is not known" ))    


    def _variance_matrix(self):
        #Variance on exceedance probability of u, using binomial approximation
        VarZu = self.exceedance_ratio * ( 1 - self.exceedance_ratio ) / self._sample.size

        #Return period of the threshold
        #rpu = 1. / (self.time_step  * self.exceedance_ratio) #TO BE ISSUED : SU_T vs. SU in droppy (np of clusters vs. nb of peaks)... + what if there are NaN ?

        #Variance-Covariance matrix
        VarMatrix = np.zeros( (3,3)  )
        
        HessianMatrix = np.zeros((2, 2))
        # d2L/dshape2
        HessianMatrix[0, 0] = -np.sum(-(2 * self.scale**2 * np.log(1 + self.shape * self.exceedances / self.scale) + 4 * self.scale * self.shape * self.exceedances * np.log(1 + self.shape * self.exceedances / self.scale) - 2 * self.scale * self.shape * self.exceedances - self.shape**3 * self.exceedances**2 + 2 * self.shape**2 * self.exceedances**2 * np.log(1 + self.shape * self.exceedances / self.scale) - 3 * self.shape**2 * self.exceedances**2) / (self.shape**3 * (self.scale + self.shape * self.exceedances)**2))
        # d2L/dscaleshape
        HessianMatrix[0, 1] = -np.sum(-self.exceedances * (1 + self.shape * self.exceedances / self.scale)**(-1 - 1 / self.shape) * (1 + self.shape * self.exceedances / self.scale)**(1 + 1 / self.shape) * (-self.scale + self.exceedances) / (self.scale * (self.scale + self.shape * self.exceedances)**2))
        # d2L/dscaleshape
        HessianMatrix[1, 0] = HessianMatrix[0, 1]
        # d2L/dscale2
        HessianMatrix[1, 1] = -np.sum((self.scale**2 - 2 * self.scale * self.exceedances - self.shape * self.exceedances **2) / (self.scale**2 * (self.scale**2 + 2 * self.scale * self.shape * self.exceedances + self.shape**2 * self.exceedances**2)))
        
        invHessian = np.linalg.inv(HessianMatrix)
        VarMatrix[0,0] = VarZu
        VarMatrix[1:3,1:3] = invHessian
        
        return VarMatrix
        

    
    def plot_rp_fit(self, rp_range=None, ax=None, **kwargs):
        """Plot return value against return period.
        
        Parameters
        ----------
        rp_range : np.ndarray or None, optional
            Range of RP to plot. The default is None.
        ax : plt.Axis, optional
            The figure. The default is None.

        Returns
        -------
        plt.Axis, optional
            The figure
        """
        
        if ax is None :
            fig, ax= plt.subplots()
            
        if rp_range is None : 
            _x = self.empirical_rp
            rp_range = np.logspace(  np.log10( np.min( _x ) ) , np.log10(np.max( _x ))*1.05   , 200 )
            
            
        ax.plot( rp_range , self.rp_to_x( rp_range ), **kwargs )
        ax.set_xscale("log")
        ax.set( xlabel = "Return period" )
        return ax
    
            
     
    def plot_rp_ci( self, ci_level=0.95, rp_range = None, ax=None, ci_type = "bootstrap", plot_type = "fill_between", alpha = 0.25, **kwargs) : 
        """Plot return value CI against return period.
        
        Parameters
        ----------
        rp_range : np.ndarray or None, optional
            Range of RP to plot. The default is None.
        alpha_ci : float
            Centered confidence interval.
        ci_type : str, optional
            How the CI is evaluated. The default is "bootstrap".
        ax : plt.Axis, optional
            The figure. The default is None.

        Returns
        -------
        plt.Axis
            The figure
        """
        if ax is None :
            fig, ax= plt.subplots()
            
        if rp_range is None : 
            _x = self.empirical_rp
            rp_range = np.logspace(  np.log10( np.min( _x ) ) , np.log10(np.max( _x ))*1.5   , 200 )
        
        x_low, x_high = self.rp_to_xci( rp = rp_range, ci_level=ci_level , ci_type = ci_type )

        if plot_type == "fill_between":
            ax.fill_between( rp_range, x_low, x_high, alpha = alpha, label=  f"{ci_type} - CI,  level = {ci_level}", **kwargs)
            ax.set_xscale("log")
        elif ci_type == "delta":
            ax.plot(x_low, label = f"Min + level = {ci_level}")
            ax.plot(x_high, label = f"Max + level = {ci_level}")
        ax.legend()
            
        return ax



class ThresholdSensitivity():

    def __init__(self, threshold_range,  **kwargs ):
        """Peak over threshold, extremes are fitted with Generalize Pareto Distribution.
        
        Parameters
        ----------
        threshold_range : np.ndarray
            Range of threshold to investigate
        **kwargs : any
            Argument passed to POT_GPD()
        """
        self.pot_l = []
        self.threshold_range = threshold_range
        for t in threshold_range : 
            self.pot_l.append( POT_GPD( **kwargs, threshold = t ) )
            
            
    def plot( self, ci_level = 0.95, plots = [ "mr" , "scale" , "shape" ] , rps = [] ):
        """Plot sensitivity to threshold.

        Parameters
        ----------
        ci_level : float, optional
            Size of centered CI. The default is 0.95.
        plots : list, optional
            What to plot. The default is [ "mr" , "scale" , "shape" ].
        rps : list, optional
            List of return period on which the sensitivity is to be evaluated. The default is [].
            
        Returns
        -------
        axs : list
            list of plt.Axes
        """
        
        fig, axs = plt.subplots( nrows = len(plots) + len(rps), sharex = True )
        if not hasattr( axs , "__len__" ):
            axs = [axs]
        
        ip = 0
        for rp in rps : 
            xrp = [ pot.rp_to_x(rp) for pot in self.pot_l  ]
            xrp_ci = np.array( [ pot.rp_to_xci(rp, ci_level) for pot in self.pot_l  ] ).reshape( len(self.threshold_range),2 )
            
            axs[ip].plot( self.threshold_range, xrp  )
            axs[ip].fill_between( self.threshold_range, xrp_ci[:,0] , xrp_ci[:,1] , alpha = 0.3)
            axs[ip].set(ylabel = f"RP = {rp:}")
            ip += 1
            
        if "shape" in plots : 
            shape = [ pot.shape for pot in self.pot_l  ]
            shape_ci = np.array([ pot.shape_ci(ci_level) for pot in self.pot_l  ])

            axs[ip].plot( self.threshold_range, shape  )
            axs[ip].fill_between( self.threshold_range, shape_ci[:,0] , shape_ci[:,1] , alpha = 0.3)
            axs[ip].set(ylabel = "shape")
            ip += 1
            

        if "scale" in plots :
            scale = [ pot.scale for pot in self.pot_l  ]
            scale_ci = np.array( [ pot.scale_ci(ci_level) for pot in self.pot_l  ] )
            
            axs[ip].plot( self.threshold_range, scale  )
            axs[ip].fill_between( self.threshold_range, scale_ci[:,0] , scale_ci[:,1] , alpha = 0.3)
            axs[ip].set(ylabel = "scale")
            ip += 1
            
        # Mean residual life
        if "mr" in plots : 
            MeanResidualLife( self.pot_l[0]._sample, threshold_range = self.threshold_range, ci_level = ci_level).plot(ax = axs[ip])
            ip += 1
            
        axs[-1].set(xlabel = "Threshold")

        return axs
        



class MeanResidualLife(  ):
    """Compute mean residual life (to assess threshold for POT).
    
    The mean residual life can help in the selection of appropriate threshold. Theoretically, threshold should be selected above a value for which the mean resiudatl life is approximately linear; the GPD assumption for threshold exceedance would then be valid.
    """
    
    def __init__(self, data, threshold_range = None ,  ci_level = 0.95 ):
        """Mean residual life calculation.
        
        Parameters
        ----------
        data : pd.Series
            The data
        threshold_range : np.ndarray (1d), optional
            Threshold range to investigate. The default is None.
        ci_level : float, optional
            Size of the centered confidence interval. The default is 0.95.
        """
        
        if threshold_range is None :
            threshold_range = np.linspace( 0.1*max(data) , 0.95*max(data) , 200  )
            
        self.df = pd.DataFrame( index = threshold_range )
        coef = stats.norm.ppf( 0.5*(1. - ci_level) )
        self.ci_level =  ci_level

        for u in self.df.index :
            excess = data [ data >= u ]
            self.df.loc[u, "Mean"] = np.mean( excess  ) - u
            self.df.loc[u, "Sigma"] = np.std( excess ) / (len(excess))**0.5
        self.df.loc[:, "Max"] = self.df.loc[:, "Mean"] - coef * self.df.loc[:, "Sigma"]
        self.df.loc[:, "Min"] = self.df.loc[:, "Mean"] + coef * self.df.loc[:, "Sigma"]
        
    
    def plot(self, ax = None, color = "darkblue"):
        """Plot Mean Residual life.

        Parameters
        ----------
        ax : plt.Axes, optional
            Where to plot. The default is None.
        color : str, optional
            Color. The default is "darkblue".

        Returns
        -------
        ax : plt.Axes
            The plot.
        """
        
        if ax is None :
            fig , ax = plt.subplots()
        ax.plot( self.df.index , self.df.Mean , color = color, label = "Mean residual life" )
        ax.fill_between( self.df.index , self.df.Min , self.df.Max, alpha = 0.3 , color = color, label = f"CI {self.ci_level:.2%}")
        ax.plot( self.df.index , self.df.Max , linestyle = "--"  , linewidth = 0.5, color = color)
        ax.plot( self.df.index , self.df.Min , linestyle =  "--" , linewidth = 0.5, color = color )
        ax.set_xlabel( "Threshold" )
        ax.set_ylabel( "Mean excess" )
        ax.legend()
        return ax
    
    

if __name__ == "__main__" : 

    from Snoopy.TimeDomain import TEST_DIR
    
    data = pd.read_csv( f"{TEST_DIR}/hs.csv", index_col = 0 , parse_dates = True ).hs
    duration = len(data) / 2922
    data_decluster = rolling_declustering( data, window = pd.offsets.Day(2) )
    
    mr = MeanResidualLife( data_decluster )
    mr.plot()

    pot = POT_GPD.FromTimeSeries( se = data, duration=duration, threshold = np.quantile(data_decluster, 0.9), window = pd.offsets.Day(2), solver = "minimize_mle" )
    
    fig, ax = plt.subplots()
    pot.plot_threshold(ax=ax)
    
    fig, ax = plt.subplots()
    pot.plot_rp_data(ax=ax, label = "data")
    pot.plot_rp_fit(ax=ax, label = "GPD")
    pot.plot_rp_ci(ax=ax, ci_level=0.95, ci_type = "delta",  color = "blue")
    pot.plot_rp_ci(ax=ax, ci_level=0.95, ci_type = "bootstrap",  color = "red")

    t = ThresholdSensitivity( sample = data_decluster, duration=duration, threshold_range = np.arange(6.0 , 14. , 0.1) )
    t.plot(  rps = [100.] )
