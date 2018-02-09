import wget
import os
import shutil
from zipfile import ZipFile
import datetime

MAF_VERSION = "1.4.4"

cwd = os.getcwd()
maf_temp_path = cwd + "\MAF"
maf_tools_path = cwd + "\pt_win.zip"
pt_win_zip = "pt_win.zip"


def cleanup():
    if os.path.isdir(maf_temp_path):
        shutil.rmtree(maf_temp_path)
    if os.path.isfile(pt_win_zip):
        os.remove(pt_win_zip)


def download_platform_tools():
    try:
        url = 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip'
        wget.download(url, maf_tools_path)
    except Exception as e:
        print "Download failed: " + e


def extract_platform_tools():
    with ZipFile(pt_win_zip, 'r') as ptzip:
        zip_root_dir = "platform-tools/"
        files_to_extract = ["adb.exe", "AdbWinApi.dll", "AdbWinUsbApi.dll", "fastboot.exe"]
        for files in files_to_extract:
            try:
                ptzip.extract(zip_root_dir + files, cwd)
            except IOError as e:
                print "Failed to extract file: " + e
        os.rename(zip_root_dir, "MAF")


def copy_files():
    files_to_copy = ["cmd-here.exe", "Disclaimer.txt"]
    for files in files_to_copy:
        cwd_file_path = os.path.normpath(cwd + "/" + files)
        maf_dir_path = os.path.normpath(cwd + "/MAF/" + files)
        try:
            shutil.copy(cwd_file_path, maf_dir_path)
        except IOError as e:
            print "Failed to copy file: " + e


def create_portable_zip():
    build_date = datetime.datetime.now().strftime("%m-%d-%Y")
    build_version = "MAF_" + MAF_VERSION + "_" + build_date + "_shimp208_weekly"
    shutil.make_archive(build_version, "zip", cwd, maf_temp_path)


print "Welcome to MAF automated build tool."
print "Running cleanup of previous builds:"

cleanup()

print "Cleanup complete."
print "Downloading platform tools:"

download_platform_tools()

print "Platform tools download complete."
print "Extracting platform tools to build directory:"

extract_platform_tools()

print "Extraction complete."
print "Copying utility files to build directory:"

copy_files()

print "Copying complete."
print "Creating portable zip of latest MAF version"

create_portable_zip()

print "Build finished successfully!"
