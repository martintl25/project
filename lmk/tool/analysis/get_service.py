import sys

inpfile = sys.argv[1]
inpfile1 = sys.argv[2]

sr = set()
with open(inpfile, 'r') as f:
    for inp in f:
        s = inp.split('\n')[0]
        sr.add(s)


cnt = 0
sr_cnt = 0
with open(inpfile1, 'r') as f:
    for inp in f:
        proc = inp.split(' ')[-1].split('\n')[0]
        cnt += 1

        for s in sr:
            if proc == s:
                sr_cnt += 1

print('service:', sr_cnt)
print('cached :', cnt - sr_cnt)
