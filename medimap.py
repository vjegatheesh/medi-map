#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb
#from google.appengine.ext import db

import jinja2
import webapp2

class Device(ndb.Model):
  devid     = ndb.StringProperty(required=True)
  devname   = ndb.StringProperty(required=True)
  latitude  = ndb.StringProperty(required=True)
  longitude = ndb.StringProperty(required=True)
  address   = ndb.StringProperty(required=True)
  health    = ndb.StringProperty(required=True)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class MainPage(webapp2.RequestHandler):
    def get(self):
        rs = Device.query().fetch(50)
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render({'devices': rs}))
        
class updateMap(webapp2.RequestHandler):
  def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('update_map.html')
        self.response.write(template.render(template_values))
        
class manageDevice(webapp2.RequestHandler):
  def get(self):
        rs = Device.query().fetch(50)
        template = JINJA_ENVIRONMENT.get_template('manage.html')
        self.response.write(template.render({'devices': rs}))
        
class addUpdateDevice(webapp2.RequestHandler):
  def post(self):
        key = self.request.get("devkey")
        dev = self.request.POST
        if key :
          d = Device.get_by_id (int(key))
          for k in dev :
            setattr(d, k, dev[k])
          d.put()
        else  :
          d = Device()
          for k in dev :
            if k != 'devkey' :
              setattr(d, k, dev[k])
          d.put()    
          
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/update', updateMap),
  ('/manage', manageDevice),
  ('/ajax/save', addUpdateDevice),
], debug=True)
