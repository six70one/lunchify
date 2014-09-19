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



import cgi
import wsgiref.handlers
import random


from google.appengine.ext import webapp
from google.appengine.ext import db

def writeDoctype(self):
  self.response.out.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\r\n""")

def writeMeta(self):
  self.response.out.write("""<meta http-equiv="content-type" content="text/xhtml; charset=utf-8"/>\r\n<meta http-equiv="cache-control" content="no-cache"/>\r\n""")

def writeHeader(self):
  writeDoctype(self)
  self.response.out.write("""<html xmlns="http://www.w3.org/1999/xhtml">\r\n""")
  self.response.out.write("""<head>\r\n""");
  writeMeta(self)
  self.response.out.write("""<link type="text/css" rel="stylesheet" href="/stylesheets/main.css" />""")
  self.response.out.write("""<title>Lunchify!</title>\r\n""")
  self.response.out.write("""</head>\r\n\r\n""");
  self.response.out.write("""<body>\r\n""")

class Restaurant(db.Model):
  name = db.StringProperty(multiline=False)
  
class MainPage(webapp.RequestHandler):
  def get(self):
    
    restaurants = db.GqlQuery("SELECT * FROM Restaurant")
    
    eatery = "the vending machine, unless you make Fred pick."
    
    eateryIndex = random.randrange(0,restaurants.count())
    backupIndex = random.randrange(0,restaurants.count())
    elevenTime = random.randrange(0,59)
    twelveTime = random.randrange(0,59)
	
    while (eateryIndex == backupIndex):
        backupIndex = random.randrange(0,restaurants.count())
		
    eatery = restaurants[eateryIndex].name
    writeHeader(self)
    self.response.out.write("""   <div class="colmask rightmenu">
	<div class="colleft">
		<div class="col1">
 <h1>Today, you're probably eating lunch at %(place)s around 11:%(#e)02d.</h1>
    <h2>Unless you don't want to.  May I suggest %(otherplace)s at 12:%(#t)02d?</h2>""" % {'place':eatery, "#e" : elevenTime, 'otherplace':restaurants[backupIndex].name, "#t" : twelveTime})
          
    self.response.out.write("""
    <h3>Is there something else you'd like to do today?</h3>
    I could <a href="/allPlaces">show you all the places to pick from! (there's at least %(num)s)</a> or 
    <a href="/addPlace">you might add someplace new...</a>
    </div>      
	<div class="col2">
	<h2>Yo Fresh, check the list!</h2>"""% {'num':restaurants.count()})
    restaurants = db.GqlQuery("SELECT * FROM Restaurant order by name asc")
    
    for restaurant in restaurants:
      self.response.out.write('* %s<br>' % restaurant.name)
    self.response.out.write("""
	</div>
	</div>
	</div>
		  <div id="footer">
	        <p>Don't forget to tell your manager how great they are today!</p>
          </div>
<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-5232872-1");
pageTracker._trackPageview();
</script>		  
  </body>
</html>\r\n""" )

class AddLocation(webapp.RequestHandler):
  def get(self):
    writeHeader(self)
    self.response.out.write("""
          <h1>What place would you like to add, sir?</h1>
          <form action="/PlaceAdded" method="post">
            <div><input type="text" name="location" size="50">
            <input type="submit" value="Do it!"></div>
          </form>
          <p>
          In case you forgot, I could <a href="/allPlaces">show you all the places I already pick from...</a>
        </body>
      </html>""")

class AddLocationResponse(webapp.RequestHandler):
  def post(self):
    writeHeader(self)
		
#	location = self.request.get

    restaurant = Restaurant()
    restaurant.name = self.request.get('location')
    restaurant.put()
    
    self.response.out.write('<html><body><h2>You added:</h2> <h1><b>')
    self.response.out.write(cgi.escape(self.request.get('location')))
    self.response.out.write("""</b></h1><p>Another one?
          <form action="/PlaceAdded" method="post">
            <div><input type="text" name="location" size="50">
            <input type="submit" value="Do it!"></div>""")
    self.response.out.write('<p> <a href="/">Back</a>')
    self.response.out.write('</body></html>')

class SeeLocations(webapp.RequestHandler):
  def get(self):
    writeHeader(self)
    self.response.out.write('<h1>All the stuff to pick from:</h1>')
    
    restaurants = db.GqlQuery("SELECT * FROM Restaurant order by name asc")
  
    
    for restaurant in restaurants:
      self.response.out.write('%s<br>' % restaurant.name)
    
    self.response.out.write('</body></html>')

def main():
  application = webapp.WSGIApplication([('/', MainPage),
                                        ('/addPlace', AddLocation),
                                        ('/PlaceAdded', AddLocationResponse),
                                        ('/allPlaces', SeeLocations)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
