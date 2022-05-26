import sys

inp_amsk = sys.argv[1]
inp_lmk = sys.argv[2]
inp_proc_event = sys.argv[3]
outputdir = sys.argv[4]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

amsk = [] # record ams kill event
lmk = [] # record lmk kill event

with open(inp_amsk, 'r') as f:
    for inp in f:
        spt = inp.split(' ')
        
        # pid, proc name, adj, kill type
        amsk.append((int(spt[1]), spt[0], int(spt[2]), spt[3].split('\n')[0]))

with open(inp_lmk, 'r') as f:
    for inp in f:
        spt = inp.split(' ')
        
        # pid, proc name, adj, kill threshold (adj)
        lmk.append((int(spt[1]), spt[0], int(spt[2]), int(spt[4])))

print(amsk[0])
print(lmk[0])

vis_amsk = [0 for i in range(len(amsk))]
vis_lmk = [0 for i in range(len(lmk))]
res_record = [] # record proc event result add kill type and killed adj
lmk_cnt = 0
ams_cnt = 0
others_cnt = 0
with open(inp_proc_event, 'r') as f:
    for inp in f:
        spt = inp.split(' ')
        pid = int(spt[0])
        proc_name = spt[1]
        fork_time = spt[2]
        exit_time = spt[3]
        time_diff = spt[4]
        exit_code = int(spt[5])

        if exit_code == -1:
            res_record.append((pid, proc_name, fork_time, exit_time, time_diff, 0, -1, -1))
            continue

        if exit_code != 9:
            print('Exit code error.')
        
        find = False
                
        for i in range(len(lmk)):
            if lmk[i][0] == pid and lmk[i][1] == proc_name and vis_lmk[i] == 0:
                res_record.append((pid, proc_name, fork_time, exit_time, time_diff, 1, lmk[i][2], lmk[i][3]))
                find = True
                vis_lmk[i] = 1
                lmk_cnt += 1
                break
        
        for i in range(len(amsk)):
            if amsk[i][0] == pid and amsk[i][1] == proc_name and vis_amsk[i] == 0:
                if find == True:
                    print('Collision', pid, proc_name)
                    break
                res_record.append((pid, proc_name, fork_time, exit_time, time_diff, 2, amsk[i][2], amsk[i][3]))
                find = True
                vis_amsk[i] = 1
                ams_cnt += 1
                break

        if find == False:
            res_record.append((pid, proc_name, fork_time, exit_time, time_diff, -1, -1, -1))
            others_cnt += 1

#for i in res_record:
#    print(i)

print('ams, lmk, other:', ams_cnt, lmk_cnt, others_cnt)

outputfile = outputdir + '/event_detail.txt'
with open(outputfile, 'w') as f:
    for pid, proc_name, fork_time, exit_time, time_diff, killby, adj, threshold in res_record:
        f.write('{} {} {} {} {} {} {} {}\n'.format(pid, proc_name, fork_time, exit_time, time_diff, killby, adj, threshold))
