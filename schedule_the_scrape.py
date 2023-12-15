

import win32serviceutil
import win32service
import win32event
import servicemanager
import socket


# WORK IN PROGRESS! 
# INITIAL STAGES OF RUNNING THE SCRAPER AS A SERVICE ON WINDOWS

# https://stackoverflow.com/questions/2031111/in-python-how-can-i-put-a-thread-to-sleep-until-a-specific-time
# Comment from author: "Here's a half-ass solution that doesn't account for clock jitter or adjustment of the clock. See comments for ways to get rid of that.""

import time
import datetime

# if for some reason this script is still running
# after a year, we'll stop after 365 days
for i in range(0,365):
    # sleep until 2AM
    t = datetime.datetime.today()
    future = datetime.datetime(t.year,t.month,t.day,2,0)
    if t.hour >= 2:
        future += datetime.timedelta(days=1)
    time.sleep((future-t).total_seconds())
    
    
    
# https://stackoverflow.com/questions/32404/how-do-you-run-a-python-script-as-a-service-in-windows
    
class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "TestService"
    _svc_display_name_ = "Test Service"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)
    
    
# Windows task scheduler: start up script on computer start: