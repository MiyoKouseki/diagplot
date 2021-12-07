from dttxml import DiagAccess
from dttxml.access import DiagXferHolder, DiagASDHolder


class Xfer(DiagXferHolder):
    def __init__(self,fname,chn_num,chn_den):
        self.fname = fname
        daccess = DiagAccess(self.fname)                    
        super().__init__(daccess,chn_num,chn_den)

    def info(self):
        _dict = {'fname':self.fname,
                 'gpstime':str(self.gps_second),
                 'chn_num':self.chn_num,
                 'chn_den':self.chn_den,
                 'bw':str(self.BW),
                 'ave':str(self.averages),
                 'window':self.window
                 }
        return _dict
        
    def __str__(self):
        txt = [ key+':'+value for key, value in self.info().items()]
        return txt
        
class Asd(DiagASDHolder):
    def __init__(self,fname,chn):
        self.fname = fname        
        daccess = DiagAccess(self.fname)
        super().__init__(daccess,chn)

    def info(self):
        _dict = {'fname':self.fname,
                 'gpstime':str(self.gps_second),
                 'chn':self.chn,
                 'bw':str(self.BW),
                 'ave':str(self.averages),
                 'window':self.window
                 }
        return _dict
        
    def __str__(self):
        txt = [ key+':'+value for key, value in self.info().items()]
        return txt
        

def is_valid_channel(daccess,chn):
    chns = daccess.channels()
    if (chn in chns[0]) or (chn in chns[1]):
        return True
    else:
        raise HogeError('Invalid channel')
        
