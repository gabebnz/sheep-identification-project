#!/bin/sh

# FTP host information
HOST='***'
USER='***'
PASS='***'

# FTP directory information
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)


#check if directory exists, if not create it
if [ ! -d Images/$YEAR/$MONTH/$DAY ]; then
    mkdir -p Images/$YEAR/$MONTH/$DAY
fi

# CD to the right location
cd Images/$YEAR/$MONTH/$DAY 



# Download the files
wget -m -nH --cut-dirs=100 --no-passive ftp://${USER}:${PASS}@${HOST}/${YEAR}/${MONTH}/${DAY}

# Delete the files that are not needed
# Deletes files that are before 7am, if the script runs on time (5.30pm). (they are black and white, no sheep, not useful for us)
find . -mmin +630 -delete

# delete jpg files that are under 550kb in size (these are severely corrupted files)
find . -type f -name "*.jpg" -size -550k -delete




# ---------- DELETE FILES AFTER 30 DAYS OLD (Save server storage space)
find /home/kauricone/TeamSheep/SheepData/Images/ -mmin +43200 -delete