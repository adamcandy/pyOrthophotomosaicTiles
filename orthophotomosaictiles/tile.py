#!/usr/bin/env python3

from .log import getLogger
log = getLogger()

class FileNotFound(Exception):
    pass

class NoImageProvided(Exception):
    pass

class Tile:

    _prefix = 'tile_'

    def __init__(self, filename=None, output=None, length=None, centre=True):
        self.source = source
        self.length = length
        self.centre = centre

        self._dimensions = None
        self._name = None
        self._openimage = None
        self.filename = None
        self.outputfilename = None

        if image is not None:
            self._openimage = image
        elif filename is not None:
            self.filename = self.getFilename(filename)
        else:
            raise NoImageProvided()
        self.setOutputFilename(self.filename)

        if scale or length or height:
            self.resize(scale=scale, length=length, height=height)

    def __str__(self):
        return '{}'.format(self.filename)

    def addNumbering(self, index=None, total=None):
        self.index = index
        self.total = total

    def getFilename(self, filename):
        from os.path import exists, realpath, expanduser
        if filename is None:
            return None
        _filename = realpath(expanduser(filename))
        if not exists(_filename):
            raise FileNotFound
        return _filename

    def setOutputFilename(self, filename):
        from os.path import dirname, realpath, expanduser
        if filename is not None:
            _filename = realpath(expanduser(filename))
            self.outputfilename = _filename

    def getOutputFilename(self):
        return self.outputfilename
    
    def getName(self):
        if self._name is None:
            if self.filename is not None:
                from os.path import splitext, basename
                name, ext = splitext(basename(self.filename))
            else:
                name = self._direct_load
            self._name = name.replace('_', ' ')
        return self._name

    def openImage(self):
        if self._openimage is None:
            from PIL import Image
            Image.MAX_IMAGE_PIXELS = None
            im = Image.open(self.filename)
            self._openimage = im
        return self._openimage

    def updateImage(self, im):
        self._openimage = im
        self._dimensions = None
        return self._openimage

    def save(self, filename=None):
        if filename is not None:
            self.setOutputFilename(filename)
        _filename = self.getOutputFilename()
        log.debug('  Saving to: {}'.format(_filename))
        from os import makedirs
        makedirs(dirname(_filename), exist_ok=True)
        self.openImage().save(_filename)

    def resize(self, scale=None, length=None, height=None):
        if (scale is None) and (length is None) and (height is None):
            return
        im = self.openImage()
        w, h = self.getDimensions()
        _scale = 1
        if height is not None:
            _scale = min(_scale, height / h)
        if length is not None:
            _scale = min(_scale, length / self.getDimensionLargest())
        if scale is not None:
            _scale = min(_scale, scale)
        w, h = int(w * _scale), int(h * _scale)
        im = im.resize((w, h), resample=3)
        self.updateImage(im)
    
    def getDimensions(self):
        if self._dimensions is None:
            im = self.openImage()
            self._dimensions = im.size
        return self._dimensions
    
    def getDimensionLargest(self):
        return max(self.getWidth(), self.getHeight())

    def getArea(self):
        dim = self.getDimensions()
        return dim[0] * dim[1]

    def getWidth(self):
        return self.getDimensions()[0]

    def getHeight(self):
        return self.getDimensions()[1]

    def show(self, image=None):
        if image is None:
            self.openImage().show()
        else:
            image.show()

    def create(self, format=None):
        import Image
        import sys

        im = self.openImage()

        zoom_level = sys.argv[4]

        if self.getWidth() % length != 0:
            xoffset = ...

        if self.getHeight() % length != 0:
            yoffset = ...

        if format is None:
            base, ext = splituser(self.filename)
            format = ext[1:]

        i, j = (0,0)
        while j < self.getHeight():
            while i < self.getWidth():
                print i, j
                tile = im.crop( (i, j, i + self.getWidth(), j + self.getHeight()) )
                tile.save('{}x{}y{}.{}'.format(self._prefix, i, j, format.lower(), format)
                i += getWidth()
                j += self.getHeight()
            i = 0


    def process(self, show=False):
        log.info('{}'.format(self))
        log.info('  Details: {}'.format(self.getDetails()))
        log.info('  Source: {} -> output: {}'.format(self.filename, self.getOutputFilename()))

        return self.openImage()




