import numpy as np

#def gempak_cloudcover(chc1, chc2, chc3):
def calc_clouds(chc1, chc2, chc3):
    
    total_cloud = {
    '1' : 0, # CLR
    '2' : 3, # SCT
    '3' : 6, # BKN
    '4' : 8, # OVC
    '5' : 9, # OBS
    '6' : 1, # FEW
    '-1': -1 # MSG
    }
    for n in range (0, chc1.size):
        chc1c = chc1[n].astype(str)[-1]
        chc2c = chc2[n].astype(str)[-1]
        chc3c = chc3[n].astype(str)[-1]
        default = -1
        chc1[n] = total_cloud.get(chc1c,default)
        chc2[n] = total_cloud.get(chc2c,default)
        chc3[n] = total_cloud.get(chc3c,default)
        
    # Now, to determine the total cloud cover, find the maxima of the layers.  
    CLDC = np.maximum.reduce([chc1,chc2,chc3])
    return CLDC

#def gempak_presWx (wnum):
def convert_wnum (wnum):
    # This dictionary maps METAR present weather codes that are read in from a GEMPAK 
    # surface station file (GEMPAK surface parameter WNUM) to the corresponding WMO 
    # integer weather code, so it can be used by MetPy's wx_code_map dictionary, as
    # defined in wx_symbols.py.
    # Source:  GEMPAK ptwcod.f
    gemWx = {
       -1: 19, # FC (Tornado)
       -2: 19, # FC (Funnel Cloud)
       -3: 19, # FC (Waterspout)
        1: 63, # RA
        2: 53, # DZ
        3: 73, # SN
        4: 90, # GR
        5: 17, # TS
        6:  5, # HZ
        7:  4, # FU
        8:  6, # DU
        9: 10, # BR
        10: 18, # SQ
        11:  0, # PY -- Not in current wx_code map
        13: 61, # -RA
        14: 65, # +RA
        15: 67, # FZRA
        16: 81, # SHRA
        17: 51, # -DZ
        18: 55, # +DZ
        19: 57, # FZDZ
        20: 71, # -SN
        21: 75, # +SN
        22: 86, # SHSN
        23: 79, # PL
        24: 77, # SG
        25: 88, # GS
        26: 89, # -GR
        27: 90, # +GR
        28:  0, # -TSSN -- Not in current wx_code map
        29: 97, # +TSSN
        30: 49, # FZFG
        31: 45, # FG
        32: 38, # BLSN
        33:  7, # BLDU
        34:  0, # BLPY -- Not in current wx_code map
        35:  0, # BLPN -- Not in current wx_code map
        36: 78, # IC
        41: 76, # UP
        49: 66, # -FZRA
        50: 67, # +FZRA
        51: 89, # -SHRA
        52: 81, # +SHRA
        53: 56, # -FZDZ
        54: 57, # +FZDZ
        55: 85, # -SHSN
        56: 86, # +SHSN
        57: 79, # -PL -- Not in current wx_code map; use PL
        58: 79, # +PL -- Not in current wx_code map; use PL
        59: 77, # -SG -- Not in current wx_code map; use SG
        60: 77, # +SG -- Not in current wx_code map; use SG
        61: 87, # -GS
        62: 88, # +GS
        63: 79, # SHPL -- Not in current wx_code map; use PL
        64: 78, # -IC -- Not in current wx_code map; use IC
        65: 78, # +IC -- Not in current wx_code map; use IC
        66: 95, # TSRA
        67: 88, # SHGS
        68:  7, # +BDLU -- Not in current wx_code map; use BLDU
        69:  0, # +BLSA -- Not in current wx_code map
        70: 39, # +BLSN
        75: 87, # -SHGS
        76: 88, # +SHGS
        77: 95, # -TSRA
        78: 97 # +TSRA        
    }
    default = 0
    for n in range (0,wnum.size):
        if (wnum[n] ==  0):
          pass
        else:
#         Up to three character codes can make up a GEMPAK weather number (WNUM).  Determine these
#         invididual GEMPAK weather code numbers, but use only the first at this time
          inum = [0, 0, 0]
          num = wnum[n]
          inum[0] = num % 80
          num = (num - inum[0]) // 80
          inum [1] = num % 80
          num = (num - inum[1]) //80
          inum [2] = num
          wnum[n] = gemWx.get(inum[0], default)

