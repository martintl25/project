import sys

# python parse_ps.py ps_proc.txt outputdir

inpfile = sys.argv[1]
outputdir = sys.argv[2]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

proc_list = set()
with open(inpfile, 'r') as f:
    for inp in f:
        spt = inp.split(' ')
        proc_name = spt[-1].split('\n')[0]
        proc_list.add(proc_name)

outputfile = outputdir + '/ps_proc_list.txt'
with open(outputfile, 'w') as f:
    for name in proc_list:
        f.write('{}\n'.format(name))
