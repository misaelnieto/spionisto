import grok

from spionisto import resource

class Spionisto(grok.Application, grok.Container):
    pass

class Index(grok.View):
    def update(self):
        resource.style.need()
