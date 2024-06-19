import os
import shutil

def copy_dir_contents(src, dest):
    shutil.rmtree(dest)
    os.mkdir(dest)
    copy_recursively(src, dest,[])

def copy_recursively(src, dest, path):
    path_string = '/'.join(path)
    files = os.listdir(src + path_string)
    for f in files:
        full_path = src + path_string + '/' + f
        dest_path = dest + path_string + '/' + f
        if os.path.isdir(full_path):
            os.mkdir(dest_path)
            copy_recursively(src, dest, path + [f])
        else:
            shutil.copy(full_path, dest_path)