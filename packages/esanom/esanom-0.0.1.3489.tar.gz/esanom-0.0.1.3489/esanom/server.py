
#################################################################################
#
# {___     {__          {__       {__
# {_ {__   {__          {_ {__   {___
# {__ {__  {__   {__    {__ {__ { {__
# {__  {__ {__ {__  {__ {__  {__  {__
# {__   {_ {__{__    {__{__   {_  {__
# {__    {_ __ {__  {__ {__       {__
# {__      {__   {__    {__       {__
#
# (C) Copyright European Space Agency, 2024
# 
# This file is subject to the terms and conditions defined in file 'LICENCE.txt', 
# which is part of this source code package. No part of the package, including 
# this file, may be copied, modified, propagated, or distributed except 
# according to the terms contained in the file ‘LICENCE.txt’.“ 
#
#################################################################################

from flask import Flask
import logging


#from gevent import monkey
#monkey.patch_all()


#####################################################################

app = Flask( __name__ )

#####################################################################

from esanom.routes.v3.api import ROUTES as routes_v3_api
app.register_blueprint( routes_v3_api , name = "routes_v3_api" , url_prefix = "/v3/api" )

from esanom.routes.v3.web import ROUTES as routes_v3_web
app.register_blueprint( routes_v3_web , name = "routes_v3_web" , url_prefix = "/v3/web" )

#####################################################################

#from esanom.routes.v4.api import ROUTES as routes_api_v4
#app.register_blueprint( routes_api_v4 , name = "routes_api_v4" , url_prefix = "/v4/api" )

#####################################################################

if __name__ == "__main__" :

    app.run( host = "0.0.0.0" , port = 13031 , debug = True )

else :

    gunicorn_logger = logging.getLogger( "gunicorn.error" )
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel( gunicorn_logger.level )

    