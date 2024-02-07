# MythTV-Stuff
Bits and pieces for MythTV

1 - **MythRecEnd.py** : This script can be installed as a USER JOB or SYSTEM EVENT (Recording Ends) to run immediately on completion of a recording job.  It creates a user readable name comprised of the %TITLE%-%SUBTITLE%-YYMMDDHHMM.ext as a symlink to the recording in a separate folder which can then be used as the source for other clients (e.g. Jellyfin, Kodi, VLC... anything that supports DLNA).

2 - **MythRecDel.py** : This script can be installed as a SYSTEM EVENT (Recording Deleted) to run immediately on deletion of a recording job.  It re-creates the symlink and then deletes it.

Both these scripts are called with the same arguments.  It's important the arguments are double quoted to prevent spaces in the title/subtitle resulting in them being broken into multiple arguments.

```
/usr/bin/python3 /path/to/script/MythRecEnd.py "%FILE%" "%TITLE%" "%SUBTITLE%"
/usr/bin/python3 /path/to/script/MythRecDel.py "%FILE%" "%TITLE%" "%SUBTITLE%"
```
