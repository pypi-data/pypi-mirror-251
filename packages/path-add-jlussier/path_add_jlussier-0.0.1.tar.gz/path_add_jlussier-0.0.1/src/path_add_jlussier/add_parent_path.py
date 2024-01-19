import os
import sys

def add_parent_path_to_sys_path(target_dir:str, search_dir:str):
    targetDirectoryName = target_dir
    currentLocation = os.path.dirname(search_dir)
    testResults = currentLocation.find(targetDirectoryName)
    targetPath = (currentLocation[0:(testResults + len(targetDirectoryName))])
    sys.path.append(targetPath)