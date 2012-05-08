# this directory is a package

from zope.i18n import MessageFactory
SpionistoMessageFactory = MessageFactory('spionisto')

#Base ports
MJPEG_PORT_BASE = 9100
TCP_PORT_BASE = 9200

CAMERA_TYPES = [
    'Dummy (GStreamer)',
    'Linksys Cisco - WVC54G'
]
