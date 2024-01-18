
/*
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
*/

CREATE TRIGGER api_insert BEFORE INSERT ON api
FOR EACH ROW 
BEGIN

  SET NEW.token = SHA2( CONCAT( NOW( ) , RAND( ) , UUID( ) , NEW.id , "7F6I12APOL" ) , 256 ) ;

  IF ( NEW.email_confirmed = 1 ) THEN
    SET NEW.email_confirmed_at = NOW( ) ;
  END IF ;

END

