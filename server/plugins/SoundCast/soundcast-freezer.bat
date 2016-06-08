@echo off
:: FREEZER.BAT - save a copy of all model inputs before it is run
:: Requires %TOOL% and %LOCATION% to be set
:: LOCATION needs to be in Cygwin format: /cygdrive/c/archive/location
set TOOL=SoundCast
set LOCATION=/cygdrive/x/DSA/Queue-Archive

:: Use borg-backup to copy inputs to the shared borg folder.
set ARCHIVE=%LOCATION%::%TOOL%
c:\cygwin64\bin\bash.exe -i -c "/usr/bin/borg create --exclude '.git*' --exclude '.idea' --exclude '*.pyc' $ARCHIVE ."
