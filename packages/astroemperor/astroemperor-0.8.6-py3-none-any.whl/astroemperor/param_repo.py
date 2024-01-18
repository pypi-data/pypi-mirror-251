# @auto-fold regex /^\s*if/ /^\s*else/ /^\s*def/
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version 1.0

# my coding convention
# **EVAL : evaluate the performance of this method
# **RED  : redo this
# **DEB  : debugging needed in this part
# **DEL  : DELETE AT SOME POINT
# **FIN  : Finish this

import numpy as np

def make_parameter(target):
    return {**dEmpty, **target}

dEmpty = { 'prior':'Uniform',
          'limits':[None, None],
          'value':-np.inf,
          'value_max':-np.inf,
          'value_mean':-np.inf,
          'value_median':-np.inf,
          
          'fixed':None,
          'prargs':None,
          'type':None,
          'ptformargs':None,
          'sigma':None,
          'GM_parameter':None,
          'posterior':None,
          'std':None,
          'sigma_frac_mean':None,
          
          'display_posterior':'',
          }


dPeriod = {'name':'Period',         
            'unit':'(Days)',        
            'is_circular':False,
            'is_hou':False,
            }

dAmplitude = {'name':'Amplitude',         
            'unit':r'($\frac{m}{s}$)',        
            'is_circular':False,
            'is_hou':False,
            }

dPhase = {'name':'Phase',         
            'unit':'(rad)',
            'is_circular':True,
            'is_hou':False,
            }

dEccentricity = {'name':'Eccentricity',         
            'unit':'',
            'is_circular':False,
            'is_hou':False,
            }

dLongitude = {'name':'Longitude',         
            'unit':'(rad)',
            'is_circular':True,
            'is_hou':False,
            }
######
dlPeriod = {'name':'lPeriod',         
            'unit':'(Days)',
            'is_circular':False,
            'is_hou':False,
            }

dAmp_sin = {'name':'Amp_sin',         
            'unit':r'($\frac{m}{s}$)',
            'is_circular':False,
            'is_hou':True,
            }


dAmp_cos = {'name':'Amp_cos',         
            'unit':'(rad)',
            'is_circular':False,
            'is_hou':True,
            }

dEcc_sin = {'name':'Ecc_sin',         
            'unit':'',
            'is_circular':False,
            'is_hou':True,
            }

dEcc_cos = {'name':'Ecc_cos',         
            'unit':'(rad)',
            'is_circular':False,
            'is_hou':True,
            }
#######

dT_0 = {'name':'T_0',         
            'unit':'(Days)',
            'is_circular':False,
            'is_hou':False,
            }

#######
#######
dOffset = {'name':'Offset',
           'unit':r'($\frac{m}{s}$)',
           'is_circular':False,
           'is_hou':False,
            }

dJitter = {'name':'Jitter',
           'unit':r'($\frac{m}{s}$)',
           'is_circular':False,
           'is_hou':False,
            }

dMACoefficient = {'name':'MACoefficient',
           'unit':r'($\frac{m}{s}$)',
           'is_circular':False,
           'is_hou':False,
            }

dMATimescale = {'name':'MATimescale',
           'unit':'(Days)',
           'is_circular':False,
           'is_hou':False,
            }

dStaract = {'name':'Staract',
           'unit':r'($\frac{m}{s}$)',
           'is_circular':False,
           'is_hou':False,
            }

#######
#######
dAcceleration = {'name':'Acceleration',
                 'unit':r'($\frac{m}{s^2}$)',
                 'is_circular':False,
                 'is_hou':False,
                }

#######
#######

dCeleJitter = {'name':'Jitter Term',
            'unit':r'($\frac{m}{s}$)',
            'is_circular':False,
            'is_hou':False,
             }

#######

dRealTerm_a = {'name':'Real Term a',
            'unit':r'($\frac{m}{s}$)',
            'is_circular':False,
            'is_hou':False,
             }

dRealTerm_c = {'name':'Real Term c',
            'unit':'',
            'is_circular':False,
            'is_hou':False,
             }

########

dRotationTerm_sigma = {'name':'Rotation Term sigma',
            'unit':r'($\frac{m}{s}$)',
            'is_circular':False,
            'is_hou':False,
             }

dRotationTerm_period = {'name':'Rotation Term period',
            'unit':'(days)',
            'is_circular':False,
            'is_hou':False,
             }

dRotationTerm_Q0 = {'name':'Rotation Term Q0',
            'unit':r'',
            'is_circular':False,
            'is_hou':False,
             }

dRotationTerm_dQ = {'name':'Rotation Term dQ',
            'unit':'',
            'is_circular':False,
            'is_hou':False,
             }

dRotationTerm_f = {'name':'Rotation Term f',
            'unit':r'',
            'is_circular':False,
            'is_hou':False,
             }

########
dMatern32Term_sigma = {'name':'Matern32 Term sigma',
            'unit':r'($\frac{m}{s}$)',
            'is_circular':False,
            'is_hou':False,
             }

dMatern32Term_rho = {'name':'Matern32 Term rho',
            'unit':r'',
            'is_circular':False,
            'is_hou':False,
             }

########


dCeleJitter = {'name':'Jitter Term',
            'unit':r'($\frac{m}{s}$)',
            'is_circular':False,
            'is_hou':False,
             }