#!/usr/bin/python

#This was directly taken from the examples included in the Tobii SDK

import pygtk
from tobii.eye_tracking_io.basic import EyetrackerException
pygtk.require('2.0')
import gtk
from time import time

glib_idle_add = None
glib_timeout_add = None
try:
    import glib
    glib_idle_add = glib.idle_add
    glib_timeout_add = glib.timeout_add
except:
    glib_idle_add = gtk.idle_add
    glib_timeout_add = gtk.timeout_add
    

import os
import math

import tobii.eye_tracking_io.mainloop
import tobii.eye_tracking_io.browsing
import tobii.eye_tracking_io.eyetracker

from tobii.eye_tracking_io.types import Point2D, Blob

class TrackStatus(gtk.DrawingArea):
    MAX_AGE = 30.0
    
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.eyetracker = None
        self.set_size_request(300, 300)
        self.connect("expose_event", self.on_expose)
        
        self.gazedata = None
        self.gaze_data_history = []
   
    def set_eyetracker(self, eyetracker):
        if self.eyetracker is not None:
            self.eyetracker.StopTracking()
            self.eyetracker.events.OnGazeDataReceived -= self.on_gazedata
        
        self.eyetracker = eyetracker
        self.gazedata = None
        if self.eyetracker is not None:
            self.eyetracker.events.OnGazeDataReceived += self.on_gazedata
            self.eyetracker.StartTracking()
    
    def on_gazedata(self, error, gaze):
        if hasattr(gaze, 'TrigSignal'):
            print "Trig signal:", gaze.TrigSignal
               
        gazedata_copy = { 'left': { 'validity':     gaze.LeftValidity,
                                    'camera_pos':   gaze.LeftEyePosition3DRelative,
                                    'screen_pos':   gaze.LeftGazePoint2D },
                          'right': { 'validity':    gaze.RightValidity,             
                                     'camera_pos':  gaze.RightEyePosition3DRelative,
                                     'screen_pos':  gaze.RightGazePoint2D          }} 
        try:
            glib_idle_add(self.handle_gazedata, error, gazedata_copy)
        except Exception, ex:
            print "  Exception occured: %s" %(ex)

    def handle_gazedata(self, error, gazedata):
        self.gazedata = gazedata
        self.gaze_data_history.append(self.gazedata)
        if len(self.gaze_data_history) > TrackStatus.MAX_AGE:
            self.gaze_data_history.pop(0)
        self.redraw()

    def redraw(self):
        if self.window:
            alloc = self.get_allocation()
            rect = gtk.gdk.Rectangle(0, 0, alloc.width, alloc.height)
            self.window.invalidate_rect(rect, True)
            self.window.process_updates(True)

    def draw_eye(self, ctx, validity, camera_pos, screen_pos, age):
        screen_pos_x = screen_pos.x - .5
        screen_pos_y = screen_pos.y - .5
        
        eye_radius = 0.075
        iris_radius = 0.03
        pupil_radius = 0.01

        opacity = 1 - age * 1.0 / TrackStatus.MAX_AGE
        if validity <= 1:
            ctx.set_source_rgba(1, 1, 1, opacity)
            ctx.arc(1 - camera_pos.x, camera_pos.y, eye_radius, 0, 2 * math.pi)
            ctx.fill()

            ctx.set_source_rgba(.5, .5, 1, opacity)
            ctx.arc(1 - camera_pos.x + ((eye_radius - iris_radius / 2) * screen_pos_x), camera_pos.y + ((eye_radius - iris_radius / 2) * screen_pos_y), iris_radius, 0, 2 * math.pi)
            ctx.fill()
            
            ctx.set_source_rgba(0, 0, 0, opacity)
            ctx.arc(1 - camera_pos.x + ((eye_radius - iris_radius / 2) * screen_pos_x), camera_pos.y + ((eye_radius - iris_radius / 2) * screen_pos_y), pupil_radius, 0, 2 * math.pi)
            ctx.fill()

    def draw(self, ctx):
        ctx.set_source_rgb(0., 0., 0.)
        ctx.rectangle(0, 0, 1, .9)
        ctx.fill()
        
        # paint left rectangle
        if self.gazedata is not None and self.gazedata['left']['validity'] == 0:
            ctx.set_source_rgb(0, 1, 0)
        else:
            ctx.set_source_rgb(1, 0, 0)
        ctx.rectangle(0, .9, .5, 1)
        ctx.fill()
        
        # paint right rectangle
        if self.gazedata is not None and self.gazedata['right']['validity'] == 0:
            ctx.set_source_rgb(0, 1, 0)
        else:
            ctx.set_source_rgb(1, 0, 0)
        ctx.rectangle(.5, .9, 1, 1)
        ctx.fill()
        
        if self.gazedata is None:
            return
        
        # paint eyes
        for eye in ('left', 'right'):
            (validity, age, camera_pos, screen_pos) = self.find_gaze(eye)
            self.draw_eye(ctx, validity, camera_pos, screen_pos, age)

    def find_gaze(self, eye):
        i = 0
        for gaze in reversed(self.gaze_data_history):
            if gaze[eye]['validity'] <= 1:
                return (gaze[eye]['validity'], i, gaze[eye]['camera_pos'], gaze[eye]['screen_pos'])
            i += 1
        return (gaze[eye]['validity'], 0, gaze[eye]['camera_pos'], gaze[eye]['screen_pos'])

    def on_expose(self, widget, event):
        context = widget.window.cairo_create()
        context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        context.clip()
        
        rect = widget.get_allocation()
        context.scale(rect.width, rect.height)

        self.draw(context)
        return False


class CalibPlot(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)

        self.set_size_request(300, 300)
        self.connect("expose_event", self.on_expose)
        
        self.calib = None
    
    def set_eyetracker(self, eyetracker):
        if eyetracker is None:
            return
        
        try:
            self.calib = eyetracker.GetCalibration(lambda error, calib: glib_idle_add(self.on_calib_response, error, calib))
        except Exception, ex:
            print "  Exception occured: %s" %(ex)
            self.calib = None
        self.redraw()
    
    def on_calib_response(self, error, calib):
        if error:
            print "on_calib_response: Error"
            self.calib = None
            self.redraw()
            return False
        
        self.calib = calib
        self.redraw()
        return False
            
    def redraw(self):
        if self.window:
            alloc = self.get_allocation()
            rect = gtk.gdk.Rectangle(0, 0, alloc.width, alloc.height)
            self.window.invalidate_rect(rect, True)
            self.window.process_updates(True)
    
    def on_expose(self, widget, event):
        context = widget.window.cairo_create()
        context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        context.clip()
        
        rect = widget.get_allocation()
        context.scale(rect.width, rect.height)

        self.draw(context)
    
    def draw(self, ctx):
        ctx.rectangle(0, 0, 1, 1)
        ctx.set_source_rgb(1, 1, 1)
        ctx.fill()
        
        if self.calib is None:
            ctx.move_to(0, 0)
            ctx.line_to(1, 1)
            ctx.move_to(0, 1)
            ctx.line_to(1, 0)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(0.001)
            ctx.stroke()
            return
        
        points = {}
        for data in self.calib.plot_data:
            points[data.true_point] = { 'left': data.left, 'right': data.right }
        
        if len(points) == 0:
            ctx.move_to(0, 0)
            ctx.line_to(1, 1)
            ctx.move_to(0, 1)
            ctx.line_to(1, 0)
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(0.001)
            ctx.stroke()
            return
        
        for p, d in points.iteritems():
            ctx.set_line_width(0.001)
            if d['left'].status == 1:
                ctx.set_source_rgb(1.0, 0., 0.)
                ctx.move_to(p.x, p.y)
                ctx.line_to(d['left'].map_point.x, d['left'].map_point.y)
                ctx.stroke()

            if d['right'].status == 1:            
                ctx.set_source_rgb(0., 1.0, 0.)
                ctx.move_to(p.x, p.y)
                ctx.line_to(d['right'].map_point.x, d['right'].map_point.y)
                ctx.stroke()
        
            ctx.set_line_width(0.005)
            ctx.set_source_rgba(0., 0., 0., 0.05)
            ctx.arc(p.x, p.y, 0.01, 0, 2 * math.pi)
            ctx.stroke ()


class Calibration:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.canvas = gtk.DrawingArea()
        self.window.add(self.canvas)
        self.canvas.connect("expose_event", self.on_expose)
        self.points = [(0.1,0.1), (0.9,0.1) , (0.5,0.5), (0.1,0.9), (0.9,0.9)]
        self.point_index = -1
        self.start_radius = 0.012
        self.current_radius = self.start_radius
        self.growth_speed = 0.00025
        self.shrink_dot = False
        self.start_time = 0
        self.on_calib_done = None

    def run(self, tracker, on_calib_done):
        self.window.fullscreen()
        self.window.show_all()
        self.on_calib_done = on_calib_done
        self.tracker = tracker
        self.point_index = -1
        self.tracker.StartCalibration(lambda error, r: glib_idle_add(self.on_calib_start, error, r))
        
    def on_calib_start(self, error, r):
        if error:
            self.on_calib_done(False, "Could not start calibration because of error. (0x%0x)" % error)
            return False
        
        self.wait_for_add()
        return False
        
    
    def on_expose(self, widget, event):
        context = widget.window.cairo_create()
        context.rectangle(event.area.x, event.area.y, event.area.width, event.area.height)
        context.clip()

        self.draw(context)
        return False
    
    def draw(self,ctx):
        if self.point_index > -1:
            x,y = self.points[self.point_index]
            if self.shrink_dot:
                self.current_radius = self.current_radius - self.growth_speed
            else:
                self.current_radius = self.current_radius + self.growth_speed
            
            bounds = self.canvas.get_allocation()
            # Draw calibration dot
            ctx.set_source_rgb(255,0,0)
            #radius = 0.012*bounds.width
            radius = self.current_radius*bounds.width
            ctx.arc(bounds.width*x, bounds.height*y, radius,0, 2 * math.pi)
            ctx.fill()
            
            # Draw center dot
            ctx.set_source_rgb(0,0,0);
            radius = 2;
            ctx.arc(bounds.width*x, bounds.height*y, radius,0, 2 * math.pi)
            ctx.fill()
            
            
    def wait_for_add(self):
        self.point_index += 1
        self.current_radius = self.start_radius
        #attempting to add this before calibration point is created
        self.start_time = time()
        self.shrink_dot = False
        glib_timeout_add(16, self.grow_dot)
        glib_timeout_add(2000, self.add_point)
        
    
    def add_point(self):
        p = Point2D()
        p.x, p.y = self.points[self.point_index]
        self.tracker.AddCalibrationPoint(p, lambda error, r: glib_idle_add(self.on_add_completed, error, r))
        return False
        
    def grow_dot(self):
		if (time() - self.start_time > 1.25):
			self.shrink_dot = True
			self.redraw()
			return True
		elif (time() - self.start_time > 2):
			return False
		else:
			self.redraw()
			return True
    

    def on_add_completed(self, error, r):
        if error:
            self.on_calib_done(False, "Add Calibration Point failed because of error. (0x%0x)" % error)
            return False
        
        if self.point_index == len(self.points) - 1:
            #This was the last calibration point
            self.tracker.ComputeCalibration(lambda error, r: glib_idle_add(self.on_calib_compute, error, r))
        else:
            #glib_timeout_add(50, self.redraw)
            self.wait_for_add()
        
        return False

    def on_calib_compute(self, error, r):
        if error == 0x20000502:
            print "CalibCompute failed because not enough data was collected"
            self.on_calib_done(False, "Not enough data was collected during calibration procedure.")
        elif error != 0:
            print "CalibCompute failed because of a server error"
            self.on_calib_done(False, "Could not compute calibration because of a server error.\n\n<b>Details:</b>\n<i>%s</i>" % (error))
        else:
            self.on_calib_done(True, "")
        self.tracker.StopCalibration(None)
        self.window.destroy()
        return False
    
    def redraw(self):
        if self.canvas.window:
            alloc = self.canvas.get_allocation()
            rect = gtk.gdk.Rectangle(0, 0, alloc.width, alloc.height)
            self.canvas.window.invalidate_rect(rect, True)


def show_message_box(parent, message, title="", buttons=gtk.BUTTONS_OK):
    def close_dialog(dlg, rid):
        dlg.destroy()

    msg = gtk.MessageDialog(parent=parent, buttons=buttons)
    msg.set_markup(message)
    msg.set_modal(False)
    msg.connect("response", close_dialog)
    msg.show()


class EyetrackerBrowser:

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(5)
        self.window.set_size_request(960, 480)

        self.eyetracker = None
        self.eyetrackers = {}        
        self.liststore = gtk.ListStore(str, str, str)

        self.treeview = gtk.TreeView(self.liststore)
        self.treeview.connect("row-activated", self.row_activated)

        self.pid_column = gtk.TreeViewColumn("PID")
        self.pid_cell = gtk.CellRendererText()
        self.treeview.append_column(self.pid_column)
        self.pid_column.pack_start(self.pid_cell, True)
        self.pid_column.set_attributes(self.pid_cell, text=0)

        self.model_column = gtk.TreeViewColumn("Model")
        self.model_cell = gtk.CellRendererText()
        self.treeview.append_column(self.model_column)
        self.model_column.pack_start(self.model_cell, True)
        self.model_column.set_attributes(self.model_cell, text=1)

        self.status_column = gtk.TreeViewColumn("Status")
        self.status_cell = gtk.CellRendererText()
        self.treeview.append_column(self.status_column)
        self.status_column.pack_start(self.status_cell, True)
        self.status_column.set_attributes(self.status_cell, text=2)

        self.trackstatus = TrackStatus()
        self.calibplot = CalibPlot()

        self.table = gtk.Table(3, 3)
        self.table.set_col_spacings(4)
        self.table.set_row_spacings(4)

        self.treeview_label = gtk.Label()
        self.treeview_label.set_alignment(0.0, 0.5)
        self.treeview_label.set_markup("<b>Discovered Eyetrackers:</b>")
        self.table.attach(self.treeview_label, 0, 1, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL)
        self.table.attach(self.treeview, 0, 1, 1, 2)
        
        self.calibplot_label = gtk.Label()
        self.calibplot_label.set_markup("<b>Calibration Plot:</b>")
        self.calibplot_label.set_alignment(0.0, 0.5)
        self.table.attach(self.calibplot_label, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL)
        self.table.attach(self.calibplot, 1, 2, 1, 2)
        
        self.trackstatus_label = gtk.Label()
        self.trackstatus_label.set_markup("<b>Trackstatus:</b>")
        self.trackstatus_label.set_alignment(0.0, 0.5)
        self.table.attach(self.trackstatus_label, 2, 3, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL)
        self.table.attach(self.trackstatus, 2, 3, 1, 2)

        self.buttonbar = gtk.HButtonBox()
        self.buttonbar.set_border_width(0)
        self.buttonbar.set_spacing(10)
        self.buttonbar.set_layout(gtk.BUTTONBOX_END)
        
        self.button = gtk.Button("Run Calibration")
        self.button.connect("clicked",self.on_calib_button_clicked)
        self.button.set_sensitive(False)
        
        self.buttonbar.add(self.button)
        
        self.eyetracker_label = gtk.Label()
        self.eyetracker_label.set_markup("<b>No eyetracker selected (double-click to choose).</b>")
        self.eyetracker_label.set_alignment(0.0, 0.5)
        self.table.attach(self.eyetracker_label, 0, 2, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL)
        self.table.attach(self.buttonbar, 2, 3, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL)

        self.window.add(self.table)
        self.window.show_all()
        
        # Setup Eyetracker stuff  
        tobii.eye_tracking_io.init()      
        self.mainloop_thread = tobii.eye_tracking_io.mainloop.MainloopThread()
        self.browser = tobii.eye_tracking_io.browsing.EyetrackerBrowser(self.mainloop_thread, lambda t, n, i: glib_idle_add(self.on_eyetracker_browser_event, t, n, i))

    def row_activated(self, treeview, path, user_data=None):
        # When an eyetracker is selected in the browser list we create a new 
        # eyetracker object and set it as the active one
        model = treeview.get_model()
        iter = model.get_iter(path)
        self.button.set_sensitive(False)
        self.trackstatus.set_eyetracker(None)
        self.calibplot.set_eyetracker(None)
        
        self.eyetracker_info = self.eyetrackers[model.get_value(iter, 0)]
        print "Connecting to:", self.eyetracker_info
        tobii.eye_tracking_io.eyetracker.Eyetracker.create_async(self.mainloop_thread,
                                                     self.eyetracker_info,
                                                     lambda error, eyetracker: glib_idle_add(self.on_eyetracker_created, error, eyetracker))
        
    #def on_eyetracker_created(self, error, eyetracker, eyetracker_info):
    def on_eyetracker_created(self, error, eyetracker):
        if error:
            print "  Connection to %s failed because of an exception: %s" % (self.eyetracker_info, error)
            if error == 0x20000402:
                show_message_box(parent=self.window, message="The selected unit is too old, a unit which supports protocol version 1.0 is required.\n\n<b>Details:</b> <i>%s</i>" % error)
            else:    
                show_message_box(parent=self.window, message="Could not connect to %s" % (self.eyetracker_info))
            return False
        
        self.eyetracker = eyetracker
        
        try:
            self.trackstatus.set_eyetracker(self.eyetracker)
            self.calibplot.set_eyetracker(self.eyetracker)
            self.button.set_sensitive(True)
            self.eyetracker_label.set_markup("<b>Connected to Eyetracker: %s</b>" % (self.eyetracker_info))
            print "   --- Connected!"
        except Exception, ex:
            print "  Exception occured: %s" %(ex)
            show_message_box(parent=self.window, message="An error occured during initialization of track status or fetching of calibration plot: %s" % (ex))
        return False

    def on_eyetracker_upgraded(self, error, protocol):
        try:
            self.trackstatus.set_eyetracker(self.eyetracker)
            self.calibplot.set_eyetracker(self.eyetracker)
            self.button.set_sensitive(True)
            self.eyetracker_label.set_markup("<b>Connected to Eyetracker: %s</b>" % (self.eyetracker_info))
            print "   --- Connected!"
        except Exception, ex:
            print "  Exception occured: %s" %(ex)
            show_message_box(parent=self.window, message="An error occured during initialization of track status or fetching of calibration plot: %s" % (ex))
        return False
    
    def on_calib_button_clicked(self, button):
        # Start the calibration procedure
        if self.eyetracker is not None:
            self.calibration = Calibration()
            self.calibration.run(self.eyetracker, lambda status, message: glib_idle_add(self.on_calib_done, status, message))
    
    def close_dialog(self, dialog, response_id):
        dialog.destroy()
    
    def on_calib_done(self, status, msg):
        # When the calibration procedure is done we update the calibration plot
        if not status:
            show_message_box(parent=self.window, message=msg)
            
        self.calibplot.set_eyetracker(self.eyetracker)
        self.calibration = None
        return False

    def on_eyetracker_browser_event(self, event_type, event_name, ei):
        # When a new eyetracker is found we add it to the treeview and to the 
        # internal list of eyetracker_info objects
        if event_type == tobii.eye_tracking_io.browsing.EyetrackerBrowser.FOUND:
            self.eyetrackers[ei.product_id] = ei
            self.liststore.append(('%s' % ei.product_id, ei.model, ei.status))
            return False
        
        # Otherwise we remove the tracker from the treeview and the eyetracker_info list...
        del self.eyetrackers[ei.product_id]
        iter = self.liststore.get_iter_first()
        while iter is not None:
            if self.liststore.get_value(iter, 0) == str(ei.product_id):
                self.liststore.remove(iter)
                break
            iter = self.liststore.iter_next(iter)
        
        # ...and add it again if it is an update message
        if event_type == tobii.eye_tracking_io.browsing.EyetrackerBrowser.UPDATED:
            self.eyetrackers[ei.product_id] = ei
            self.liststore.append([ei.product_id, ei.model, ei.status])
        return False
        

    def delete_event(self, widget, event, data=None):
        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        self.eyetracker = None
        self.calibplot.set_eyetracker(None)
        self.trackstatus.set_eyetracker(None)
        self.browser.stop()
        self.browser = None
        gtk.main_quit()

    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.gdk.threads_init()
        gtk.main()
        self.mainloop_thread.stop()

# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    eb = EyetrackerBrowser()
    eb.main()
