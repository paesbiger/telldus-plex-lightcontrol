#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import urllib2
import xml.etree.ElementTree as ET
from os.path import expanduser
import logging
import logging.handlers
import httplib
import time
import urllib
from tellcore.telldus import TelldusCore, Device

def LampON():
  device = Device(4)
  device.turn_on()

def LampOFF():
  device = Device(4)
  device.turn_off()

serverURL = 'http://192.168.1.55:32400/status/sessions'
state = ''
playstatus = ''
core = TelldusCore()


while True:

  server = urllib2.urlopen(serverURL)  # Replace the IP and Port with those of your server
  data = server.read()
  server.close()
  tree = ET.fromstring(data)
  for video in tree.iter('Video'):
    state = video.find('Player').get('state')
 
  # Playstatus displays current status, and is initialized from null
  # State is the value read from the player, the difference from last status (Playstatus) determines action

  if playstatus == 'playing':
    if state == 'paused':
      #Changed from playing2paused
      LampON()
      playstatus = 'paused'
    elif state == '':
      playstatus = ''
      LampON()

  if playstatus == 'paused':
    if state == 'playing':
      playstatus = 'playing'
      #Changed from paused2playing
      LampOFF()
    elif state == '':
      playstatus = ''
      LampON()

  if playstatus == '':
    if state == 'playing':
      playstatus = 'playing'
      LampOFF()

  time.sleep(3)
  state = ''
