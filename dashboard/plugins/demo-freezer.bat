@echo off
:: FREEZER.BAT - save a copy of all model inputs before it is run
set TOOL=Demo

:: ARCHIVE is the path to the inputs git repository
set ARCHIVE_DRIVE=X:
set ARCHIVE=X:\DSA\Queue-Archive\inputs\%TOOL%

:: Use rsync to add/remove all files except Git configuration
:: (this cmd syncs files from current working directory to X: folder above)
:: (rsync server settings are on dsadashboard in /etc/rsyncd.conf)
::rsync -vrltz --delete --exclude '.git*' * /cygdrive/c/Users/Billy/Desktop/Archive/inputs/%TOOL%
rsync -vrltz --delete --exclude '.git*' * rsync://dsadashboard/tools/%TOOL%
if ERRORLEVEL 1 exit 6

:: switch to network archive drive and folder, and commit changes
%ARCHIVE_DRIVE%
cd %ARCHIVE%

:: -A option does a full add/remove of all files, whether new, existing, or deleted.
git add -A .

:: Record changes as if user did it themselves
git commit -m "$PROJECT / Series $SERIES / Version $TAG" --author "Automated <no-one@psrc.org>"

:: Git-fat stores large files separately so repo doesn't get huge
:: See https://github.com/cyaninc/git-fat
git fat push

:: Tag with the run log number
if defined RUNLOG git tag %RUNLOG%
