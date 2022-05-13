#!/bin/bash
 
# The source path to backup. Can be local or remote.
# Original: SOURCE=servername:/source/dir/
SOURCE=/data/VSCode/pysystemtrade-me/private/


# Where to store the incremental backups
# Original: DESTBASE=/backup/servername_data
DESTBASE=/mnt/leopard/samba/trading/Backup/pysystemtrade-me
 
# Where to store today's backup
DEST="$DESTBASE/$(date +%Y-%m-%d)"
# Where to find yesterday's backup
YESTERDAY="$DESTBASE/$(date -d yesterday +%Y-%m-%d)/"
 
# Use yesterday's backup as the incremental base if it exists
if [ -d "$YESTERDAY" ]
then
	OPTS="--link-dest $YESTERDAY"
fi
 
# Run the rsync
rsync -av --delete $OPTS "$SOURCE" "$DEST"