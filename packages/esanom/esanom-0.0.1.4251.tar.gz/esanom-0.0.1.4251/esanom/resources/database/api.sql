
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

CREATE TABLE `api` (

    `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `token` varchar(255) NOT NULL CHECK (`token` <> ""),

    `name` varchar(255) NOT NULL CHECK (`name` <> ""),
    `email` varchar(255) DEFAULT "",

    `ip` varchar(255) DEFAULT "127.,192.168.,172.,10.",
    `enabled` BOOLEAN DEFAULT 0,

    `email_confirmed` BOOLEAN DEFAULT 0,
    `email_confirmed_at` DATETIME DEFAULT NULL,

    `io_maxsize` int UNSIGNED DEFAULT 10485760,
    `fs_maxsize` int UNSIGNED DEFAULT 104857600,

    `limiter_minute` int UNSIGNED DEFAULT 60,
    
    `expires_at` DATETIME DEFAULT (NOW() + INTERVAL 6 MONTH) ,

    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`) ,
    UNIQUE KEY `token` (`token`) ,
    UNIQUE KEY `name` (`name`) ,
    KEY `enabled` (`enabled`) 

) ENGINE=InnoDB,AUTO_INCREMENT=101;
 




