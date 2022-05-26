import sys

inpfile = sys.argv[1]
outputdir = sys.argv[2]

if outputdir[-1] == '/':
    outputdir = outputdir[:-1]

app2time = {}
pre_app = ""
cur_app = ""
start_time = 0
with open(inpfile, 'r') as f:
    for inp in f:
        if inp.find("time") != -1:
            time = int(float(inp.split('=')[1].split(' ')[0]))

            if pre_app == "":
                start_time = time

        if inp.find("mFocusedApp") != -1:
            cur_app = inp.split(' ')[-2].split('/')[0]

            if cur_app != pre_app and pre_app != "":
                if pre_app not in app2time:
                    app2time[pre_app] = []
                
                app2time[pre_app].append((start_time, time))
                start_time = time

            pre_app = cur_app

if cur_app != pre_app and pre_app != "":
    if pre_app not in app2time:
        app2time[pre_app] = []
    
    app2time[pre_app].append((start_time, time))


outputfile = outputdir + '/cur_app_res.txt'
with open(outputfile, 'w') as f:
    for app_name, time_list in app2time.items():
        f.write('{}\n'.format(app_name))
        for beg, end in time_list:
            f.write('{} {}\n'.format(beg, end))
