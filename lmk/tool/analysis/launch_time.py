import sys
import math

inputfile = sys.argv[1]
pre_condition = int(sys.argv[2])

launch_time_distribution = [0 for i in range(6)]
skip = 0
total_cnt = 0
avg_time = 0
with open(inputfile, 'r') as f:
    for inp in f:
        if skip < pre_condition:
            skip += 1
            continue

        total_cnt += 1
        spt = inp.split(',')
        for i in range(1, len(spt)):
            if spt[i] == '':
                continue
            t = abs(int(spt[i]))
            avg_time += t

            t //= 1000
            if t >= 5:
                launch_time_distribution[5] += 1
            else:
                launch_time_distribution[t] += 1


print('avg time:', math.floor(avg_time / total_cnt))
print('launch time distribution')
print(launch_time_distribution)
