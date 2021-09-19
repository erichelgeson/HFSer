import subprocess
import tempfile
from os import listdir
from os.path import isfile, join


def md5_hash(file_name):
    import hashlib
    return hashlib.md5(open(file_name, 'rb').read()).hexdigest()


# Config #
drivers_dir = "drivers"
driver_files = [f for f in listdir(drivers_dir) if isfile(join(drivers_dir, f))]
known_drivers = []
for file in driver_files:
    file_hash = md5_hash(f"{drivers_dir}/{file}")
    known_drivers.append({"driver": file, "hash": file_hash})


def driver_extract(image, driver_file=None):
    """Given a file, extract the driver to a temp location and return the path"""
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
    for driver in known_drivers:
        if driver['hash'] == extracted_hash:
            print(f"{image_file}: has the {driver['driver']} installed.")
            return driver


def switch_driver(file_name, driver):
    """Given a image file replace the driver with the one provided"""
    # TODO: Replace with python bytes instead of call out to dd
    cmd = ["dd", f"if=drivers/{driver['driver']}", f"of={file_name}", "seek=64", "count=32", "bs=512", "conv=notrunc"]
    proc = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if proc.returncode == 0:
        driver_check(file_name)


print("HFSer")
print('''^..^      /
/_/\_____/
   /\   /\ 
  /  \ /  \ ''')

# image_file = "HD10_512-OpenRetroSCSI 7.0.1.hda"
image_file = "RaSCSI-Boot-8.hda"
print(f"Checking {image_file}...")
results = driver_check(image_file)
if results is None:
    print("Unknown driver installed.")
    exit(1)

print("We know about these drivers:")
index = 0
for driver in known_drivers:
    print(f"{index}: {driver['driver']}")
    index += 1
print(f"q: Quit")
user_input = input("Switch? ")
try:
    switch_to = known_drivers[int(user_input)]
except:
    exit(0)
print(f"Switching {image_file} to a {switch_to['driver']}")
switch_driver(image_file, switch_to)
