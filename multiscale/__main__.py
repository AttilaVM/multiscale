"""multiscale

Usage:
  multiscale <source-directory> <destination-directory> [--ratio=<ratio>] [--resolutions=<resolutions>] [--compact]
  multiscale --version

Options:
  -s --ratio=<ratio>                 The ratio to tran [default: 2]
  -r --resolutions=<resolutions>     The display resolutions, which are used to calculate the different image sizes [default: 1366,1920,1440,1600,1280,1024]
  -c --compact                         If set the, destination dir will be populated directly with the rescaled images differentiated by their name: original-name.extension --> original-name-resolution.extension
  --version                          Print version
"""


import sys
from docopt import docopt
from functools import partial
from itertools import product as cproduct

from multiscale.elevate import channel
from multiscale.utils import *
from multiscale.pymagick import loadImg, saveImg, scaleImg


# CLI option processing and validation schema
# {option-name: [transformFun, validatorFun]...}
proccessors = {"source-directory":
               [None,
                lambda s: isDirReadable(s, "source dir is not accessible.")],

               "destination-directory":
               [None,
                lambda s: isDirWriteable(s, "destination dir is not writeable.")],

               "ratio":
               [float,
                isValidRatio],

               "resolutions": [lambda s: list(map(int, s.split(","))),
                               isValidResList]}


def multiscale(srcDir, dstDir, ratio, resolutions, compact):
    # Derive data
    imgWidths = map(lambda x: round(ratio * x), resolutions)
    for imgWidth, srcFileName in cproduct(imgWidths, os.listdir(srcDir)):
        srcFilePath = os.path.join(srcDir, srcFileName)
        if not isImageFile(srcFilePath):
            continue
        # Create destination path according to user compact option
        if compact:
            newFileName = appendToFileName(srcFileName, ("-" + str(imgWidth)))
            dstFilePath = os.path.join(dstDir, newFileName)
        else:
            subDirPath = os.path.join(dstDir, "{}x".format(imgWidth))
            dstFilePath = os.path.join(subDirPath, srcFileName)
            if not os.access(subDirPath, os.R_OK):
                os.mkdir(subDirPath)
        # Load, resize and save image
        channel(srcFilePath,
                [loadImg,
                 partial(scaleImg, imgWidth, imgWidth, keepRatio=True),
                 partial(saveImg, dstFilePath)])


def main():
    opts = unMark(docopt(__doc__))
    # --version --> print version
    if opts["version"]:
        print(__version__)
        sys.exit(0)

    # transform options
    for k, v in proccessors.items():
        transformFun = v[0]
        if transformFun is None:
            continue
        opts[k] = transformFun(opts[k])
    # validate options
    for k, v in proccessors.items():
        validatorFun = v[1]
        validatorFun(opts[k])
    # call main app function
    multiscale(opts["source-directory"],
               opts["destination-directory"],
               opts["ratio"],
               opts["resolutions"],
               opts["compact"])

if __name__ == '__main__':
    main()
