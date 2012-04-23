from fanstatic import Library, Resource
from js.bootstrap import bootstrap

library = Library('spionisto', 'static')

style = Resource(library, 'style.css', depends=[bootstrap])

