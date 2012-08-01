geventweet
==========

Real-time Twitter streaming python web app using gevent and gevent-socketio.

The idea was to get a working and nice example of how to write a simple asynchronous web application using socketIO with python.
I took inspiration from the examples provided by the ``gevent-socketio`` team and the work of ajdavis/chirp, thank you guys.


technical overview
==================

``geventweet`` uses the following :

Main asynchronous logic and socketIO support by :
* gevent (http://www.gevent.org/)
* gevent-socketio (https://github.com/abourget/gevent-socketio)

Twitter Streaming API support by :
* tweetstream (http://pypi.python.org/pypi/tweetstream)

HTML5 interface using :
* bootstrap (https://github.com/twitter/bootstrap)


installation
============

Before you run the app, make sure you have the following available :
* ``gevent-socketio`` python module and its dependencies
* ``tweetstream`` python module

The ``bootstrap`` part is provided, don't worry about it.


try it out
==========

Just clone this repository and run geventweet.py with the following REQUIRED arguments :
$ python geventweet.py -u YOUR_TWITTER_LOGIN -p YOUR_TWITTER_PASSWD -k KEYWORD1,KEYWORD2


gentoo users
============

The required packages exist on the ultrabug overlay.
See http://git.overlays.gentoo.org/gitweb/ or use layman for easy installation ;)