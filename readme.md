# RTCONVERT

This script converts RT in seconds to RT in minutes in GPM XML files.

## Installation on Windows

The /dist/rtconvert.exe executable file was created with py2exe.  Microsoft's [Visual C++ runtime components](https://www.microsoft.com/en-us/download/details.aspx?id=29) might be required to use the application.

## Usage

GUI: Drag and drop an XML file or directory of XML onto the rtconvert.exe application

Command Line: python rtconvert.py filename.xml

If converting a directory of files, RTConvert will spawn a number of subprocesses equal to the number of CPU cores for multiprocessing.