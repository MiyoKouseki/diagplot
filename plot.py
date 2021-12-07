import numpy as np
from matplotlib import figure
from matplotlib.gridspec import GridSpec
from error import HogeError

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
        from diag import Asd, Xfer # fixme
        if all([isinstance(_data,Asd) for _data in data]):
            nrows, ncols = 1,1
            huge = 'asd' #fixme
        elif all([isinstance(_data,Xfer) for _data in data]):
            nrows, ncols = 3,1
            huge = 'xfer' #fixme
        else:
            print(data)
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
                        plot_func(_data.FHz,_data.asd)
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
