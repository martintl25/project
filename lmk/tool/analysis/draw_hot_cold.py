import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import sys
import random

inputfile = sys.argv[1] # hot_cold.txt
preproc_cnt = int(sys.argv[2]) # pre-process apps cnt 
outputfile = sys.argv[3]
#outputdir = sys.argv[3]

#if outputdir[-1] == '/':
#    outputdir = outputdir[:-1]

if len(sys.argv) > 4:
    seq_file = sys.argv[4]

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


apps = {} 
apps_flow = []
idx = 1
apps_list = []
with open(inputfile, 'r') as f:
    for inp in f:
        spt = inp.split(' ')
        proc = spt[-1].split('\n')[0]
        
        if spt[0][0] == 'h':
            hc = 'h'
        else:
            hc = 'c'

        apps_flow.append((hc, proc))
        if proc not in apps:
            apps[proc] = idx
            idx += 1
            apps_list.append(proc)

if len(sys.argv) > 4:
    idx = 1
    with open(seq_file, 'r') as f:
        for inp in f:
            proc = inp.split('\n')[0]
            apps[proc] = idx
            idx += 1
else:
    idx = 1
    random.shuffle(apps_list)
    for proc in apps_list:
        apps[proc] = idx
        idx += 1

fig, ax = plt.subplots()
cnt = 0
for idx, (hc, proc) in enumerate(apps_flow):
    if cnt < preproc_cnt:
        ax.scatter(idx + 1, apps[proc] - 1, c = 'gray', marker='^')
        cnt += 1
        continue

    if hc == 'h':
        ax.scatter(idx + 1, apps[proc] - 1, c = 'red', marker='o')
    else:
        ax.scatter(idx + 1, apps[proc] - 1, c = 'blue', marker='x')

srt_proc = []
for k, v in apps.items():
    srt_proc.append((v, proc_mapping[k]))
srt_proc.sort()

ticks = []
for _, v in srt_proc:
    ticks.append(v)

plt.yticks(np.arange(len(ticks)), ticks)
plt.ylabel('Process name', fontsize=14)
plt.xlabel('Launch seqence', fontsize=14)

for label in (ax.get_xticklabels() + ax.get_yticklabels()):
	label.set_fontsize(14)

pre_cond = mlines.Line2D([], [], color='gray', marker='^', linestyle='None', label='pre-cond')
cs = mlines.Line2D([], [], color='blue', marker='x', linestyle='None', label='cold start')
hs = mlines.Line2D([], [], color='red', marker='o', linestyle='None', label='hot start')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), handles=[pre_cond, cs, hs], loc='lower left', ncol=3, mode="expand", borderaxespad=0., prop={'size': 12})

#outputfile = outputdir + '/hc_distribute.png'
outputfile = outputfile + '.png'
fig.savefig(outputfile)
plt.close()
