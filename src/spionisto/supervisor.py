from zope.interface import Interface
import grok
import xmlrpclib

SUPERVISORD_URI = 'http://admin:admin@localhost:9000'

class SupervisordStatus(grok.View):
    grok.name('supervisor')
    grok.context(Interface)

    def status(self):
        try:
            s = xmlrpclib.ServerProxy(SUPERVISORD_URI)
            return {
                'online': True,
                'version': s.twiddler.getAPIVersion()
            }
        except:
            return {
                'online': False
            }

    def render(self):
        return 'Supervisord status view'
