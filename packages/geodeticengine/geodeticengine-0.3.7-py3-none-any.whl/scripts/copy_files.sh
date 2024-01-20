#!/bin/bash

# set the source directory and destination directory paths
source_dir="/workspaces/GeodeticEngine/src/pypi/src/proj_files/cdn.proj.org"
destination_dir=$(python -c "import pyproj; print(pyproj.datadir.get_user_data_dir())")

# copy all files from the source directory to the destination directory
cp -r "$source_dir"/* "$destination_dir/"