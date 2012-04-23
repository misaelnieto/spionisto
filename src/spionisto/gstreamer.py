#Python
import random

#Zope & Grok
from zope.interface import Interface
import grok

#Spionisto
from spionisto.camera import ICamera, CAMERA_TYPES


class IGStreamerPipeline(Interface):
    """
    Marker interface to adapt objects to a gstreamer pipeline
    """

    def pipeline(port):
        """
        Returns the gstreamer pipeline acording to context.

        @port parameter is needed to allocate http ports
        """

PATTERNS = ['smpte', 'snow', 'black', 'white', 'red', 'green', 'blue', 
            'checkers-1', 'checkers-2', 'checkers-4', 'checkers-8',
            'circular', 'blink', 'smpte75', 'zone-plate', 'gamut',
            'chroma-zone-plate', 'solid-color', 'ball', 'smpte100',
            'bar']

_DUMMY_PIPELINE = "videotestsrc pattern=%s ! video/x-raw-rgb, framerate=15/1,"\
                  " width=640, height=480 !  jpegenc ! multipartmux boundary=spionisto ! "\
                  "tcpclientsink port=%s"

_LINKSYS_PIPELINE = "souphttpsrc location=%s ! asfdemux ! decodebin2"\
                    "video/x-raw-rgb, framerate=15/1, width=640, height=480 ! "\
                    "jpegenc ! multipartmux boundary=spionisto ! "\
                    "tcpclientsink port=%s"

class PipelineAdapter(grok.Adapter):
    grok.context(ICamera)
    grok.provides(IGStreamerPipeline)

    def pipeline(self, port):
        if self.context.camera_model == CAMERA_TYPES[0]:
            return _DUMMY_PIPELINE %(random.choice(PATTERNS), port)
        else: #Assume linksys
            return _LINKSYS_PIPELINE %(self.context.media_stream_uri, port)
