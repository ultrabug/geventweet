#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()

import argparse
import gevent
import json
import tweetstream

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace

sessions = set()

class TweetStreamNS(BaseNamespace):
	def on_get_tweets(self):
		""" A new client wants to be fed """
		sessions.add(self)
		print "active sessions : %s" % len(sessions)

	def recv_disconnect(self):
		""" Bye bye, remove the session from our set """
		try:
			sessions.remove(self)
		except:
			pass
		finally:
			print "active sessions : %s" % len(sessions)
			self.disconnect(silent=True)

class GeventTweetStream():
	def __init__(self, options):
		self.run(options)

	def emit(self, name, value):
		""" Send the tweet to all connected clients """
		for handler in sessions:
			handler.emit(name, json.dumps(value))

	def run(self, options):
		""" Serve tweets for le ever """
		track_list = options.keywords.split(',')
		while True:
			try:
				with tweetstream.FilterStream(options.username, options.password, track=track_list) as stream:
					for tweet in stream:
						try:
							if '#' in tweet["text"]:
								# Messages containing a # trigger a cleanup of the screen
								self.emit('reset', '')
							else:
								self.emit('tweet',
									{
										'user': tweet["user"]["screen_name"],
										'text': tweet["text"],
										'date': tweet["created_at"],
									}
								)
						except:
							pass
						finally:
							gevent.sleep(.1)
			except tweetstream.AuthenticationError:
				print "Access denied to Twitter Stream API, bad credentials ?"
				break
			except Exception, e:
				print "Twitter Stream API exception (%s)" % str(e)
				gevent.sleep(5)

def http404(start_response):
	""" 404 handler """
	start_response('404 Not Found', [])
	return []

def application(env, start_response):
	""" Our web serving app """
	path = env['PATH_INFO'].strip('/') or 'index.html'

	# static stuff
	if path.startswith('static/') or path == "index.html":
		try:
			data = open(path).read()
		except Exception:
			return http404(start_response)

		if path.endswith(".js"):
			content_type = "text/javascript"
		elif path.endswith(".css"):
			content_type = "text/css"
		elif path.endswith(".png"):
			content_type = "image/png"
		elif path.endswith(".swf"):
			content_type = "application/x-shockwave-flash"
		else:
			content_type = "text/html"

		start_response('200 OK', [('Content-Type', content_type)])
		return [data]

	# socketIO request
	if path.startswith('socket.io/'):
		socketio_manage(env, {'': TweetStreamNS})
	else:
		return http404(start_response)

if __name__ == '__main__':
	""" Main command line run """
	parser = argparse.ArgumentParser(add_help=True)
	parser.add_argument('-k', action="store", required=True, dest="keywords", type=str, help="comma separated list of keywords to filter on")
	parser.add_argument('-p', action="store", required=True, dest="password", type=str, help="your twitter password")
	parser.add_argument('-u', action="store", required=True, dest="username", type=str, help="your twitter username")
	options = parser.parse_args()

	try:
		server = SocketIOServer(
			('', 8000), application, resource='socket.io', policy_server=True, policy_listener=('0.0.0.0', 10843)
		)

		# Our tweet streamer sits in a greenlet, link it to our server for clean shutdown
		gts = gevent.spawn(GeventTweetStream, options)
		gts.link(server.stop)

		server.serve_forever()
	except KeyboardInterrupt:
		gts.kill()
		server.stop()
