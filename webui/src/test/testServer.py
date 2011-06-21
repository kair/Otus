#!/usr/bin/env python2.4
#

import BaseHTTPServer
import SimpleHTTPServer
import urllib
import random
import json

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

  def do_GET(self):
    form = {}
    if self.path.find('?') > -1:
      parts = self.path.split('?')
      queryName = parts[0]
      queryStr = parts[1]
      form = {}
      for queryParam in queryStr.split('&'):
        items = queryParam.split('=')
        if len(items) > 1:
          form[items[0]] = items[1]
        else:
          form[items[0]] = ""

    print self.path
    print queryName

    if (queryName == '/q'):
      f = open("./data3.json", "r")
      text = ''
      for l in f:
        text += l
      f.close()

      body = text
    else:
      body = '["a", "b", "c"]' 

    if 'callback' in form:
      body = ('%s(%s);' % (form['callback'], body))

    self.send_response(200)
    self.send_header('Content-Type', 'text/javascript')
    self.send_header('Content-Length', len(body))
    self.send_header('Expires', '-1')
    self.send_header('Cache-Control', 'no-cache')
    self.send_header('Pragma', 'no-cache')
    self.end_headers()

    self.wfile.write(body)
    self.wfile.flush()
    self.connection.shutdown(1)

bhs = BaseHTTPServer.HTTPServer(('', 4242), MyHandler)
bhs.serve_forever()
