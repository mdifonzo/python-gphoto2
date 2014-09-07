#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2014  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# camera-capture.py example by Matt DiFonzo  mdifonzo@gmail.com
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

import gphoto2 as gp

def capture(camera, context, dstpath='image.jpg'):
        """ Capture an image - verify file capture format on camera before setting dstpath """
        camfile = gp.check_result(gp.gp_file_new())
        campath = gp.CameraFilePath()
        
        starttime = time.time()

        gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE, campath, context))
        
        gp.gp_camera_file_get(camera, campath.folder, campath.name, gp.GP_FILE_TYPE_NORMAL, camfile, context)
        gp.gp_file_save(camfile, dstpath)
        gp.gp_file_unref(camfile)
        gp.check_result(gp.gp_camera_file_delete(camera, campath.folder, campath.name, context))

        endtime = round(time.time() - starttime, 2)
        print ('capture complete in {}s'.format(endtime))	        

def main():
        logging.basicConfig(
                format='%(levelname)s: %(name)s: %(message)s', level=logging.CRITICAL)
        gp.check_result(gp.use_python_logging())
        camera = gp.check_result(gp.gp_camera_new())
        context = gp.gp_context_new()
        gp.check_result(gp.gp_camera_init(camera, context))

        capture(camera, context, 'image.jpg')

        gp.check_result(gp.gp_camera_exit(camera, context))
        return 0

if __name__ == "__main__":
        sys.exit(main())