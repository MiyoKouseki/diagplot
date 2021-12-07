from dtt2hdf import read_diaggui,DiagAccess # need
import re
import numpy as np
import gpstime

import warnings
warnings.simplefilter('ignore')

prefix = '/kagra/Dropbox/Measurements/VIS'
# ------------------------------------------------------------------------------
def search_fromto(opt,stg,excd,excp,dof,readp):
    '''
    '''
    _from = 'K1:VIS-{0}_{1}_{3}_{2}_OUT'.format(opt,stg,excd,excp)
    if 'GAS' in stg:
        _from = 'K1:VIS-{0}_{3}_{2}_{1}_OUT'.format(opt,stg,excp,excd)
        _to = 'K1:VIS-{0}_{3}_{2}_{1}_IN1_DQ'.format(opt,stg,readp,dof)
    else:
        if readp in ['BLEND_ACC','BLEND_LVDT']:
            #
            # FIX ME: should use *_OUT_DQ
            #
            _to = 'K1:VIS-{0}_{1}_{2}{3}_OUT'.format(opt,stg,readp,dof)
        elif readp in ['LVDTINF','ACCINF','OSEMINF']:
            #
            # FIX ME: should use *_OUT_DQ
            #
            _to = 'K1:VIS-{0}_{1}_{2}_{3}_OUT'.format(opt,stg,readp,dof) 
        elif readp in ['IDAMP','DAMP']:
            _to = 'K1:VIS-{0}_{1}_{2}_{3}_IN1_DQ'.format(opt,stg,readp,dof)
        else:
            raise ValueError('{0} is invalid readpoint.'.format(readp))
    return _from,_to

# ------------------------------------------------------------------------------
def read_tfdata(fname,chname_to,chname_from):
    '''
    '''
    print(chname_from,'->',chname_to)
    factor = -1 # unknown factor in dtt2xml bug.
    info = {}
    try:
        data = DiagAccess(fname)
        freq = data.xfer(chname_to,chname_from).FHz        
        coh = data.xfer(chname_to,chname_from).coh
        _tf = data.xfer(chname_to,chname_from).xfer        
        mag = np.abs(_tf)
        phase = np.rad2deg(np.angle(_tf))*factor        
        info['bw'] = data.xfer(chname_to,chname_from).BW
        info['ave'] = data.xfer(chname_to,chname_from).averages
        info['gps'] = data.xfer(chname_to,chname_from).gps_second
        info['win'] = data.xfer(chname_to,chname_from).window
        info['snr'] = data.xfer(chname_to,chname_from).SNR_estimate
    except RuntimeWarning:
        return None
    except ValueError as e:
        #print('ValueError',traceback.format_exc())
        print('- Invalid data',chname_from,chname_to,fname.split('_')[-1])
        return None
    except KeyError as e:
        #print('KeyError.',traceback.format_exc())
        print('- No channel',chname_from,chname_to,fname.split('_')[-1])
        return None
    except FileNotFoundError as e:
        #print('FileNotFoundError.',traceback.format_exc())
        print('- No file',fname)
        return None
    except AttributeError as e:
        print('AttributeError',traceback.format_exc())
        return None
    
    return freq,mag,phase,coh,info

# ------------------------------------------------------------------------------
def read_asd(fname,chname,savetxt=False):
    '''
    '''
    try:
        data = DiagAccess(fname)
        _freq = data.asd(chname).FHz
        _mag = data.asd(chname).asd
    except RuntimeWarning:
        return np.nan,np.nan
    except ValueError as e:
        print('ValueError',traceback.format_exc())
        return np.nan,np.nan
    except KeyError as e:
        #print('KeyError.',traceback.format_exc())
        return np.nan,np.nan
    except FileNotFoundError as e:
        #print('FileNotFoundError.',traceback.format_exc())
        return np.nan,np.nan
    except AttributeError as e:
        #print('AttributeError',traceback.format_exc())
        return np.nan,np.nan

    return _freq,_mag,_info
    
def read_diag(fname,chname_to,chname_from,savetxt=False,oltf=False):
    '''
    '''
    if chname_from!=chname_to:
        _freq,_mag,_angle,_coh,_info = read_tf(fname,chname_to,chname_from,
                                               savetxt=savetxt,oltf=oltf)
        return _freq,_mag,_angle,_coh,_info
    else:
        chname = chname_to
        _freq,_mag,_info = read_asd(fname,chname,savetxt=savetxt)
        return _freq,_mag,np.nan,np.nan,_info

# ------------------------------------------------------------------------------
def get_diagdata(tftype,grd,chname_from,chname_to,
                 refnum=0,savetxt=False,oltf=False):
    '''
    '''
    re_fmt = r'K1:VIS-([^_]+)_([^_]+)_([^_]+)_([^_]+)_([^_]+)'
    if 'GAS' in chname_from or 'GAS' in chname_to:
        optic,excdof,excpoint,stage,_   = re.match(re_fmt,chname_from).groups()
        optic,readdof,readpoint,stage,_ = re.match(re_fmt,chname_to).groups()        
    else:
        optic,stage,excpoint,excdof,_   = re.match(re_fmt,chname_from).groups()
        optic,stage,readpoint,readdof,_ = re.match(re_fmt,chname_to).groups()
    #
    fname = prefix+'/TF/{0}_{1}_{2}_{3}_{4}_{5}_{6}.xml'.format(
        tftype,grd,optic,stage,excpoint,excdof,refnum) # Fix me
    #
    if tftype in ['PLANT','OLTF']:            
        return read_diag(fname,chname_to,chname_from,savetxt=savetxt,oltf=oltf)
    elif tftype in ['SPECTRA']:
        chname = chname_to
        return read_diag(fname,chname,chname,savetxt=savetxt,oltf=oltf)
    else:
        raise ValueError('{0}'.format(tftype))
