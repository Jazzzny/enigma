import os
import urllib.request
import tempfile
import progressbar
import argparse
import platform
import subprocess
import tarfile
import time
import shutil

helptxt = "Soon:tm:"
parser = argparse.ArgumentParser(description=helptxt)
parser.add_argument("-d", "--download", help = "Show Output")
args = parser.parse_args()


pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


tempdir = tempfile.TemporaryDirectory()
os.chdir(tempdir.name)

path = os.getcwd()
print("Working directory is: "+path)


def DownloadLegacy(DownloadVersion):
    print("Downloading Legacy Installer for "+DownloadVersion)
    if DownloadVersion == "10.8":
        urllib.request.urlretrieve("https://updates.cdn-apple.com/2021/macos/031-0627-20210614-90D11F33-1A65-42DD-BBEA-E1D9F43A6B3F/InstallMacOSX.dmg","Working.dmg", show_progress)
    elif DownloadVersion == "10.7":
        urllib.request.urlretrieve("https://updates.cdn-apple.com/2021/macos/041-7683-20210614-E610947E-C7CE-46EB-8860-D26D71F0D3EA/InstallMacOSX.dmg","Working.dmg", show_progress)
    elif DownloadVersion == "TESTING":
        urllib.request.urlretrieve("https://updates.cdn-apple.com/2019/cert/041-87779-20191017-fcbc4e09-65e2-4332-83bd-9dfe7013e409/MacProEFIUpdate.dmg","Working.dmg",show_progress)
    else:
        print("Error! Invalid macOS release specified.")
    print("Disk Image Downloaded! Downloading 7zip...")
    if platform.system() == "Windows":
        urllib.request.urlretrieve("https://www.7-zip.org/a/7zr.exe","7zip.exe",show_progress)
    #    p = subprocess.run("7zr.exe", "x", tempdir.name + "\Working.dmg", "-o", tempdir.name + "\Extracted")

    if platform.system() == "Darwin":
        #Download 7zip
        urllib.request.urlretrieve("https://www.7-zip.org/a/7z2107-mac.tar.xz","7zip.tar.xz",show_progress)
        sevenzipextracted = tarfile.open('7zip.tar.xz')
        sevenzipextracted.extractall("./7zipmac")
        sevenzipextracted.close()
        #Perform extraction
        p = subprocess.run(['./7zipmac/7zz', "x", "./Working.dmg", "-o./Extracted/"])
        shutil.move(r"./Extracted/Install Mac OS X/InstallMacOSX.pkg", "./InstallESDInstaller.pkg")
        l = subprocess.run(['./7zipmac/7zz', "x", "./InstallESDInstaller.pkg", "-o./Extracted/", "-txar"])
        shutil.move(r"./Extracted/InstallMacOSX.pkg/InstallESD.dmg", r"./Install Mac OS X "+DownloadVersion+".dmg")
        #cleanup
        print("macOS "+DownloadVersion+" InstallESD downloaded! Cleaning up...")
        os.remove("7zip.tar.xz")
        os.remove("InstallESDInstaller.pkg")
        os.remove("Working.dmg")
        shutil.rmtree("7zipmac")
        shutil.rmtree("Extracted")
        #Prompt user
        print("Opening directory... (Please copy the InstallESD, it will be deleted once Python is closed!)")
        l = subprocess.run(['open', "./"])
        input("Press Enter to exit...")
DownloadLegacy(args.download)
