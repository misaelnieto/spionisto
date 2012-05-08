# Python
import xmlrpclib

#Grok & Zope
import grok
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.interface import Interface
from zope.processlifetime import IDatabaseOpenedWithRoot

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

@grok.subscribe(IDatabaseOpenedWithRoot)
def launch_pipelines(event):
    from spionisto.interfaces import ICamera
    from spionisto.interfaces import ICameraGstreamerPipeline
    db, connection, root, root_folder = getInformationFromEvent(event)

    s_api = xmlrpclib.ServerProxy(SUPERVISORD_URI)
    for app in root_folder.values():
        for camera_id in app:
            if ICamera.providedBy(app[camera_id]):
                print 'Launching camera ', ICameraGstreamerPipeline(app[camera_id]).pipeline()


