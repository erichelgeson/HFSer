# HFSer

HFSer is an HFS SCSI Driver tool to extract, swap, and manage SCSI Drivers for vintage Macintosh computers.

Please make a backup and don't use this on any critical drive image without one.

## Why?

Images for [BlueSCSI](https://scsi.blue) or [RaSCSI](https://rascsi.com) can sometimes have a driver that is incompatible with your machine. This allows you to swap out that driver for one that is.

The primary use would be wanting to swap out Lido to use an image on a Macintosh Plus.

## CLI

An interactive CLI is provided to use most of the libraries functions.

```
./hfser.py <filename>
```

```
./hfser.py MacHD-2048MB.hda
HFSer

        ^..^      /
MOOF!   /_/\_____/
           /\   /\ 
          /  \ /  \ 

MacHD-2048MB.hda has the Lido-7.56.img SCSI Driver installed.

 1) Switch Driver
 2) Extract Driver
 3) SCSI Drivers I know about

 4) Quit
    
Action? 
```

## Module

This can be imported into other python projects as a module.

## TODO

* Add more drivers. (If you have one that is not listed please include it via PR)
* Replace `dd` usage with python.
* More testing.
