from zope import schema
from zope.interface import Interface
from zope.schema.fieldproperty import FieldProperty
import grok

from spionisto import resource
from spionisto.app import Spionisto
from spionisto import SpionistoMessageFactory as _

CAMERA_TYPES = [
    'Dummy (GStreamer)',
    'Linksys Cisco - WVC54G'
]

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

class Camera(grok.Model):
    grok.implements(ICamera)

    overlay_text = FieldProperty(ICamera['overlay_text'])
    hostname = FieldProperty(ICamera['hostname'])
    camera_model = FieldProperty(ICamera['camera_model'])

    def mjpeg_stream_url(self):
        return 'http://localhost:1337/mjpeg'


class Index(grok.View):
    grok.context(ICamera)

    def render(self):
        return str (self.context)


class CameraAddForm(grok.AddForm):
    grok.context(Spionisto)
    grok.name('add')
    form_fields = grok.AutoFields(ICamera).omit('id')
    template = grok.PageTemplateFile('camera_templates/form.pt')

    label = _(u'Add a new camera')

    def update(self):
        resource.style.need()
        resource.validation_js.need()

    @grok.action(_(u'Add camera'))
    def add_camera(self, **data):
        new_camera = Camera()
        self.applyData(new_camera, **data)
        camera_id = len(self.context)
        self.context[camera_id] = new_camera

        self.flash(_(u'Added new camera'))
        return self.redirect(self.application_url())

class EditForm(grok.EditForm):
    grok.context(ICamera)
    form_fields = grok.AutoFields(ICamera)
    template = grok.PageTemplateFile('camera_templates/form.pt')
    
    label = _(u'Edit a camera')

    def update(self):
        resource.style.need()

    @grok.action(_(u'Save changes'))
    def add_camera(self, **data):
        self.applyData(self.context, **data)
        grok.notify(grok.ObjectModifiedEvent(self.context))

        self.flash(_(u'Changes were saved'))
        return self.redirect(self.application_url())

    @grok.action(_(u'Cancel'))
    def handle_cancel(self, **data):
        self.flash(_(u'Cancel edition'))
        return self.redirect(self.application_url())
