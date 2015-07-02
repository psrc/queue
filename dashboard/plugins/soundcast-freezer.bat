@echo off
:: FREEZER.BAT - save a copy of all model inputs before it is run
set TOOL=SoundCast

:: ARCHIVE is the path to the inputs git repository
set ARCHIVE_DIR=X:
set ARCHIVE=X:\DSA\Dashboard-Freezer\inputs\%TOOL%

:: Use rsync to add/remove all files except Git configuration
:: (this cmd syncs files from current working directory to X: folder above)
:: (rsync server settings are on dsadashboard in /etc/rsyncd.conf)
rsync -vrltz --delete --exclude '.git*' * rsync://dsadashboard/tools/%TOOL%
if ERRORLEVEL 1 exit 6

:: switch to network archive drive and folder, and commit changes
%ARCHIVE_DIR%
cd %ARCHIVE%

:: -A option does a full add/remove of all files, whether new, existing, or deleted.
git add -A .

:: Record changes as if user did it themselves
git commit -m "$PROJECT / Series $SERIES / Version $TAG" --author "Automated <noone@psrc.org>"

:: Git-fat stores large files separately so repo doesn't get huge
:: See https://github.com/cyaninc/git-fat
git fat push

:: Tag with the run log number
if defined RUNLOG git tag %RUNLOG%
