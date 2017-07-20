"""multiscale

Usage:
  multiscale <source-directory> <destination-directory> [--ratio=<ratio>] [--resolutions=<resolutions>]

Options:
  -s --ratio=<ratio>               The ratio to tran [default: 2]
  -r --resolutions=<resolutions>     The di [default: 1366,1920,1440,1600,1280,1024]

"""

from docopt import docopt
from functools import partial

from utils import *
from elevate import channel
from pymagick import loadImg, saveImg, scaleImg


# CLI option processing and validation schema
# {option-name: [transformFun, validatorFun]...}
casters = {"source-directory":
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


def multiscale(srcDir, dstDir, ratio, resolutions):
    global cliPrint
    # Derive data
    imgWidths = map(lambda x: round(ratio * x), resolutions)

    for imgWidth in imgWidths:
        subDirPath = os.path.join(dstDir, "{}x".format(imgWidth))
        # create subdirs in destination, if non-existent
        if not os.access(subDirPath, os.R_OK):
            os.mkdir(subDirPath)
        # Create scale steps
        for srcFileName in os.listdir(srcDir):
            srcFilePath = os.path.join(srcDir, srcFileName)
            if isImageFile(srcFilePath):
                dstFilePath = os.path.join(subDirPath, srcFileName)
                channel(srcFilePath,
                        [loadImg,
                         partial(scaleImg, imgWidth, imgWidth, keepRatio=True),
                         partial(saveImg, dstFilePath)])
            else:
                continue


if __name__ == '__main__':
    opts = unMark(docopt(__doc__))
    # transform options
    for k, v in casters.items():
        transformFun = v[0]
        if transformFun is None:
            continue
        opts[k] = transformFun(opts[k])
    # validate options
    for k, v in casters.items():
        validatorFun = v[1]
        validatorFun(opts[k])
    # call main function
    multiscale(opts["source-directory"],
               opts["destination-directory"],
               opts["ratio"],
               opts["resolutions"])
