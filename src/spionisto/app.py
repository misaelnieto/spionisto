from zope.interface import Interface
import grok

from spionisto import resource

class Spionisto(grok.Application, grok.Container):
    pass

class Master(grok.View):
    """
    This is the main macro for consistent look & field
    """
    grok.context(Interface)


class Index(grok.View):
    selected_camera = '0'

    def update(self, selected=None):
        resource.style.need()
        if selected in self.context:
            self.selected_camera = selected
        else:
            self.selected_camera = '0'

    def li_class(self, camera_id):
        if camera_id == self.selected_camera:
            return 'active'

        return ''



class About(grok.View):
    def update(self):
        resource.style.need()


class ControlPanel(grok.View):
    def update(self):
        resource.style.need()
