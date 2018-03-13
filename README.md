# File Checker
[![Build Status](https://travis-ci.org/iattempt/FileChecker.svg?branch=master)](https://travis-ci.org/iattempt/FileChecker) [![codecov](https://codecov.io/gh/iattempt/FileChecker/branch/master/graph/badge.svg)](https://codecov.io/gh/iattempt/FileChecker)

A checker/detector could check name of file/directory is expectable or not.

# Features
+ Only test particular files/directories.
+ Ignore particular files/directories.
+ Supports checking of most common format of letter-cases (upper, lower, camel, and pascal-case).
+ Supports checking of convention of word separators (underscore-to-dash/dash-to-underscore).

# How does this work?
+ Parse directories
    1. Walk over the directories under CHECK_DIR
    2. Exclude directories *not* in ONLY_DIRS
    3. Exclude directories in IGNORE_DIRS
    4. Check the directories with DIR_FORMATS

+ Parse files
    1. Walk over the directories under CHECK_DIR
    2. Exclude the directories *not* in ONLY_DIRS
    3. Exclude the directories in IGNORE_DIRS
    4. Exclude the files *not* in ONLY_FILES
    5. Exclude the files in IGNORE_FILES
    6. Check the directories with FILE_FORMATS

# How to use

### Installation
+ If you have git installed, then run the following command: `pip install git+https://github.com/iattempt/FileChecker.git`
+ If you do _not_ have git installed, then run the following command: `pip install --upgrade https://github.com/iattempt/FileChecker/tarball/master`

### Running
+ `pip install -r requirements.txt`
+ And now you can use the package!
