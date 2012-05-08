from fanstatic import Library, Resource
from js.bootstrap import bootstrap
from js.jquery import jquery

library = Library('spionisto', 'static')

style = Resource(library, 'style.css', depends=[bootstrap])
validation_js = Resource(library, 'validation.js', depends=[jquery])

