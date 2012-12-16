#!/usr/env/python
# 
# A script for automatically tagging MP3s from the 78records.cdbpdx.com website.
# By Aengus Walton (ventolin.org) 2009
#
# You may freely distribute and change this script, as long as you leave this header intact and unmodified.

from BeautifulSoup import BeautifulSoup
from mutagen.easyid3 import EasyID3
import mutagen.id3 
from mutagen.mp3 import MP3
import sys,os 

def execute():
    html = ""
    mp3Location =  sys.argv[-1]
    if not mp3Location.endswith("/") and not mp3Location.endswith("\\"):
        mp3Location += "/"
    for line in open(sys.argv[-2]):
        if line[:10] == "<tr><td><a":
            html+=line
    for line in html.splitlines():
        soup = BeautifulSoup(line)
        filename = str(soup.tr.td.a["href"])
        filename = mp3Location + filename[filename.rfind("/") + 1:]
        title = str(soup.tr.td.a.contents[0]).replace("<b>","").replace("</b>","").title()
        artist = str(soup.tr.td.nextSibling.contents[0])
        label = str(soup.tr.td.nextSibling.nextSibling.contents[0])
        catNo = str(soup.tr.td.nextSibling.nextSibling.nextSibling.contents[0])
        
        # tag the mp3:
        try:
            mp3 = EasyID3(filename)
            mp3["title"] = title
            mp3["artist"] = artist
            mp3["website"] = label + u" " + catNo
            mp3.save()
            print "Saved " + filename
        except:
            print "File not found - check the location of " + str(sys.argv[-2]) + " in relation to the mp3s."
            print "Error occurred processing " + filename  
        
        
def printUsage():
    print "Usage:"
    print "- First, make sure the MP3s have ID3 headers"
    print "  (e.g. add a blank Artist field to all MP3s.)"
    print "- Then, execute the tagger as such:"
    print ""
    print "tagger.py <index.html file> <path to mp3s>"
    print ""
    print "e.g.:"
    print "tagger.py ./index.html ./list/"
    print ""

if not len(os.sys.argv) > 2 or not os.path.isdir(sys.argv[-1]) or not os.path.isfile(sys.argv[-2]):
    printUsage()
else:      
    execute()
