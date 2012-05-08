from zope.interface import Interface

class IGStreamerPipeline(Interface):
    """
    Marker interface to adapt objects to a gstreamer pipeline
    """

    def pipeline(port):
        """
        Returns the gstreamer pipeline acording to context.

        @port parameter is needed to allocate http ports
        """