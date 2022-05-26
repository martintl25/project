import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import sys
import random

inputfile = sys.argv[1] # hot_cold.txt
inputfile1 = sys.argv[2]
preproc_cnt = int(sys.argv[3]) # pre-process apps cnt 

freq_apps = set()
with open(inputfile1, 'r') as f:
    for inp in f:
        freq_apps.add(inp.split('\n')[0])

proc_mapping = {
    'com.king.candycrushsaga' : 'CC',
    'com.twitter.android' : 'TW',
    'com.android.chrome' : 'CH',
    'org.telegram.messenger' : 'TL',
    'com.rovio.baba' : 'AB',
    'com.facebook.orca' : 'MG',
    'org.mozilla.firefox' : 'FX',
    'com.facebook.katana' : 'FB',
    'com.google.android.youtube' : 'YT',
    'com.ss.android.ugc.trill' : 'TT',
    'com.reddit.frontpage' : 'RD',
    'com.devsisters.gb' : 'CR',
    'com.instagram.android' : 'IG',
    'com.playrix.homescapes' : 'HS',
    'com.ea.game.pvzfree_row' : 'PZ',
    'com.outfit7.movingeye.swampattack' : 'AT'
}


pre_condition = 0
freq_penalty = 0
with open(inputfile, 'r') as f:
    for inp in f:
        if pre_condition < preproc_cnt:
            pre_condition += 1
            continue
        spt = inp.split(' ')
        proc = spt[-1].split('\n')[0]
        
        if spt[0][0] == 'c':
            if proc in freq_apps:
                freq_penalty += 1

print('freq penalty:', freq_penalty)
