from diag import Xfer,Asd
from search import find_xfers
from plot import Plot

import unittest
from test.data import xfer_info,asd_info

class TestRead(unittest.TestCase):
    def test_xfer_read(self):
        ''' 
        '''
        fname = './test/data/PLANT_ITMX_STANDBY_IM_TEST_L_0007.xml'
        chn_num   = 'K1:VIS-ITMX_IM_DAMP_L_IN1_DQ'
        chn_den = 'K1:VIS-ITMX_IM_TEST_L_EXC'        
        xfer = Xfer(fname,chn_num,chn_den)
        a = xfer.info()
        b = xfer_info
        self.assertEqual(a,b)

    def test_asd_read(self):
        ''' 
        '''
        fname = './test/data/PLANT_ITMX_STANDBY_IM_TEST_L_0007.xml'
        chn   = 'K1:VIS-ITMX_IM_DAMP_L_IN1_DQ'
        asd = Asd(fname,chn)
        a = asd.info()
        b = asd_info
        self.assertEqual(a,b)        

class TestPlot(unittest.TestCase):        
    def test_xfer_plot(self):
        ''' 
        '''
        fname = './test/data/PLANT_ITMX_STANDBY_IM_TEST_L_0007.xml'
        chn_num   = 'K1:VIS-ITMX_IM_DAMP_L_IN1_DQ'
        chn_den = 'K1:VIS-ITMX_IM_TEST_L_EXC'        
        xfer = Xfer(fname,chn_num,chn_den)
        fname = './test/data/PLANT_ITMX_STANDBY_IM_TEST_Y_0009.xml'
        chn_num   = 'K1:VIS-ITMX_IM_DAMP_Y_IN1_DQ'
        chn_den = 'K1:VIS-ITMX_IM_TEST_Y_EXC'        
        xfer2 = Xfer(fname,chn_num,chn_den)                
        plot = Plot(xfer,xfer2)
        plot.savefig('test_xfer_plot.png')
        plot.close()

    def test_asd_plot(self):
        ''' 
        '''
        fname = './test/data/PLANT_ITMX_STANDBY_IM_TEST_L_0007.xml'
        chn   = 'K1:VIS-ITMX_IM_DAMP_L_IN1_DQ'
        asd = Asd(fname,chn)        
        plot = Plot(asd)
        hoge = plot.savefig('test_asd_plot.png')
        plot.close()

# class TestSearch(unittest.TestCase):
#     def test_xfer_search(self):
#         import glob    
#         sources = glob.glob('./test/data/*.xml')
#         #chn_num   = 'K1:VIS-ITMX_IM_DAMP_L_IN1_DQ'
#         #chn_den = 'K1:VIS-ITMX_IM_TEST_L_EXC'
#         chn_num   = 'K1:VIS-ITMX_BF_COILOUTF_H3_IN1_DQ'
#         chn_den = 'K1:VIS-ITMX_IM_TEST_L_EXC'                        
#         find_xfers(sources,chn_num,chn_den)
#         pass
        
if __name__=='__main__':    
    unittest.main()    
