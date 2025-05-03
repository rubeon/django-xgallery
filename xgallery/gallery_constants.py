#!/usr/bin/env python
# encoding: utf-8
"""
gallery_constants.py

Created by Eric Williams on 2007-03-21.
Copyright (c) 2007 xoffender Administration & Development. All rights reserved.
"""
grStatusCodes={}

grStatusCodes['SUCCESS']                         = 0
grStatusCodes['PROTOCOL_MAJOR_VERSION_INVALID']  = 101
grStatusCodes['PROTOCOL_MINOR_VERSION_INVALID']  = 102
grStatusCodes['PROTOCOL_VERSION_FORMAT_INVALID'] = 103
grStatusCodes['PROTOCOL_VERSION_MISSING']        = 104
grStatusCodes['PASSWORD_WRONG']                  = 201
grStatusCodes['LOGIN_MISSING']                   = 202
grStatusCodes['UNKNOWN_COMMAND']                 = 301
grStatusCodes['MISSING_ARGUMENTS']               = 302
grStatusCodes['NO_ADD_PERMISSION']               = 401
grStatusCodes['NO_FILENAME']                     = 402
grStatusCodes['UPLOAD_PHOTO_FAIL']               = 403
grStatusCodes['NO_WRITE_PERMISSION']             = 404
grStatusCodes['NO_VIEW PERMISSION']              = 405
grStatusCodes['NO_CREATE_ALBUM_PERMISSION']      = 501
grStatusCodes['CREATE_ALBUM_FAILED']             = 502
grStatusCodes['MOVE_ALBUM_FAILED']               = 503
grStatusCodes['ROTATE_IMAGE_FAILED']             = 504
