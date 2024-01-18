
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

CREATE TABLE `pipeline` (

    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    
    `out_task_id` INT UNSIGNED DEFAULT NULL,
    `in_task_id` INT UNSIGNED DEFAULT NULL,

    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
    
    PRIMARY KEY (`id`),
    KEY `out_task_id` (`out_task_id`),
    KEY `in_task_id` (`in_task_id`),
    CONSTRAINT `pipeline_out_1` FOREIGN KEY (`out_task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE,
    CONSTRAINT `pipeline_in_1` FOREIGN KEY (`in_task_id`) REFERENCES `task` (`id`) ON DELETE CASCADE,

    CONSTRAINT pipeline_unique_out_in UNIQUE (out_task_id,in_task_id)

) ENGINE=InnoDB,AUTO_INCREMENT=101;
