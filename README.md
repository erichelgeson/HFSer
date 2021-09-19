# HFSer

HFSer is an HFS SCSI Driver tool to extract, swap, and manage SCSI Drivers for vintage Macintosh computers.

Please make a backup and don't use this on any critical drive image without one.

## Why?

Images for BlueSCSI & RaSCSI can sometimes have a driver that is incompatible with your machine. This allows you to swap out that driver for one that is. 

The primary use would be wanting to swap out Lido to use an image on a Macintosh Plus.

## CLI

An interactive CLI is provided to use most of the libraries functions.

```bash
./hfser.py <filename>
```

## Module

This can be imported into other python projects as a module.

## TODO

* Add more drivers
* Replace `dd` usage with python.
