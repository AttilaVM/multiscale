# multiscale #

A PythonMagick based module and CLI tool to scale all images from one source directory to multiple sizes, separated into different sub-directories or in one directory with size postfixed names. The new sizes are calculated from the given list of display resolutions and ratio.: display_resolution * ratio

The must common display resolutions are used by default.

I wrote this script to help out my daily workflow. So new features will be added on demand, however if you have a good idea to implement, do not hesitate to make a fork request or issue.

Unfortunately [PyPi](https://pypi.python.org/pypi/PythonMagick/0.5) does not contain source distribution or egg for PythonMagick so you can install it easily with a Package Manager on Linux or OS X, on Windows use the [precomplied installer](https://stackoverflow.com/questions/13409643/trouble-installing-pythonmagick-windows-7)

## TODO ##
- [ ] Make code asynchronous
