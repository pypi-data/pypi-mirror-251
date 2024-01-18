
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

import sys
import os
import mysql.connector as mysql
from mysql.connector import errorcode, Error , errors
from esanom import config as _config , util as _util 

#####################################################################

def init( ) :

    try :
        db = mysql.connect( **_config.DATA[ "database" ] )
        cursor = db.cursor( )
    except Exception as e :
        print( f"database create_tables connect exception {e}" )
        sys.exit( 4 )

    ####

    sql_files = [
        "api" , "role" , "group" ,
        "api_role" , "api_group" ,
        "roleadmin" , "roleuser" , "rolemodel" , "roledashboard" ,
        "task" , "pipeline" ,
        "taxonomy" , "quantity" , "unit" ,
        "input" , "output" ,
        "triggers"
    ]

    for sql_file in sql_files :

        sql_fp = _config.DATA[ "_package_fp" ] + f"/resources/database/{sql_file}.sql"

        ####

        if not os.path.isfile( sql_fp ) :

            cursor.close( )
            db.close( )
            print( f"create_tables not isfile {sql_fp}")
            sys.exit( 4 )

        ####

        with open( sql_fp , "r" ) as f : sql = f.read( )

        try :

            cursor.execute( sql )

        except Error as err :

            cursor.close( )
            db.close( )

            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR and sql_file == "api" :
                print( "DATABASE SETUP SKIPPING" )
                return

            print( f"create_tables {sql_file} {err.msg}" )
            sys.exit( 4 )

        ####

    cursor.close( )
    db.close( )

    init_tables( )

#####################################################################

def init_tables( ) :

    # Admin api, role, api_role
    api_id = insert_fromdict( "api" ,  { "name" : "admin" , "email" : _config.get( "admin_api_email" ) , "ip" : _config.get( "admin_api_ip" ) , "enabled" : 1 , "email_confirmed" : 1 } )
    role_id = insert_fromdict( "role" ,  { "name" : "admin" } )
    api_role_id = insert_fromdict( "api_role" ,  { "api_id" : api_id , "role_id" : role_id } )

    # user/model/dashboard role
    role_id = insert_fromdict( "role" ,  { "name" : "user" } )
    role_id = insert_fromdict( "role" ,  { "name" : "model" } )
    role_id = insert_fromdict( "role" ,  { "name" : "dashboard" } )

    # Default group
    group_id = insert_fromdict( "group" ,  { "name" : "default" } )

#####################################################################

def insert_fromdict( table , data ) :

    data_keys = list( data.keys( ) )

    cols = [  ]
    vals = [  ]
    qu = [  ]

    for data_key in data_keys :
        cols.append( f"`{data_key}`" )
        vals.append( data[ data_key ] )
        qu.append( "%s" )

    q_table = f"`{table}`"
    q_cols = ",".join( cols )
    q_places = ",".join( qu )

    sql = f"INSERT INTO {q_table} ( {q_cols} ) VALUES( {q_places} )" 

    return( db_query_insert( sql , vals ) )

def update_fromdict( table , id , data ) :

    kset = [ ]
    vals = [ ]

    data_keys = list( data.keys( ) )
    for data_key in data_keys :
        kset.append( f"`{data_key}`=%s" )
        vals.append( data[ data_key ] )

    vals.append( id )

    kset_str = ",".join( kset )

    sql = f"UPDATE `{table}` SET {kset_str} WHERE id=%s LIMIT 1"

    res = db_query_update( sql , vals )

    return( res )

def delete_fromid( table , id ) :

    sql = f"DELETE from `{table}` WHERE id=%s LIMIT 1"
    vals = [ id ]

    return( db_query_delete( sql , vals ) )

#####################################################################

def db_query_insert( sql , params ) :

    db = mysql.connect( **_config.DATA[ "database" ] , autocommit = True )
    cursor = db.cursor( )

    lid = None

    try :
        cursor.execute( sql , params )
        lid = cursor.lastrowid
    except errors.IntegrityError as e :
        print( f"database query_insert IntegrityError {e}" )
    except mysql.Error as e :
        print( f"database query_insert Error {e}" )

    cursor.close( )
    db.close( )

    return( lid )

def db_query_update( sql , params ) :

    db = mysql.connect( **_config.DATA[ "database" ] , autocommit = True )
    cursor = db.cursor( )

    flag = None

    try :
        cursor.execute( sql , params )
        flag = True
    except errors.IntegrityError as e :
        print( f"{e}" )
    except mysql.Error as e :
        print( f"{e}" )

    cursor.close( )
    db.close( )

    return( flag )

def db_query_select_row( sql , params , rdict = True ) :

    db = mysql.connect( **_config.DATA[ "database" ] )
    cursor = db.cursor( buffered = False , dictionary = rdict )

    cursor.execute( sql , params )

    rows = cursor.fetchall( )

    cursor.close( )
    db.close( )

    if len( rows ) != 1 : return( None )

    return( rows[ 0 ] )

def db_query_select_rows( sql , params = ( ) , rdict = True ) :

    db = mysql.connect( **_config.DATA[ "database" ] )
    cursor = db.cursor( buffered = False , dictionary = rdict )

    cursor.execute( sql , params )

    rows = cursor.fetchall( )

    cursor.close( )
    db.close( )

    return( rows )


def db_query_delete(  sql , params ) :

    db = mysql.connect( **_config.DATA[ "database" ] , autocommit = True )
    cursor = db.cursor( )

    flag = None

    try :
        cursor.execute( sql , params )
        flag = True
    except errors.IntegrityError as e :
        print( f"{e}" )
    except mysql.Error as e :
        print( f"{e}" )

    cursor.close( )
    db.close( )

    return( flag )
            
#####################################################################

def api_getbytoken( token ) :

    sql = "SELECT api.*,role.name AS role_name FROM api,api_role,role WHERE api.token=%s AND api_role.api_id=api.id AND api_role.role_id=role.id LIMIT 1"

    params = ( token , )

    return( db_query_select_row( sql , params ) )

#####################################################################

def admin_state( db ) :
    return( db_query_select_rows( f"SELECT * from `{db}`" ) )

#####################################################################

def model_state_rolemodel( api_id ) :
    rolemodel = db_query_select_row(
        "SELECT name,specs,enabled,updateable,heartbeats,created_at,updated_at,heartbeat_at from rolemodel where api_id=%s LIMIT 1" ,
        ( api_id , )
    )

    return( rolemodel )

def model_state_task( api_id ) :

    rolemodel = db_query_select_row(
        "SELECT id from rolemodel where api_id=%s AND enabled=1 LIMIT 1" ,
        ( api_id , )
    )

    if rolemodel == None : return( [ ] )

    tasks = db_query_select_rows(
        "SELECT id,status,heartbeats,created_at,updated_at,scheduled_at,running_at,ended_at,heartbeat_at from task where rolemodel_id=%s AND archived=0" ,
        ( rolemodel[ "id" ] , )
    )

    return( tasks )

def model_state_group( api_id ) :
    
    sql = "SELECT group.name FROM `api`,`group`,`api_group` WHERE api.id=%s AND api.id=api_group.api_id AND `group`.id=api_group.group_id"
    params = [ api_id ]
    rows = db_query_select_rows( sql , params )

    names = [ ]

    for row in rows : names.append( row[ "name" ] )

    return( names )

def model_specs( api_id , name , specs ) :

    row = db_query_select_row(
        "SELECT id,enabled,updateable from rolemodel where api_id=%s LIMIT 1" ,
        ( api_id , )
    )

    if row == None :
        # FIXME TODO check return value
        rolemodel_id = db_query_insert(
            "INSERT INTO rolemodel (api_id, name , specs) VALUES(%s,%s,%s)" ,
            ( api_id , name , specs ) 
        )
        return( True )

    if row[ "enabled" ] == 1 :
        print( f"NOP ENABLED {api_id}" )
        return( None )

    if row[ "updateable" ] == 0 :
        print( f"NOP NOT UPDATEABLE {api_id}" )
        return( None )

    sql = "UPDATE rolemodel SET updateable=0,specs=%s WHERE id=%s LIMIT 1"
    vals = ( specs , row[ "id" ] )

    return( db_query_update( sql ,vals ) )


def model_task_pluck( api_id ) :

    # Why not do this after connect???
    rolemodel = db_query_select_row(
        f"SELECT id from rolemodel where api_id=%s LIMIT 1" ,
        ( api_id , )
    )

    if rolemodel == None : return( None )

    db = mysql.connect( **_config.DATA[ "database" ] , autocommit = False )
    cursor = db.cursor( buffered = False , dictionary = True )

    ####

    sql = f"SELECT * from task where rolemodel_id=%s AND status=%s AND ( scheduled_at<=NOW() ) order by scheduled_at ASC LIMIT 1 FOR UPDATE SKIP LOCKED;"
    cursor.execute( sql , ( rolemodel[ "id" ] , "CREATED", ) )

    ####

    rows = cursor.fetchall( )

    if len( rows ) != 1 :
        db.commit( )
        cursor.close( )
        db.close( )
        return( None )

    ####

    sql = "UPDATE task SET status=%s,running_at=NOW() WHERE id=%s;"
    params = ( "RUNNING" , rows[ 0 ]["id"])

    try :
        cursor.execute( sql , params )
    except errors.IntegrityError as e:
        print(f"{e}")

    db.commit( )

    ####

    cursor.close( )
    db.close( )

    ####

    return( rows[ 0 ] )


def model_task_by_model_api( api_id , task_id ) :

    rolemodel = db_query_select_row(
        f"SELECT id from rolemodel where api_id=%s LIMIT 1" ,
        ( api_id , )
    )

    if rolemodel == None : return( None )

    task = db_query_select_row(
        f"SELECT * from task where id=%s AND rolemodel_id=%s LIMIT 1" ,
        ( task_id , rolemodel[ "id" ] )
    )

    return( task )


def model_task_heartbeat( id ):

    task = db_query_select_row(
        f"SELECT rolemodel_id from task where id=%s LIMIT 1" ,
        ( id , )
    )

    if task == None : return( None )

    sql = "UPDATE task SET heartbeat_at=NOW(),heartbeats=heartbeats+1 WHERE id=%s;"
    params = [ id ]
    db_query_update(sql,params) 

    sql = "UPDATE rolemodel SET heartbeat_at=NOW(),heartbeats=heartbeats+1 WHERE id=%s;"
    params = [ task["rolemodel_id"] ]
    db_query_update(sql,params) 

    return( True )


def model_outputs( id , outputs_fp):
    sql = "UPDATE task SET status=%s,outputs_fp=%s,ended_at=NOW() WHERE id=%s;"
    params = [ "COMPLETED" , outputs_fp , id ]
    return( db_query_update(sql,params) )


#####################################################################

def user_state_model( api_id ) :

        models = api_model( api_id ) 

        names = [ ] 
        
        for model in models : names.append( model[ "name" ] )

        return( names )

def user_state_task( api_id ) :

        tasks = db_query_select_rows(
            "SELECT id,status,heartbeats,created_at,updated_at,scheduled_at,running_at,ended_at,heartbeat_at from task where api_id=%s AND archived=0" ,
            ( api_id, )
        )

        return( tasks )

def user_state_group( api_id ) :
        sql = "SELECT group.name FROM `api`,`group`,`api_group` WHERE api.id=%s AND api.id=api_group.api_id AND `group`.id=api_group.group_id"
        params = [ api_id ]
        rows = db_query_select_rows( sql , params )
        names = [ ]
        for row in rows :
            names.append( row[ "name" ] )
        return( names )



def user_specs( api_id , name ) :

    groups = db_query_select_rows(
        "SELECT group_id from api_group where api_id=%s" ,
        [ api_id ] 
    )
    if len( groups ) == 0 : return( [ ] )
    #print(groups)

    g_ids = [ ]
    for r in groups : g_ids.append( r[ "group_id" ] )

    ####

    in1 = ",".join( map( str , g_ids ) )
    groups_users = db_query_select_rows(
        f"SELECT api_id from api_group where api_id!=%s AND group_id IN ({in1})" ,
        [ api_id ] 
    )
    if len( groups_users ) == 0 : return( [ ] )
    #print(groups_users)
    a_ids = [ ]
    for r in groups_users : a_ids.append( r[ "api_id" ] )

    ####

    in1 = ",".join( map( str , a_ids ) )
    where1 = "api_role.api_id=api.id AND role.id=api_role.role_id AND role.name='model'"
    model_api_ids = db_query_select_rows(
        f"SELECT api.id from api,role,api_role where api.id IN (%s) AND {where1}" ,
        [ in1 ]
    )
    if len( model_api_ids ) == 0 : return( [ ] )
    #print(model_api_ids)

    ####

    rows = db_query_select_rows(
        f"SELECT specs from rolemodel where name=%s AND api_id IN (%s)" ,
        [ name , in1 ]
    )

    if len(rows)!=1:
        print(f"multiple rows...? {api_id} {name}")
        return( [ ] )


    return( rows[ 0 ][ "specs" ] )


def user_model_id( api_id , model_name ) :

    groups = db_query_select_rows(
        "SELECT group_id from api_group where api_id=%s" ,
        [ api_id ] 
    )
    if len( groups ) == 0 : return( [ ] )
    #print(groups)

    g_ids = [ ]
    for r in groups : g_ids.append( r[ "group_id" ] )

    ####

    in1 = ",".join( map( str , g_ids ) )
    groups_users = db_query_select_rows(
        f"SELECT api_id from api_group where api_id!=%s AND group_id IN ({in1})" ,
        [ api_id ] 
    )
    if len( groups_users ) == 0 : return( [ ] )
    #print(groups_users)
    a_ids = [ ]
    for r in groups_users : a_ids.append( r[ "api_id" ] )

    ####

    in1 = ",".join( map( str , a_ids ) )
    where1 = "api_role.api_id=api.id AND role.id=api_role.role_id AND role.name='model'"
    model_api_ids = db_query_select_rows(
        f"SELECT api.id from api,role,api_role where api.id IN (%s) AND {where1}" ,
        [ in1 ]
    )
    if len( model_api_ids ) == 0 : return( [ ] )
    #print(model_api_ids)

    ####

    rows = db_query_select_rows(
        f"SELECT id from rolemodel where name=%s AND api_id IN ({in1})" ,
        [ model_name ]
    )

    if len(rows)!=1 :
        print(f"rows!=1 {api_id} {model_name}")
        return( None )

    return( rows[ 0 ][ "id" ] )


def user_inputs( api_id , rolemodel_id , project , inputs_fp ) :

    row_id = db_query_insert(
        f"INSERT INTO task (api_id,rolemodel_id,project,inputs_fp) VALUES (%s,%s,%s,%s)" ,
        [ api_id , rolemodel_id , project , inputs_fp]
    )        

    return( row_id )


def user_outputs( api_id , task_id ) :
    task = db_query_select_row(
        f"SELECT * from task where id=%s AND api_id=%s AND status=%s LIMIT 1" ,
        [ task_id , api_id , "COMPLETED" ]
    )
    return( task )

def user_cancel( api_id , task_id ) :
    sql = "UPDATE task SET status=%s,ended_at=NOW() WHERE id=%s AND api_id=%s AND status<>%s LIMIT 1;"
    params = [ "CANCELLED" , task_id , api_id , "COMPLETED" ]
    return( db_query_update(sql,params) )

def user_archive( api_id , task_id ) :
    sql = "UPDATE task SET archived=1 WHERE id=%s AND api_id=%s AND archived=0 LIMIT 1;"
    params = [ task_id , api_id  ]
    return( db_query_update(sql,params) )


            
#####################################################################

def api_model( api_id ) :

    # Select group ids api belongs to
    groups = db_query_select_rows(
        "SELECT group_id from api_group where api_id=%s" ,
        [ api_id  ]
    )
    if len( groups ) == 0 : return( [ ] )

    g_ids = [ ]
    for r in groups : g_ids.append( r[ "group_id" ] )

    ####

    # Select api ids that belong to groups ids (not including this one)
    in1 = ",".join( map( str , g_ids ) )
    groups_users = db_query_select_rows(
        "SELECT api_id from api_group where api_id!=%s AND group_id IN (%s)" ,
        [ api_id , in1 ] 
    )
    if len( groups_users ) == 0 : return( [ ] )

    a_ids = [ ]
    for r in groups_users : a_ids.append( r[ "api_id" ] )

    ####

    in1 = ",".join( map( str , a_ids ) )
    where1 = "api_role.api_id=api.id AND role.id=api_role.role_id AND role.name='model'"
    model_api_ids = db_query_select_rows(
        f"SELECT api.id from api,role,api_role where api.id IN (%s) AND {where1}" ,
        [ in1 ]
    )
    if len( model_api_ids ) == 0 : return( [ ] )

    ####

    rows = db_query_select_rows(
        "SELECT name,specs from rolemodel where enabled=1 AND api_id IN (%s)" ,
        [ in1 ] 
    )

    return( rows )
