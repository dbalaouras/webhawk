#!/usr/bin/env bash

# Get full path to the directory of this file
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null

VENV_NAME="webhawk-venv"

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

# Create venv
[[ -d "$VENV_NAME" ]] || virtualenv -p /usr/bin/python2.7 $VENV_NAME


# Activate Virtual Env
source "$VENV_NAME/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install Prerequisites
pip install -q -r requirements.txt

deactivate