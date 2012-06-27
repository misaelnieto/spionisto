#!/usr/bin/env python

import sys, os, time, thread
import ConfigParser
import glib, gobject
import pygst
pygst.require("0.10")
import gst

class IPCameraProxy(object):

    pipeline = None

    def __init__(self, pipeline):
        self.pipeline = gst.parse_launch(pipeline)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.pipeline.set_state(gst.STATE_NULL)

        elif t == gst.MESSAGE_ERROR:
            self.pipeline.set_state(gst.STATE_NULL)
            err, debug = message.parse_error()
            print "Error: %s" % err, debug

    def start(self):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)


def load_configuration(filename):
    """
    Loads configuration. Just returns the port
    """
    config = ConfigParser.SafeConfigParser()
    config.read(filename)
    return config.get('spionisto', 'pipeline')

if __name__ == '__main__':
    pipeline = load_configuration(sys.argv[1])
    proxy = IPCameraProxy(pipeline)
    thread.start_new_thread(proxy.start, ())
    gobject.threads_init()
    loop = glib.MainLoop()
    loop.run()
