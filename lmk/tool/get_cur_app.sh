echo "time=`cat /proc/uptime`"
dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'
