# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Tobii controller for kelpy
# original author: Hiroyuki Sogo, modified by Horea Christian (for psychopy)
# modified for kelpy by Amanda Yung
# original version: https://github.com/TheChymera/E2att/blob/1c09a0d46b6627346bafba60739329c626d759ce/letobii.py
#
# *** Tobii SDK 3.0 is required. Get it at:
# http://www.tobii.com/en/eye-tracking-research/global/landingpages/analysis-sdk-30
# Also add it to your PYTHONPATH environment variable. The 'tobii' package is located in:
# tobiisdk/python27/modules
#
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#the 'tobii' here is the tobii sdk package
from tobii.eye_tracking_io.basic import EyetrackerException

import os
import datetime

import tobii.eye_tracking_io.mainloop
import tobii.eye_tracking_io.browsing
import tobii.eye_tracking_io.eyetracker
import tobii.eye_tracking_io.time.clock
import tobii.eye_tracking_io.time.sync


class TobiiController:
    def __init__(self, screen):
        self.eyetracker = None
        self.eyetrackers = {}
        self.screen = screen
        self.gazeData = []
        self.eventData = []
        self.datafile = None
        
        tobii.eye_tracking_io.init()
        self.clock = tobii.eye_tracking_io.time.clock.Clock()
        self.mainloop_thread = tobii.eye_tracking_io.mainloop.MainloopThread()
        self.browser = tobii.eye_tracking_io.browsing.EyetrackerBrowser(self.mainloop_thread, lambda t, n, i: self.on_eyetracker_browser_event(t, n, i))
        self.mainloop_thread.start()
        
    def wait_for_find_eyetracker(self, timeout=1000):
	"""
	Look for the eyetracker. Times out after x seconds
	"""
	start_time = self.clock.get_time()/1000000
	print "Looking for Tobii eyetracker..."
	
        while len(self.eyetrackers.keys())==0:
             if (self.clock.get_time()/1000000 - start_time > timeout):
		print "***No Tobii found! Make sure it is connected. Quitting..."
		self.destroy()
		quit()
        
    def on_eyetracker_browser_event(self, event_type, event_name, eyetracker_info):
        # When a new eyetracker is found we add it to the treeview and to the 
        # internal list of eyetracker_info objects
        if event_type == tobii.eye_tracking_io.browsing.EyetrackerBrowser.FOUND:
            self.eyetrackers[eyetracker_info.product_id] = eyetracker_info
            return False
        
        # Otherwise we remove the tracker from the treeview and the eyetracker_info list...
        del self.eyetrackers[eyetracker_info.product_id]
        
        # ...and add it again if it is an update message
        if event_type == tobii.eye_tracking_io.browsing.EyetrackerBrowser.UPDATED:
            self.eyetrackers[eyetracker_info.product_id] = eyetracker_info
        return False
        
    def destroy(self):
        self.eyetracker = None
        self.browser.stop()
        self.browser = None
        self.mainloop_thread.stop()
        
    ############################################################################
    # activation methods
    ############################################################################
    def activate(self,eyetracker):
        eyetracker_info = self.eyetrackers[eyetracker]
        print "Connecting to:", eyetracker_info
        tobii.eye_tracking_io.eyetracker.Eyetracker.create_async(self.mainloop_thread,
                                                     eyetracker_info,
                                                     lambda error, eyetracker: self.on_eyetracker_created(error, eyetracker, eyetracker_info))
        
        while self.eyetracker==None:
            pass
        self.syncmanager = tobii.eye_tracking_io.time.sync.SyncManager(self.clock,eyetracker_info,self.mainloop_thread)
        
    def on_eyetracker_created(self, error, eyetracker, eyetracker_info):
        if error:
            print "  Connection to %s failed because of an exception: %s" % (eyetracker_info, error)
            if error == 0x20000402:
                print "The selected unit is too old, a unit which supports protocol version 1.0 is required.\n\n<b>Details:</b> <i>%s</i>" % error
            else:
                print "Could not connect to %s" % (eyetracker_info)
            return False
        
        self.eyetracker = eyetracker
        
    ############################################################################
    # calibration methods
    ############################################################################
    
	#none for now since the lab does tobii calibration through TobiiStudio...
   
    ############################################################################
    # tracking & data methods
    ############################################################################
    
    def start_tracking(self):
        self.gazeData = []
        self.eventData = []
        self.eyetracker.events.OnGazeDataReceived += self.on_gazedata
        self.eyetracker.StartTracking()
    
    def stop_tracking(self):
        self.eyetracker.StopTracking()
        self.eyetracker.events.OnGazeDataReceived -= self.on_gazedata
        self.flush_data()
        self.gazeData = []
        self.eventData = []
    
    def on_gazedata(self,error,gaze):
        self.gazeData.append(gaze)
    
    def get_gaze_position(self,gaze):
	"""
	Returns left x,y and right x,y positions in screen coordinates.
	Since Tobii uses normalized units, need to multiply by screen size. 
	This assumes that the kelpy window is fullsized; may need to change this for future versions?
		
	"""
    	# Verify that the gaze data is valid, otherwise reject it.
    	# Summarized from the Tobii SDK Guide:
	# 0 = found both eyes
    	# 1 = found one eye, probably the correct eye assignment
    	# 2 = found one eye, but not sure which
    	# 3 = found one eye, but probably the other eye
    	# 4 = found no eyes
    	# Should just use data with code 0 or 1 (reject 2+)
            
	if gaze.LeftValidity >= 2 and gaze.RightValidity >= 2:
		return (None,None,None,None)

        return (int(gaze.LeftGazePoint2D.x*self.screen.get_width()),
                int(gaze.LeftGazePoint2D.y*self.screen.get_height()),
                int(gaze.RightGazePoint2D.x*self.screen.get_width()),
                int(gaze.RightGazePoint2D.y*self.screen.get_height()))
    
    def get_current_gaze_position(self):
	"""
	Returns latest gaze position
		
	"""
    
        if len(self.gazeData)==0:
            return (None,None,None,None)
        else:
            return self.get_gaze_position(self.gazeData[-1])
    
    
    def get_left_gaze(self):
	"""
	Returns only the left gaze point, or None tuple if not valid
		
	"""
	return self.get_current_gaze_position()[0:2]
		
    def get_right_gaze(self):
	"""
	Returns only the right gazepoint, or None tuple if not valid
		
	"""
	return self.get_current_gaze_position()[2:4]
		
    def get_center_gaze(self):
	"""
	Averages the left and right gaze points
    
	"""
	gaze_point = self.get_current_gaze_position()
		
	if None in gaze_point:
	    return (None,None)
	else:
	    return int((gaze_point[0] + gaze_point[2])/2), int((gaze_point[1] + gaze_point[3])/2)
    

    #pre-existing data writing methods; adjusted slightly for validity codes
    def set_data_file(self,filename):
        print 'set datafile ' + filename
        self.datafile = open(filename,'w')
        self.datafile.write('Recording date:\t'+datetime.datetime.now().strftime('%Y/%m/%d')+'\n')
        self.datafile.write('Recording time:\t'+datetime.datetime.now().strftime('%H:%M:%S')+'\n')
        self.datafile.write('Recording resolution\t%d x %d\n\n' % (self.screen.get_width(), self.screen.get_height()))
        
    def close_data_file(self):
        print 'datafile closed'
        if self.datafile != None:
            self.flush_data()
            self.datafile.close()
        
        self.datafile = None
    
    def record_event(self,event):
        t = self.syncmanager.convert_from_local_to_remote(self.clock.get_time())
        self.eventData.append((t,event))
    
    def flush_data(self):
        if self.datafile == None:
            print 'data file is not set.'
            return
        
        if len(self.gazeData)==0:
            return
        
        self.datafile.write('\t'.join(['TimeStamp',
                                       'GazePointXLeft',
                                       'GazePointYLeft',
                                       'ValidityLeft',
                                       'GazePointXRight',
                                       'GazePointYRight',
                                       'ValidityRight',
                                       'GazePointX',
                                       'GazePointY',
                                       'Event'])+'\n')
        timeStampStart = self.gazeData[0].Timestamp
        for g in self.gazeData:
            self.datafile.write('%.1f\t%.4f\t%.4f\t%d\t%.4f\t%.4f\t%d'%(
                                (g.Timestamp-timeStampStart)/1000.0,
                                g.LeftGazePoint2D.x*self.screen.get_width() if g.LeftValidity<=1 else -1.0,
                                g.LeftGazePoint2D.y*self.screen.get_height() if g.LeftValidity<=1 else -1.0,
                                g.LeftValidity,
                                g.RightGazePoint2D.x*self.screen.get_width() if g.RightValidity<=1 else -1.0,
                                g.RightGazePoint2D.y*self.screen.get_height() if g.RightValidity<=1 else -1.0,
                                g.RightValidity))
            if g.LeftValidity >= 2 and g.RightValidity >= 2: #not detected
                ave = (-1.0,-1.0)
            elif g.LeftValidity >= 2:
                ave = (g.RightGazePoint2D.x,g.RightGazePoint2D.y)
            elif g.RightValidity >= 2:
                ave = (g.LeftGazePoint2D.x,g.LeftGazePoint2D.y)
            else:
                ave = ((g.LeftGazePoint2D.x+g.RightGazePoint2D.x)/2,
                       (g.LeftGazePoint2D.y+g.RightGazePoint2D.y)/2)
                
            self.datafile.write('\t%.4f\t%.4f\t'%ave)
            self.datafile.write('\n')
        
        formatstr = '%.1f'+'\t'*9+'%s\n'
        for e in self.eventData:
            self.datafile.write(formatstr % ((e[0]-timeStampStart)/1000.0,e[1]))
        
        self.datafile.flush()
