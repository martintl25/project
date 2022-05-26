import sys

'''
    parsing the raw lmk data,
    and output format is 
    (proc name, proc pid, proc adj, free mem, threshold adj, threshold mem)

    python3 parse_lmk.py inpfile(raw_lmk.txt) outdir
'''

inpfile = sys.argv[1]
outputdir = sys.argv[2]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

outputfile = outputdir + '/lmk_res.txt'

s = set()
with open(inpfile, 'r') as fin:
    with open(outputfile, 'w') as fout:
        cnt = 0
        ch = True
        for line in fin:
            #print(line)
            spt = line.split(' ')
            proc_name = spt[2].split("'")[1]
            proc_pid = spt[3].split('(')[1].split(')')[0]
            proc_adj = spt[5].split(',')[0]
            free_mem = spt[10]
            threshold_adj = spt[-9].split('\\')[0]
            threshold_mem = spt[-12]
            print(proc_name, proc_pid, proc_adj, free_mem, threshold_adj, threshold_mem)
            fout.write('{} {} {} {} {} {}\n'.format(proc_name, proc_pid, proc_adj, free_mem, threshold_adj, threshold_mem))
