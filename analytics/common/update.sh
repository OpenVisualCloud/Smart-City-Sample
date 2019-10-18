#!/bin/bash -e

REPO="https://github.com/OpenVisualCloud/Ad-Insertion-Sample/archive/v19.10.tar.gz"
DIR=$(dirname $(readlink -f "$0"))

cd "$DIR"

test -d app && git rm -rf app
mkdir tmp
cd tmp
wget -O repo.tar.gz "$REPO"
tar xvfz repo.tar.gz --strip-components=3 --wildcards '*/ad-insertion/video-analytics-service'
cp -r app ..
cd ..
rm -rf tmp

git add app

