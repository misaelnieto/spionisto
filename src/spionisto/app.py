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
    def update(self):
        resource.style.need()


class About(grok.View):
    def update(self):
        resource.style.need()


class ControlPanel(grok.View):
    def update(self):
        resource.style.need()
