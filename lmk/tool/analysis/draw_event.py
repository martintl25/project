import matplotlib.pyplot as plt
import numpy as np
import sys

inputfile = sys.argv[1] # event_detail.txt
inputfile1 = sys.argv[2] # cur_app_res.txt
outputdir = sys.argv[3]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

record = []
proc2idx = {}
time_list = []
proc_idx = 1

# add cur_app time
proc2idx['cur_app'] = proc_idx
proc_idx += 1

with open(inputfile, 'r') as f:
    for inp in f:
        spt = inp.split(' ')
        pid = int(spt[0])
        proc_name = spt[1]
        fork_time = float(spt[2])
        exit_time = float(spt[3])
        timediff = float(spt[4])
        killby = int(spt[5])
        adj = int(spt[6])
        threshold = spt[7]

        if killby == -1:
            continue

        # not consider ams kill now
        # if want to show the ams kill, comment this if
        if killby == 2:
            continue

        if proc_name not in proc2idx:
            proc2idx[proc_name] = proc_idx
            proc_idx += 1

        time_list.append(fork_time)
        if exit_time != -1:
            time_list.append(exit_time)

        record.append((pid, proc_name, fork_time, exit_time, timediff, killby, adj, threshold))

cur_app_record = []
with open(inputfile1, 'r') as f:
    for inp in f:
        spt = inp.split(' ')

        if len(spt) == 1: # app name
            cur_app = inp.split('\n')[0]
        elif len(spt) == 2:
            beg, end = inp.split(' ')
            beg = int(beg)
            end = int(end)

            time_list.append(beg)
            time_list.append(end)

            cur_app_record.append((beg, end, cur_app))

time_list.sort()

discre_time = {}
t_idx = 1
for t in time_list:
    if t not in discre_time:
        discre_time[t] = t_idx
        t_idx += 1

discre_time[-1] = -1

fig, ax = plt.subplots(figsize=(50, 50))

cur_app_record.sort()
#color = 0
for beg, end, cur_app in cur_app_record:
    y_val = proc2idx['cur_app'] - 1
    beg = discre_time[beg]
    end = discre_time[end]
    x = (beg + end) / 2
    if cur_app == 'H':
        ax.barh("cur_app", width = end - beg, left = beg, height = 0.5, color = 'blue')
        ax.text(x, y_val, cur_app, ha='center', va='center', color='black')
    else:
        ax.barh("cur_app", width = end - beg, left = beg, height = 0.5, color = 'red')
        ax.text(x, y_val, cur_app, ha='center', va='center', color='black')

    #color ^= 1

lasttime = {}
for pid, proc_name, fork_time, exit_time, timediff, killby, adj, threshold in record:
    y_val = proc2idx[proc_name] - 1
    beg = discre_time[fork_time]
    end = discre_time[exit_time]
    td = str(int(timediff))
    x = (beg + end) / 2
    if killby == 1:
        if proc_name not in lasttime:
            ax.barh(proc_name, width = end - beg, left = beg, height = 0.5, color = 'red')
            ax.text(x, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time
        else:
            ax.barh(proc_name, width = beg - discre_time[lasttime[proc_name]], left = discre_time[lasttime[proc_name]], height = 0.5, color = 'black')
            xx = (discre_time[lasttime[proc_name]] + beg) / 2
            tdd = str(int(fork_time - lasttime[proc_name]))
            ax.text(xx, y_val, tdd, ha='center', va='center', color='white')

            ax.barh(proc_name, width = end - beg, left = beg, height = 0.5, color = 'red')
            ax.text(x, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time
        #ax.hlines(y * 10, beg, end, colors='red', label = td)
    elif killby == 2:
        if proc_name not in lasttime:
            ax.barh(proc_name, width = end - beg, left = beg, height = 0.5, color = 'blue')
            ax.text(x, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time
        else:
            ax.barh(proc_name, width = beg - discre_time[lasttime[proc_name]], left = discre_time[lasttime[proc_name]], height = 0.5, color = 'black')
            xx = (discre_time[lasttime[proc_name]] + beg) / 2
            tdd = str(int(fork_time - lasttime[proc_name]))
            ax.text(xx, y_val, tdd, ha='center', va='center', color='white')

            ax.barh(proc_name, width = end - beg, left = beg, height = 0.5, color = 'blue')
            ax.text(x, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time

        #ax.hlines(y * 10, beg, end, colors='blue', label = td)
    elif killby == 0:
        if proc_name in lasttime:
            ax.barh(proc_name, width = beg - discre_time[lasttime[proc_name]], left = discre_time[lasttime[proc_name]], height = 0.5, color = 'black')
            xx = (discre_time[lasttime[proc_name]] + beg) / 2
            tdd = str(int(fork_time - lasttime[proc_name]))
            ax.text(xx, y_val, tdd, ha='center', va='center', color='white')

srt_proc = []
for k, v in proc2idx.items():
    srt_proc.append((v, k))
srt_proc.sort()

ticks = []
for _, v in srt_proc:
    ticks.append(v)

plt.yticks(np.arange(len(ticks)), ticks)

outputfile = outputdir + '/res.png'
fig.savefig(outputfile)
plt.close()
