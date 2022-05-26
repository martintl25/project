import sys

inpfile = sys.argv[1]
outputdir = sys.argv[2]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

pid2proc = {} # record pid to proc
pid2starttime = {} # record pid start time for fork
res_record = [] # record the result the process, record (pid, proc name, start time, end time, time diff, exit_code) 
proc_list = set() # record the all process name
each_proc_record = {} # record the each process, record (pid, proc name, start time, end time, time diff, exit_code)
with open(inpfile, 'r') as f:
    for inp in f:
        event = inp[:4]
        
        if event == "fork":
            spt = inp.split(' ')
            tid = int(spt[-3].split('=')[-1])
            pid = int(spt[-2].split('=')[-1])
            time = int(spt[-1].split('=')[-1]) // 1000000000
            # orig -> the time is from 1970
            # sec, usec = spt[-1].split('=')[-1].split('.')
            # time = int(sec) + int(usec) * 0.000001
            
            if pid == tid:
                # check if pid exist or not
                if pid in pid2proc and pid2proc[pid] != -1:
                    print('Error', inp)
                else:
                    # if pid not exist, init the pid and proc info
                    pid2proc[pid] = -1
                    pid2starttime[pid] = time
            else:
                # if pid != tid means this is a thread, 
                # because the pid == tid would occur later, thus we can init the pid and proc first
                # and set the time to -1 means it is not the real time the pid start
                if pid not in pid2proc:
                    pid2proc[pid] = -1
                    pid2starttime[pid] = -1
        elif event == "comm":
            spt = inp.split(' ')
            tid = int(spt[1].split('=')[-1])
            pid = int(spt[2].split('=')[-1])
            comm = spt[3].split('=')[-1]
            time = int(spt[4].split('=')[-1]) // 1000000000
            # orig -> the time is from 1970
            # sec, usec = spt[4].split('=')[-1].split('.')
            # time = int(sec) + int(usec) * 0.000001

            if pid in pid2proc:
                if pid2proc[pid] == -1:
                    if comm != 'zygote' and comm != '<pre-initialized>' and len(comm) > 0:
                        # set proc name
                        pid2proc[pid] = comm
                        proc_list.add(comm)

        elif event == "exit":
            spt = inp.split(' ')
            tid = int(spt[1].split('=')[-1])
            pid = int(spt[2].split('=')[-1])
            exit_code = int(spt[3].split('=')[-1])
            time = int(spt[4].split('=')[-1]) // 1000000000
            # orig -> the time is from 1970
            # sec, usec = spt[4].split('=')[-1].split('.')
            # time = int(sec) + int(usec) * 0.000001

            if pid == tid:
                if pid in pid2proc:
                    if pid2proc[pid] != -1 and pid2starttime[pid] != -1 and exit_code == 9:
                        print(pid, pid2proc[pid], pid2starttime[pid], time, time - pid2starttime[pid], exit_code)
                        res_record.append((pid, pid2proc[pid], pid2starttime[pid], time, time - pid2starttime[pid], exit_code))

                        if pid2proc[pid] not in each_proc_record:
                            each_proc_record[pid2proc[pid]] = []
                        each_proc_record[pid2proc[pid]].append((pid, pid2starttime[pid], time, time - pid2starttime[pid], exit_code))

                    del pid2proc[pid]
                    del pid2starttime[pid]

for pid, proc in pid2proc.items():
    if proc != -1 and pid2starttime[pid] != -1 and proc in each_proc_record:
        each_proc_record[proc].append((pid, pid2starttime[pid], -1, -1, -1))
        res_record.append((pid, proc, pid2starttime[pid], -1, -1, -1))


outputfile = outputdir + '/proc_list.txt'
with open(outputfile, 'w') as f:
    proc_list = list(proc_list)
    proc_list.sort()
    for proc in proc_list:
        f.write('{}\n'.format(proc))

outputfile = outputdir + '/proc_event_res.txt'
with open(outputfile, 'w') as f:
    for pid, proc_name, fork_time, exit_time, timediff, exit_code in res_record:
        f.write('{} {} {} {} {} {}\n'.format(pid, proc_name, fork_time, exit_time, timediff, exit_code))

outputfile = outputdir + '/each_proc_record.txt'
with open(outputfile, 'w') as f:
    for proc_name, lists in each_proc_record.items():
        f.write('{}\n'.format(proc_name))
        for pid, fork_time, exit_time, timediff, exit_code in lists:
            f.write('{} {} {} {} {} {}\n'.format(pid, proc_name, fork_time, exit_time, timediff, exit_code))
