'''
Created on 25/ago/2013

@author: katta
'''
import os

class SystemInfo(object):
    '''
    classdocs
    '''
    
    def load(self):
        return 'load average: %s %s %s' % os.getloadavg()

    def uptime(self):
        uptime_file = open('/proc/uptime')
        uptime = uptime_file.readline().split()[0]
        uptime_file.close()

        uptime = float(uptime)
        (uptime,secs) = (int(uptime / 60), uptime % 60)
        (uptime,mins) = divmod(uptime,60)
        (days,hours) = divmod(uptime,24)

        uptime = 'uptime: %d day%s, %d:%02d' % (days, days != 1 and 's' or '', hours, mins)
        return uptime
    
    def __meminfo(self):
        meminfo_file = open('/proc/meminfo')
        meminfo = {}
        for x in meminfo_file:
            try:
                (key,value,junk) = x.split(None, 2)
                key = key[:-1] # strip off the trailing ':'
                meminfo[key] = int(value)
            except:
                pass
        meminfo_file.close()
        return meminfo
    
    def memusage(self):
        meminfo=self.__meminfo()

        memusage = 'Memory used: %d of %d kB (%d%%) - %d kB free' \
                   % (meminfo['MemTotal']-meminfo['MemFree'],
                      meminfo['MemTotal'],
                      100 - (100*meminfo['MemFree']/meminfo['MemTotal']),
                      meminfo['MemFree'])
        return (memusage)
    def hasSwap(self):
        if self.__meminfo()['SwapTotal']:
            return True
        else:
            return False
    
    def swapusage(self):
        meminfo=self.__meminfo()
        if meminfo['SwapTotal']:
            swapusage = 'Swap used: %d of %d kB (%d%%) - %d kB free' \
                      % (meminfo['SwapTotal']-meminfo['SwapFree'],
                         meminfo['SwapTotal'],
                         100 - (100*meminfo['SwapFree']/meminfo['SwapTotal']),
                         meminfo['SwapFree'])
            return swapusage
    def who(self):
        who_pipe = os.popen('/usr/bin/who', 'r')
        who = who_pipe.read().strip()
        who_pipe.close()
        return who
    
    def df(self):
        dfpath=SystemUtils.which('df')
        with os.popen('%s -h' % dfpath,'r') as df_p:
            return df_p.read()

    
    def serverinfo(self):
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % ( version, loadavg, )