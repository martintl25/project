import sys

inputfile = sys.argv[1] # lmk_recover.txt

restart_services = []
child_parent = []
candidate = []
with open(inputfile, 'r') as f:
    for inp in f:
        if inp.find('Candidate') != -1:
            candidate.append(inp)
        elif inp.find('Kill') != -1:
            spt = inp.split(' ')
            proc_name = spt[2][1:-1]
            proc_pid = spt[3][1:-2]

            # child parent penalty
            if proc_name == 'com.android.chrome':
                penalty = 0 # child parent
                for s in candidate:
                    if s.find('com.android.chrome:sandboxed_process') != -1:
                        penalty += 1

                child_parent.append(penalty)
            
            # restart service penalty
            for s in candidate:
                spt = s.split(', ')
                candidate_pid = int(spt[1])

                if candidate_pid == int(proc_pid) and int(spt[-1]) == 1:
                    restart_services.append((proc_name, proc_pid))
            candidate = []


print('child parent:', sum(child_parent))
#print(child_parent)

print('restart servie:', len(restart_services))
#for i in restart_services:
#    print(i)
