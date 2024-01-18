
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
import time
import datetime
import json
from functools import wraps
from flask import current_app , Blueprint , request , Response , g as _g , make_response , send_file
from esanom import database as _database

###############
from hashlib import sha256
import random

def get_test_uid( postfix = "" ) :
    return( "_test_" + sha256( format( random.getrandbits( 128 ) , 'x' ).encode( 'utf-8' ) ).hexdigest( ) + "_" + postfix )

import psutil

def get_status( ) :

    task_results = { }
    task_results[ "fs" ] = { }
    partitions = psutil.disk_partitions( )

    partition_percent_max = 0

    for partition in partitions :
        partition_data = { }
        partition_data[ "path" ] = partition[ 1 ]
        partition_data[ "percent" ] = psutil.disk_usage( partition[ 1 ] ).percent
        partition_data[ "total" ] = psutil.disk_usage( partition[ 1 ] ).total
        partition_data[ "free" ] = psutil.disk_usage( partition[ 1 ] ).free
        partition_data[ "used" ] = psutil.disk_usage( partition[ 1 ] ).used

        task_results[ "fs" ][ partition_data[ "path" ] ] = partition_data

        if partition_data[ "percent" ] > partition_percent_max: partition_percent_max = partition_data[ "percent" ]

    task_results[ "partition_percent_max" ] = partition_percent_max
    task_results[ "virtual_memory" ] = psutil.virtual_memory( )
    task_results[ "swap_memory" ] = psutil.swap_memory( )
    task_results[ "cpu_percent" ] = psutil.cpu_percent( interval = 1 , percpu = False )
    task_results[ "getloadavg" ] = psutil.getloadavg( )
    task_results[ "boot_time" ] = psutil.boot_time( )

    proc_iter = psutil.process_iter( attrs = [ "pid" , "name" , "cmdline" , "cpu_percent" , "memory_percent" ] )
    proc_iter_data = [ ]

    for p in proc_iter :
        proc_iter_data.append( p.info )

    task_results[ "process_iter" ] = proc_iter_data
    task_results[ "process_iter_len" ] = len( proc_iter_data )

    return( task_results )
###############




ROUTES_VERSION = 3

ROUTES = Blueprint( "routes" , __name__ )

#####################################################################

def decorator_token_required( f ) :

    @wraps( f )
    def decorator_function( *args , **kwargs ) :

        if not "Authorization" in request.headers : return( response_error( e_msg = "No token supplied" , e_code = 9102 , http_code = 401 ) )

        ####

        authorization_header = request.headers.get( "Authorization" )
        authorization_header_parts = authorization_header.split( " " )

        if len( authorization_header_parts ) != 2 : return( response_error( e_msg = "authorization_header_parts" , e_code = 9111 , http_code = 401 ) )

        token = authorization_header_parts[ 1 ]

        if len( token.strip( ) ) != 64 : return( response_error( e_msg = "token" , e_code = 9115 , http_code = 401 ) )

        ####

        _g.api = _database.api_getbytoken( token )

        if _g.api == None : return( response_error( e_msg = "get_api_by_token" , e_code = 9126 , http_code = 401 ) )

        ####

        if not _g.api[ "enabled" ] : return( response_error( e_msg = "api enabled" , e_code = 9135 , http_code = 403 ) )

        #if int( request.headers.get( "Content-Length" ) or 0 ) > _g.api[ "io_maxsize" ] :
        if int( request.headers.get( "Content-Length" ) or 0 ) > 8388608 :
            return( response_error( e_msg = "content length max size" , e_code = 9139 , http_code = 401 ) )

        ####

        #print( f"FIXME TODO {__file__} {request.remote_addr}")
        user_match_ip = _g.api[ "ip" ]

        if user_match_ip != None and user_match_ip != "" :

            remote_ip = request.headers.get( "X-Forwarded-For" )

            if not remote_ip : remote_ip = request.remote_addr

            user_match_ip_parts = user_match_ip.split( "," )

            flag_user_match_ip = False

            for user_match_ip_part in user_match_ip_parts:
                if remote_ip.startswith( user_match_ip_part ) :
                    flag_user_match_ip = True
                    break

            if not flag_user_match_ip : return( response_error( e_msg = f"{remote_ip} api ip" , e_code = 9154 , http_code = 401 ) )

        return( f( *args , **kwargs ) )

    return( decorator_function )

####

def decorator_role_required( role_name ) :
    def decorator_function( f ) :
        @wraps( f )
        def wrapped( *args , **kwargs ) :
            if _g.api[ "role_name" ] != role_name : return( response_error( e_msg = "role" , e_code = 9229 , http_code = 403 ) )
            return( f( *args , **kwargs ) )
        return( wrapped )
    return( decorator_function )


def decorator_request_json( f ) :

    @wraps( f )
    def decorator_function( *args , **kwargs ) :

        if len( request.data ) == 0 : return( response_error( e_msg = "data empty" , e_code = 9266 , http_code = 400 ) )

        if request.content_type != "application/json" : return( response_error( e_msg = "content type" , e_code = 9271 , http_code = 400 ) )


        if not request.is_json : return( response_error( e_msg = "not is_json" , e_code = 9274 , http_code = 400 ) )

        try :
            if not isinstance( request.json , dict ) : return( response_error( e_msg = "not dict" , e_code = 9274 , http_code = 400 ) )
        except Exception as e :
            return( response_error( e_msg = "bad json" , e_code = 9274 , http_code = 400 ) )

        return( f( *args , **kwargs ) )

    return( decorator_function )


#####################################################################

def response_default( messages = False ) :

    res = {
        "VERSION" : ROUTES_VERSION ,
        "TIME" : time.time( ) ,
        "STATUS" : "OK"
    }

    if messages != False : res[ "MESSAGES" ] = messages

    return( Response( json.dumps( res , default = str ) , status = 200 , mimetype = "application/json" ) )

def response_error( e_msg = "GENERAL" , e_code = 9999 , http_code = 200 ) :

    current_app.logger.warning( f"{e_code},{e_msg}" )

    return(
        Response(
            json.dumps( {
                "VERSION" : ROUTES_VERSION ,
                "TIME" : time.time( ) ,
                "STATUS" : "ERROR" ,
                "ERROR_MESSAGE" : e_msg ,
                "ERROR_CODE" : e_code 
            } , default = str ) ,
            status = http_code , mimetype = "application/json"
        )
    )

#####################################################################

@ROUTES.route( "/admin_state" , methods = [ "GET" ] )
@decorator_token_required
@decorator_role_required( "admin" )
def admin_state( ) :

    messages = { }

    messages[ "api" ] = _database.admin_state( "api" )
    messages[ "role" ] = _database.admin_state( "role" )
    messages[ "group" ] = _database.admin_state( "group" )
    
    messages[ "roleadmin" ] = _database.admin_state( "roleadmin" )
    messages[ "roleuser" ] = _database.admin_state( "roleuser" )
    messages[ "rolemodel" ] = _database.admin_state( "rolemodel" )
    messages[ "roledashboard" ] = _database.admin_state( "roledashboard" )

    messages[ "task" ] = _database.admin_state( "task" )
    messages[ "api_role" ] = _database.admin_state( "api_role" )
    messages[ "api_group" ] = _database.admin_state( "api_group" )
    messages[ "pipeline" ] = _database.admin_state( "pipeline" )

    return( response_default( messages ) )

@ROUTES.route( "/admin_create" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "admin" )
@decorator_request_json
def admin_create( ) :

    # FIXME TODO check table is VALID!!!

    if not "table" in request.args : return( response_error( e_msg = "request args" , e_code = 9287 , http_code = 400 ) )

    id = _database.insert_fromdict( request.args.get( "table" ) , request.json )

    if id == None : return( response_error( e_msg = "id none" , e_code = 9287 , http_code = 400 ) )

    messages = { "id" : id }

    return( response_default( messages ) )

@ROUTES.route( "/admin_update" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "admin" )
@decorator_request_json
def admin_update( ) :

    if not "table" in request.args : return( response_error( e_msg = "request args" , e_code = 9287 , http_code = 400 ) )
    if not "id" in request.args : return( response_error( e_msg = "request args" , e_code = 9287 , http_code = 400 ) )

    table = request.args.get( "table" , default = "" ) 
    if table.strip( ) == "" : return( response_error( e_msg = "table blank" , e_code = 9348 , http_code = 400 ) )

    id_str = request.args.get( "id" , default = "" ) 
    if not id_str.isdigit( ): return( response_error( e_msg = "id not isdigit" , e_code = 9348 , http_code = 400 ) )
    id = int( float( id_str ) )
    if not id > 0 : return( response_error( e_msg = "not id" , e_code = 9274 , http_code = 400 ) )

    res = _database.update_fromdict( table , id , request.json )

    if res == None : return( response_error( e_msg = "res none" , e_code = 9317 , http_code = 400 ) )

    return( response_default( ) )

@ROUTES.route( "/admin_delete" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "admin" )
@decorator_request_json
def admin_delete( ) :

    if not "table" in request.args : return( response_error( e_msg = "request args" , e_code = 9287 , http_code = 400 ) )
    if not "id" in request.args : return( response_error( e_msg = "request args" , e_code = 9287 , http_code = 400 ) )

    table = request.args.get( "table" , default = "" ) 
    if table.strip( ) == "" : return( response_error( e_msg = "table blank" , e_code = 9348 , http_code = 400 ) )

    id_str = request.args.get( "id" , default = "" ) 
    if not id_str.isdigit( ) : return( response_error( e_msg = "id not isdigit" , e_code = 9348 , http_code = 400 ) )
    id = int( float( id_str ) )
    if not id > 0 : return( response_error( e_msg = "not id" , e_code = 9274 , http_code = 400 ) )


    res = _database.delete_fromid( table , id )

    if res == None :
        return( response_error( e_msg = "res none" , e_code = 9317 , http_code = 400 ) )

    return( response_default( ) )

#####################################################################

@ROUTES.route( "/model_state" , methods = [ "GET" ] )
@decorator_token_required
@decorator_role_required( "model" )
def model_state( ) :

    messages = { }

    messages[ "model" ] = _database.model_state_rolemodel( api_id = _g.api[ "id" ] )
    messages[ "task" ] = _database.model_state_task( api_id = _g.api[ "id" ] )
    messages[ "group" ] = _database.model_state_group( api_id = _g.api[ "id" ] )

    return( response_default( messages ) )

@ROUTES.route( "/model_specs" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "model" )
@decorator_request_json
def model_specs( ) :

    if not "name" in request.json : return( response_error( e_msg = "not name" , e_code = 91109 , http_code = 400 ) )

    res = _database.model_specs( _g.api[ "id" ] , request.json[ "name" ] , request.data )

    if res == None : return( response_error( e_msg = "res none" , e_code = 91109 , http_code = 400 ) )

    return( response_default( ) )

@ROUTES.route( "/model_inputs" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "model" )
@decorator_request_json
def model_inputs( ) :

    task = _database.model_task_pluck( _g.api[ "id" ] )

    if task == None : return( response_error( e_msg = "task none" , e_code = 91109 , http_code = 400 ) )

    ####

    fp = f"/tmp/nomfs/{task['inputs_fp']}"

    response = make_response( send_file( fp , "application/octet-stream" ) )
    response.headers[ "NOM_TASK_ID" ] = task[ "id" ]
    return( response )

@ROUTES.route( "/model_heartbeat" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "model" )
@decorator_request_json
def model_heartbeat( ) :

    task_id = request.args.get( "id" , default = "" )
    if not task_id.isdigit( ) : return( response_error( e_msg = "bad id" , e_code = 91177 , http_code = 400 ) )

    task = _database.model_task_by_model_api( _g.api[ "id" ] , task_id )

    if task == None : return( response_error( e_msg = "task none" , e_code = 91109 , http_code = 400 ) )

    _database.model_task_heartbeat( task_id )

    messages = {
        "status" : task[ "status" ]
    }

    return( response_default( messages ) )

@ROUTES.route( "/model_outputs" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "model" )
def model_outputs( ) :

    if request.content_type != "application/octet-stream" : 
        return( response_error( e_msg = "content type" , e_code = 91087 , http_code = 400 ) )

    if len( request.data ) == 0 : return( response_error( e_msg = "len request data 0" , e_code = 91091 , http_code = 401 ) )

    task_id = request.args.get( "id" , default = "" )
    if not task_id.isdigit( ) : return( response_error( e_msg = "bad id" , e_code = 91177 , http_code = 400 ) )

    task = _database.model_task_by_model_api( _g.api[ "id" ] , task_id )
    if task == None : return( response_error( e_msg = "task none" , e_code = 91109 , http_code = 400 ) )

    ####

    model_id = task[ "rolemodel_id" ]

    outputs_fp = datetime.datetime.now( ).strftime( "%y%m/%d/%H/%Y%m%d%H%M%S_" + get_test_uid( ) + ".raw" )

    outputs_fp_dir = os.path.dirname( outputs_fp )

    os.makedirs( f"/tmp/nomfs/{outputs_fp_dir}" , exist_ok = True )

    with open( f"/tmp/nomfs/{outputs_fp}" , "wb" ) as f :
        f.write( request.data  )

    ####

    res = _database.model_outputs( task_id , outputs_fp )

    if res == None : return( response_error( e_msg = "res none" , e_code = 91109 , http_code = 400 ) )

    return( response_default( ) )


#####################################################################

@ROUTES.route( "/user_state" , methods = [ "GET" ] )
@decorator_token_required
@decorator_role_required( "user" )
def user_state( ) :

    messages = { }

    messages[ "model" ] = _database.user_state_model( api_id = _g.api[ "id" ] )
    messages[ "task" ] = _database.user_state_task( api_id = _g.api[ "id" ] )
    messages[ "group" ] = _database.user_state_group( api_id = _g.api[ "id" ] )

    return( response_default( messages ) )


@ROUTES.route( "/user_specs" , methods = [ "GET" ] )
@decorator_token_required
@decorator_role_required( "user" )
def user_specs( ) :

    name = request.args.get( "name" , default = "" ) 
    if name.strip( ) == "" : return( response_error( e_msg = "name blank" , e_code = 9348 , http_code = 400 ) )

    messages = { }

    messages[ "specs" ] = _database.user_specs( _g.api[ "id" ] , name )

    return( response_default( messages ) )


@ROUTES.route( "/user_inputs" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "user" )
def user_inputs( ) :

    if request.content_type != "application/octet-stream" : 
        return( response_error( e_msg = "content type != octet-stream" , e_code = 91087 , http_code = 400 ) )

    if len( request.data ) == 0 : return( response_error( e_msg = "len request data 0" , e_code = 91091 , http_code = 401 ) )

    name = request.args.get( "name" , default = "" ) 
    if name.strip( ) == "" : return( response_error( e_msg = "name" , e_code = 91091 , http_code = 401 ) )

    project = request.args.get( "project" , default = "" ) 

    model_id = _database.user_model_id( _g.api[ "id" ] , name )
    if model_id == None : return( response_error( e_msg = "model id?" , e_code = 9098 , http_code = 401 ) )

    ####

    inputs_fp = datetime.datetime.now( ).strftime( "%y%m/%d/%H/%Y%m%d%H%M%S_" + get_test_uid( ) + ".raw" )

    inputs_fp_dir = os.path.dirname( inputs_fp )

    os.makedirs( f"/tmp/nomfs/{inputs_fp_dir}" , exist_ok = True )

    with open( f"/tmp/nomfs/{inputs_fp}" , "wb" ) as f :
        f.write( request.data  )

    ####

    res = _database.user_inputs( _g.api[ "id" ] , model_id , project , inputs_fp )

    if res == None : return( response_error( e_msg = "res none" , e_code = 91109 , http_code = 400 ) )

    messages = { "id" : res }

    return( response_default( messages ) )

@ROUTES.route( "/user_outputs" , methods = [ "GET" ] )
@decorator_token_required
@decorator_role_required( "user" )
def user_outputs( ) :

    task_id_str = request.args.get( "id" , default = "" )
    if not task_id_str.isdigit( ) : return( response_error( e_msg = "bad id" , e_code = 91177 , http_code = 400 ) )
    task_id = int( float( task_id_str ) )


    task = _database.user_outputs( _g.api[ "id" ] , task_id )
    if task == None : return( response_error( e_msg = "task none" , e_code = 91109 , http_code = 400 ) )

    ####

    fp = f"/tmp/nomfs/{task['outputs_fp']}"
    response = make_response( send_file( fp , "application/octet-stream" ) )
    return( response )

@ROUTES.route( "/user_cancel" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "user" )
def user_cancel( ) :

    task_id_str = request.args.get( "id" , default = "" )
    if not task_id_str.isdigit( ) : return( response_error( e_msg = "bad id" , e_code = 91177 , http_code = 400 ) )
    task_id = int( float( task_id_str ) )

    task = _database.user_cancel( _g.api[ "id" ] , task_id )
    if task == None : return( response_error( e_msg = "task none" , e_code = 91109 , http_code = 400 ) )

    ####

    return( response_default( ) )

@ROUTES.route( "/user_archive" , methods = [ "POST" ] )
@decorator_token_required
@decorator_role_required( "user" )
def user_archive( ) :

    task_id_str = request.args.get( "id" , default = "" )
    if not task_id_str.isdigit( ) : return( response_error( e_msg = "bad id" , e_code = 91177 , http_code = 400 ) )
    task_id = int( float(task_id_str))

    task = _database.user_archive( _g.api[ "id" ] , task_id )
    if task == None : return( response_error( e_msg = "task none" , e_code = 91109 , http_code = 400 ) )

    ####

    return( response_default( ) )


@ROUTES.route( "/dashboard_state" , methods = [ "GET" ] )
@decorator_token_required
@decorator_role_required( "dashboard" )
def dashboard_state( ) :

    messages = { }

    messages[ "psutils" ] = get_status( )

    return( response_default( messages ) )

