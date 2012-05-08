from spionisto import TCP_PORT_BASE

__all__ = ['pipeline', ]

_P = [
    'souphttpsrc location=http://%s/img/video.asf',
    'asfdemux',
    'ffdec_mpeg4',
    'video/x-raw-rgb, framerate=15/1, width=640, height=480',
    'clockoverlay text="%s" valign=bottom shaded-background=true font-desc="Courier bold 24"'
    'jpegenc',
    'multipartmux boundary=spionisto',
    'tcpclientsink port=%s',
]


def pipeline(context):
    return ' ! '.join(_P) % (
        context.hostname, 
        context.overlay_text, 
        TCP_PORT_BASE + context.id
    )
