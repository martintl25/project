import sys

# python update_all_proc_name.py 1112/proc_list.txt outputdir
# python update_all_proc_name.py 1112/ps_proc_list.txt outputdir

inputfile = sys.argv[1]
inputfile1 = sys.argv[2]
outputdir = sys.argv[3]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

proc_name = set()
with open(inputfile, 'r') as f:
    for inp in f:
        name = inp.split('\n')[0]
        proc_name.add(name)

with open(inputfile1, 'r') as f:
    for inp in f:
        name = inp.split('\n')[0]
        proc_name.add(name)

outputfile = outputdir + '/total_proc_list.txt'
with open(outputfile, 'w') as f:
    for name in proc_name:
        f.write('{}\n'.format(name))
