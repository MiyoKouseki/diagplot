from dttxml import DiagAccess
from dttxml.access import DiagXferHolder, DiagASDHolder
from matplotlib import figure
from matplotlib.gridspec import GridSpec
import numpy as np

class HogeError(Exception):        
    pass


def is_valid_channel(daccess,chn):
    chns = daccess.channels()
    if (chn in chns[0]) or (chn in chns[1]):
        return True
    else:
        raise HogeError('Invalid channel')
    

class Xfer(DiagXferHolder):
    def __init__(self,fname,chn_num,chn_den):
        self.daccess = DiagAccess(fname)                    
        super().__init__(self.daccess,chn_num,chn_den)

        
class Asd(DiagASDHolder):
    def __init__(self,fname,chn):
        daccess = DiagAccess(fname)
        super().__init__(daccess,chn)


AXES_PARAMS = [
    'projection', 'title',  # standard options
    'sharex', 'xlim', 'xlabel', 'xscale',  # X-axis params
    'sharey', 'ylim', 'ylabel', 'yscale',  # Y-axis params
    'epoch', 'insetlabels',  # special GWpy extras
]

class Plot(figure.Figure):
    def __init__(self, *data, **kwargs):
        super().__init__(figsize=(8,10),dpi=100)
        self._init_axes(data,**kwargs)
        
    def _init_axes(self,data,**kwargs):
        axes_kw = {key: kwargs.pop(key) for key in AXES_PARAMS if
                   key in kwargs}

        # fixme
        if all([isinstance(_data,Asd) for _data in data]):
            nrows, ncols = 1,1
            huge = 'asd' #fixme
        elif all([isinstance(_data,Xfer) for _data in data]):
            nrows, ncols = 3,1
            huge = 'xfer' #fixme
        else:
            raise HogeError('hoge')

        # fixme
        gs = GridSpec(nrows, ncols)
        for row in range(nrows):
            for col in range(ncols):
                axes_kw['xscale'] = 'log'                
                axes_kw['yscale'] = 'log'
                if row==2: #fixme
                    axes_kw['xlabel'] = 'Frequency[Hz]'
                axes_kw['ylabel'] = ''
                ax = self.add_subplot(gs[row,col], **axes_kw)
                
                # fixme
                plot_func = getattr(ax, 'plot')            
                for _data in data:
                    if huge=='asd':
                        plot_func(_data.FHz,_asd.asd)
                    elif huge=='xfer':
                        if row==0:
                            plot_func(_data.FHz,np.abs(_data.xfer))
                        elif row==1:
                            plot_func(_data.FHz,np.rad2deg(np.angle(_data.xfer)))
                        elif row==2:
                            plot_func(_data.FHz,_data.coh)
                        else:
                            raise HogeError('')
                    else:
                        raise HogeError('')
            
    def close(self):
        from matplotlib.pyplot import close
        close(self)
        
if __name__=='__main__':
    import glob    
    xmlfiles = glob.glob('./test/data/*.xml')    
    fname1 = xmlfiles[0]
    fname2 = xmlfiles[1]    
    
    _from = 'K1:VIS-ITMX_BF_COILOUTF_V1_EXC'
    _to   = 'K1:VIS-ITMX_BF_LVDTINF_V1_OUT_DQ'

    xfer = Xfer(fname1,_from,_to)
    asd1 = Asd(fname1,_to)
    asd2 = Asd(fname2,_to)
    #plot = Plot(asd1,asd2)
    #plot = Plot(asd1)
    plot = Plot(xfer)
    plot.savefig('hoge.png')
    plot.close()
