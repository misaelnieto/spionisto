import grok
from zope.schema.fieldproperty import FieldProperty


from spionisto import resource
from spionisto import SpionistoMessageFactory as _
from spionisto.app import Spionisto
from spionisto import CAMERA_TYPES
from spionisto.interfaces import (
    ICamera,
    ICameraGstreamerPipeline,
    ICameraStreamURL
)
import spionisto.gstreamer



class Camera(grok.Model):
    grok.implements(ICamera)

    overlay_text = FieldProperty(ICamera['overlay_text'])
    hostname = FieldProperty(ICamera['hostname'])
    camera_model = FieldProperty(ICamera['camera_model'])

    def mpeg_stream_url():
        from spionisto.tools import ICameraStreamURL
        return ICameraStreamURL(self).mjpeg()


class Index(grok.View):
    grok.context(ICamera)

    def render(self):
        return str (self.context)

##############################################################################
## Forms

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


#############################################################################
## Adapters

class PipelineAdapter(grok.Adapter):
    grok.context(ICamera)
    grok.provides(ICameraGstreamerPipeline)

    def pipeline(self):
        if self.context.camera_model == CAMERA_TYPES[0]:
            return spionisto.gstreamer.dummy.pipeline(self.context)
        else: #Assume linksys
            return spionisto.gstreamer.wvc54g.pipeline(self.context)


class StreamUrlAdapter(grok.Adapter):
    grok.context(ICamera)
    grok.provides(ICameraStreamURL)

    def mjpeg(self):
        return 'http://localhost:%i/mjpeg_stream'% (
            MJPEG_PORTBASE + context.id
        )
