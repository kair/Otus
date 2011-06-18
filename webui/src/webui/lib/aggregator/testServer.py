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
      queryStr = self.path.split('?')[1]
      form = dict([queryParam.split('=') for queryParam in queryStr.split('&')])

    f = open("./data1.json", "r")
    text = ''
    for l in f:
      text += l
    f.close()

    data = json.loads(text)
    for arr in data:
      for item in arr['data']:
        item[0] = item[0]*1000
    body = json.dumps(data)

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
