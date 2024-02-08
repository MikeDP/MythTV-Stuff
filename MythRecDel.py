#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ###########################################################################
#  Name: MythRecDel.py
#
#  A USER job to remove the symlink once a recording is deleted from MythTV
#
#  MYTHTV USER ARGS:
#      %FILE%     - Full filename and path for recording
#      %TITLE%    - Title of recording
#      %SUBTITLE% - Subtitle for recording, could be ''
#
#  v.0.2   06/02/2024 Beta
#  ##########################################################################

__title__ = "MythRecDel"
__author__ = "Mike Pollard"
__version__= "v0.2"

import os
import sys
import argparse
from syslog import syslog

REC_FOLDER = "/var/lib/mythtv/recordings/"   # Original MythTV recordings
LINKS_FOLDER = "/var/lib/mythtv/Recordings/" # Human readable symlink to recordings

def sanitize_filename(filename):
    """Replace non-ASCII characters with underscores"""
    return ''.join(c if ord(c) < 128 else '_' for c in filename)

def main():
    """Delete symlink to original recording"""
    try:
        parser = argparse.ArgumentParser(description='Create a symlink with title and subtitle after each MythTV recording.')
        parser.add_argument('filename', help='The original filename of the recording')
        parser.add_argument('title', help='The title of the recording')
        parser.add_argument('subtitle', nargs='?', default='', help='The subtitle of the recording (optional)')
        args = parser.parse_args()

        # Check for 'null' or empty arguments
        if not all([args.filename, args.title]):
            syslog("Error: Missing required arguments.")
            return

        # Replace non-ASCII characters with underscores
        title = sanitize_filename(args.title)
        subtitle = sanitize_filename(args.subtitle)
        syslog(f"Deleting: Initial args: |{args.filename}|{args.title}|{args.subtitle}|")

        # Extract the file extension from the original filename and add the path
        _, original_extension = os.path.splitext(args.filename)

        # Extract the start time from the filename
        start_time = args.filename[8:-5]

        # Re-create the symlink name with the sanitized title, subtitle
        if subtitle:
            symlink = f"{LINKS_FOLDER}{title}-{subtitle}-{start_time}{original_extension}"
        else:
            symlink = f"{LINKS_FOLDER}{title}-{start_time}{original_extension}"

        # and delete the symlink
        syslog(f'Deleting {symlink}')
        if os.path.exists(symlink):
            os.remove(symlink)
            syslog(f'Deleted "{symlink}"')

    except Exception as e:
        syslog(f'MythRecDel Exception: {e} at line {sys.exc_info()[2].tb_lineno}')
