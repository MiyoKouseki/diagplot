#!/home/controls/miniconda3/envs/miyoconda37/bin/python 
#! coding:utf-8
import re
import threading
import numpy as np
import subprocess
import argparse
import ezca
from plot import plot_diag,plot_couple2,plot_couple,plot_spectra
    
import os
import warnings
warnings.simplefilter('ignore')

all_optics = ['ETMX','ETMY','ITMX','ITMY',
              'BS','SRM','SR2','SR3',
              'PRM','PR2','PR3',
              'MCI','MCO','MCE','IMMT1','IMMT2',
              'OSTM','OMMT1','OMMT2']

prefix = '/kagra/Dropbox/Measurements/VIS'

template_dict = {'TM':'/TEMPLATE/PLANT_SAFE_ITMX_TM_TEST_L_0000.xml',
                 'IM':'/TEMPLATE/PLANT_SAFE_ITMX_BF_TEST_L_0000.xml',
                 'BF':'/TEMPLATE/PLANT_SAFE_ITMX_BF_TEST_L_0000.xml',
                 'GAS':'/TEMPLATE/PLANT_SAFE_ITMX_GAS_TEST_F0_0000.xml',
                 'IP':'/TEMPLATE/PLANT_SAFE_ITMX_IP_TEST_L_0000.xml'}

readpoints_dict = {'TM':[['OLDAMP'],[None]],
                   'BF':[['DAMP','OLDAMP'],['LVDTINF']],
                   'GAS':[['DAMP'],['LVDTINF']],
                   'IM':[['DAMP','OLDAMP'],['OSEMINF']],
                   'IP':[['IDAMP'],['BLEND_ACC','BLEND_LVDT','IDAMP','LVDTINF','ACCINF']]}
readdofs_dict = {'IP_IDAMP':['L','T','Y'],
                 'IP_BLEND_ACC':['L','T','Y'],
                 'IP_BLEND_LVDT':['L','T','Y'],
                 'BF_DAMP':['L','T','V','R','P','Y'],
                 'MN_DAMP':['L','T','V','R','P','Y'],
                 'IM_DAMP':['L','T','V','R','P','Y'],
                 'IP_DAMP':['L','T','Y'],
                 'TM_OLDAMP':['L','P','Y'],
                 'IM_OLDAMP':['L','P','Y'],
                 'BF_OLDAMP':['L','P','Y'],
                 'GAS_DAMP':['F0','F1','F2','F3','BF','SF'],
                 'BF_LVDTINF':['H1','H2','H3','V1','V2','V3'],
                 'MN_OSEMINF':['H1','H2','H3','V1','V2','V3'],
                 'IM_OSEMINF':['H1','H2','H3','V1','V2','V3'],
                 'IP_LVDTINF':['H1','H2','H3'],
                 'IP_ACCINF':['H1','H2','H3','H4'],
                 'IP_FLDACCINF':['H1','H2','H3'],
                 'PF_WIT':['L','P','Y'],
                 'MN_WIT':['L','T','V','R','P','Y'],
                 'TM_WIT':['L','P','Y']}
excdofs_dict = {'BF_TEST':['L','T','V','R','P','Y'],
                'MN_TEST':['L','T','V','R','P','Y'],
                'IM_TEST':['L','T','V','R','P','Y'],
                'IP_TEST':['L','T','Y'],
                'TM_TEST':['L','P','Y'],
                'TEST_GAS':['F0','F1','F2','F3','BF','SF'],
                'BF_COILOUTF':['H1','H2','H3','V1','V2','V3'],
                'MN_COILOUTF':['H1','H2','H3','V1','V2','V3'],
                'IM_COILOUTF':['H1','H2','H3','V1','V2','V3'],
                'IP_COILOUTF':['H1','H2','H3'],
                'TM_COILOUTF':['H1','H2','H3','H4']}

def readpoints_are(stages,excdofs,plottype='TEST2DAMP'):
    '''
    '''
    stage = stages[0] # Fix me?
    if plottype in ['TEST2DAMP','COIL2DAMP']:
        readpoints = readpoints_dict[stage][0]
    elif plottype in ['COIL2INF']:
        readpoints = readpoints_dict[stage][1]
    elif plottype in ['DAMP2DAMP']:
        readpoints = readpoints_dict[stage][0]        
    else:
        raise ValueError('!!')                   
    return readpoints

def readdofs_are(stages,readpoints,excdofs,plottype='TEST2DAMP'):
    '''
    '''
    stage = stages[0] # fix me
    readdofs_list = []
    for readpoint in readpoints:
        name = '{0}_{1}'.format(stage,readpoint)
        readdofs = readdofs_dict[name]
        if len(excdofs)<len(readdofs):
            readdofs = excdofs
            readdofs_list += [readdofs]  
        else:
            readdofs_list += [readdofs]
        
    return readdofs_list

def excpoints_are(mtypes,stages,excdofs,plottype):
    '''
    '''
    stage = stages[0] # Fix me?
    if plottype in ['TEST2DAMP']:
        return ['TEST']
    elif plottype in ['DAMP2DAMP']:
        return ['DAMP']    
    elif plottype in ['COIL2INF','COIL2DAMP']:
        readpoints = readpoints_dict[stage][1]
        return ['COILOUTF']
    else:
        raise ValueError('!!',plottype)                   

# ------------------------------------------------------------------------------
def run_diag(fname):
    ''' Run shell command which executes the diaggui xml file.

    This function runs the diaggui file and output some files;
     * prefix+'/log/tmp_*_in' is a command file to execute via diag command,
     * prefix+'/log/tmp*_out' is a stdout file for shell command,
     * prefix+'/log/tmp*_err' is a stderr file for shell command.

    Parameters
    ----------
    fname: `str`
        File name of the diaggui xml file.

    '''
    if not os.path.exists(fname):
        raise ValueError('{0} does not exist.'.format(fname))
    
    # make command file for execution
    with open(fname.replace('.xml','.in'),'w') as f:
        txt = 'open\nrestore {0}\nrun -w\nsave {0}\nquit\n'.format(fname)
        f.write(txt)
    print('{0} - Run'.format(fname.split('/')[-1]))
    
    # run diag command with command file
    with open(fname.replace('.xml','.in'),'r') as tmp_in:
        with open(fname.replace('.xml','.out'),'w') as tmp_out:
            with open(fname.replace('.xml','.err'),'w') as tmp_err:
                _num = np.random.choice([0,1])
                ret = subprocess.run('NDSSERVER=k1nds{0}:8088 diag'.format(_num),
                                     shell=True,
                                     check=True,
                                     stdin=tmp_in,
                                     stdout=tmp_out,
                                     stderr=tmp_err)
    if ret.returncode==0:        
        print('{0} - Finish'.format(fname.split('/')[-1]))
    else:
        raise ValueError('!')

def open_all(optics,stages,dofs):
    '''
    '''
    # open LIGO Filters of the TEST
    for optic in optics:
        for stage in stages:
            for dof in dofs:
                open_LIGOFilter(optic,stage,'TEST',dof)
                    
    # open master switch
    for optic in optics:
        open_masterswitch(optic,stage)
        
def available_optics_are(optics,plot=False):
    '''
    '''
    if not plot:
        cms = 'VIS-{0}_COMMISH_MESSAGE'
        ok = [optic for optic in optics if 'SC' in ezca[cms.format(optic)]]
        return ok        
    else:
        return optics


def open_LIGOFilter(optic,stage,func,dof):
    #ezca.get_LIGOFilter('VIS-{0}_{1}_{2}_{3}'.format(optic,stage,func,dof))\
    #.only_on('INPUT','OUTPUT','DECIMATION')
    #ezca['VIS-SRM_F0_TEST_GAS_GAIN'] = 1
    #
    # do nothing.
    #
    pass


def twr_or_pay(stage):
    '''
    '''
    if stage in ['BF','IP','GAS']:
        return 'TWR'
    elif stage in ['TM','IM','MN']:
        return 'PAY'
    else:
        raise ValueError('!')

def open_masterswitch(optic,stage):
    '''
    '''    
    if isinstance(stage,str):
        _part = twr_or_pay(stage)
        ezca['VIS-{0}_{1}_MASTERSWITCH'.format(optic,_part)]=True
        if _part=='PAY':        
            ezca['VIS-{0}_{1}_MASTERSWITCH'.format(optic,'TWR')]=True
            
    else:
        raise ValueError('!')
        
    
def close_masterswitch(optic,stage):
    '''
    '''
    if isinstance(stage,str):
        _part = twr_or_pay(stage)
        ezca['VIS-{0}_{1}_MASTERSWITCH'.format(optic,_part)]=False
        if _part=='PAY':        
            ezca['VIS-{0}_{1}_MASTERSWITCH'.format(optic,'TWR')]=False        
    else:
        raise ValueError('!')
    

# ------------------------------------------------------------------------------
def masterswitch_is_open(optic,stage):
    '''
    '''
    _part = twr_or_pay(stage)
    return ezca['VIS-{0}_{1}_MASTERSWITCH'.format(optic,_part)]==True    

def is_safe(optic):
    return ezca['GRD-VIS_{0}_STATE_S'.format(optic)]=='SAFE'

def is_ready_to_measure(optic,stage):
    if is_safe(optic) and masterswitch_is_open(optic,stage):
        print('{0}_{1} is ready.'.format(optic,stage))
        return True
    else:
        print('{0}_{1} is not ready.'.format(optic,stage))        
        return False

def new_fname(template,grd,mtype,optic,stage,excpoint,excdof,refnumber):
    '''
    '''
    fmt = '(.+)_(.+)_(.+)_(.+)_(.+)_(.+)_(.+).xml'
    _mtype,_grd,_optic,_stage,_excpoint,_excdof,_ref = re.match(
        fmt,template.split('/TEMPLATE/')[1]).groups()
    new = template.replace(_optic,optic).replace('_'+_excdof+'_','_'+excdof+'_')
    new = new.replace('_'+_stage+'_','_'+stage+'_')
    new = new.replace(_grd,grd)
    new = new.replace(_excpoint,excpoint)
    new = new.replace(_mtype,mtype)
    new = new.replace('0000','{0:04d}'.format(refnumber))
    if mtype in ['PLANT','OLTF','SPECTRA']:
        new_fname = new.replace('./TEMPLATE/',prefix+'/TF/')
    else:
        raise ValueError('!')
    
    return new_fname

# ------------------------------------------------------------------------------    
def run_tf_measurement(template,grdstates,mtypes,optic,stages,new_refnumber,
                       excpoints,excdofs,
                       run=False,ave=5,bw=0.01,amps=None,
                       debug=False):
    
    ''' Run diaggui xml file which measures the Transfer Function.
    
    This function runs shell command which executes the diaggui xml file for TF
    measurement. Name of the file is given by  arguments


    Parameters
    ----
    template: `str`
        name of the template diaggui file.

    target_optic: `str`
        optic name that you want to measure

    target_stage: `str`
        stage name that you want to measure

    Returns
    ----
    None
    '''
    
    # Check if measurement is OK.
    mtype = mtypes[0]
    
    # run diag
    for mtype,grdstate in zip(mtypes,grdstates):
        for stage in stages:
            for excpoint in excpoints:
                for excdof,amp in zip(excdofs,amps):
                    # new_fname
                    fname = new_fname(
                        template,grdstate,mtype,optic,stage,
                        excpoint,excdof,new_refnumber)
                    # run
                    if run:
                        run_copy(excdof,fname,template,optic,stage,run=True,
                                 ave=ave,bw=bw,amp=amp)
                        #save_burt(optic)
                        run_diag(fname)
                    else:
                        raise ValueError('!')
            
    # close master_switch
    # if grdstate in ['SAFE']:
    #     close_masterswitch(optic,stage)

    return fname,True

def save_burt(optic,fname):
    '''
    '''
    ezca['K1:FEC-103_SDF_SAVE_TYPE'] = 'TABLE TO FILE'
    eaca['K1:FEC-103_SDF_SAVE_OPTS'] = 'SAVE AS'
    #ezca['K1:FEC-103_SDF_SAVE_AS_NAME'] = fname.replace('.xml','.snap')

# ------------------------------------------------------------------------------
        
def run_copy(dof,new_fname,template,optic,stage,
             run=False,oltf=False,ave=5,bw=0.01,amp=5):
    ''' Copy template file to working directory.

    This function run shell command which copies template file for TF measurement
    to measurement directory. File path to this directory is given by new_fname().
    
    Parameters
    ----------
    template: `str`
        Diaggui template file name.

    optic: `str`
        Optic name which you want to measure.

    stage: `str`
        Stage name which you want to measure.

    run: optional
        If true, execute shell command. Default is false.

    '''    
    # new_fname
    fname_fmt = '(.+)_(.+)_(.+)_(.+)_(.+)_(.+)_(.+).xml'
    if 'GAS' in template:
        _mtype,_grd,_opt,_excd,_excp,_stg,_ref = re.match(fname_fmt,
                                                          template.split('/')[-1]).\
                                                          groups()
        mtype,grd,opt,excd,excp,stg,ref = re.match(fname_fmt,
                                                   new_fname.split('/')[-1]).\
                                                   groups()        
    else:        
        _mtype,_grd,_opt,_stg,_excp,_excd,_ref = re.match(fname_fmt,
                                                          template.split('/')[-1]).\
                                                          groups()
        mtype,grd,opt,stg,excp,excd,ref = re.match(fname_fmt,
                                                   new_fname.split('/')[-1]).\
                                                   groups()        
    fname = new_fname
    # make command
    cmd = "cp -rf {0} {1}".format(template,fname)
    # Rename excpoint
    cmd += "; sed -i -e 's/{1}_{3}_{7}_{5}_EXC/{2}_{4}_{8}_{6}_EXC/' {0}".\
        format(fname,_opt,opt,_stg,stg,_excd,excd,_excp,excp)
    cmd += "; sed -i -e 's/{1}_{3}_{7}_{5}_OUT/{2}_{4}_{8}_{6}_OUT/' {0}".\
        format(fname,_opt,opt,_stg,stg,_excd,excd,_excp,excp)
    cmd += "; sed -i -e 's/{1}_{3}_{7}_{5}_IN2/{2}_{4}_{8}_{6}_IN2/' {0}".\
        format(fname,_opt,opt,_stg,stg,_excd,excd,'DAMP','DAMP')
    # Rename readpoint
    if not 'GAS' in excd:
        if stg in ['IM','MN']:
            _readpoints = ['DAMP','LVDTINF','COILOUTF'] #template
            readpoints  = ['DAMP','OSEMINF','COILOUTF']
        elif stg in ['BF']:
            _readpoints = ['DAMP','LVDTINF','COILOUTF'] #template
            readpoints  = ['DAMP','LVDTINF','COILOUTF']
        else:
            _readpoints,readpoints = [],[]
        for _readpoint, readpoint in zip(_readpoints,readpoints):        
            cmd += "; sed -i -e 's/{1}_{3}_{5}/{2}_{4}_{6}/' {0}".\
                format(fname,_opt,opt,_stg,stg,_readpoint,readpoint)    
    # --- Fix me ---
    #
    cmd += "; sed -i -e 's/VIS-{1}/VIS-{2}/' {0}".format(fname,_opt,opt)
    cmd += """; sed -i -e 's/<Param Name="Averages" Type="int">5/"""\
        """<Param Name="Averages" Type="int">{1}/' {0}""".format(fname,ave)
    cmd += """; sed -i -e 's/<Param Name="BW" Type="double" Unit="Hz">"""\
        """0.1/<Param Name="BW" Type="double" Unit="Hz">{1}/' {0}""".format(
            fname,bw)
    cmd += """; sed -i -e 's/Type="double">34/Type="double">{1}/' {0}""".\
        format(fname,amp) # for amplitude        
    # run
    if run:
        subprocess.run(cmd,shell=True,check=True)
        if os.path.getsize(fname)<6700: # unuse
            raise ValueError('{0} is invalid file due to small file size. Please open the file by diaggui.'.format(fname))

# ------------------------------------------------------------------------------        
def template_is(mtypes,optics,stages,excdofs):
    '''
    '''    
    #
    mtype = mtypes[0] # Fix me
    stage = stages[0] # Fix me    
    if mtype in ['PLANT','SPECTRA','OLTF']:
        pass
    else:
        raise ValueError('!')
    #
    if 'GAS' in excdofs:
        template = '.' + template_dict['GAS']
    elif not 'GAS' in excdofs:
        template = '.' + template_dict[stage]
    else:
        raise ValueError('{0}!'.format(stage))
    #
    return template

# ------------------------------------------------------------------------------
if __name__=="__main__":
    ezca = ezca.Ezca(timeout=2)
    parser = argparse.ArgumentParser(
        prog='main.py',
        description='If you want to execute the template dtt file for IM stage '\
        'in PRM, PR2, and PRM, please request above command.',
        usage=prefix+'/main.py -t CLT -o PRM PR2 PR3 -s IM -d L T Y --plot '\
        '--refs 33',
        epilog='Please bug report to Kouseki Miyo (miyo@icrr.u-tokyo.ac.jp)')
    parser.add_argument('-m',nargs='+',required=True,
                        help='Type of the measurement. Please choose from PLANT,'\
                        ' OLTF, SPECTRA.')
    parser.add_argument('-o',nargs='+',required=True,
                        help='Please give a name list of the optics: e.g. PRM '\
                        'PR2 PR3')
    parser.add_argument('-s',nargs='+',required=True,
                        help='Please give a name list of the stage: e.g. IM.')
    parser.add_argument('-d',nargs='+',required=True,
                        help='Please give a name list of the DOFs: e.g. L T V R'\
                        ' P Y.')
    parser.add_argument('--run',default=False,
                        help='If you execute the measurement files actualy, '\
                        'please give this option. If not, dtt template will not'\
                        ' run.')
    parser.add_argument('--plot',default=False,
                        help='If you plot, please give this option.')
    parser.add_argument('--debug',action='store_true',
                        help='')
    parser.add_argument('--runbw','--bandwidth',default=0.03,
                        help='')
    parser.add_argument('--runave','--average',default=10,
                        help='')
    parser.add_argument('--runamp','--amplitude',nargs='+',default=[5,5],
                        help='')
    parser.add_argument('--plotxlim',nargs='+',default=[1e-3,30],
                        help='')
    parser.add_argument('--yes',action='store_true',
                        help='')
    parser.add_argument('--plotrefs',nargs='+',required=False,default=[0,1],
                        help='')
    parser.add_argument('--plotgrds',nargs='+',required=False,default=['SAFE','SAFE'],
                        help='')                
    args = parser.parse_args()
    #
    # Arguments
    #
    mtypes = args.m
    optics = available_optics_are(args.o,plot=args.plot)    
    stages = args.s
    excdofs = args.d
    amp = args.runamp
    grds = args.plotgrds
    if 'GAS' in excdofs:
        excdofs = args.s        
        stages = args.d
    else:
        pass

    #
    # --------------------------------------------------------------------------
    if args.plot:
        excpoints = excpoints_are(mtypes,stages,excdofs,plottype=args.plot)
        readpoints = readpoints_are(stages,excdofs,plottype=args.plot)
        readdofs = readdofs_are(stages,readpoints,excdofs,plottype=args.plot)
        pltkwargs = {'refnums':args.plotrefs,'savetxt':True,
                     'xlim':list(map(float,args.plotxlim))}
        print(stages)
        print(excpoints)
        print(readpoints)
        print(readdofs)
        #
        if args.plot in ['COIL2INF']:
            plot_diag(args.plot,mtypes,grds,optics,stages,excpoints,excdofs,
                      readpoints,readdofs,**pltkwargs)
            exit()
        if args.plot in ['TEST2DAMP','DAMP2DAMP']:
            plot_diag(args.plot,mtypes,grds,optics,stages,excpoints,excdofs,
                      readpoints,readdofs,**pltkwargs)        
            plot_couple(args.plot,mtypes,grds,optics,stages,excpoints,excdofs,
                        readpoints,readdofs,**pltkwargs)
            exit()
        if args.plot in ['SPECTRA']:
            print(readpoints)
            print(readdofs)
            plot_spectra(args.plot,mtypes,grds,optics,stages,excpoints,excdofs,
                         readpoints,readdofs,**pltkwargs)
            exit()
    #
    # --------------------------------------------------------------------------    
    if args.run in ['TEST2DAMP','COIL2INF','COIL2DAMP','SPECTRA','DAMP2DAMP']:
        # Refnumber        
        with open('.'+'/refnumber.txt','r') as f:
            current_refnumber = int(f.readline())
            new_refnumber = current_refnumber + 1
        with open('.'+'/refnumber.txt','w') as f:
            f.write(str(new_refnumber))
        if not args.debug:
            open_all(optics,stages,excdofs)
            
        # template
        template = template_is(mtypes,optics,stages,excdofs)

        # Excitation amplitudes: amp
        if args.run in ['SPECTRA']:
            amp = [0]*len(excdofs)

        if 'GAS' in excdofs:
            if len(amp)!=len(stages):
                raise ValueError('{0}!={1}'.format(len(amp),len(stages)))
        else:
            if len(amp)!=len(excdofs):
                raise ValueError('{0}!={1}'.format(len(amp),len(excdofs)))
        
        # Time estimation
        _time = int(1./float(args.runbw)*float(args.runave)*len(excdofs)/60/2)    
        if not args.yes:
            ans = input('It takes {0} minutes. Do you want to measure? [y/N]'.\
                        format(_time))
            if ans not in ['y','yes','Y']:
                raise ValueError('You chose {0}. Stop.'.format(ans))
        else:
            ans = print('It takes {0} minutes. Do you want to measure? [y/N]'.\
                    format(_time))
            
        grdstate = 'SAFE' # Fix me
        grdstates = [ezca['GRD-VIS_{0}_STATE_S'.format(optic)] for optic in optics]
        # Execution
        t = []
        for optic in optics:
            excpoints = excpoints_are(mtypes,stages,excdofs,plottype=args.run)
            _t = threading.Thread(target=run_tf_measurement,
                                  args=(template,grdstates,mtypes,optic,stages,
                                        new_refnumber,excpoints,excdofs),
                                  kwargs={'run':True,
                                          'ave':args.runave,'bw':args.runbw,
                                          'amps':amp,'debug':args.debug})
            _t.start()
            t += [_t]                      
