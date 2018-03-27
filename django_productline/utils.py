from __future__ import unicode_literals, print_function, division

import os
import zipfile
import re


def create_or_append_to_zip(file_handle, zip_path, arc_name=None):
    """
    Append file_handle to given zip_path with name arc_name if given, else file_handle. zip_path will be created.
    :param file_handle: path to file or file-like object
    :param zip_path: path to zip archive
    :param arc_name: optional filename in archive
    """
    with zipfile.ZipFile(zip_path, 'a') as my_zip:
        if arc_name:
            my_zip.write(file_handle, arc_name)
        else:
            my_zip.write(file_handle)


def zipdir(src_path, target_path, wrapdir=''):
    """
    Zips the path
    :param wrapdir: wrap all contents in an additional dir
    :return:
    """

    # TODO: DEPRECATED remove

    zipf = zipfile.ZipFile(target_path, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(src_path):
        # exclude generated_static-dir
        if 'generated_static' not in root:
            for file in files:
                path = os.path.join(root, file)
                # get the relative path from the src_path in order to avoid an archive
                # of absolute paths including your home directory.
                rel_path = os.path.relpath(path, src_path)
                zipf.write(path, os.path.join(wrapdir, rel_path))

    zipf.close()


def tardir(src_path, target_path, wrapdir):
    """
    Tars the path
    :param wrapdir: wrap all contents in an additional dir
    :return:
    """
    import tarfile

    with tarfile.open(target_path, 'w') as tar:
        tar.add(src_path, arcname=wrapdir, exclude=lambda filename:filename == 'generated_static')

    with tarfile.open(target_path, 'r') as tar:
        tar.extractall()



def compare_version(version1, version2):
    """
    Compares two versions.
    """
    def normalize(v):
        return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
    return (normalize(version1) > normalize(version2))-(normalize(version1) < normalize(version2))
