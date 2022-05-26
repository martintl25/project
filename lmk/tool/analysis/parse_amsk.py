import sys

'''
    parsing the raw logcat data for ams kill,
    and output format is
    (proc name, proc pid, proc adj, kill type)

    python3 parse_amsk.py inpfile(amsk.txt) outdir
'''

inpfile = sys.argv[1]
outputdir = sys.argv[2]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

outputfile = outputdir + '/amsk_res.txt'

with open(inpfile, 'r') as fin:
    with open(outputfile, 'w') as fout:
        for inp in fin:
            spt = inp.split(' ')
            spt = [i for i in spt if i]
            pid_proc = spt[7]
            proc_adj = spt[9].split(')')[0]
            kill_type = spt[10]

            proc_pid = pid_proc[:pid_proc.find(":")]
            proc_name = pid_proc[pid_proc.find(":") + 1:]
            proc_name = proc_name.split("/")[0]
            
            fout.write('{} {} {} {}\n'.format(proc_name, proc_pid, proc_adj, kill_type))
            #print(proc_name, proc_pid, proc_adj, kill_type)
