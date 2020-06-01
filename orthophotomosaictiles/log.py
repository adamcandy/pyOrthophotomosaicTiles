#!/usr/bin/env python3

import logging

__NAME__ = 'OrthoPhotoTile'

################################################################################
#### Global variables ##########################################################
################################################################################

#log = None

################################################################################
#### Logging setup #############################################################
################################################################################

def loggingInit(options):

    # Setup the log handlers to stdout and file.
    log = logging.getLogger(__NAME__)

    if options.debug or options.logfiledebug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    prefix = ''
    if options.timestamp:
        prefix = '%(asctime)s '
    formatter_info  = logging.Formatter(prefix + '%(message)s', datefmt='%Y%m%d %H:%M.%S')
    formatter_debug = logging.Formatter(prefix + '%(levelname)s | %(message)s', datefmt='%Y%m%d %H:%M.%S')

    if options.stdout:
        from sys import stdout as _stdout
        handler_stdout = logging.StreamHandler(_stdout)
        if options.debug:
            handler_stdout.setLevel(logging.DEBUG)
            handler_stdout.setFormatter(formatter_debug)
        else:
            handler_stdout.setLevel(logging.INFO)
            handler_stdout.setFormatter(formatter_info)
        log.addHandler(handler_stdout)

    if options.logfile:
        handler_file = logging.FileHandler(
            options.logfile,
            mode='a',
            encoding='UTF-8',
            )
        if options.debug:
            handler_file.setLevel(logging.DEBUG)
            handler_file.setFormatter(formatter_debug)
        else:
            handler_file.setLevel(logging.INFO)
            handler_file.setFormatter(formatter_info)
        log.addHandler(handler_file)

    if options.logfiledebug:
        handler_file_debug = logging.FileHandler(
            options.logfiledebug,
            mode='a',
            encoding='UTF-8',
            )
        handler_file_debug.setLevel(logging.DEBUG)
        handler_file_debug.setFormatter(formatter_debug)
        log.addHandler(handler_file_debug)


    #log.info('* ' + '-' * 4 + ' Start up ' + '-' * 40)
    #log.info('\n\n* ' + '-' * 15 + ' Start up ' + '-' * 40)
    log.debug('Log enabled with debugging messages')
    if options.logfile:
        log.info('Logging to file enabled, to: {}'.format(options.logfile))
    if options.logfiledebug:
        log.info('Logging debug messages to file enabled, to: {}'.format(options.logfiledebug))

    return log

def getLogger():
    return logging.getLogger(__NAME__)

def isDebug():
    log = getLogger()
    return log.level == logging.DEBUG

