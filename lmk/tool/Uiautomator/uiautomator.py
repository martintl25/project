import uiautomator2 as u2
import sys
import time
import random
import os
import pandas as pd
from io import StringIO
from datetime import datetime
import json
import subprocess

packages = {'Facebook': ['com.facebook.katana', '.LoginActivity'],
            'Chrome': ['com.android.chrome', 'com.google.android.apps.chrome.Main'],
            'YouTube': ['com.google.android.youtube', 'com.google.android.apps.youtube.app.watchwhile.WatchWhileActivity'],
            'Reddit': ['com.reddit.frontpage', 'launcher.default'],
            'Instagram': ['com.instagram.android', 'com.instagram.mainactivity.MainActivity'],
            'Twitter': ['com.twitter.android', 'com.twitter.app.main.MainActivity'],
            'Angry Birds 2': ['com.rovio.baba', 'com.unity3d.player.UnityPlayerActivity'],
            'Firefox': ['org.mozilla.firefox', 'org.mozilla.fenix.HomeActivity'],
            'Maps': ['com.google.android.apps.maps', 'com.google.android.maps.MapsActivity'],
            'Gmail': ['com.google.android.gm', '.ConversationListActivityGmail'],
            'TikTok': ['com.ss.android.ugc.trill', 'com.ss.android.ugc.aweme.splash.SplashActivity'],
            'Candy Crush': ['com.king.candycrushsaga', '.CandyCrushSagaActivity'],
            'Telegram': ['org.telegram.messenger', 'org.telegram.ui.LaunchActivity'],
            'Messenger': ['com.facebook.orca', '.auth.StartScreenActivity'],
            'Cookie Run': ['com.devsisters.gb', '.AppActivity'],
            'MoPTT': ['mong.moptt', '.MainActivity'],
            'Zombie': ['com.ea.game.pvzfree_row', '.PvZActivity'],
            'Homescapes': ['com.playrix.homescapes', '.GoogleGameActivity'],
            'Attack': ['com.outfit7.movingeye.swampattack', 'com.libo7.swampattack.MainActivity']}

filename = sys.argv[2]+datetime.today().strftime('_%m%d_%H%M')

class AppConfig:
    def __init__(self, app_config):
        self.name = app_config[0]
        self.test_round = app_config[1]
        self.round_search_cnt = app_config[2]
        self.search_list = []
        self.cur_search_ptr = 0

        path = './config/' + self.name + '.txt'
            
        try:
            with open(path, 'r') as search_list_file:
                for inp in search_list_file:
                    spt = inp.split('\n')[0]
                    self.search_list.append(spt)
                    # if len(self.search_list) == self.round_search_cnt * self.test_round:
                    #    break
        except:
            print('file not exist.')
    
    def get_search_text(self):
        tmp = self.cur_search_ptr
        self.cur_search_ptr = (self.cur_search_ptr + 1) % len(self.search_list)
        return self.search_list[tmp]

    def get_app_config(self):
        return self

class Automator:
    '''
        Auto use the application
    '''

    def __init__(self):
        self.device = u2.connect()
        self.apps = {}
        self.app_handler = {}
        self.fb_is_first_time_open = True
        self.swipe_times = 10
        #self.swipe_down_times_browser = 10
        #self.swipe_up_times_browser = 5
        self.swipe_down_times_browser = 3
        self.swipe_up_times_browser = 1
        self.device.set_fastinput_ime(False)
        self.device.implicitly_wait(600.0)
        self.device.set_new_command_timeout(600)
        self.device.wait_timeout = 600.0
        self.test_round = 0
        self.trace_flow = []

        # chrome setting
        self.chrome_cur_tab_idx = 0

        # firefox setting
        self.fx_cur_tab_idx = 0


    def setup_apps(self, app_config):
        self.apps[app_config.name] = app_config

        if app_config.test_round > self.test_round:
            self.test_round = app_config.test_round
        
        if app_config.name not in self.app_handler:
            if app_config.name == 'YouTube':
                self.app_handler[app_config.name] = self.youtube
            elif app_config.name == 'Chrome':
                self.app_handler[app_config.name] = self.chrome
            elif app_config.name == 'Firefox':
                self.app_handler[app_config.name] = self.firefox
            elif app_config.name == 'Twitter':
                self.app_handler[app_config.name] = self.twitter
            elif app_config.name == 'Facebook':
                self.app_handler[app_config.name] = self.facebook
            elif app_config.name == 'Reddit':
                self.app_handler[app_config.name] = self.reddit
            elif app_config.name == 'Instagram':
                self.app_handler[app_config.name] = self.instagram
            elif app_config.name == 'Gmail':
                self.app_handler[app_config.name] = self.open_swipe
            elif app_config.name == 'Maps':
                self.app_handler[app_config.name] = self.googlemap
            elif app_config.name == 'TikTok':
                self.app_handler[app_config.name] = self.tiktok
            else:
                print(app_config.name + ' not found, default open and sleep')
                self.app_handler[app_config.name] = self.open_sleep

    def setup_trace_flow(self, test_round, trace_flow):
        self.test_round = int(test_round)

        for app_name in trace_flow:
            self.trace_flow.append(app_name)

    
    '''
    def chrome(self, app_config):
        print('chrome start')
        
        try:
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()

                time.sleep(1.5)
                self.device.press('search')
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(2)
                self.device.press('enter')
                time.sleep(10)
                
                for _ in range(self.swipe_down_times_browser):
                    time.sleep(1)
                    self.device.swipe(805, 1631, 813, 821, 0.2)
                for _ in range(self.swipe_up_times_browser):
                    time.sleep(1)
                    self.device.swipe(813, 821, 805, 1631, 0.2)
        except:
            print('chrome error')
    '''

    def chrome(self, app_config):
        print('chrome start')
        
        try:
            # self.device(resourceId='com.android.chrome:id/tab_switcher_button').click()
            for cnt in range(app_config.round_search_cnt):
                # print(self.chrome_cur_tab_idx, self.chrome_tab_cnt)

                '''
                orig
                if cnt != 0:
                    self.device(resourceId='com.android.chrome:id/tab_switcher_button').click()

                    if self.chrome_cur_tab_idx < 4:
                        self.device.swipe(805, 821, 805, 1631)
                        time.sleep(1)
                        self.device.swipe(805, 821, 805, 1631)
                        time.sleep(1)
                    else:
                        self.device.swipe(805, 1631, 805, 821)
                        time.sleep(1)
                        self.device.swipe(805, 1631, 805, 821)
                        time.sleep(1)

                    if self.chrome_cur_tab_idx == 0:
                        self.device.click(374, 793)
                    elif self.chrome_cur_tab_idx == 1:
                        self.device.click(1066, 793)
                    elif self.chrome_cur_tab_idx == 2:
                        self.device.click(374, 1708)
                    elif self.chrome_cur_tab_idx == 3:
                        self.device.click(1066, 1708)
                    elif self.chrome_cur_tab_idx == 4:
                        self.device.click(374, 1713)
                    elif self.chrome_cur_tab_idx == 5:
                        self.device.click(1066, 1713)
                '''

                self.device(resourceId='com.android.chrome:id/tab_switcher_button').click()
                time.sleep(3)

                #if (self.device(resourceId='com.android.chrome:id/tab_list_view').child(className='android.widget.FrameLayout', clickable=True, index=cnt).exists):
                #    self.device(resourceId='com.android.chrome:id/tab_list_view').child(className='android.widget.FrameLayout', clickable=True, index=cnt).click()
                if (self.device(resourceId='com.android.chrome:id/tab_list_view').child(className='android.widget.FrameLayout', clickable=True, index=self.chrome_cur_tab_idx).exists):
                    self.device(resourceId='com.android.chrome:id/tab_list_view').child(className='android.widget.FrameLayout', clickable=True, index=self.chrome_cur_tab_idx).click()
                else:
                    self.device(resourceId='com.android.chrome:id/new_tab_view').click()
                    self.device(resourceId='com.android.chrome:id/search_box').click()
                time.sleep(5)

                search_text = app_config.get_search_text()

                time.sleep(1.5)
                self.device.press('search')
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                #if cnt == 0:
                #    self.device.send_keys('https://vip.udn.com/vip/index')
                #else:
                #    self.device.send_keys(search_text)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(2)
                self.device.press('enter')
                time.sleep(10)
                
                for _ in range(self.swipe_down_times_browser):
                    time.sleep(1)
                    self.device.swipe(805, 1631, 813, 821, 0.2)
                for _ in range(self.swipe_up_times_browser):
                    time.sleep(1)
                    self.device.swipe(813, 821, 805, 1631, 0.2)

                if cnt != app_config.round_search_cnt - 1:
                    self.chrome_cur_tab_idx = (self.chrome_cur_tab_idx + 1) % app_config.round_search_cnt
                
                time.sleep(2)

        except:
            print('chrome error')
    '''
    def firefox(self, app_config):
        print('firefox start')

        try:
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()

                time.sleep(1.5)
                self.device.click(700, 180)
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(2)
                self.device.press('enter')
                time.sleep(10)
                
                for _ in range(self.swipe_down_times_browser):
                    time.sleep(1)
                    self.device.swipe(805, 1631, 813, 821, 0.2)
                for _ in range(self.swipe_up_times_browser):
                    time.sleep(1)
                    self.device.swipe(813, 821, 805, 1631, 0.2)
        except:
            print('firefox error')
    '''
    def firefox(self, app_config):
        print('firefox start')

        try:
            for cnt in range(app_config.round_search_cnt):
                # print(self.fx_cur_tab_idx, self.fx_tab_cnt)

                '''
                orig
                if cnt != 0:
                    self.device(resourceId='org.mozilla.firefox:id/counter_box').click()
                    time.sleep(3)

                    if self.fx_cur_tab_idx == 0:
                        self.device(resourceId='org.mozilla.firefox:id/tab_item', index='0').click()
                    elif self.fx_cur_tab_idx == 1:
                        self.device(resourceId='org.mozilla.firefox:id/tab_item', index='1').click()
                    elif self.fx_cur_tab_idx == 2:
                        self.device(resourceId='org.mozilla.firefox:id/tab_item', index='2').click()
                    elif self.fx_cur_tab_idx == 3:
                        self.device(resourceId='org.mozilla.firefox:id/tab_item', index='3').click()

                time.sleep(15)
                '''

                print('click tab')
                self.device(resourceId='org.mozilla.firefox:id/counter_box').click()
                time.sleep(5)

                print('tab select')
                self.device(resourceId='org.mozilla.firefox:id/tab_item', index=self.fx_cur_tab_idx).click()
                #if (self.device(resourceId='org.mozilla.firefox:id/tab_item').count > cnt):
                    #self.device(resourceId='org.mozilla.firefox:id/tab_item', index=cnt).click()
                #    self.device(resourceId='org.mozilla.firefox:id/tab_item', index=self.fx_cur_tab_idx).click()
                #else:
                #    self.device(resourceId='org.mozilla.firefox:id/new_tab_button').click()
                time.sleep(5)

                search_text = app_config.get_search_text()
                time.sleep(1.5)
                print('click search bar')
                self.device(resourceId='org.mozilla.firefox:id/mozac_browser_toolbar_url_view').click()
                # self.device.click(700, 180)
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                print('send url')
                #if self.fx_cur_tab_idx == 0:
                #    self.device.send_keys('https://vip.udn.com/vip/index')
                #else:
                #    self.device.send_keys(search_text)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(2)
                self.device.press('enter')
                time.sleep(10)
                
                for _ in range(self.swipe_down_times_browser):
                    time.sleep(1)
                    self.device.swipe(805, 1631, 813, 821, 0.2)
                for _ in range(self.swipe_up_times_browser):
                    time.sleep(1)
                    self.device.swipe(813, 821, 805, 1631, 0.2)

                if cnt != app_config.round_search_cnt - 1:
                    self.fx_cur_tab_idx = (self.fx_cur_tab_idx + 1) % app_config.round_search_cnt

                time.sleep(2)

        except:
            print('firefox error')


    def youtube(self, app_config):
        print('youtube start')

        try:
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()
            
                time.sleep(5)
                self.device.press('search')
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(1.5)
                self.device.press('enter')
                time.sleep(2)
                self.device.click(700, 1750)
                time.sleep(20)
        except:
            print('youtube error')

    def twitter(self, app_config):
        print('twitter start')

        try:
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()

                time.sleep(1.5)
                self.device.press('search')
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(2)
                self.device.press('enter')
                time.sleep(5)
                
                for _ in range(self.swipe_times):
                    time.sleep(1)
                    self.device.swipe(805, 1631, 813, 821, 0.1)
        except:
            print('twitter error')

    def facebook(self, app_config):
        print('facebook start')

        try:
            self.fb_is_first_time_open = True
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()

                time.sleep(1.5)

                # if device(resourceId='com.facebook.katana:id/(name removed)', className='android.widget.EditText').exists:
                #     device(resourceId='com.facebook.katana:id/(name removed)', className='android.widget.EditText').click()
                # else:
                #     device(resourceId='com.facebook.katana:id/(name removed)', className='android.widget.Button').click()
                if self.fb_is_first_time_open:
                    self.device(resourceId='com.facebook.katana:id/(name removed)', className='android.widget.Button', text='').click()
                    self.fb_is_first_time_open = False
                else:
                    self.device(resourceId='com.facebook.katana:id/(name removed)', className='android.widget.EditText').click()
                
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(1.5)
                self.device.press('enter')
                time.sleep(5)
                self.device.click(993, 602)
                time.sleep(5)

                for _ in range(self.swipe_times):
                    time.sleep(1)
                    self.device.swipe(805, 1631, 813, 821, 0.1)
            
                self.device.press('back')
                time.sleep(1)
                self.device.press('back')
                time.sleep(1)
            self.device.press('back')
            time.sleep(1)
            self.device.press('back')
            time.sleep(1)
        except:
            print('fb error')

    def instagram(self, app_config):
        print('instagram start')

        try:
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()

                time.sleep(1.5)
                self.device(resourceId = 'com.instagram.android:id/tab_bar').child(index=1).click()
                time.sleep(1.5)
                self.device(resourceId = 'com.instagram.android:id/action_bar_search_edit_text').click()
                time.sleep(1)
                self.device(resourceId = 'com.instagram.android:id/action_bar_search_edit_text').click()
                time.sleep(1)
                self.device.send_keys(search_text)
                print(search_text)
                self.device.press('enter')
                time.sleep(2)
                self.device(resourceId = 'com.instagram.android:id/recycler_view').child(index=0).click()
                time.sleep(5)

                for _ in range(self.swipe_times):
                    time.sleep(1)
                    self.device.swipe(805, 2000, 813, 1000, 0.1)
        except:
            print('ig error')

    def reddit(self, app_config):
        print('reddit start')

        try:
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()

                time.sleep(1.5)
                self.device.click(700, 160)
                time.sleep(1.5)
                self.device(resourceId='com.reddit.frontpage:id/search_clear_icon').click()
                time.sleep(1.5)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(2)
                self.device(resourceId='com.reddit.frontpage:id/search_results').child(index=0).click()
                time.sleep(5)

                for _ in range(self.swipe_times):
                    time.sleep(1)
                    self.device.swipe(805, 1631, 813, 821, 0.1)
        except:
            print('rd error')

    def open_swipe(self, app_config):
        print(app_config.name + ' open_swipe start')
        
        try:
            time.sleep(5)
            for _ in range(app_config.round_search_cnt):
                for __ in range(self.swipe_times):
                    time.sleep(1.5)
                    self.device.swipe(805, 1631, 813, 821, 0.1)
                for __ in range(self.swipe_times//2):
                        time.sleep(1.5)
                        self.device.swipe(813, 821, 805, 1631, 0.1)
        except:
            print(app_config.name + ' open_swipe error')

    def open_swipe_up(self, app_config):
        print(app_config.name + ' open_swipe_up start')
        
        try:
            time.sleep(5)
            for _ in range(app_config.round_search_cnt):
                for __ in range(self.swipe_times):
                    time.sleep(1.5)
                    self.device.swipe(805, 1631, 813, 821, 0.1)
        except:
            print(app_config.name + ' open_swipe_up error')

    def open_sleep(self, app_config):
        print(app_config.name + ' open_sleep start')
        try:
            time.sleep(20)
            #time.sleep(app_config.round_search_cnt * 15)
        except:
            print(app_config.name + ' open_sleep error')

    def tiktok(self, app_config):
        print('tiktok start')
        
        try:
            time.sleep(2)
            for _ in range(app_config.round_search_cnt):
                time.sleep(10)
                self.device.swipe(805, 1631, 813, 821, 0.1)
        except:
            print('tiktok error')
    
    def googlemap(self, app_config):
        print('googlemap start')
        
        try:
            for _ in range(app_config.round_search_cnt):
                search_text = app_config.get_search_text()

                time.sleep(1.5)
                self.device(resourceId='com.google.android.apps.maps:id/search_omnibox_text_box', className='android.widget.EditText').click()
                time.sleep(1.5)
                self.device.clear_text()
                time.sleep(1.5)
                self.device(resourceId='com.google.android.apps.maps:id/search_omnibox_text_box', className='android.widget.EditText').click()
                time.sleep(1.5)
                self.device.send_keys(search_text)
                print(search_text)
                time.sleep(2)
                self.device.press('enter')
                time.sleep(15)
        
        except:
            print('googlemap error')
    
    def run(self):
        self.device.screen_on()
        self.device.unlock()
        self.device.press('home')

        os.system('adb shell "echo 100 > /sys/class/power_supply/battery/capacity"')

        for app_name in self.apps.keys():
            os.system('adb shell rm -rf /data/data/' + packages[app_name][0] + '/cache/*')
        os.system('adb shell "echo 3 > /proc/sys/vm/drop_caches"')

        tmp = os.popen("adb shell cat /proc/vmstat").read()
        tmp = StringIO(tmp)
        vmstat_df = pd.read_csv(tmp, sep=" ", header=None, index_col=0, names=[-1])
        
        tmp = os.popen("adb shell cat /proc/diskstats| head -n 73 | tail -n 3  | awk '{print $3\" \"$10}'").read()
        tmp = StringIO(tmp)
        disk_w_df = pd.read_csv(tmp, sep=" ", header=None, index_col=0, names=[-1])

        tmp = os.popen("adb shell cat /proc/diskstats| head -n 73 | tail -n 3  | awk '{print $3\" \"$6}'").read()
        tmp = StringIO(tmp)
        disk_r_df = pd.read_csv(tmp, sep=" ", header=None, index_col=0, names=[-1])

        launch_time_df = pd.DataFrame(index=self.trace_flow, columns=list(range(0, self.test_round)))
        
        null_file = open(os.devnull, 'w')
        cpu_file = open(filename + '_cpu.txt', 'a')
        cmd = 'adb shell vmstat -n 1'
        cpu_proc = subprocess.Popen(cmd.split(), stdout=cpu_file, stderr=null_file)

        mem_file = open(filename + '_mem.txt', 'w')

        try:
            for cur_round in range(0, self.test_round):
                print('** cur round: ', cur_round)
                
                for idx in range(len(self.trace_flow)):
                    app_name = self.trace_flow[idx]

                    print('start running: ', app_name)

                    os.system('adb shell dumpsys gfxinfo '+packages[app_name][0]+' reset > /dev/null')
                    time.sleep(2)
                    
                    mem_tmp = os.popen('adb shell cat /proc/meminfo').read()
                    cur_mem = mem_tmp.split(' kB')[1].split(' ')[-1]
                    print('cur mem:', cur_mem)
                    mem_file.write('{}\n'.format(cur_mem))

                    
                    time.sleep(5)
                    #tmp = os.popen("adb shell am start -W "+packages[app_name][0]+"/"+packages[app_name][1]+" | awk '{if($1==\"TotalTime:\") print $2}'").read()
                    #tmp = tmp[:-1]
                    tmp = os.popen("adb shell am start -W "+packages[app_name][0]+"/"+packages[app_name][1]).read()
                    #cold_start = True

                    print(tmp)

                    #if tmp.find('Warning: Activity not started, its current task has been brought to the front') != -1:
                    #    cold_start = False

                    try:
                        launch_time = int(tmp.split('TotalTime')[0].split(' ')[-1])
                    except:
                        launch_time = int(tmp.split('Complete')[0].split(' ')[-1])

                    print('launch_time:', launch_time)

                    #if cold_start == False:
                    #    launch_time = -launch_time
                    launch_time_df.iloc[idx, cur_round] = launch_time
                    
                    #if tmp.isnumeric():
                    #    launch_time_df.iloc[idx, cur_round] = int(tmp)
                    #else:
                    #    print(tmp)
                    
                    time.sleep(2)

                    self.app_handler[app_name](self.apps[app_name])
                    os.system('adb shell dumpsys gfxinfo '+packages[app_name][0]+' reset >> '+filename+'_frame.txt')
                    time.sleep(2)
                    self.device.press('home')

                tmp = os.popen("adb shell cat /proc/vmstat").read()
                tmp = StringIO(tmp)
                tmp_df = pd.read_csv(tmp, sep=" ", header=None, index_col=0, names=[cur_round])
                vmstat_df[cur_round] = tmp_df[cur_round]

                tmp = os.popen("adb shell cat /proc/diskstats| head -n 73 | tail -n 3  | awk '{print $3\" \"$10}'").read()
                tmp = StringIO(tmp)
                tmp_df = pd.read_csv(tmp, sep=" ", header=None, index_col=0, names=[cur_round])
                disk_w_df[cur_round] = tmp_df[cur_round]

                tmp = os.popen("adb shell cat /proc/diskstats| head -n 73 | tail -n 3  | awk '{print $3\" \"$6}'").read()
                tmp = StringIO(tmp)
                tmp_df = pd.read_csv(tmp, sep=" ", header=None, index_col=0, names=[cur_round])
                disk_r_df[cur_round] = tmp_df[cur_round]
        finally:
            cpu_proc.kill()

            out_df = vmstat_df.append(disk_r_df)
            out_df = out_df.append(disk_w_df)
            out_df = out_df.append(launch_time_df)
            out_df.to_csv(filename+'.csv')

if __name__ == '__main__':
    autoTest = Automator()

    config_file = sys.argv[1]

    with open(config_file, 'r') as f:
        config_list = json.load(f)

        for app_config in config_list:
            app = AppConfig(app_config)
            autoTest.setup_apps(app)

    trace_flow_file = sys.argv[3]
    with open(trace_flow_file, 'r') as f:
        test_round = -1
        trace_flow = []
        for inp in f:
            spt = inp.split('\n')[0]

            if test_round == -1:
                test_round = int(spt)
            else:
                trace_flow.append(spt)

        autoTest.setup_trace_flow(test_round, trace_flow)

    autoTest.run()       
