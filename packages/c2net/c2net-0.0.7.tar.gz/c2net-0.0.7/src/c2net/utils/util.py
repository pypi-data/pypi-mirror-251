import os
import shutil
from . import constants
def unzip_data(zipfile_path, unzipfile_path, data_download_method):
    try:
        if zipfile_path.endswith(".tar.gz"):
            shutil.unpack_archive(zipfile_path, unzipfile_path, 'gztar')
            unzip_success = True
        elif zipfile_path.endswith(".zip"):
            shutil.unpack_archive(zipfile_path, unzipfile_path, 'zip')
            unzip_success = True
        else:
            print(f'❌ The dataset is not in tar.gz or zip format!')
            unzip_success = False
    except Exception as e:
        print(f'❌ Extraction failed for {zipfile_path}: {str(e)}')
        print(f'❌ Extraction failed. Please proceed with manual extraction.')
    finally:
        try:
            if data_download_method == constants.DATA_DOWNLOAD_METHOD_MOXING:
                os.remove(zipfile_path)
        except Exception as e:
            print(f'Deletion failed for {zipfile_path}: {str(e)},but this does not affect the operation of the program, you can ignore')
    return unzip_success
def is_directory_empty(path):
    """
    is directory empty
    """
    if len(os.listdir(path)) == 0:
        return True
    else:
        return False
def get_nonempty_subdirectories(directory):
    """
    get nonempty subdirectories
    """
    nonempty_subdirectories = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            if any(os.scandir(entry.path)):
                nonempty_subdirectories.append(entry.name)
    return nonempty_subdirectories