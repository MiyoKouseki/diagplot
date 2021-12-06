import numpy as np
from dtt2hdf import read_diaggui,DiagAccess # need

import matplotlib.pyplot as plt
import traceback

import warnings
warnings.simplefilter('ignore')
from read import get_diagdata

prefix = '/kagra/Dropbox/Measurements/VIS'

alpha_list = [1.0, 0.6]
linestyle_list = ['-','--']
color_list = ['#1f77b4','#ff7f0e','#2ca02c','#dc143c']


typea = ['ETMX','ETMY','ITMX','ITMY']
typeb = ['BS','SRM','SR2','SR3']
typebp = ['PRM','PR2','PR3']
typeci = ['MCI','MCO','MCE','IMMT1','IMMT2']
typeco = ['OSTM','OMMT1','OMMT2']

def sustype_is(optics):
    '''
    '''
    if all([optic in typea for optic in optics]):
        return 'TYPEA'
    elif all([optic in typeb for optic in optics]):
        return 'TYPEB'
    elif all([optic in typebp for optic in optics]):
        return 'TYPEBP'
    elif all([optic in typeci for optic in optics]):
        return 'TYPECI'
    elif all([optic in typeco for optic in optics]):
        return 'TYPECO'
    else:
        raise ValueError('!'.format(optics))

def doftype_is(excds):
    '''
    '''
    excds = set(excds)
    if excds=={'L','T','Y'} or excds=={'H1','H2','H3'}:
        return 'H'
    elif excds=={'L','P','Y'}:
        return 'T'
    elif excds=={'R','P','V'} or excds=={'V1','V2','V3'}:
        return 'V'
    elif all([excd in ['F0','F1','F2','F3','BF','SF'] for excd in excds]):
        return 'G'        
    else:
        raise ValueError('!',excds)

def add_info(ax,refnums,info_list):
    '''
    '''
    text = ''                
    for refnum,info in zip(refnums,info_list):
        if not info==None:
            date,bw,ave,win = info
            grd = 'SAFE'
            text += 'REF{0}\n- GuardState: {2}\n- Date: {1} UTC'\
                '\n- Bw: {3:1.1e} Hz\n- Ave: {4:d}\n\n'.\
                format(refnum,date,grd,bw,ave)
        else:
            pass
    _ax = ax[-1][-1]
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    _ax.text(1.05,0.01,text,transform=_ax.transAxes, fontsize=10,
             bbox=props,
             verticalalignment='bottom',horizontalalignment='left')

def add_legend(ax,label_list):
    '''
    '''
    _ax = ax[0][-1]
    leg = _ax.legend(label_list,numpoints=1,markerscale=5,
                     bbox_to_anchor=(1.02, 1.01),loc='upper left',
                     fontsize=7)
    # leg = _ax.legend(label_list,loc='lower left',numpoints=1,markerscale=5,
    #                     fontsize=10)
    [l.set_linewidth(3) for l in leg.legendHandles]

def plot_multitf(ax_diag,tftype,grds,optics,stage,excpoint,
                 excdofs,readpoint,rp,readdofs,refnums,
                 savetxt=True,xlim=[1e-3,30]):
    '''
    '''
    if tftype in ['PLANT']:
        ylim=[1e-6,1e2]
        oltf = False
    elif tftype in ['OLTF']:
        ylim=[1e-2,1e2]
        oltf = True
    else:
        raise ValueError('!')
    
    # -- Start Plot--
    # j: plot other figure
    # i: plot same figure
    for excdof in excdofs:
        for j,readdof in enumerate(readdofs[rp]):
            subtitle_diag = '{0} -> {1}'.format(excdof,readdof)
            #print(subtitle_diag)
            label_list = []
            for i,optic in enumerate(optics):
                _from,_to = search_fromto(tftype,
                    optic,stage,excdof,
                    excpoint,readdof,readpoint)
                info_list = []
                for k,refnum in enumerate(refnums):
                    w, mag, phase, coh, info = get_diagdata(
                        tftype,grds[k],_from,_to,refnum,
                        savetxt=savetxt,oltf=oltf)
                    # Fix me
                    info_list += [info]
                    #
                    if isinstance(w,np.ndarray):
                        label_diag = '{1} (REF{0})'.\
                            format(refnum,optic)
                    elif np.isnan(w):
                        label_diag='{1} (REF{0}) None'.\
                            format(refnum,optic)
                    else:
                        raise ValueError('!')
                    #
                    # Choose plot axis
                    if readdof==excdof:
                        ax = ax_diag
                        label = label_diag
                        label_list += [label]
                        subtitle = subtitle_diag
                        if optic==optics[-1] and refnum==refnums[-1]:
                            grid=True
                        else:
                            grid=False
                            #print(optic)
                        plot_tf(
                            w,mag,phase,coh,ax_diag[:,j],
                            label=label,alpha=alpha_list[k],
                            linestyle=linestyle_list[k],
                            color=color_list[i],grid=grid,
                            subtitle=subtitle,linewidth=1,
                            xlim=xlim,ylim=ylim)
    return info_list
                            
# ------------------------------------------------------------------------------
def plot_tf(w,mag,phase,coh,_ax=None,label='None',style='-',subtitle='No title',
            grid=False,
            ylim=[1e-6,1e2],xlim=[1e-3,10],oltf=False,**kwargs):
    '''
    '''
    if isinstance(_ax,np.ndarray) and len(_ax)==3:
        _ax[0].set_title(subtitle,fontsize=20)            
        _magplot = _ax[0].loglog(w,mag,label=label,**kwargs)
        _color = _magplot[0].get_color()
        _ax[0].set_ylim(ylim[0],ylim[1])    
        _ax[2].semilogx(w,coh,label=label,**kwargs)
        kwargs['linestyle'] = 'None' # Fix me
        _ax[1].semilogx(w,phase,'o',label=label,markersize=1,**kwargs)        
        _ax[1].set_ylim(-185,185)
        _ax[1].set_yticks(range(-180,181,90))
        _ax[2].set_ylim(0,1.01)
        _ax[2].set_xlim(xlim[0],xlim[1])
        leg = _ax[0].legend(loc='lower left',numpoints=1,markerscale=5,
                           fontsize=7)
        [l.set_linewidth(3) for l in leg.legendHandles]
        if grid:
            [__ax.grid(color='k', alpha=0.3,
                       linestyle='--', which='both') for __ax in _ax]
    else:
        raise ValueError('!',len(_ax))
    
# ------------------------------------------------------------------------------
def plot_asd(w,mag,ax=None,label='None',style='-',subtitle='No title',
             ylim=[1e-6,1e1],
             oltf=False,xlim=[1e-3,10],**kwargs):
    '''
    '''
    if isinstance(ax,np.ndarray) and len(ax)==3:
        if not subtitle=='':
            ax[0].set_title(subtitle,fontsize=20)
        hoge = ax[0].loglog(w,mag,style,label=label,**kwargs)
        _color = hoge[0].get_color()
        #ax[0].set_ylim(ylim[0],ylim[1])            
        #ax[1].semilogx(w,phase,'o',label=label,markersize=2,**kwargs)
        #ax[2].semilogx(w,coh,style,label=label,**kwargs)
        ax[1].set_ylim(-185,185)
        ax[1].set_yticks(range(-180,181,90))
        ax[2].set_ylim(0,1.01)
        ax[2].set_xlim(xlim[0],xlim[1])
        leg = ax[0].legend(loc='lower left',numpoints=1,markerscale=5,fontsize=10)
        [l.set_linewidth(3) for l in leg.legendHandles]
        [_ax.grid(color='k', alpha=0.5,linestyle='--', which='both') for _ax in ax]
    else:
        raise ValueError('!')
    
# ------------------------------------------------------------------------------    
def search_fromto(tftype,opt,stg,excd,excp,dof,readp):
    '''
    '''
    if tftype in ['PLANT']:
        _from = 'K1:VIS-{0}_{1}_{3}_{2}_OUT'.format(opt,stg,excd,excp)
    elif tftype in ['OLTF']:
        _from = 'K1:VIS-{0}_{1}_{3}_{2}_IN2'.format(opt,stg,excd,excp)
    else:
        raise ValueError('!')

    #
    # Fix me    
    if 'GAS' in stg: 
        if tftype in ['PLANT']:
            _from = 'K1:VIS-{0}_{3}_{2}_{1}_OUT'.format(opt,stg,excp,excd)
            _to = 'K1:VIS-{0}_{3}_{2}_{1}_IN1_DQ'.format(opt,stg,readp,dof)            
        elif tftype in ['OLTF']:
            _from = 'K1:VIS-{0}_{3}_{2}_{1}_IN2'.format(opt,stg,excp,excd)
            _to = 'K1:VIS-{0}_{3}_{2}_{1}_IN1_DQ'.format(opt,stg,readp,dof)            
        else:
            raise ValueError('!')
    else:
        if readp in ['BLEND_ACC','BLEND_LVDT']:
            _to = 'K1:VIS-{0}_{1}_{2}{3}_OUT'.format(opt,stg,readp,dof)
        elif readp in ['LVDTINF','ACCINF','OSEMINF']:
            _to = 'K1:VIS-{0}_{1}_{2}_{3}_OUT'.format(opt,stg,readp,dof)
        elif readp in ['IDAMP','DAMP','OLDAMP']:
            _to = 'K1:VIS-{0}_{1}_{2}_{3}_IN1_DQ'.format(opt,stg,readp,dof)
        else:
            raise ValueError('{0} is invalid readpoint.'.format(readp))
    #

    return _from,_to

def set_labels(ax,dof):
    '''
    '''
    nrow = ax.shape[1]
    [ax[2][k].set_xlabel('Frequency [Hz]',fontsize=15) for k in range(nrow)]            
    ax[1][0].set_ylabel('Phase\n[Degree]',fontsize=15)
    ax[2][0].set_ylabel('Coherence',fontsize=15)
    [ax[i][j].tick_params(labelsize=12) for i in range(3) for j in range(nrow)]

    if dof in ['L','T','V','SF','BF','F0','F1','F2','F3']:
        ax[0][0].set_ylabel('Magnitude\n[um/count]',fontsize=15)
    elif dof in ['R','P','Y']:
        ax[0][0].set_ylabel('Magnitude\n[urad/count]',fontsize=15)
    elif dof in ['H1','H2','H3','H4','V1','V2','V3']:
        ax[0][0].set_ylabel('Magnitude\n[um/count]',fontsize=15)
    else:
        raise ValueError('!',dof)
    
# ------------------------------------------------------------------------------
def plot_diag(plottype,tftypes,grds,optics,stages,excpoints,excdofs,readpoints,
              readdofs,refnums=['0','1'],xlim=(1e-3,30),savetxt=True):
    '''
    '''
    #
    if plottype in ['COIL2DAMP']:
        return False
    #
    refnums = list(map(int,refnums)) # Fix me    
    refnums = list(map(lambda num:'{0:04d}'.format(num),refnums)) # Fix me
    stage = stages[0] # Fix me
    #
    # Diag plot
    for tftype in tftypes:
        for rp,readpoint in enumerate(readpoints):
            for excpoint in excpoints:
                # Init figure.
                nrow = max(len(readdofs[rp]),len(stages),3)
                fig,ax = plt.subplots(
                    3,nrow,figsize=(14,8),dpi=100,
                    sharex=True,sharey='row',
                    gridspec_kw={'height_ratios': [2,1,1]})
                plt.subplots_adjust(wspace=0.1, hspace=0.1, right=0.8)
                sustype = sustype_is(optics)
                # Set Title
                title = '{0}_{1}'.format(sustype,stage)
                fig.suptitle(title,fontsize=25)
                # Set fname
                excdof,readdof = excdofs[0],readdofs[0]# Fix me
                fname = prefix+'/{0}_{1}_{2}_{3}_{4}2{5}.png'.format(
                    tftype,doftype_is(excdofs)+'DIAG',
                    stage,sustype,excpoint,readpoint)
                print(fname)
                # Plot
                info_list = plot_multitf(ax,tftype,grds,
                                         optics,stage,excpoint,excdofs,
                                         readpoint,rp,readdofs,refnums,
                                         savetxt=savetxt,xlim=xlim)
                #add_legend(ax,label_list)
                add_info(ax,refnums,info_list)
                fig.savefig(fname)
                plt.close()
                
# ------------------------------------------------------------------------------
def plot_spectra(plottype,tftypes,optics,stages,excpoints,excdofs,readpoints,
                 readdofs,refnums=['0','1'],
                 xlim=(1e-3,30),savetxt=True):
    '''
    '''
    if plottype in ['COIL2DAMP']:
        return False
    if not isinstance(tftypes,list):
        raise ValueError('tftypes is not list type: {0}'.format(tftypes))
    if not isinstance(optics,list):
        raise ValueError('optics is not list type: {0}'.format(optics))
    if not isinstance(excpoints,list):
        raise ValueError('excpoints is not list type: {0}'.format(excpoints))        
    if not isinstance(excdofs,list):
        raise ValueError('excdofs is not list type: {0}'.format(excdofs))        
    if not isinstance(readpoints,list):
        raise ValueError('readpoints is not list type: {0}'.format(readpoints))        

    refnums = list(map(int,refnums)) # Fix me    
    refnums = list(map(lambda num:'{0:04d}'.format(num),refnums)) # Fix me
    stage = stages[0] # Fix me
    
    # Diag plot
    for tftype in tftypes:
        for rp,readpoint in enumerate(readpoints):
            for excpoint in excpoints:            
                # Init figure.
                nrow = max(len(readdofs[rp]),len(stages),3)
                fig_diag,ax_diag = plt.subplots(3,nrow,figsize=(14,8),dpi=100,
                                      sharex=True,sharey='row',
                                      gridspec_kw={'height_ratios': [2, 1,1]})
                plt.subplots_adjust(wspace=0.1, hspace=0.1,right=0.8)
                fig_diag.suptitle('{1}_{2} -> {1}_{3}'.\
                                  format(tftype,stage,excpoint,readpoint),
                                  fontsize=25)
                # -- Start Plot--
                # j: plot other figure
                # i: plot same figure
                sustype = sustype_is(optics)
                for excdof in excdofs:
                    for j,readdof in enumerate(readdofs[rp]):
                        subtitle_diag = '{0} -> {1}'.format(excdof,readdof)
                        #print(subtitle_diag)
                        label_list = []                        
                        for i,optic in enumerate(optics):
                            _from,_to = search_fromto(tftype,
                                optic,stage,excdof,
                                excpoint,readdof,readpoint)
                            for k,refnum in enumerate(refnums):
                                w, mag, phase, coh, info = get_diagdata(
                                    tftype,grds[k],_from,_to,refnum,
                                    savetxt=savetxt)
                                if isinstance(w,np.ndarray):
                                    label_diag = 'Ref{0}: {1}'.\
                                        format(refnum,optic)
                                elif np.isnan(w):
                                    label_diag='Ref{0}: {1} [None]'.\
                                        format(refnum,optic)
                                else:
                                    raise ValueError('!')
                                # Choose plot axis
                                if readdof==excdof:
                                    ax = ax_diag
                                    label = label_diag
                                    label_list += [label]
                                    subtitle = subtitle_diag
                                    plot_asd(w,mag,ax[:,j],label=label,
                                             subtitle=subtitle,linewidth=1,
                                             xlim=xlim)
                # -- End Plot--
                fname_diag = prefix+'/{0}_{1}_{2}_{3}_{4}_DIAG.png'.\
                    format(tftype,sustype,stage,excpoint,readpoint)
                print(fname_diag)
                set_labels(ax_diag,readdof)
                fig_diag.savefig(fname_diag)
                #plt.show()    
                plt.close()
                
# ------------------------------------------------------------------------------
def plot_couple(plottype,tftypes,grds,optics,stages,excpoints,excdofs,readpoints,
                readdofs,refnums=['0','1'],
                xlim=(1e-3,30),savetxt=True):
    '''
    '''
    if not isinstance(tftypes,list):
        raise ValueError('tftypes is not list type: {0}'.format(tftypes))
    if not isinstance(optics,list):
        raise ValueError('optics is not list type: {0}'.format(optics))
    if not isinstance(excpoints,list):
        raise ValueError('excpoints is not list type: {0}'.format(excpoints))        
    if not isinstance(excdofs,list):
        raise ValueError('excdofs is not list type: {0}'.format(excdofs))
    if not isinstance(readpoints,list):
        raise ValueError('readpoints is not list type: {0}'.format(readpoints))
    #
    #
    refnums = list(map(int,refnums)) # Fix me
    refnums = list(map(lambda num:'{0:04d}'.format(num),refnums)) # Fix me
    stage = stages[0] # Fix me
    #
    # Cross plot
    for tftype in tftypes:
        for rp,readpoint in enumerate(readpoints):
            for excpoint in excpoints:
                for _,optic in enumerate(optics):
                    # Init figure.
                    nrow = max(len(readdofs[rp]),len(stages),3)
                    fig_couple,ax_couple = plt.subplots(
                        3,nrow,figsize=(14,8),
                        dpi=100,
                        sharex=True,sharey='row',
                        gridspec_kw={'height_ratios': [2, 1,1]})
                    plt.subplots_adjust(wspace=0.1, hspace=0.1,right=0.8)
                    fig_couple.suptitle(
                        '{1}_{2}'.format(
                            tftype,optic,stage,excpoint,readpoint),
                        fontsize=25)
                    #
                    # -- Start Plot--
                    # j: plot other figure
                    # i: plot same figure
                    label_list = []
                    for i,excdof in enumerate(excdofs):                                        
                        for j,readdof in enumerate(readdofs[rp]):                
                            subtitle_couple = '{1}'.format(excdof,readdof)
                            _from,_to = search_fromto(tftype,
                                optic,stage,excdof,
                                excpoint,readdof,readpoint)
                            info_list = []                            
                            for k,refnum in enumerate(refnums):
                                w, mag, phase, coh, info = get_diagdata(
                                    tftype,grds[k],_from,_to,refnum,
                                    savetxt=savetxt)
                                info_list += [info]
                                if isinstance(w,np.ndarray):
                                    label_couple = '{1} -> {2} (REF{0})'.\
                                        format(refnum,excdof,readdof)
                                elif np.isnan(w):
                                    label_couple='{1} -> {2} (REF{0}) None'.\
                                        format(refnum,excdof,readdof)
                                else:
                                    raise ValueError('!')                                
                                # Choose plot axis
                                if excdof==readdof:
                                    linewidth=3
                                else:
                                    linewidth=1
                                ax = ax_couple
                                label = label_couple
                                label_list += [label]
                                subtitle = subtitle_couple
                                if excdof==readdof:
                                    linewidth = 3
                                else:
                                    linewidth = 1
                                plot_tf(
                                        w,mag,phase,coh,ax_couple[:,j],
                                        label=label,alpha=alpha_list[k],
                                        linestyle=linestyle_list[k],
                                        color=color_list[i],
                                        subtitle=subtitle,linewidth=linewidth,
                                        xlim=xlim)                                
                                # plot_tf(w,mag,phase,coh,ax[:,j],
                                #         label=label,
                                #         subtitle=subtitle,
                                #         linewidth=linewidth,
                                #         xlim=xlim)
                    # -- End Plot--
                    fname_couple =   prefix+'/{0}_{1}_{2}_{3}_{4}2{5}.png'.\
                        format(tftype,doftype_is(excdofs)+'COUPLE',stage,optic,excpoint,readpoint)
                    print(fname_couple)
                    add_info(ax_couple,refnums,info_list)                    
                    set_labels(ax_couple,readdof)
                    fig_couple.savefig(fname_couple)
                    #plt.show()
                    plt.close()
                    
# # ------------------------------------------------------------------------------
def plot_couple2(plottype,tftypes,optics,stages,excpoints,excdofs,readpoints,
                  readdofs,refnums=['0','1'],
                  xlim=(1e-3,30),savetxt=True):
     '''
     '''
     pass
#     if not isinstance(tftypes,list):
#         raise ValueError('tftypes is not list type: {0}'.format(tftypes))
#     if not isinstance(optics,list):
#         raise ValueError('optics is not list type: {0}'.format(optics))
#     if not isinstance(excpoints,list):
#         raise ValueError('excpoints is not list type: {0}'.format(excpoints))        
#     if not isinstance(excdofs,list):
#         raise ValueError('excdofs is not list type: {0}'.format(excdofs))        
#     if not isinstance(readpoints,list):
#         raise ValueError('readpoints is not list type: {0}'.format(readpoints))        

#     refnums = list(map(int,refnums)) # Fix me    
#     refnums = list(map(lambda num:'{0:04d}'.format(num),refnums)) # Fix me
#     stage = stages[0] # Fix me
    
#     # Cross plot
#     for tftype in tftypes:
#         for rp,readpoint in enumerate(readpoints):
#             for excpoint in excpoints:
#                 for excdof in excdofs:                                
#                     # Init figure.
#                     nrow = max(len(readdofs[rp]),len(stages),3)
#                     fig_diag,ax_diag = plt.subplots(3,nrow,figsize=(14,8),dpi=100,
#                                                     sharex=True,sharey='row',
#                                                     gridspec_kw={'height_ratios': [2, 1,1]})
#                     plt.subplots_adjust(wspace=0.1, hspace=0.1,right=0.8)
#                     fig_diag.suptitle('{0}_{1}_{2}_DIAG'.format(tftype,stage,readpoint),
#                                       fontsize=25)
#                     # -- Start Plot--
#                     # j: plot other figure
#                     # i: plot same figure
#                     for j,readdof in enumerate(readdofs[rp]):                
#                         subtitle_diag = '{0} -> {1}'.format(excdof,readdof)
#                         print(subtitle_diag)
#                         sustype = sustype_is(optics)
#                         for i,optic in enumerate(optics):
#                             _from,_to = search_fromto(tftype,optic,stage,excdof,
#                                                       excpoint,readdof,readpoint)
#                             for k,refnum in enumerate(refnums):
#                                 w, mag, phase, coh = get_diagdata(tftype,grd,_from,_to,refnum,
#                                                             savetxt=savetxt)
#                                 if isinstance(w,np.ndarray):
#                                     label_diag = '{1} (REF{0})'.format(refnum,optic)
#                                 elif np.isnan(w):
#                                     label_diag='{1} (REF{0}) None'.format(refnum,optic)
#                                 else:
#                                     raise ValueError('!')                                
#                                 # Choose plot axis
#                                 ax = ax_diag
#                                 label = label_diag
#                                 subtitle = subtitle_diag
#                                 plot_tf(w,mag,phase,coh,ax_diag[:,j],label=label,
#                                         subtitle=subtitle,linewidth=1,xlim=xlim)                                    
#                     # -- End Plot--
#                     fname_diag = prefix+'/{0}_{1}_{2}_{3}_{4}_{5}_CROSS.png'.format(
#                         tftype,sustype,stage,readpoint,excpoint,excdof)
#                     print(fname_diag)
#                     set_labels(ax_diag,readdof)
#                     fig_diag.savefig(fname_diag)
#                     #plt.show()
#                     plt.close()
                    
# ------------------------------------------------------------------------------                    
if __name__=='__main__':
    pass
