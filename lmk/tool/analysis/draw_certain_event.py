import matplotlib.pyplot as plt
import numpy as np
import sys

inputfile = sys.argv[1] # event_detail.txt
# inputfile1 = sys.argv[2] # cur_app_res.txt
inputfile1 = sys.argv[2] # certain event
outputdir = sys.argv[3]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

record = []
proc2idx = {}
time_list = []
proc_idx = 1

# add cur_app time
# proc2idx['cur_app'] = proc_idx
# proc_idx += 1

certain_proc = set()
with open(inputfile1, 'r') as f:
    for inp in f:
        proc = inp.split('\n')[0]
        certain_proc.add(proc)

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
        if killby == 2:
            continue

        if proc_name not in certain_proc:
            continue

        if proc_name not in proc2idx:
            proc2idx[proc_name] = proc_idx
            proc_idx += 1

        time_list.append(fork_time)
        if exit_time != -1:
            time_list.append(exit_time)

        record.append((pid, proc_name, fork_time, exit_time, timediff, killby, adj, threshold))

time_list.sort()

discre_time = {}
t_idx = 1
for t in time_list:
    if t not in discre_time:
        discre_time[t] = t_idx
        t_idx += 1

discre_time[-1] = -1

fig, ax = plt.subplots(figsize=(50, 50))

shift_time = {}
lasttime = {}
for pid, proc_name, fork_time, exit_time, timediff, killby, adj, threshold in record:
    y_val = proc2idx[proc_name] - 1
    beg = discre_time[fork_time]
    end = discre_time[exit_time]
    td = str(int(timediff))
    x = (beg + end) / 2

    if proc_name not in shift_time:
        shift_time[proc_name] = beg
    shift = shift_time[proc_name] 



    if killby == 1:
        if proc_name not in lasttime:
            ax.barh(proc_name, width = end - beg, left = beg - shift, height = 0.5, color = 'red')
            ax.text(x - shift, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time
        else:
            ax.barh(proc_name, width = beg - discre_time[lasttime[proc_name]], left = discre_time[lasttime[proc_name]] - shift, height = 0.5, color = 'black')
            xx = (discre_time[lasttime[proc_name]] + beg) / 2
            tdd = str(int(fork_time - lasttime[proc_name]))
            ax.text(xx - shift, y_val, tdd, ha='center', va='center', color='white')

            ax.barh(proc_name, width = end - beg, left = beg - shift, height = 0.5, color = 'red')
            ax.text(x - shift, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time
        #ax.hlines(y * 10, beg, end, colors='red', label = td)
    elif killby == 2:
        if proc_name not in lasttime:
            ax.barh(proc_name, width = end - beg, left = beg - shift, height = 0.5, color = 'blue')
            ax.text(x - shift, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time
        else:
            ax.barh(proc_name, width = beg - discre_time[lasttime[proc_name]], left = discre_time[lasttime[proc_name]] - shift, height = 0.5, color = 'black')
            xx = (discre_time[lasttime[proc_name]] + beg) / 2
            tdd = str(int(fork_time - lasttime[proc_name]))
            ax.text(xx - shift, y_val, tdd, ha='center', va='center', color='white')

            ax.barh(proc_name, width = end - beg, left = beg - shift, height = 0.5, color = 'blue')
            ax.text(x - shift, y_val, td, ha='center', va='center', color='black')
            lasttime[proc_name] = exit_time

        #ax.hlines(y * 10, beg, end, colors='blue', label = td)
    elif killby == 0:
        if proc_name in lasttime:
            ax.barh(proc_name, width = beg - discre_time[lasttime[proc_name]], left = discre_time[lasttime[proc_name]] - shift, height = 0.5, color = 'black')
            xx = (discre_time[lasttime[proc_name]] + beg) / 2
            tdd = str(int(fork_time - lasttime[proc_name]))
            ax.text(xx - shift, y_val, tdd, ha='center', va='center', color='white')

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
