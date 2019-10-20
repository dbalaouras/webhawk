#!/usr/bin/env bash

# Get full path to the directory of this file
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null

LOGO="
=====================================================
      _      __    __   __ __            __
     | | /| / /__ / /  / // /__ __    __/ /__
     | |/ |/ / -_) _ \/ _  / _ \`/ |/|/ /  '_/
     |__/|__/\__/_.__/_//_/\_,_/|__,__/_/\_\\


               WebHook MicroFramework
=====================================================
"

# Print some intro
echo "$LOGO"

echo "Bootstraping WebHawk Environment..."

# Install pip
pip install virtualenv

# Go into the app root directory
cd "$SCRIPTPATH/../"

# Upgrade pip
pip install --upgrade pip

# Install pipenv
pip install pipenv

# Create virtual environment and install dependencies using Pipenv
pipenv install
