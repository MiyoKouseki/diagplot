import sqlite3
from dttxml import DiagAccess
from dttxml import dtt_read
from gwpy.time import tconvert

class DiagDB():
    def __init__(self,dbname):
        self.dbname = dbname

    def __enter__(self):
        self.con = sqlite3.connect(self.dbname)
        self.cur = self.con.cursor()        
        return self

    def __exit__(self, exc_type, exc_value, traceback):        
        #self.cur.close()
        self.con.commit()
        self.con.close()
        
    def init_table(self):
        return _init_table(self.cur)

    def regist_diags(self,diagfnames):
        return _regist_diags(self.cur,diagfnames)

def get_diagdata(fname):    
    tree = ET.parse(fname)    
    root = tree.getroot()
    utc = root.findall("./*/Time[@Name='TestTimeUTC']")[0].text
    _num = root.findall("./*/Param[@Name='AChannels']")[0].text
    _fmt = "./*/Param[@Name='MeasurementChannel[{0}]']"
    ach = [root.findall(_fmt.format(i))[0].text \
           for i in range(int(_num))]       
    return utc,ach

def get_diagdata(fname):
    dacc = DiagAccess(fname)
    #channels = list(dacc.channels()[0])
    #print(dacc.asd(channels[0]))
    
    dacc = dtt_read(fname)
    channels = list(dacc.results.PSD.keys())
    _asd = dacc.results.PSD[channels[0]]
    utc = tconvert(int(_asd.gps_second))
    bw = _asd.BW
    ave = _asd.averages
    return utc,channels,bw,ave


def _init_table(cur):
    '''    
    diag.db 
     - measurements table: 測定ファイルのパスや測定日時など
     - channels table: チャンネルがどの測定ファイルにあるか
    Params:
    cur: dbcoursol
    '''
    create_table = '''
    CREATE TABLE measurements(
    id integer primary key autoincrement, 
    path text UNIQUE, 
    utc_date text, 
    bw float,
    ave int
    );
    CREATE TABLE channels(
    chname text, measurements_id integer,
    UNIQUE (chname, measurements_id)
    );'''
    cur.executescript(create_table)
    
    
def _regist_diags(cur,diagfnames):
    '''
    '''
    for diagfname in diagfnames:
        utc, achs, bw, ave = get_diagdata(diagfname)
        
        _cmd = """
        INSERT INTO measurements (path,utc_date,bw,ave)
        SELECT '{0}','{1}','{2}','{3}'
        WHERE NOT EXISTS (
        SELECT * FROM measurements
        WHERE path="{0}"
        )
        """.format(diagfname,utc,bw,ave)
        ans = cur.execute(_cmd)        
        print('{0} channels are found in {1}'.\
              format(len(achs),diagfname))
        
        measurements_id = ans.lastrowid        
        for chname in achs:
            _cmd = """
            INSERT INTO channels (chname,measurements_id)
            SELECT '{0}','{1}'
            WHERE NOT EXISTS (
            SELECT * FROM channels
            WHERE chname="{0}" AND measurements_id="{1}"
            )
            """.format(chname,measurements_id)            
            cur.execute(_cmd)
        
if __name__=='__main__':
    import xml.etree.ElementTree as ET
    import glob
    import os
    diagfnames = glob.glob('./test/data/*.xml')
        
    with DiagDB('diag.sql') as _db:
        _db.init_table()
        _db.regist_diags(diagfnames)
    
    chname = 'K1:VIS-ITMX_IP_IDAMP_T_IN1_DQ'
    with DiagDB('diag.sql') as _db:
        _get_fname = '''
        SELECT M.utc_date,M.bw,M.ave
        FROM channels AS C
          JOIN measurements AS M
          ON C.measurements_id=M.id
        where 
          C.chname like "{0}" AND
          M.utc_date >= '2021-11-01 00:00' AND
          M.utc_date <= '2021-12-01 18:00' 
        '''.format(chname)
        _db.cur.execute(_get_fname)
        for val in _db.cur.fetchall():
            print(val)
