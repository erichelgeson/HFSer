#!/usr/bin/env python3
import hfser
import sys

try:
    image_file = sys.argv[1]
except:
    print("Pass in an image name as the first argument")
    exit(1)


def drivers_we_know():
    print(f"\nWe know about these drivers:\n")
    index = 0
    for driver in hfser.known_drivers():
        print(f" {index}: {driver['driver']}")
        index += 1


def switch_driver():
    print(f"Changing driver for `{image_file}`")
    drivers_we_know()
    print("")
    switch_input = input("Switch? ")
    try:
        switch_to = hfser.known_drivers()[int(switch_input)]
    except Exception as e:
        print(f"Bad input '{switch_input}', exiting.")
        exit(1)
    print(f"Switching {image_file} to a {switch_to['driver']}")
    hfser.switch_driver(image_file, switch_to)


def check_image():
    try:
        results = hfser.driver_check(image_file)
        if results is None:
            print("Unknown driver installed or bad file... Proceed with caution and be sure to have a backup!")
        else:
            print(f"{image_file} has the {results['driver']} SCSI Driver installed.")
    except:
        print("Unknown driver installed or bad file... Proceed with caution and be sure to have a backup!")


def menu():
    print("""
 1) Switch Driver
 2) Extract Driver
 3) SCSI Drivers I know about

 4) Quit
    """)
    user_input = int(input("Action? "))
    print("")
    if user_input == 1:
        check_image()
        switch_driver()
        menu()
    elif user_input == 2:
        hfser.driver_extract(image_file, "extracted.img")
        print("Driver is now in extracted.img")
        menu()
    elif user_input == 3:
        drivers_we_know()
        menu()


if __name__ == "__main__":
    print("HFSer")
    print('''
        ^..^      /
MOOF!   /_/\_____/
           /\   /\ 
          /  \ /  \ 
''')

    check_image()
    menu()
