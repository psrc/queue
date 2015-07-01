#!/bin/bash
# Archive_inputs.sh -- save a copy of all model inputs before it is run

ARCHIVE_REPO=/c/users/billy/desktop/soundcast/archive
RUN_DIR="${SCRATCH}/${PROJECT}/${SERIES}"

# Use rsync to add/remove all files except Git configuration
rsync -vrultz --delete --exclude '.git*'  $RUN_DIR  $ARCHIVE_REPO

# -A option does a full add/remove of all files, whether new, existing, or deleted.
git add -A .

# Record changes as if user did it themselves
git commit -m "$PROJECT / Series $SERIES / Version $TAG" --author "$AUTHOR"

# Git-fat stores large file objects on filesystem separately
# See https://github.com/cyaninc/git-fat
git fat push

# Tag with the run log number
git tag $RUNLOG

