
from dttxml import DiagAccess


def find_xfers(sources,chn_num,chn_den):

    for source in sources:
        try:
            dacc = DiagAccess(source)
            channels = dacc.channels()
            if chn_num in channels[0] and chn_den in channels[0]:
                print(source)
            else:
                pass
        except: # fixme
            pass

