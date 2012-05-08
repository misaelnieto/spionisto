from setuptools import setup, find_packages

version = '0.1'
long_description = (
    open('README.txt').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='spionisto',
      version=version,
      description="surveillance system for IP Cameras made with Python ad GStreamer",
      long_description=long_description,
      # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Zope3",
        "Framework :: ZODB",
        "Intended Audience :: Developers",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications :: Conferencing",
        "Topic :: Communications :: Conferencing",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "Topic :: Multimedia :: Video",
        ],
      keywords="gstreamer camera mjpeg",
      author="Noe Nieto",
      author_email="nnieto@noenieto.com",
      url="https://github.com/tzicatl/spionisto",
      license="GPLv3",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grok',
                        'grokui.admin',
                        'fanstatic',
                        'zope.fanstatic',
                        'grokcore.startup',
                        # Add extra requirements here
                        'js.bootstrap',
                        ],
      entry_points={
          'fanstatic.libraries': [
              'spionisto = spionisto.resource:library',
          ]
      })
