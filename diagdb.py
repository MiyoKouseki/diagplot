import sqlite3

class DiagDB():
    def __init__(self,dbname):
        self.dbname = dbname

    def __enter__(self):
        self.con = sqlite3.connect(self.dbname)
        self.cur = self.con.cursor()        
        return self

    def __exit__(self, exc_type, exc_value, traceback):        
        self.cur.close()
        self.con.commit()
        self.con.close()
        print('close')
        
    def init_db(self):
        return _init_db(self.cur)

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


def _init_db(cur):
    '''    
    diag.db 
     - measurements table: 測定ファイルのパスや測定日時など
     - channels table: チャンネルがどの測定ファイルにあるか
    Params:
    cur: dbcoursol
    '''    
    cur.execute('''CREATE TABLE measurements
    (fname text unique, date text)''')        
    cur.execute('''CREATE TABLE channels
    (chname text, fname text)''')            
    
    
def _regist_diags(cur,diagfnames):
    '''
    '''
    for diagfname in diagfnames:
        utc, achs = get_diagdata(diagfname)        
        cur.execute("INSERT INTO measurements VALUES ('{0}','{1}')".\
                    format(diagfname,utc))
        for chname in achs:
            cur.execute("INSERT INTO channels VALUES ('{0}','{1}')".\
                        format(chname,diagfname))                    
        print('{0} channels are found in {1}'.format(len(achs),diagfname))    
        
if __name__=='__main__':
    import xml.etree.ElementTree as ET
    import glob
    import os
    diagfnames = glob.glob('./test/data/*.xml')
        
    # with DiagDB('diag.sql') as _db:
    #     _db.init_db()
    #     _db.regist_diags(diagfnames[:5])

    # with DiagDB('diag.sql') as _db:
    #     _db.regist_diags(diagfnames[5:10])    
    
    chname = 'K1:VIS-ITMX_IP_IDAMP_T_IN1_DQ'
    with DiagDB('diag.sql') as _db:
        _cmd = 'SELECT fname FROM channels where chname like "{0}"'.\
            format(chname)
        _db.cur.execute(_cmd)
        for val in _db.cur.fetchall():
            print(val)
