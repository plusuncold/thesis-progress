#!/bin/bash

THESIS_FOLDER=~/folder/the/pdf/is/in/
LOG_FOLDER=~/folder/to/put/the/logs

# Change if you want the state file (thesis_plan.org) to be in a different folder
STATE_FILE_FOLDER="$LOG_FOLDER"

# Backup records
# DATE=`date +%Y-%m-%d`
# BACKUP_LOCATION=~/backup_location
# cp state.csv "$BACKUP_LOCATION"/state_$DATE.csv
# cp page_count.csv "$BACKUP_LOCATION"/page_count_$DATE.csv

python3 calc_logs.py "$THESIS_FOLDER" "$STATE_FILE_FOLDER" "$LOG_FOLDER"
