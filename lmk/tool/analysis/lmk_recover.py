import sys

inpfile = sys.argv[1]
total_proc_list = sys.argv[2]
outputdir = sys.argv[3]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

proc_list = set()
with open(total_proc_list, 'r') as f:
    for inp in f:
        name = inp.split('\n')[0]
        proc_list.add(name)

outputfile = outputdir + '/lmk_recover.txt'
with open(outputfile, 'w') as f:
    with open(inpfile, 'r') as inpf:
        pid2proc = {}
        for inp in inpf:
            if inp.find('Candidate') != -1:
                spt = inp.split(', ')
                proc_name = spt[0].split(' ')[-1]
                proc_pid = int(spt[1])

                if len(proc_name) < 15:
                    full_name = proc_name
                else:
                    cnt = 0
                    full_name = ""
                    for name in proc_list:
                        if name[-len(proc_name):] == proc_name:
                            full_name = name
                            cnt += 1

                    if cnt == 0:
                        print('not in proc list')
                        print(inp)
                        full_name = proc_name
                    elif cnt >= 2:
                        print('= = 22')
                        print(full_name, proc_name)
                
                if proc_pid in pid2proc:
                    if pid2proc[proc_pid] != full_name:
                        print('Same pid lol')
                pid2proc[proc_pid] = full_name
                
                f.write(inp.replace(proc_name, full_name))
            else:
                spt = inp.split(' ')
                proc_name = spt[2].split("'")[1]
                proc_pid = int(spt[3].split('(')[1].split(')')[0])

                if proc_name == '<pre-initialized>' or proc_name == 'zygote':
                    full_name = pid2proc[proc_pid]
                else:
                    full_name = proc_name

                f.write(inp.replace(proc_name, full_name))
