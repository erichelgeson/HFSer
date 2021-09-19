import subprocess
import tempfile
from os import listdir
from os.path import isfile, join

# Config #
drivers_dir = "drivers"


def md5_hash(file_name):
    """Helper to compute and return a hash of a file"""
    import hashlib
    return hashlib.md5(open(file_name, 'rb').read()).hexdigest()


def known_drivers():
    """Return a List of Dicts with the file name and hash of the drivers we know about."""
    driver_files = [f for f in listdir(drivers_dir) if isfile(join(drivers_dir, f))]
    drivers = []
    for file in driver_files:
        file_hash = md5_hash(f"{drivers_dir}/{file}")
        drivers.append({"driver": file, "hash": file_hash})
    return drivers


def driver_extract(image, driver_file=None):
    """Given a file, extract the driver to a temp location or provided path, and return that path"""
    if driver_file is None:
        driver_file = tempfile.mktemp()
    # TODO: Replace with python bytes instead of call out to dd
    proc = subprocess.run(["dd", f"if={image}", f"of={driver_file}", "skip=64", "count=32", "bs=512"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if proc.returncode == 0:
        return driver_file
    return None


def driver_check(file_name):
    """Given a file, return the known driver if found."""
    extracted_driver = driver_extract(file_name)
    extracted_hash = md5_hash(extracted_driver)
    for driver in known_drivers():
        if driver['hash'] == extracted_hash:
            return driver


def switch_driver(file_name, driver):
    """Given a image file replace the driver with the one provided, and return the new Driver object."""
    # TODO: Replace with python bytes instead of call out to dd
    cmd = ["dd", f"if=drivers/{driver['driver']}", f"of={file_name}", "seek=64", "count=32", "bs=512", "conv=notrunc"]
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if proc.returncode == 0:
        driver_check(file_name)