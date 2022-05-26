import sys

inputfile = sys.argv[1] # event_detail.txt
inputfile1 = sys.argv[2] # cur_app_res.txt
pre_condition = int(sys.argv[3])
outputdir = sys.argv[4]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

event = []
tmp_event = []
with open(inputfile, 'r') as f:
    for inp in f:
        spt = inp.split(' ')
        proc_name = spt[1]
        start_time = int(spt[2])
        end_time = int(spt[3])
        killby = int(spt[5])

        if killby == -1:
            continue

        # ams not use cur
        if killby == 2:
            continue

        # event.append((start_time, end_time, proc_name))
        tmp_event.append((start_time, end_time, proc_name))

cur_app_event = []
cur_app = ""
with open(inputfile1, 'r') as f:
    for inp in f:
        spt = inp.split(' ')

        if len(spt) == 1:
            cur_app = inp.split('\n')[0]
        elif len(spt) == 2:
            beg, end = inp.split(' ')
            beg = int(beg)
            end = int(end)

            cur_app_event.append((beg, end, cur_app))

for s, e, pc_name in tmp_event:
    for c_s, c_e, c_pc_name in cur_app_event:
        if c_pc_name != pc_name:
            continue
        if s > c_s and s - c_s == 1:
            s = c_s
    event.append((s, e, pc_name))


event.sort()
cur_app_event.sort()

app_list = ['com.rovio.baba', 'com.facebook.katana', 'com.reddit.frontpage', 'com.ss.android.ugc.trill', 'com.twitter.android', 'com.android.chrome', 'com.king.candycrushsaga', 'org.mozilla.firefox', 'com.google.android.youtube', 'org.telegram.messenger', 'com.facebook.orca', 'com.instagram.android', 'com.google.android.apps.maps', 'com.google.android.gm', 'com.devsisters.gb', 'mong.moptt', 'com.outfit7.movingeye.swampattack', 'com.playrix.homescapes', 'com.ea.game.pvzfree_row']
service_app = ['com.facebook.katana', 'com.reddit.frontpage', 'org.telegram.messenger', 'com.facebook.orca']
child_parent_app = 'com.android.chrome'

app_cold_start = {}
for app in app_list:
    app_cold_start[app] = True

cur_alive_process = {} # using dict to implement multiset, because may add in the same round
cur_alive_process_record = [] # if the process never die (means end time == -1) no need to add
each_process_respawn_time = {}
each_process_last_killed_time = {}
event_idx = 0 # current event idx
hc_tmp = []
for beg, end, cur_app in cur_app_event:
    # remove the process killed by lmk before cur_app stat
    # print('cur:', beg, end, cur_app)
    
    while event_idx < len(event):
        process_beg, process_end, process_name = event[event_idx]
        # print('event:', process_beg, process_end, process_name)

        if process_beg <= beg:
            if process_name not in cur_alive_process:
                cur_alive_process[process_name] = 0
            cur_alive_process[process_name] += 1
            if process_end != -1:
                cur_alive_process_record.append(event[event_idx])

            if process_name in each_process_last_killed_time:
                if each_process_last_killed_time[process_name] == -1:
                    print('Error last time == -1')
                respawn_time = process_beg - each_process_last_killed_time[process_name]

                if process_name not in each_process_respawn_time:
                    each_process_respawn_time[process_name] = []
                each_process_respawn_time[process_name].append(respawn_time)
                each_process_last_killed_time[process_name] = process_end
            else:
                if process_end != -1:
                    each_process_last_killed_time[process_name] = process_end

            
            if process_name in app_cold_start:
                app_cold_start[process_name] = True

            event_idx += 1
        else:
            break
    
    while 1:
        status = False
        for i in range(len(cur_alive_process_record)):
            process_beg, process_end, process_name = cur_alive_process_record[i]

            if process_end <= beg:
                cur_alive_process[process_name] -= 1

                if process_name in app_cold_start:
                    app_cold_start[process_name] = True

                if cur_alive_process[process_name] == 0:
                    del cur_alive_process[process_name]

                del cur_alive_process_record[i]
                status = True
                break


        if status == False:
            break

    if cur_app in app_cold_start:
        if app_cold_start[cur_app]:
            hc_tmp.append(('cold:', cur_app))
        else:
            hc_tmp.append(('hot:', cur_app))
        
        app_cold_start[cur_app] = False

# rm no need
hc_record = []
hc_record.append(hc_tmp[0])
for i in range(1, len(hc_tmp)):
    if hc_tmp[i][1] == hc_tmp[i - 1][1]:
        continue
    else:
        hc_record.append(hc_tmp[i])


hot_start = 0
cold_start = 0
pre_condition_cnt = 0
#print(len(hc_record)) # the len must equal to the workload length
with open(outputdir + '/hc.txt', 'w') as f:
    for i in range(len(hc_record)):
        if pre_condition_cnt >= pre_condition:
            if hc_record[i][0].find('hot') != -1:
                hot_start += 1
            else:
                cold_start += 1
        f.write('{} {}\n'.format(hc_record[i][0], hc_record[i][1]))
        pre_condition_cnt += 1

print('hot start:', hot_start)
print('cold start:', cold_start)

total_respawn_cnt = 0
rs_in_60 = 0
for k, v in each_process_respawn_time.items():
    total_respawn_cnt += len(v)

    for i in v:
        if i <= 60:
            rs_in_60 += 1

with open(outputdir + '/60s.txt', 'w') as f:
    for k, v in each_process_respawn_time.items():
        for i in v:
            if i <= 60:
                f.write('{}\n'.format(k))


print('respawn <= 60s:', rs_in_60)
print('respawn >  60s:', total_respawn_cnt - rs_in_60)
