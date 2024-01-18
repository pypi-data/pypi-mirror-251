
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

CREATE TABLE `unit` (

    `id` int UNSIGNED NOT NULL AUTO_INCREMENT,
    `quantity_id` INT UNSIGNED DEFAULT NULL,
    `name` varchar(255) NOT NULL CHECK (`name` <> ""),

    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,

    PRIMARY KEY (`id`) ,
    KEY `quantity_id` (`quantity_id`),
    
    CONSTRAINT `unit_ibfk_1` FOREIGN KEY (`quantity_id`) REFERENCES `quantity` (`id`) ON DELETE CASCADE

) ENGINE=InnoDB,AUTO_INCREMENT=101;
 




