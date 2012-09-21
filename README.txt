=========================
Spionisto server software
=========================

DESCRIPTION
-----------

Spionisto is a survilleance software created from opensource technologies and 
standards such as:

 * Python
 * Grok
 * GStreamer
 * zc.buildout
 * supervisord


Install instructions for Fedora 17
----------------------------------

.. note:: You will need internet connection for some of these commands.

Install dependencies using yum:

    yum install -y git make automake gcc python-devel

Get a copy of this repo using git:

    git clone git://github.com/tzicatl/spionisto.git

If you get a message saying something like this:

    The authenticity of host 'github.com (XX.XX.XX.XX' can't be stablished
    RSA key fingerprint ....
    Are you sure you want con continue connecting (yes/no)? 

This is a message from SSH complaining about the authenticity of github's RSA
certificate because it has never seen it before. It is fairly safe to sure to
answer ``yes`` and hit enter here.

That should have created a new ``spionisto`` directory. Now run the bootstrap
script that is inside that directory:

    cd spionisto
    python -S bootstrap.py

A few messages will be printed and at the end you will se printed something
like:

    Got zc.buildout 1.5.2
    Generated script '/home/user/spionisto/bin/buildout'

That's a good sign so we can continue with the buildout process. From within
the spionisto directory run the following command:

    bin/buildout

That will start the buildout process. A lot of messages will be printed in the
screen. That's `zc.buildout <http://buildout.org>`_ doing it's job: It's
assembling the spionisto application from a lot of small software parts
scatered across the internet. If everything goes well, at the end you will see
the following message:

After finished run:

    bin/supervisord -c parts/etc/supervisord.conf

And open this URL in your browser: http://localhost:8080. You will be asked a
username and password. By default they both are ``admin``.

There's two panels: one for installed applications (Empty at this time), and
one for adding applications. Select the name for the application (eg:
spionisto) and click on the ``Create`` button.

Now the ``spionisto`` app is listed on the installed applications. Click on
the link and you will be welcomed with a big box saying *No cameras*. Now you
are in the spionisto application.


Troubleshooting
---------------

1) Command 'gcc' failed with status 1

R: Install the yum dependencies.


