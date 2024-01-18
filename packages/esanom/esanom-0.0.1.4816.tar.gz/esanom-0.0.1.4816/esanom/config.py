
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

import os
import sys
import json
import jsonschema

#####################################################################

# FIXME TODO check environment variable for NOM_CONFIG_FILEPATH 

CONFIG_FNDEFAULT = "nom_config.json"

DATA = { }

DATA_SCHEMA = {

    "type" : "object" ,
    "properties" : {

        "database" : {

            "type" : "object" ,
            "additionalProperties" : False ,
            "required" : [ "host" , "port" , "user" , "passwd" , "database" ] ,
            "properties" : {

                "host" : { "type" : "string" } ,
                "port" : { "type" : "string" } ,
                "user" : { "type" : "string" } ,
                "passwd" : { "type" : "string" } ,
                "database" : { "type" : "string" }

            } ,

        } ,

        "cache_filepath" : { "type" : "string" } ,
        "admin_api_email" : { "type" : "string" } ,
        "admin_api_ip" : { "type" : "string" } 

    }

}

#####################################################################

def init( ) :

    global DATA

    cwd_fp = os.getcwd( )

    config_fp = f"{cwd_fp}/{CONFIG_FNDEFAULT}"

    ####

    if not os.path.isfile( config_fp ) :
        print( f"ERROR CONFIG FILE NOT {config_fp}" )
        sys.exit( 4 )

    ####

    with open( config_fp ) as f :
        try :
            DATA = json.loads( f.read( ) )
        except json.decoder.JSONDecodeError as e :
            print( f"ERROR JSONDecodeError {e.msg}" )
            sys.exit( 4 )

    ####

    try :
        jsonschema.validate( instance = DATA , schema = DATA_SCHEMA )
    except jsonschema.ValidationError as e :
        print( f"CONFIG validate DATA_SCHEMA jsonschema.exceptions.ValidationError {e}" )
        sys.exit( 4 )

    DATA[ "_package_fp" ] = os.path.abspath( os.path.dirname( __file__ ) )
    DATA[ "_cwd_fp" ] = cwd_fp

    ####

    #print(DATA)

    return( True )

#####################################################################

def val( k ) :
    return( f"{k}...bar" )

def get( k ) :
    if not k in DATA : return( None )
    return(DATA[k])

