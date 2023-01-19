#!/bin/bash

set -e
DIR_SUFFIX=""
#PROFILE_ARGS="-pr=Macos"

BUILD_DIR=build$DIR_SUFFIX
CONAN_INSTALL_DIR=conan_install$DIR_SUFFIX
mkdir -p $BUILD_DIR $CONAN_INSTALL_DIR

rm -rf $BUILD_DIR $CONAN_INSTALL_DIR
LOCKFILE=$CONAN_INSTALL_DIR/conan.lock

#conan config install ./ -sf=config --type dir
#conan lock create conanfile.py --update --build=missing --lockfile=$BASE_LOCKFILE --lockfile-out=$LOCKFILE $PROFILE_ARGS $CONAN_OPTIONS
conan install -if $CONAN_INSTALL_DIR $PWD #--build=missing --lockfile=$LOCKFILE
conan build -bf $BUILD_DIR -if $CONAN_INSTALL_DIR .
#cmake --build $BUILD_DIR --config Release --target package