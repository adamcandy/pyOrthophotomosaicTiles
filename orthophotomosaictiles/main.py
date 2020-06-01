#!/usr/bin/env python3

from signal import signal, SIGINT, SIGTERM
from .trap import signal_handler

signal(SIGINT, signal_handler)
signal(SIGTERM, signal_handler)

################################################################################
#### Main ######################################################################
################################################################################


def main():
    from .options import checkOptions, getOutput
    from .log import loggingInit
    from .trap import isTrapped
    from .tile import Tile
    options = checkOptions()
    log = loggingInit(options)

    log.debug('Sources: {} -> output folder: {}'.format(', '.join(options.sources), options.outfolder))

    sources = []
    for i, filename in enumerate(options.sources):
        source = Tile(filename, scale=options.scale, length=options.length, height=options.height)
        source.setOutputFilename(getOutput(source.filename))
        sources.append(source)

    for source in sources:
        source.process()

        if options.show:
            source.show()
        else:
            source.save()

    log.info('Complete and closed cleanly')

if __name__ == '__main__':
    main()

