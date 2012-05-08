#Zope
from zope.interface import Interface
from zope import schema

#spionisto
from spionisto import CAMERA_TYPES
from spionisto import SpionistoMessageFactory as _

##############################################################################
#Basic content-types

class ICamera(Interface):
    id = schema.Int(
        title=_(u'Camera Id'),
        description=_(u'Camera ID is used to dynamically assign ports'),
        readonly=True
    )
    overlay_text = schema.TextLine(
        title = _(u'Overlay text'),
        description = _(u'This text will be overlaid in the top of the video. Text cannot be longer than 80 chars.'),
        max_length = 80
    )
    hostname = schema.ASCIILine(
        title = _(u'Hostname or IP Address'),
        description = _(u'This is the hostname or the IP address of the IP camera'), 
    )
    camera_model = schema.Choice(
        title = _(u'Select camera model'),
        description = _(u'Select one camera from the list of supported models'),
        values = CAMERA_TYPES
    )

    def snapshot_url():
        """
        Returns the url for a snapshot of the camera.
        """

    def mjpeg_stream_url():
        """
        Returns a url for the MJPEG stream of this camera
        """

#############################################################################
## Adapters

class ICameraGstreamerPipeline(Interface):
    """
    Adapts a camera to a gstreamer pipeline
    """

    def pipeline():
        """
        Returns the gstreamer pipeline acording to context.
        """

class ICameraStreamURL(Interface):
    """
    Adapts a camera to a MJPEG stream url
    """

    def mjpeg():
        """
        Returns the url of the MJPEG stream acording to context
        """
