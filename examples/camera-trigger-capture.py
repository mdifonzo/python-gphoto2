#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2014  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# camera-trigger-capture.py example by Matt DiFonzo  mdifonzo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import logging
import sys
import time
import os

import gphoto2 as gp

def list_files(camera, context, campath='/'):
	result = []
	gp_list = gp.check_result(gp.gp_list_new())
	# get files
	gp.check_result(gp.gp_camera_folder_list_files(camera, campath, gp_list, context))
	for n in range(gp.gp_list_count(gp_list)):
		result.append(os.path.join(campath, gp.check_result(gp.gp_list_get_name(gp_list, n))))
	# read folders
	folders = []
	gp.check_result(gp.gp_list_reset(gp_list))
	gp.check_result(gp.gp_camera_folder_list_folders(camera, campath, gp_list, context))
	for n in range(gp.gp_list_count(gp_list)):
		folders.append(gp.check_result(gp.gp_list_get_name(gp_list, n)))
	gp.gp_list_unref(gp_list)
	# recurse over subfolders
	for name in folders:
		result.extend(list_files(camera, context, os.path.join(campath, name)))
	return (result)

def trigger_capture(camera, context, dstpath='image.jpg'):
	""" Trigger capture must be used instead of capture if you want to shoot while the mirror is locked up
	and you do not want to re-focus - set capture format on camera"""
        timeout = 20
        starttime = time.time()

        gp.check_result(gp.gp_camera_trigger_capture(camera, context))
        filefound = [False, False]

        while filefound[1] != gp.GP_EVENT_FILE_ADDED:
                filefound = gp.gp_camera_wait_for_event(camera, 10000, context)
                if time.time() - starttime > timeout:
                        print ('operation timed out')
                        return False
	
	campath = '/'
        filelist = list_files(camera, context, campath)

        for f in filelist:
                filename = f.strip(campath)
                camfile = gp.check_result(gp.gp_file_new())
                gp.gp_camera_file_get(camera, campath, filename, gp.GP_FILE_TYPE_NORMAL, camfile, context)
                gp.gp_file_save(camfile, dstpath)
                gp.gp_file_unref(camfile)
                gp.gp_camera_file_delete(camera, campath, filename, context)
                
        endtime = round(time.time() - starttime, 2)
        print ('capture complete in {}s'.format(endtime))	        

def main():
        logging.basicConfig(
                format='%(levelname)s: %(name)s: %(message)s', level=logging.CRITICAL)
        gp.check_result(gp.use_python_logging())
        camera = gp.check_result(gp.gp_camera_new())
        context = gp.gp_context_new()
        gp.check_result(gp.gp_camera_init(camera, context))

        trigger_capture(camera, context, 'image.jpg')

        gp.check_result(gp.gp_camera_exit(camera, context))
        return 0

if __name__ == "__main__":
        sys.exit(main())