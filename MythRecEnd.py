#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ###########################################################################
#  Name: MythRecEnd.py
#
#  A USER job to symlink and rename the recording with a sensible name for
#  use by any networked DLNA type client.
#
# MYTHTV USER ARGS:
#      %FILE%     - Full filename and path for recording
#      %TITLE%    - Title of recording
#      %SUBTITLE% - Subtitle for recording, could be ''
#
#  v.0.2   25/01/2024 Beta
#  ##########################################################################

__title__ = "MythRecEnd"
__author__ = "Mike Pollard"
__version__= "v0.2"

import os
import sys
import argparse
from syslog import syslog

REC_FOLDER = "/var/lib/mythtv/recordings/"   # MythTV real recordings
LINKS_FOLDER = "/var/lib/mythtv/Recordings/" # Symlinks with human readable name

def sanitize_filename(filename):
    """Replace non-ASCII characters with underscores"""
    return ''.join(c if ord(c) < 128 else '_' for c in filename)

def main():
    """Create symlink to original recording"""
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
        syslog(f"Linking: Initial args: |{args.filename}|{title}|{subtitle}|")

        # Extract the file extension from the original filename and add the path
        _, original_extension = os.path.splitext(args.filename)
        full_filename = f"{REC_FOLDER}{args.filename}"

        # Extract the start time from the filename
        start_time = args.filename[8:-5]

        # Create a symlink with the sanitized title, subtitle and time in another folder
        if args.subtitle:
            new_filename = f"{LINKS_FOLDER}{title}-{subtitle}-{start_time}{original_extension}"
        else:
            new_filename = f"{LINKS_FOLDER}{title}-{start_time}{original_extension}"

        # and create symlink
        syslog('Linking...')
        os.symlink(full_filename, new_filename)
        syslog(f"Linked: {new_filename} to {full_filename}")

    except Exception as e:
        syslog(f'MythRecEnd Exception: {e} at line {sys.exc_info()[2].tb_lineno}')


if __name__ == "__main__":
    main()
