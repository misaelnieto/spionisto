from zope import schema
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
import grok

from spionisto import resource
from spionisto.app import Spionisto
from spionisto import SpionistoMessageFactory as _

CAMERA_TYPES = [
    'Dummy (GStreamer)',
    'Linksys'
]

class ICamera(Interface):
    overlay_text = schema.TextLine(
        title = _(u'Overlay text'),
        description = _(u'This text will be overlaid in the top of the video. Text cannot be longer than 80 chars.'),
        max_length = 80
    )
    media_stream_uri = schema.URI(
        title = _(u'Media stream URI'),
        description = _(u'This is the URL where the video stream is available'), 
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

class Camera(grok.Model):
    grok.implements(ICamera)

    overlay_text = FieldProperty(ICamera['overlay_text'])
    media_stream_uri = FieldProperty(ICamera['media_stream_uri'])
    camera_model = FieldProperty(ICamera['camera_model'])

    def snapshot_url(self):
        return 'http://localhost:1337/snapshot'

    def mjpeg_stream_url(self):
        return 'http://localhost:1337/mjpeg'


class Index(grok.View):
    grok.context(ICamera)

    def render(self):
        return str (self.context)


class AddForm(grok.AddForm):
    grok.context(Spionisto)
    form_fields = grok.AutoFields(ICamera)
    template = grok.PageTemplateFile('camera_templates/form.pt')

    label = _(u'Add a new camera')

    def update(self):
        resource.style.need()

    @grok.action(_(u'Add camera'))
    def add_camera(self, **data):
        new_camera = Camera()
        self.applyData(new_camera, **data)
        camera_id = str(len(self.context))
        self.context[camera_id] = new_camera
        grok.notify(grok.ObjectAddedEvent(new_camera))

        return self.redirect(self.url(new_camera))
