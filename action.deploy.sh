#!/bin/bash

# Define paths
REPO_PATH="/var/www/html/ajholzer.net"

# Go to repo path or exit if it does not exist
cd "$REPO_PATH" || exit 1


# ################### #
#  Update local repo  #
# ################### #

# Clear repo and pull from github
echo "Cleaning and pulling from GitHub..."
git reset --hard HEAD
git clean -fd
git pull origin main
