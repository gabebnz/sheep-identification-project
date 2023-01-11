#!/bin/sh

#
# ONLY RUN THIS SCRIPT IF YOU WANT THE ENTIRE YEARS DATA TO BE DOWNLOADED
# 



# FTP host information
HOST='***'
USER='***'
PASS='***'

# FTP directory information
YEAR=2022
MONTH=09
DAY=27


#check if directory exists, if not create it
if [ ! -d Images/$YEAR/$MONTH/$DAY ]; then
    mkdir -p Images/$YEAR/$MONTH/$DAY
fi

# CD to the right location
cd Images/$YEAR/$MONTH/$DAY

# Download the files
wget -m -nH --cut-dirs=100 --no-passive ftp://${USER}:${PASS}@${HOST}/${YEAR}/${MONTH}/${DAY}


# Delete the files that are not needed
# delete jpg files that are under 350kb in size (these are severely corrupted files)
#find . -type f -name "*.jpg" -size -350k -delete

exit 0

