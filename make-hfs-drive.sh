#!/bin/bash

## Adapted from easyinstall.sh from RASCSI

function formatDrive() {
    diskPath="$1"
    volumeName="$2"

    if [ ! $(command -v hformat) ]; then
        # Install hfsutils to have hformat to format HFS
        brew install hfsutils
    fi

    if [ ! -x hfdisk/hfdisk ]; then
        # Clone, compile and install 'hfdisk', partition tool
        git clone git://www.codesrc.com/git/hfdisk.git && \
            cd hfdisk && \
            make && \
            cd .. &> /dev/null
    fi

    # Inject hfdisk commands to create Drive with correct partitions
    (echo i; echo ; echo C; echo ; echo 32; echo "Driver_Partition"; echo "Apple_Driver"; echo C; echo ; echo ; echo "${volumeName}"; echo "Apple_HFS"; echo w; echo y; echo p;) | hfdisk/hfdisk "$diskPath" &> /dev/null
    partitionOk=$?

    if [ $partitionOk -eq 0 ]; then
        if [ ! -f lido-driver.img ];then
            echo "Downloading Lido driver..."
            wget -q https://github.com/akuker/RASCSI/raw/master/lido-driver.img
        fi

        # Burn Lido driver to the disk
        dd if=lido-driver.img of="$diskPath" seek=64 count=32 bs=512 conv=notrunc

        driverInstalled=$?
        if [ $driverInstalled -eq 0 ]; then
            # Format the partition with HFS file system
            hformat -l "${volumeName}" "$diskPath" 1
            hfsFormattedOk=$?
            if [ $hfsFormattedOk -eq 0 ]; then
                echo "Disk created with success. ${diskPath}"
            else
                echo "Unable to format HFS partition."
                return 4
            fi
        else
            echo "Unable to install Lido Driver."
            return 3
        fi
    else
        echo "Unable to create the partition."
        return 2
    fi
}

function createDrive() {
    if [ $# -ne 2 ]; then
        echo "To create a Drive, volume size and volume name must be provided"
        echo "$ createDrive 600 \"RaSCSI Drive\""
        echo "Drive wasn't created."
        return
    fi

    driveSize=$1
    driveName=$2
    drivePath="${driveName}-${driveSize}MB.hda"
    
    if [ ! -f $drivePath ]; then
        echo "Creating a ${driveSize}MB Drive"
        dd if=/dev/zero of=$drivePath bs=1m count=$driveSize &> /dev/null

        echo "Formatting drive with HFS"
        formatDrive "$drivePath" "$driveName"

    else
        echo "Error: drive already exists - ${drivePath}"
    fi
}

cd $(dirname $0)
echo "Create BlueSCSI or RaSCSI images..."
echo -n "Enter drive size in MB: "
read size
echo -n "Enter drive name: "
read name
echo
createDrive $size $name

echo
