# Python
import ConfigParser
import os
import tempfile
import xmlrpclib
from os.path import (
    dirname,
    join,
    abspath
)

#Grok & Zope
import grok
from zope.app.appsetup.bootstrap import getInformationFromEvent
from zope.interface import Interface
from zope.processlifetime import IDatabaseOpenedWithRoot

#Spionisto
from spionisto import MJPEG_PORT_BASE, TCP_PORT_BASE
from spionisto.interfaces import ICamera
from spionisto.interfaces import ICameraGstreamerPipeline

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

    db, connection, root, root_folder = getInformationFromEvent(event)

    s_api = xmlrpclib.ServerProxy(SUPERVISORD_URI)

    #Get the path to the scritps
    scripts_dir = join(dirname(abspath(__file__)), 'scripts')
    cam_script = join(scripts_dir, 'ip-camera.py')
    proxy_script = join(scripts_dir, 'gst-proxy.py')
    config_dir = tempfile.mkdtemp(prefix='spionisto')

    for app in root_folder.values():
        for camera in app.values():
            if ICamera.providedBy(camera):
                #Get pipeline and ports
                pipeline = ICameraGstreamerPipeline(camera).pipeline()
                port_http = MJPEG_PORT_BASE + camera.id
                port_tcp = TCP_PORT_BASE + camera.id

                #Create configuration file
                config_filename = os.path.join(config_dir, '%i.ini' % camera.id)
                config_file = ConfigParser.SafeConfigParser()
                config_file.add_section('spionisto')
                config_file.set('spionisto', 'port-http', str(port_http))
                config_file.set('spionisto', 'port-tcp', str(port_tcp))
                config_file.set('spionisto', 'pipeline', pipeline.encode('ascii', 'ignore'))
                with open(config_filename, 'wb') as fp:
                    config_file.write(fp)

                #Use supervisor's twiddler API to launch the proxy and the ipcamera
                s_api.twiddler.addProgramToGroup(
                    'dynamic',
                    'cam_script_%i' % camera.id,
                    {'command':'%s %s'%(cam_script, config_filename),
                     'autostart':'true',
                     'autorestart':'false', 'startsecs':'0'}
                )
                print 'command : %s %s'%(cam_script, config_filename)
                s_api.twiddler.addProgramToGroup(
                    'dynamic',
                    'proxy_script_%i' % camera.id,
                    {'command':'%s %s'%(proxy_script, config_filename),
                     'autostart':'true',
                     'autorestart':'false', 'startsecs':'2'}
                )
                print 'command : %s %s'%(proxy_script, config_filename)



