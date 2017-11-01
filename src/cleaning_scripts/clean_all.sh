#!/usr/bin/env sh

# There is definitely a better way to do this, but this is not that way

echo "Starting cleaning..."
python clean_FY02-FY06.py
echo "2002-2006 done..."
python clean_FY07.py
echo "2007 done..."

echo "Done!"
