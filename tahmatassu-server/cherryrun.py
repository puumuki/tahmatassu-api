#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tahmatassu Web Server
~~~~~~~~~~~~~~~~~~~~~
CherryPy run script for Tahmatassu Web Server. 
Simple and easy way to run tahmatassu in production.
:copyright: (c) 2014 by Teemu Puukko.
:license: MIT, see LICENSE for more details.
"""
from .server import app
from flask import Flask
import cherrypy
from paste.translogger import TransLogger

def run_server():
  # Enable WSGI access logging via Paste
  app_logged = TransLogger(app)

  # Mount the WSGI callable object (app) on the root directory
  cherrypy.tree.graft(app_logged, '/')

  # Set the configuration of the web server
  cherrypy.config.update({
    'engine.autoreload_on': app.config.get('ENGINE_AUTO_RELOAD'),
    'log.screen': app.config.get('LOG_SCREEN'),
    'server.socket_port': app.config.get('PORT'),
    'server.socket_host': app.config.get('HOST')
  })

  # Start the CherryPy WSGI web server
  try:
    cherrypy.engine.start()
    cherrypy.engine.block()         
  except KeyboardInterrupt:
    cherrypy.engine.exit()

if __name__ == '__main__':
  run_server()
