#Python
import random

from spionisto import TCP_PORT_BASE

_PATTERNS = ['smpte', 'snow', 'black', 'white', 'red', 'green', 'blue', 
            'checkers-1', 'checkers-2', 'checkers-4', 'checkers-8',
            'circular', 'blink', 'smpte75', 'zone-plate', 'gamut',
            'chroma-zone-plate', 'solid-color', 'ball', 'smpte100',
            'bar']

_DUMMY_PIPELINE = 'videotestsrc pattern=%s ! video/x-raw-rgb, framerate=15/1, width=640, height=480 !  '\
                  'clockoverlay text="%s" valign=bottom shaded-background=true font-desc="Courier bold 24" ! '\
                  'jpegenc ! multipartmux boundary=spionisto ! '\
                  'tcpclientsink port=%s'


__all__ = ['pipeline']

def pipeline(context):
    return _DUMMY_PIPELINE %(
        random.choice(_PATTERNS), context.overlay_text, 
        TCP_PORT_BASE + context.id
    )
