#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# ###########################################################################
#  Name: MythUserRename.py
#
#  A USER job to symlink and rename the recording with a sensible name for
#  use by any networked DLNA type client.
#
#  MYTHTV USER ARGS:
#      %FILE%     - Full filename and path for recording
#      %TITLE%    - Title of recording
#      %SUBTITLE% - Subtitle for recording, could be ''
#
#  v.0.1   25/01/2024 Alpha
#  ##########################################################################

__title__ = "MythUserRename"
__author__ = "Mike Pollard"
__version__= "v0.1"

import os
import argparse

def sanitize_filename(filename):
    """Replace non-ASCII characters with underscores"""
    return ''.join(c if ord(c) < 128 else '_' for c in filename)

def main():
    """Create symlink to original recording"""
    parser = argparse.ArgumentParser(description='Create a symlink with title and subtitle after each MythTV recording.')
    parser.add_argument('original_filename', help='The original filename of the recording')
    parser.add_argument('title', help='The title of the recording')
    parser.add_argument('subtitle', nargs='?', default='', help='The subtitle of the recording (optional)')
    args = parser.parse_args()

    # Check for 'null' or empty arguments
    if not all([args.original_filename, args.title]):
        print("Error: Missing required arguments.")
        return

    # Replace non-ASCII characters with underscores
    args.title = sanitize_filename(args.title)
    args.subtitle = sanitize_filename(args.subtitle)

    # Extract the file extension from the original filename
    _, original_extension = os.path.splitext(args.original_filename)

    # Create a symlink with the sanitized title and subtitle in another folder
    new_folder = "/path/to/symlinks/"
    if args.subtitle:
        new_filename = f"{new_folder}{args.title}_{args.subtitle}{original_extension}"
    else:
        new_filename = f"{new_folder}{args.title}{original_extension}"

    os.symlink(args.original_filename, new_filename)

if __name__ == "__main__":
    main()
