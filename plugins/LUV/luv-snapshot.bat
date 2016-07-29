@echo on
:: FREEZER.BAT - save a copy of all model inputs before it is run
:: Requires %TOOL% and %LOCATION% and %QUEUE_RUN_ID% to be set
:: LOCATION needs to be in Cygwin format: /cygdrive/c/archive/location
set LOCATION=/cygdrive/x/DSA/Queue-Archive/%COMPUTERNAME%
set TOOL=Demo

set ARCHIVE=%LOCATION%::%TOOL%-%QUEUE_RUN_ID%

set BORG_UNKNOWN_UNENCRYPTED_REPO_ACCESS_IS_OK=yes
set BORG_RELOCATED_REPO_ACCESS_IS_OK=yes

call borg.bat init -e none %LOCATION%
call borg.bat create --exclude '.git*' --exclude '.idea' --exclude '*.pyc' %ARCHIVE% .
